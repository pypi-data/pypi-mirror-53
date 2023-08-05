# django-saml2-auth-signout-redirect
A plugin to redirect users to a URL (usually an ADFS logout URL) in django-saml2-auth

# Introduction

By default, django-saml2-auth only signs out users in the local Django application.  For security reasons,
the logout needs to be passed to the IdP (identity provider).  Otherwise, a user who clicks the login
button will be logged in again without providing a password (or otherwise).  If you are able to sign the request
(i.e. provide a cert and key), please see `django-saml2-auth-signout-slo`.  If you are not able -- or do not 
want -- to sign the logout request, this plugin is your next-best option.  Instead of a true Single SignOut,
this plugin will let you redirect the user to the IdP's logout page, defaulting to the ADFS `idpinitiatedsignin`
page.

# Example

In settings.py:

    INSTALLED_APPS += (
        ...
        'django_saml2_auth',
        # ensure the plugin is loaded
        'django_saml2_auth_signout_redirect',
        ...
    )
    
    # this is the "usual" config object from django-saml2-auth
    SAML2_AUTH = {
        'DEFAULT_NEXT_URL': '/',
        'PLUGINS': {
            # use this package in lieu of DEFAULT signout plugin 
            'SINGOUT': ['REDIRECT'],
        },
        # optionally specify the URL
        'LOGOUT_REDIRECT_URL': 'https://<idp.com>/<logout>
    }

# ADFS

By default, this package redirects a user to `<SSO Endpoint>/idpinitiatedsignon.aspx` which provides manual 
login/logout on ADFS servers.  Unless you're using an unconventional SSO path, this should work out-of-the-box.