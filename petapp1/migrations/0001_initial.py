# Generated by Django 5.1 on 2024-12-19 10:08

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(code='invalid_name', message='Name can contain only alphabets and spaces', regex='^[a-zA-Z\\s]+$')])),
                ('breed', models.CharField(max_length=30)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='The minimun age value for pet is 1 years'), django.core.validators.MaxValueValidator(15, message='The maximum age for pet is 15 years.')])),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(10000, message='The minimum priced pet should be 10000 rupees.')])),
                ('type', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='pet_images/')),
            ],
            options={
                'permissions': [('can_add_pet', 'Can add a pet'), ('can_update_pet', 'Can update a pet')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(code='invalid_product_name', message='Product Name can contain only alphabets and spaces', regex='^[a-zA-Z\\s]+$')])),
                ('category', models.CharField(max_length=15)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1000, message='The minimum priced pet product should be 1000 rupees.')])),
                ('quantity_in_stock', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='product_images/')),
            ],
        ),
        migrations.CreateModel(
            name='PetUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('email1', models.CharField(max_length=50)),
                ('phone1', models.CharField(max_length=14)),
                ('address1', models.CharField(max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField()),
                ('payment_method', models.CharField(max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp1.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp1.order')),
                ('pet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp1.pet')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp1.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('date_added', models.DateTimeField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pet_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='petapp1.pet')),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='petapp1.product')),
            ],
        ),
    ]
