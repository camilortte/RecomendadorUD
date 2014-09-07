# -*- encoding: utf-8 -*-
from configurations import Configuration

import os
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
class Base(Configuration):
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    
    SECRET_KEY = 'oo*-tbab-(tdkyvo6bdc9=ir+75@#@bio^5w$17p9%l$qfdd55'

    
    DEBUG=True

    ALLOWED_HOSTS = []
    MAX_UPLOAD_SIZE = 5242880 #5 MB
    MAX_UPLOAD_PER_USER=3
    MAX_IMAGES_PER_PLACE=8

    INSTALLED_APPS = (
       #'grappelli', #http://django-grappelli.readthedocs.org/en/latest/customization.html
        #'admin_tools.theming',
        #'admin_tools.menu',
        #'admin_tools.dashboard',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'haystack',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',    
        'allauth.socialaccount.providers.google',  
        'allauth.socialaccount.providers.twitter', 
        'allauth.socialaccount.providers.facebook',   
        'djrill',
        'parsley',         
        'apps.account_system',    
        'apps.establishment_system', #https://github.com/dcramer/django-ratings
        'apps.externals.djangoratings',
        #'south',     #https://github.com/agiliq/Django-parsley  #http://parsleyjs.org/
        #'drealtime',   #https://bitbucket.org/inzane/django-realtime
        'dajaxice',     #http://django-dajaxice.readthedocs.org/en/latest/
        'dajax',
        'notifications',#https://github.com/django-notifications/django-notifications
        #'dajax',       #http://django-dajax.readthedocs.org/en/latest/
        'configurations',    
        'geoposition',  #http://django-geoposition.readthedocs.org/
        #'ajax_select',
        #'apps.djadmin_ext',
        'imagekit',
        #'fluent_comments',
        'crispy_forms',       
        #'django_comments_xtd',
        'rest_framework',
        'selectable', #http://django-selectable.readthedocs.org/en/latest/admin.html
        'autocomplete_light',
        'queued_search', #https://github.com/toastdriven/queued_search
        'bootstrap3', #https://github.com/dyve/django-bootstrap3
        'mathfilters',#https://github.com/dbrgn/django-mathfilters
    )

    #HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.BaseSignalProcessor'
    #HAYSTACK_SIGNAL_PROCESSOR = 'apps.establishment_system.signals.QueuedSignalProcessor'
    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


    # HAYSTACK_CONNECTIONS = {
    #     'default': {
    #         'ENGINE': 'xapian_backend.XapianEngine',
    #         'PATH': os.path.join(os.path.dirname(__file__), 'xapian_index')
    #     },
    # }   

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        },
    }

    # HAYSTACK_CONNECTIONS = {
    #     'default': {
    #         'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    #     },
    # }
    
    #COMMENTS_APP = 'fluent_comments'
    #COMMENTS_APP = 'django_comments_xtd'
    #COMMENTS_APP = 'django.contrib.comments'
    #COMMENTS_XTD_CONFIRM_EMAIL =True
    #COMMENTS_XTD_MODEL = "apps.establishment_system.models.Comentario"
    #COMMENTS_XTD_FORM_CLASS = "apps.establishment_system.forms.CommentForm"
    #FLUENT_COMMENTS_EXCLUDE_FIELDS = ('name', 'email', 'url')
    COMMENT_MAX_LENGTH=500

    #COMMENTS_XTD_CONFIRM_EMAIL = False

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',    
        #'drealtime.middleware.iShoutCookieMiddleware',
    )

    ROOT_URLCONF = 'RecomendadorUD.urls'

    WSGI_APPLICATION = 'RecomendadorUD.wsgi.application'

    TEMPLATE_DIRS = (
        join(BASE_DIR,  'templates'),
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )

    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

    

    # Internationalization

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'America/Bogota'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/
    STATIC_URL = '/static/'    
    STATICFILES_DIRS = (    
        join(BASE_DIR,  'static'),
    )

    # STATIC_URL =join(BASE_DIR,'/static/')
    #STATIC_ROOT =join(BASE_DIR,'static')



    #Custom model users
    AUTH_USER_MODEL = 'account_system.User'

    
    #
    #Mandrill Configuration
    #
    MANDRILL_API_KEY = "dF6LAeaL1H2ZGsbU-Ypu6Q"

    #EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
    EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
    DEFAULT_FROM_EMAIL='camilolinchis@recomendadorud.com'

    ##DJANGO-ALLAUTH
    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.request",
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        "apps.establishment_system.context_processors.notificaciones",
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",

    )

    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",    
    )


    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'dajaxice.finders.DajaxiceFinder',
    )

    SITE_ID = 2

        
    ACCOUNT_ADAPTER =('allauth.account.adapter.DefaultAccountAdapter')
        #Specifies the adapter class to use, allowing you to alter certain default behaviour.
    ACCOUNT_AUTHENTICATION_METHOD ='username'#('username' | 'email' | 'username_email')   
        #Specifies the login method to use – whether the user logs in by entering his username, e-mail address, or either one of both.
    ACCOUNT_CONFIRM_EMAIL_ON_GET =True
        #Determines whether or not an e-mail address is automatically confirmed by a mere GET request.
    ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL ='/accounts/new_user/'
        #The URL to redirect to after a successful e-mail confirmation, in case no user is logged in.
    ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL ='/accounts/new_user/'
    EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL ='/accounts/new_user/'
        #The URL to redirect to after a successful e-mail confirmation, in case of an authenticated user.
        # Set to None to use settings.LOGIN_REDIRECT_URL.
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =3
        #Determines the expiration date of email confirmation mails (# of days).
    ACCOUNT_EMAIL_REQUIRED =True
        #The user is required to hand over an e-mail address when signing up.
    ACCOUNT_EMAIL_VERIFICATION ='mandatory'
        #Determines the e-mail verification method during signup – choose one of 'mandatory', 'optional', or 'none'. When set to '
        #mandatory' the user is blocked from logging in until the email address is verified. 
        #Choose 'optional' or 'none' to allow logins with an unverified e-mail address.
        #In case of 'optional', the e-mail verification mail is still sent, whereas in case of 'none' no e-mail verification mails are sent.
    ACCOUNT_EMAIL_SUBJECT_PREFIX ='[RecomendadorUD] '
        #Subject-line prefix to use for email messages sent. By default, the name of the current Site (django.contrib.sites) is used.
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = ('http')
        #The default protocol used for when generating URLs, e.g. for the password forgotten procedure. 
        #Note that this is a default only – see the section on HTTPS for more information.
    ACCOUNT_LOGOUT_ON_GET =False
        #Determines whether or not the user is automatically logged out by a mere GET request. See documentation for the LogoutView for details.
    ACCOUNT_LOGOUT_REDIRECT_URL ='/'
        #The URL (or URL name) to return to after the user logs out. This is the counterpart to Django’s LOGIN_REDIRECT_URL.
    ACCOUNT_SIGNUP_FORM_CLASS ='apps.account_system.forms.SignupExtendForm'
        #A string pointing to a custom form class (e.g. ‘myapp.forms.SignupForm’) that is used during signup to ask the user 
        #for additional input (e.g. newsletter signup, birth date). This class should implement a def signup(self, request, user) 
        #method, where user represents the newly signed up user.
    ACCOUNT_SIGNUP_PASSWORD_VERIFICATION =True
        #When signing up, let the user type in his password twice to avoid typo’s.
    ACCOUNT_UNIQUE_EMAIL =True
        #Enforce uniqueness of e-mail addresses.
    ACCOUNT_USER_MODEL_USERNAME_FIELD ='username'
        #The name of the field containing the username, if any. See custom user models.
    ACCOUNT_USER_MODEL_EMAIL_FIELD ='email'
        #The name of the field containing the email, if any. See custom user models.
    #ACCOUNT_USER_DISPLAY ="user.username"
        #A callable (or string of the form ‘some.module.callable_name’) that takes a user as its only argument and returns the 
        #display name of the user. The default implementation returns user.username.
    ACCOUNT_USERNAME_MIN_LENGTH =4
        #An integer specifying the minimum allowed length of a username.
    ACCOUNT_USERNAME_BLACKLIST =[]
        #A list of usernames that can’t be used by user.
    ACCOUNT_USERNAME_REQUIRED =True
        #The user is required to enter a username when signing up. Note that the user will be asked to do so even if 
        #ACCOUNT_AUTHENTICATION_METHOD is set to email. Set to False when you do not wish to prompt the user to enter a username.
    ACCOUNT_PASSWORD_INPUT_RENDER_VALUE =False
        #render_value parameter as passed to PasswordInput fields.
    ACCOUNT_PASSWORD_MIN_LENGTH =4
        #An integer specifying the minimum password length.
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =True
        #The default behaviour is to automatically log the user in once he confirms his email address. By changing this setting to False he will not be logged in, but redirected to the ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL
    ACCOUNT_SESSION_REMEMBER =None
        #Controls the life time of the session. Set to None to ask the user ('Remember me?'), False to not remember, and True to always remember.
    ACCOUNT_SESSION_COOKIE_AGE =1814400
        #How long before the session cookie expires in seconds. Defaults to 1814400 seconds, or 3 weeks.
    SOCIALACCOUNT_ADAPTER ='allauth.socialaccount.adapter.DefaultSocialAccountAdapter'
    #SOCIALACCOUNT_ADAPTER ='apps.account_system.views.AccountAdapter'
        #Specifies the adapter class to use, allowing you to alter certain default behaviour.
    SOCIALACCOUNT_QUERY_EMAIL =ACCOUNT_EMAIL_REQUIRED
        #Request e-mail address from 3rd party account provider? E.g. using OpenID AX, or the Facebook 'email' permission.
    SOCIALACCOUNT_AUTO_SIGNUP =False
        #Attempt to bypass the signup form by using fields (e.g. username, email) retrieved from the social account provider. 
        #If a conflict arises due to a duplicate e-mail address the signup form will still kick in.
    SOCIALACCOUNT_EMAIL_REQUIRED =ACCOUNT_EMAIL_REQUIRED
        #The user is required to hand over an e-mail address when signing up using a social account.
    SOCIALACCOUNT_EMAIL_VERIFICATION =ACCOUNT_EMAIL_VERIFICATION
        #As ACCOUNT_EMAIL_VERIFICATION, but for social accounts.
    #SOCIALACCOUNT_PROVIDERS (= dict)
        #Dictionary containing provider specific settings.


    LOGIN_REDIRECT_URLNAME='/home/'
    LOGOUT_REDIRECT_URL='/home/'

    SOCIALACCOUNT_PROVIDERS = { 
            'google':{ 
                'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile','email'],
                'AUTH_PARAMS': { 'access_type': 'online' },
                'VERIFIED_EMAIL': False
            },
            'facebook':{
                'SCOPE': ['email', 'publish_stream'],
                #'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
                'METHOD': 'oauth2',
                'LOCALE_FUNC':  lambda request: 'en_us',
                #'VERIFIED_EMAIL': False
            }
        }   

    FIXTURE_DIRS = (        
        join(BASE_DIR,  '/account_system/fixtures/'),
        join(BASE_DIR,  '/establishment_system/fixtures/'),
    )

    #AJAX_SELECT_BOOTSTRAP = False

    MEDIA_ROOT =  join(BASE_DIR,  'media')
    MEDIA_URL = '/media/'


    

    """
    Twitter:
        Apikey=6cO8HoMTIuOaMAyFNT1yxSea0
        Secret=XolegaJvDWvyGREcziHv8q7GkyKsXNUjEmJh0lVRY4HM8B2N0c

    Facebook:
        ApiKey=543350239130783
        apiSecret=7a6bc2911c658b8418131d057ab44335

    Google+:
        ApiKey=481544714964-9jtarg0p2l7qm4ep7ea4u3ors9hpd43b.apps.googleusercontent.com
        secret=HY5M6bs8qpX02dcSsqKtCJ3-
    """


    REST_FRAMEWORK = {
        # Use hyperlinked styles by default.
        # Only used if the `serializer_class` attribute is not set on a view.
        #'DEFAULT_MODEL_SERIALIZER_CLASS':            'rest_framework.serializers.HyperlinkedModelSerializer',

        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        # 'DEFAULT_PERMISSION_CLASSES': [
        #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        # ],

        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    }

    GRAPPELLI_ADMIN_TITLE= "RecomendadorUD"
    #ADMIN_TOOLS_MENU="RecomendadorUD"
    



class Dev(Base):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True    
    DEBUG_TOOLBAR_PATCH_SETTINGS = True
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
    SOCIALACCOUNT_EMAIL_VERIFICATION =None
    ACCOUNT_EMAIL_VERIFICATION =None
    

    INSTALLED_APPS = Base.INSTALLED_APPS + (                     
        'django_extensions',
        'debug_toolbar',    
    )

    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    MIDDLEWARE_CLASSES =   Base.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    #('debug_toolbar.middleware.DebugToolbarMiddleware',) + Base.MIDDLEWARE_CLASSES

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    
      
class Prod(Base):
    DEBUG = False
    ALLOWED_HOSTS=['localhost']





#Slider menu = https://github.com/codrops/Blueprint-SlidePushMenus