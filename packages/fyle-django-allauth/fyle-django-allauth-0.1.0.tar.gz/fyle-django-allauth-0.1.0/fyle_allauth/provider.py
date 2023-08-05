"""
django-allauth provider.py
"""

from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class FyleAccount(ProviderAccount):
    pass


class FyleProvider(OAuth2Provider):
    """
    Fyle Provider class
    """
    id = 'fyle'
    name = 'Fyle'
    account_class = FyleAccount

    def extract_uid(self, data):
        """
        Extracts the unique user ID from `data`
        """
        return str(data['data']['id'])

    def extract_common_fields(self, data):
        """
        Extracts fields from `data` that will be used to populate the
        `User` model in the `SOCIALACCOUNT_ADAPTER`'s `populate_user()`
        method.

        For example:

            {'first_name': 'John'}

        :return: dictionary of key-value pairs.
        """
        return dict(email=data['data'].get('employee_email'),
                    username=data['data'].get('employee_email'),
                    name=data['data'].get('full_name'))

    def get_default_scope(self):
        """
        Get the OAuth scopes
        :return: list of scopes
        """
        scope = ['read', 'write', ]
        return scope


providers.registry.register(FyleProvider)
provider_classes = [FyleProvider]
