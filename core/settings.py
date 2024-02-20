import os
from pathlib import Path
from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--a!fh_jxnr@y)23^^l^bb4!o-%5v$153qy4yd!1h^r@p3!kv0^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'siteauth',
    'inventory',
    'data',
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

AUTH_USER_MODEL ='siteauth.User'

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


UNFOLD = {
    "SITE_TITLE": "Data Visualization Project",
    "SITE_HEADER": "Data is Prower",
    "SITE_URL": "/",
    "STYLES": [
        lambda request: static("css/admin_style.css"),
    ],
    "DASHBOARD_CALLBACK": "inventory.views.dashboard_callback",
    # "SCRIPTS": [
    #     lambda request: static("js/script.js"),
    # ],
    "SIDEBAR": { 
        "show_search": True,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Adminstration"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:siteauth_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Inventory"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:inventory_product_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Warehouse"),
                        "icon": "warehouse", # Supported icon set: https://fonts.google.
                        "link": reverse_lazy("admin:inventory_warehouse_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("In Out Orders"),
                        "icon": "front_loader", # Supported icon set: https://fonts.google.
                        "link": reverse_lazy("admin:inventory_productinout_changelist"),
                        "permission": lambda request: request.user.is_staff,                        
                    },
                    {
                        "title": _("Stock"),
                        "icon": "front_loader", # Supported icon set: https://fonts.google.
                        "link": reverse_lazy("admin:inventory_stock_changelist"),
                        "permission": lambda request: request.user.is_staff,                        
                    }
                ],
            },
            {
                "title": _("Data"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Market Prices"),
                        "icon": "price_change",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:data_marketpricedata_changelist"),
                        "permission": lambda request: request.user.is_staff,
                    },
                ],
            },
        ],
    },
}