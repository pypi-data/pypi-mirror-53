from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django_saml2_auth import utils
from django_saml2_auth.plugins import SignoutPlugin
from django_saml2_auth.views import _get_saml_client
from saml2.ident import decode


class SingleLogOutSignoutHandler(SignoutPlugin):
    KEY = 'REDIRECT'

    @classmethod
    def signout(cls, request):
        """Logs the user out of the local system and redirects them to the REDIRECT URL in the SAML Metadata"""
        name_id = decode(request.session['name_id'])
        logout(request)

        saml_client = _get_saml_client(utils.get_current_domain(request))
        saml_client.local_logout(name_id)

        url = settings.SAML2_AUTH.get('LOGOUT_REDIRECT_URL')
        if url is None:
            # default to ADFS style logouts
            url = '{}?wa=wsignout1.0'.format(saml_client.sso_location())

        return HttpResponseRedirect(url)
