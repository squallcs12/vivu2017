from allauth.socialaccount import providers
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class FacebookProvider2(FacebookProvider):
    id = 'facebook'

    def extract_common_fields(self, data):
        fields = super(FacebookProvider2, self).extract_common_fields(data)
        if not fields['username']:
            fields['username'] = fields['email']
        if not fields['username']:
            fields['username'] = 'fb_{}'.format(data['id'])
        return fields


providers.registry.register(FacebookProvider2)


class FacebookOAuth2Adapter2(FacebookOAuth2Adapter):
    provider_id = FacebookProvider2.id


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter2
