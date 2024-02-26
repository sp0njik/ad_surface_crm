# Generated by Django 4.2.7 on 2024-02-26 13:36

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('ad_surface', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
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
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('phone', models.CharField(max_length=10, verbose_name='номер телефона')),
                ('legal_address', models.CharField(max_length=100, verbose_name='юридический адрес')),
                ('actual_address', models.CharField(max_length=100, verbose_name='фактический адрес')),
                ('inn', models.CharField(max_length=12, verbose_name='ИНН')),
                ('kpp', models.CharField(max_length=9, verbose_name='КПП')),
                ('ogrn', models.CharField(max_length=13, verbose_name='ОГРН')),
                ('checking_account', models.CharField(max_length=20, verbose_name='Расчётный счёт')),
                ('correspondent_account', models.CharField(max_length=20, verbose_name='Корреспондентский счёт')),
                ('bik', models.CharField(max_length=9, verbose_name='БИК')),
                ('bank_name', models.CharField(max_length=100, verbose_name='Название банка')),
                ('bank_address', models.CharField(max_length=100, verbose_name='Адрес банка')),
                ('is_agency', models.BooleanField(default=False, verbose_name='агенство')),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='агенство')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
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
            name='Placement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateField(verbose_name='начало размещения')),
                ('duration', models.DurationField(validators=[django.core.validators.MinValueValidator(datetime.timedelta(days=1))], verbose_name='продолжительность размещения')),
                ('invoice', models.FileField(blank=True, null=True, upload_to='files')),
                ('reconciliation', models.FileField(blank=True, null=True, upload_to='files')),
                ('contract_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='номер договора')),
                ('installation_cost', models.IntegerField(blank=True, null=True, verbose_name='стоимость монтажа')),
                ('dismantling_cost', models.IntegerField(blank=True, null=True, verbose_name='стоимость демонтажа')),
                ('production_cost', models.IntegerField(blank=True, null=True, verbose_name='стоимость производства')),
                ('placement_cost', models.IntegerField(blank=True, null=True, verbose_name='стоимость размещения')),
                ('accruals', models.IntegerField(blank=True, null=True, verbose_name='начисления')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='placements_data', to=settings.AUTH_USER_MODEL, verbose_name='организация')),
                ('surface', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='ad_surface.surface', verbose_name='поверхность')),
            ],
        ),
        migrations.CreateModel(
            name='PlacementFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files')),
                ('placement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.placement')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='placements',
            field=models.ManyToManyField(through='customer.Placement', to='ad_surface.surface', verbose_name='размещение'),
        ),
        migrations.AddField(
            model_name='company',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]