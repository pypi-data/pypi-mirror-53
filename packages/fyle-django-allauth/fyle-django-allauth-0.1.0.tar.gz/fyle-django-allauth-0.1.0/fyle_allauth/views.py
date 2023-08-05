import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import FyleProvider


class FyleOAuth2Adapter(OAuth2Adapter):
    """
    Fyle OAuth2Adapter
    """
    provider_id = FyleProvider.id
    web_url = 'https://staging.fyle.in'

    access_token_url = '{0}/api/oauth/token'.format(web_url)
    authorize_url = '{0}/app/main/#/oauth/authorize'.format(web_url)
    profile_url = '{0}/api/tpa/v1/employees/my_profile'.format(web_url)

    def complete_login(self, request, app, token, **kwargs):
        """
        Returns a SocialLogin instance
        """
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(FyleOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(FyleOAuth2Adapter)
