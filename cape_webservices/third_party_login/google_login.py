# Copyright 2018 BLEMUNDSBURY AI LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from authomatic import Authomatic
from cape_webservices.third_party_login.third_party_login_settings import CONFIG, SECRET_SALT
from cape_webservices.third_party_login.third_party_login_core import SanicAdapter, \
    upsert_login_redirect, oauth_init
from sanic import response
from cape_webservices.app.app_settings import URL_BASE
from cape_webservices.app.app_settings import app_endpoints

_endpoint_route = lambda x: app_endpoints.route(URL_BASE + x, methods=['GET', 'POST'])
from logging import debug, warning


@_endpoint_route('/user/google-oauth2callback')
async def redirect_login_record_session_google(request):
    success_cb, error_cb, adapter, first_response = oauth_init(request)

    if adapter is None:
        return first_response

    authomatic = Authomatic(config=CONFIG, secret=SECRET_SALT)

    result = authomatic.login(adapter, 'google',
                              # session=session['authomatic'],
                              session_saver=lambda: None)
    if result:
        if result.error:
            warning("Google login error", result.error)
            return response.redirect('%s?error=%s' % (error_cb, result.error))
        elif result.user:
            debug("Google login success", result.user)
            result.user.update()
            debug("Google login update success", result.user)
            userdict = result.user.to_dict()
            return upsert_login_redirect(request, "google:" + userdict['email'], result.user.to_dict(), success_cb, adapter)
    return adapter.response
