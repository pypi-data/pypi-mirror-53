# fyle-django-allauth

Fyle OAuth 2.0 provider for django-allauth, lets you associate Fyle accounts with your User accounts.


## Dependencies
Install  [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html) and configure it.



## Quick start

1. Install fyle-django-allauth

    ```
    pip install fyle-django-allauth
    ```

2. Include 'fyle_allauth' in the INSTALLED_APPS section of settings.py :
    ```
    INSTALLED_APPS = (
    ...
    'django.contrib.sites',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'fyle_allauth'  # new 
    ```

4. Fyle App registration (get your client_id and client_secret here)
    1. Login to [Fyle](https://app.fyle.in)
    2. Goto settings and click on Developers
    3. Click on create new app, enter the details and select type as OAuth 2.0
    4. For Redirect URI enter 
        1. 'http://localhost:8000/accounts/fyle/login/callback/' for development
        2. 'https://your_domain/accounts/fyle/login/callback/' for production
    5. Note down the client_secret and client_id
    
5. Open django-admin and create a new record under Social Applications
    Select Fyle as provider and enter the above noted client_secret and client_id.
    
    Final step is to add our site to the Chosen sites on the bottom.
    

6. Visit http://localhost:8000/accounts/fyle/login to login using your Fyle account.


7. If using a custom user model then add the below lines to settings.py
```
# For custom user model that has email as the user identifying field
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Disable verification mail [optional]
ACCOUNT_EMAIL_VERIFICATION = 'none'  
``` 
For more info on customisation refer the django-allauth [documentation](https://django-allauth.readthedocs.io/en/latest/advanced.html#custom-user-models)