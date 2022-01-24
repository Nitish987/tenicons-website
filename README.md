Simple image distribution website, in djnago. User can get free images and able to download images from the site.

### Required fields in settings.py

##### secret key
SECRET_KEY = 'YOUR_SECRET_KEY'

##### database setup 
Setting up mysql database or do your own setup
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'YOUR_DB_NAME',
        'USER': 'YOUR_USER',
        'PASSWORD': 'YOUR_USER_PASSWORD',
        'HOST': 'localhost',
        'PORT': 'YOUR_PORT',
    }
}
```

##### cloud storage storage setup for static files
```
DEFAULT_FILE_STORAGE = 'DEFAULT_FILE_STORAGE'
STATICFILES_STORAGE = 'STATICFILES_STORAGE'
GS_STATIC_BUCKET_NAME = 'GS_STATIC_BUCKET_NAME'
GS_MEDIA_BUCKET_NAME = 'GS_MEDIA_BUCKET_NAME'
GS_PROJECT_ID = 'GS_PROJECT_ID'
```

##### Email setup
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'YOUR_EMAIL_ID'
EMAIL_HOST = 'SMTP_HOST'
EMAIL_PORT = 'PORT_NUMBER_IN_INTEGER'
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = "YOUR_EMAIL_ID_PASSWORD"
```

###### >Run migrations and migrate in your projects 

read django documentation for more info