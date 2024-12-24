from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission
from .models import Pet, Product, PetUser, Cart, Order, OrderItem
from .forms import CustomAuthenticationForm, ContactForm, PetUserForm, PetForm, ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView
import razorpay
from django.conf import settings

# Create your views here.
def homepage(request):
    return render(request, 'home.html')

def aboutpage(request):
    return render(request, 'about.html')

def contactpage(request):
    return render(request, 'contact.html')

def contact_submit_page(request):
    return render(request, 'contact_submit.html')

def privacypolicypage(request):
    return render(request, 'privacy_policy.html')

def termspage(request):
    return render(request, 'terms.html')

def faqpage(request):
    return render(request, 'faq.html')

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        # If "remember me" is not checked, set session expiry to browser close
        if not form.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)  # Session expires on browser close
        return super().form_valid(form)

@login_required
def assign_permission_to_user(request):
    try:
        # Assign "can_add_pet" permission to "shree94"
        pet_user = get_object_or_404(PetUser, username="shree94")
        permission = Permission.objects.get(codename="can_add_pet")
        pet_user.user_permissions.add(permission)

        # Assign "can_update_pet" permission to "rohit94"
        pet_user2 = get_object_or_404(PetUser, username="sakshi2000")
        permission2 = Permission.objects.get(codename="can_update_pet")
        pet_user2.user_permissions.add(permission2)

        return HttpResponse("Permissions added successfully.")
    except Exception as e:
        return HttpResponse(f"Error while assigning permissions: {e}")

def UserCreateView(request):
    if request.method == 'POST':
        pet_user_form = PetUserForm(request.POST)
        if pet_user_form.is_valid():
            pet_user_form.save()
            return redirect('petuser_list')  
        else:
            print("Form errors:", pet_user_form.errors) 
    else:
        pet_user_form = PetUserForm()
    return render(request, 'user_create_form.html', {'pet_user_form': pet_user_form})


def search_view(request):
    query = request.GET.get('q')
    pet_manager = Pet.objects.search(query)
    return render(request, 'search_results.html', {'query': query, 'pet_manager': pet_manager})


class PetUserList(ListView):
    model = PetUser
    template_name = "petuser_list.html"
    context_object_name = 'users'

class PetList(ListView):
    model = Pet
    template_name = "pet_list.html"
    context_object_name = 'pets'

class PetCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = "pet_create_form.html"
    success_url = reverse_lazy('pet_list')

    permission_required = 'petapp1.can_add_pet'

class PetDetailView(DetailView):
    model = Pet
    template_name = "pet_detail_view.html"

class PetUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Pet
    template_name = "pet_update_form.html"
    fields = ['name', 'breed', 'age', 'price', 'type', 'description']
    success_url = reverse_lazy('pet_list')

    permission_required = 'petapp1.can_update_pet'

class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = "pet_delete_view.html"
    success_url = reverse_lazy('pet_list')


class ProductList(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = 'products'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_create_form.html"
    success_url = reverse_lazy('product_list')

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail_view.html"

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = "product_update_form.html"
    fields = ['product_name', 'category', 'price', 'quantity_in_stock', 'description', 'image']
    success_url = reverse_lazy('product_list')

    permission_required = 'petapp1.can_update_product'

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_delete_view.html"
    success_url = reverse_lazy('product_list')


# the cart functionality
class AddToCartView(View):
    def post(self, request):
        if request.user.is_authenticated:
            pet_id = request.POST.get('pet_id')
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))

            pet = None
            product = None

            if pet_id:
                pet = get_object_or_404(Pet, id=pet_id)

            if product_id:
                product = get_object_or_404(Product, id=product_id)

            if not pet and not product:
                return JsonResponse({'error': 'No pet or product added to cart'}, status=400)

            cart_item, created = Cart.objects.get_or_create(
                customer_id = request.user,
                pet_id = pet,
                product_id = product,
                defaults = {'quantity': quantity, 'date_added': now()}
            )

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return redirect('view_cart')
        return JsonResponse({'error': 'You need to log in first..!'}, status=403)

