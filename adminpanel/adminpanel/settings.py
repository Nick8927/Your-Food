from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '..' / '.env')

SECRET_KEY = 'django-insecure-g16q($w85n-#ch7boms@m=8+tx(a(o@48@b6d%1bwq8@_*1u3!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'adminpanel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'adminpanel.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "YourFood Админка",
    "site_header": "Панель управления YourFood 🍰",
    "site_brand": "YourFood",
    "welcome_sign": "Добро пожаловать в мир вкуснях! 👁‍🗨",
    # "copyright": "© 2025 YourFood",
    "search_model": ["dashboard.Users", "dashboard.Products"],

    "topmenu_links": [
        {"name": "Главная", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],

    "icons": {
        "dashboard.Users": "fas fa-user",
        "dashboard.Categories": "fas fa-tag",
        "dashboard.Products": "fas fa-cookie",
        "dashboard.Carts": "fas fa-shopping-cart",
        "dashboard.FinallyCarts": "fas fa-clipboard-check",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "order_with_respect_to": ["dashboard", "auth"],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",  # другие: darkly, cyborg, journal, lux, minty, solar, etc, flatly
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_colour": "navbar-yellow",
    "accent": "accent-yellow",
    "navbar": "navbar-blue navbar-blue",
    "no_navbar_border": False,
    "sidebar": "sidebar-light-blue",
    "sidebar_nav_small_text": False,
    "custom_css": "css/custom_admin.css",
}
