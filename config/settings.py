from pathlib import Path
import os
import environ
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, True))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = [""]


# Application definition
SYSTEM_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # [Django-Rest-Framework]
    "rest_framework",
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    
    # django-rest-auth
    'dj_rest_auth',
    'dj_rest_auth.registration',

    #django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    "corsheaders",  # CORS
    "drf_yasg",  # swagger
]

CUSTOM_APPS = [
    "accounts.apps.AccountsConfig",
    "posts.apps.PostsConfig",
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS


#dj-rest-auth 관련 환경 설정
REST_AUTH = {
    #jwt-token 관련
    # jwt 인증 방식을 사용할지 여부
    'USE_JWT': True, 
    # JWT_AUTH_HTTPONLY : 쿠키를 http only로 할 것인지 여부 (default == True)
    # 위 설정을 refresh token을 보안상의 이유로 http only 쿠키를 설정할 필요가 있다, refresh_token을 cookie로 전달
    
    # refresh token을 담은 쿠키 이름
    'JWT_AUTH_REFRESH_COOKIE': "refresh_token",
    #jwt쿠키 csrf 검사
    'JWT_AUTH_COOKIE_USE_CSRF' : True,
    #세션 로그인 기능 (default == True), 세션 로그인을 False로 하지 않으면 sessionid가 쿠키로 남기 때문에 지워주었다.
    'SESSION_LOGIN' : False,
    'JWT_AUTH_HTTPONLY':False,
    #custom한 serializer로 변경
    'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',


}
#simple JWT 환경 설정
SIMPLE_JWT = {
    'JWT_SECRET_KEY': SECRET_KEY,   # JWT 에 서명하는데 사용되는 시크릿키. 장고의 시크릿키가 디폴트.
    'JWT_ALGORITHM': 'HS256',       # PyJWT 에서 암호화 서명에 지원되는 알고리즘으로 마찬가지로 이것 또한 기본값.
    'JWT_VERIFY_EXPIRATION' : True, # 토큰 만료 시간 확인. 기본값 True.
    
    
    'JWT_ALLOW_REFRESH': True,      # 토큰 새로고침 기능 활성화. 기본값 False.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

# rest_framework에서의 permission과 authentication
REST_FRAMEWORK = {
    
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # "rest_framework.authentication.SessionAuthentication", 지우면 API 엔드포인트에서 로그인이 안되니 주의하자!!
    #'rest_framework.authentication.SessionAuthentication',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        [
            'dj_rest_auth.jwt_auth.JWTCookieAuthentication' ]
    ),
    
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1

ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    
    'allauth.account.middleware.AccountMiddleware',

]

ROOT_URLCONF = 'config.root_urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
MYSQL_DB = env('MYSQL_DB')
if MYSQL_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env("DB_NAME"),
            'USER': env("DB_USER"),
            'PASSWORD': env("DB_PASSWORD"),
            'HOST': env("DB_HOST"),
            'PORT': env("DB_PORT"),
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,  # 원하는 최소 길이로 변경
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'validators.CharacterClassesValidator',
    },
    {
        'NAME': 'validators.NoConsecutiveCharactersValidator',
    },
]


# Internationalization
LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL='/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Customizing User model
AUTH_USER_MODEL = "accounts.User"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER") # 발신할 이메일
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD") # 발신할 메일의 비밀번호
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER