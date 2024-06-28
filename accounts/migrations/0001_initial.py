# Generated by Django 5.0.6 on 2024-06-28 11:11

import accounts.models
import datetime
import django.contrib.auth.validators
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
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user_type', models.CharField(choices=[('NO', 'normal'), ('RO', 'restaurant owner')], default='NO', max_length=5)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('phone_country_code', models.CharField(choices=[('+93', '+93 (Afghanistan)'), ('+355', '+355 (Albania)'), ('+213', '+213 (Algeria)'), ('+376', '+376 (Andorra)'), ('+244', '+244 (Angola)'), ('+1-268', '+1-268 (Antigua and Barbuda)'), ('+54', '+54 (Argentina)'), ('+374', '+374 (Armenia)'), ('+61', '+61 (Australia)'), ('+43', '+43 (Austria)'), ('+994', '+994 (Azerbaijan)'), ('+1-242', '+1-242 (Bahamas)'), ('+973', '+973 (Bahrain)'), ('+880', '+880 (Bangladesh)'), ('+1-246', '+1-246 (Barbados)'), ('+375', '+375 (Belarus)'), ('+32', '+32 (Belgium)'), ('+501', '+501 (Belize)'), ('+229', '+229 (Benin)'), ('+975', '+975 (Bhutan)'), ('+591', '+591 (Bolivia)'), ('+387', '+387 (Bosnia and Herzegovina)'), ('+267', '+267 (Botswana)'), ('+55', '+55 (Brazil)'), ('+673', '+673 (Brunei)'), ('+359', '+359 (Bulgaria)'), ('+226', '+226 (Burkina Faso)'), ('+257', '+257 (Burundi)'), ('+238', '+238 (Cabo Verde)'), ('+855', '+855 (Cambodia)'), ('+237', '+237 (Cameroon)'), ('+1', '+1 (Canada)'), ('+236', '+236 (Central African Republic)'), ('+235', '+235 (Chad)'), ('+56', '+56 (Chile)'), ('+86', '+86 (China)'), ('+57', '+57 (Colombia)'), ('+269', '+269 (Comoros)'), ('+242', '+242 (Congo)'), ('+506', '+506 (Costa Rica)'), ('+385', '+385 (Croatia)'), ('+53', '+53 (Cuba)'), ('+357', '+357 (Cyprus)'), ('+420', '+420 (Czech Republic)'), ('+243', '+243 (Democratic Republic of the Congo)'), ('+45', '+45 (Denmark)'), ('+253', '+253 (Djibouti)'), ('+1-767', '+1-767 (Dominica)'), ('+1-809', '+1-809 (Dominican Republic)'), ('+593', '+593 (Ecuador)'), ('+20', '+20 (Egypt)'), ('+503', '+503 (El Salvador)'), ('+240', '+240 (Equatorial Guinea)'), ('+291', '+291 (Eritrea)'), ('+372', '+372 (Estonia)'), ('+268', '+268 (Eswatini)'), ('+251', '+251 (Ethiopia)'), ('+679', '+679 (Fiji)'), ('+358', '+358 (Finland)'), ('+33', '+33 (France)'), ('+241', '+241 (Gabon)'), ('+220', '+220 (Gambia)'), ('+995', '+995 (Georgia)'), ('+49', '+49 (Germany)'), ('+233', '+233 (Ghana)'), ('+30', '+30 (Greece)'), ('+1-473', '+1-473 (Grenada)'), ('+502', '+502 (Guatemala)'), ('+224', '+224 (Guinea)'), ('+245', '+245 (Guinea-Bissau)'), ('+592', '+592 (Guyana)'), ('+509', '+509 (Haiti)'), ('+504', '+504 (Honduras)'), ('+36', '+36 (Hungary)'), ('+354', '+354 (Iceland)'), ('+91', '+91 (India)'), ('+62', '+62 (Indonesia)'), ('+98', '+98 (Iran)'), ('+964', '+964 (Iraq)'), ('+353', '+353 (Ireland)'), ('+972', '+972 (Israel)'), ('+39', '+39 (Italy)'), ('+225', '+225 (Ivory Coast)'), ('+1-876', '+1-876 (Jamaica)'), ('+81', '+81 (Japan)'), ('+962', '+962 (Jordan)'), ('+7', '+7 (Kazakhstan)'), ('+254', '+254 (Kenya)'), ('+686', '+686 (Kiribati)'), ('+850', '+850 (Korea North)'), ('+82', '+82 (Korea South)'), ('+965', '+965 (Kuwait)'), ('+996', '+996 (Kyrgyzstan)'), ('+856', '+856 (Laos)'), ('+371', '+371 (Latvia)'), ('+961', '+961 (Lebanon)'), ('+266', '+266 (Lesotho)'), ('+231', '+231 (Liberia)'), ('+218', '+218 (Libya)'), ('+423', '+423 (Liechtenstein)'), ('+370', '+370 (Lithuania)'), ('+352', '+352 (Luxembourg)'), ('+261', '+261 (Madagascar)'), ('+265', '+265 (Malawi)'), ('+60', '+60 (Malaysia)'), ('+960', '+960 (Maldives)'), ('+223', '+223 (Mali)'), ('+356', '+356 (Malta)'), ('+692', '+692 (Marshall Islands)'), ('+222', '+222 (Mauritania)'), ('+230', '+230 (Mauritius)'), ('+52', '+52 (Mexico)'), ('+691', '+691 (Micronesia)'), ('+373', '+373 (Moldova)'), ('+377', '+377 (Monaco)'), ('+976', '+976 (Mongolia)'), ('+382', '+382 (Montenegro)'), ('+212', '+212 (Morocco)'), ('+258', '+258 (Mozambique)'), ('+95', '+95 (Myanmar)'), ('+264', '+264 (Namibia)'), ('+674', '+674 (Nauru)'), ('+977', '+977 (Nepal)'), ('+31', '+31 (Netherlands)'), ('+64', '+64 (New Zealand)'), ('+505', '+505 (Nicaragua)'), ('+227', '+227 (Niger)'), ('+234', '+234 (Nigeria)'), ('+389', '+389 (North Macedonia)'), ('+47', '+47 (Norway)'), ('+968', '+968 (Oman)'), ('+92', '+92 (Pakistan)'), ('+680', '+680 (Palau)'), ('+970', '+970 (Palestine)'), ('+507', '+507 (Panama)'), ('+675', '+675 (Papua New Guinea)'), ('+595', '+595 (Paraguay)'), ('+51', '+51 (Peru)'), ('+63', '+63 (Philippines)'), ('+48', '+48 (Poland)'), ('+351', '+351 (Portugal)'), ('+974', '+974 (Qatar)'), ('+40', '+40 (Romania)'), ('+7', '+7 (Russia)'), ('+250', '+250 (Rwanda)'), ('+1-869', '+1-869 (Saint Kitts and Nevis)'), ('+1-758', '+1-758 (Saint Lucia)'), ('+1-784', '+1-784 (Saint Vincent and the Grenadines)'), ('+685', '+685 (Samoa)'), ('+378', '+378 (San Marino)'), ('+239', '+239 (Sao Tome and Principe)'), ('+966', '+966 (Saudi Arabia)'), ('+221', '+221 (Senegal)'), ('+381', '+381 (Serbia)'), ('+248', '+248 (Seychelles)'), ('+232', '+232 (Sierra Leone)'), ('+65', '+65 (Singapore)'), ('+421', '+421 (Slovakia)'), ('+386', '+386 (Slovenia)'), ('+677', '+677 (Solomon Islands)'), ('+252', '+252 (Somalia)'), ('+27', '+27 (South Africa)'), ('+211', '+211 (South Sudan)'), ('+34', '+34 (Spain)'), ('+94', '+94 (Sri Lanka)'), ('+249', '+249 (Sudan)'), ('+597', '+597 (Suriname)'), ('+46', '+46 (Sweden)'), ('+41', '+41 (Switzerland)'), ('+963', '+963 (Syria)'), ('+886', '+886 (Taiwan)'), ('+992', '+992 (Tajikistan)'), ('+255', '+255 (Tanzania)'), ('+66', '+66 (Thailand)'), ('+670', '+670 (Timor-Leste)'), ('+228', '+228 (Togo)'), ('+676', '+676 (Tonga)'), ('+1-868', '+1-868 (Trinidad and Tobago)'), ('+216', '+216 (Tunisia)'), ('+90', '+90 (Turkey)'), ('+993', '+993 (Turkmenistan)'), ('+688', '+688 (Tuvalu)'), ('+256', '+256 (Uganda)'), ('+380', '+380 (Ukraine)'), ('+971', '+971 (United Arab Emirates)'), ('+44', '+44 (United Kingdom)'), ('+1', '+1 (United States)'), ('+598', '+598 (Uruguay)'), ('+998', '+998 (Uzbekistan)'), ('+678', '+678 (Vanuatu)'), ('+379', '+379 (Vatican City)'), ('+58', '+58 (Venezuela)'), ('+84', '+84 (Vietnam)'), ('+967', '+967 (Yemen)'), ('+260', '+260 (Zambia)'), ('+263', '+263 (Zimbabwe)')], default='+91', max_length=10)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('profile_picture_url', models.URLField(default="https://res.cloudinary.com/dgzc1nbnk/image/upload/v1719566986/profiles.png'")),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'male'), ('F', 'female'), ('O', 'other')], max_length=1)),
                ('biography', models.TextField(blank=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', accounts.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_Of_otp', models.CharField(choices=[('email', 'E'), ('phone', 'P')], max_length=10)),
                ('otp', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiring_at', models.DateTimeField(default=datetime.datetime(2024, 6, 28, 11, 26, 16, 909953, tzinfo=datetime.timezone.utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