class CartView(ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(customer_id=self.request.user)
        return Cart.objects.none()
    
    """ def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add cart count to context to pass to the base template
        if self.request.user.is_authenticated:
            cart_count = Cart.objects.filter(customer_id=self.request.user).count()
        else:
            cart_count = 0
        context['cart_count'] = cart_count
        return context"""
    
class RemoveFromCartView(View):
    def post(self, request, cart_id):
        if request.user.is_authenticated:
            cart_item = get_object_or_404(Cart, id=cart_id, customer_id=request.user)
            cart_item.delete()
            return redirect('view_cart')
        
class CreateOrderView(View):
    def post(self, request):
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(customer_id=request.user)
            if not cart_items:
                return JsonResponse({'error': 'Cart is empty'})
            
            total_amount = 0
            for item in cart_items:
                if item.pet_id:
                    total_amount += item.pet_id.price * item.quantity
                elif item.product_id:
                    total_amount += item.product_id.price * item.quantity
            
            order = Order.objects.create(
                user_id = request.user,
                order_date = now(),
                total_amount = total_amount    
            )

            for item in cart_items:
                if item.pet_id:
                    OrderItem.objects.create(
                        order_id=order,
                        pet_id=item.pet_id,
                        quantity=item.quantity,
                        price=item.pet_id.price * item.quantity
                    )
                elif item.product_id:
                    OrderItem.objects.create(
                        order_id=order,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.product_id.price * item.quantity
                    )
            
            cart_items.delete()

            return redirect('order_summary', order_id=order.id)
        return JsonResponse({'error': 'You need to log in first'}, status=403)


class OrderSummaryView(View):
    template_name = 'order_summary.html'

    def get(self, request, order_id):
        if request.user.is_authenticated:
            # Fetch the order
            order = get_object_or_404(Order, id=order_id, user_id=request.user)
            
            # Fetch the related order items
            order_items = OrderItem.objects.filter(order_id=order)
            
            # Prepare context data for rendering
            context = {
                'order': order,
                'order_items': order_items,
            }
            return render(request, self.template_name, context)
        else:
            return JsonResponse({'error': 'You need to log in first.'}, status=403)
        
class ProceedToPaymentView(View):
    template_name = 'proceed_to_payment.html'

    def get(self, request, order_id):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=order_id, user_id=request.user)

            # Ensure the order is pending and unpaid
            if order.payment_status != 'PENDING':
                return JsonResponse({'error': 'This order is already processed.'}, status=400)

            # Razorpay client setup
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            
            # Razorpay order creation
            razorpay_order = client.order.create({
                'amount': int(order.total_amount * 100),  # Convert to paisa
                'currency': 'INR',
                'payment_capture': '1'
            })

            # Save Razorpay order ID to the database
            order.razorpay_payment_id = razorpay_order['id']
            order.save()

            context = {
                'order': order,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_api_key': settings.RAZORPAY_API_KEY,
                'order_total': order.total_amount,
                'user_email': request.user.email,
                'user_name': request.user.username,
            }

            return render(request, self.template_name, context)
        else:
            return JsonResponse({'error': 'You need to log in first.'}, status=403)

    def post(self, request, order_id):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=order_id, user_id=request.user)
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        
            # Capture Razorpay payment details
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_signature = request.POST.get('razorpay_signature')

            # Verify payment signature
            try:
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature,
                }
                client.utility.verify_payment_signature(params_dict)

                # Payment is successful, update the order
                order.payment_status = 'COMPLETED'
                order.save()
                return redirect('payment_success', order_id=order.id)
            except razorpay.errors.SignatureVerificationError as e:
                # Log error and update order status
                order.payment_status = 'FAILED'
                order.save()
                return JsonResponse({'error': 'Payment verification failed.'}, status=400)
        else:
            return JsonResponse({'error': 'You need to log in first.'}, status=403)

class PaymentSuccessView(View):
    template_name = 'payment_success.html'

    def post(self, request, order_id):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=order_id, user_id=request.user)

            # Verify payment
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            try:
                params_dict = {
                    'razorpay_order_id': request.POST.get('razorpay_order_id'),
                    'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
                    'razorpay_signature': request.POST.get('razorpay_signature'),
                }
                client.utility.verify_payment_signature(params_dict)
                order.payment_status = 'COMPLETED'
                order.save()
                return render(request, self.template_name, {'order': order})
            except razorpay.errors.SignatureVerificationError:
                order.payment_status = 'FAILED'
                order.save()
                return JsonResponse({'error': 'Payment verification failed.'}, status=400)
        else:
            return JsonResponse({'error': 'You need to log in first.'}, status=403)
        
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save contact data to the database
            return redirect('contact_submit')  # Redirect to the contact_submit page
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
