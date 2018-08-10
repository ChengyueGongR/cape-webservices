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

from typing import Union
from sanic import Sanic
from logging import info
from cape_webservices.configuration.configuration_core import configuration_endpoints
from cape_webservices.errors.errors_core import errors_endpoints
from cape_webservices.app.app_core import app_endpoints
from cape_webservices.app.app_annotation_endpoints import app_annotation_endpoints
from cape_webservices.app.app_document_endpoints import app_document_endpoints
from cape_webservices.app.app_saved_reply_endpoints import app_saved_reply_endpoints
from cape_webservices.app.app_inbox_endpoints import app_inbox_endpoints
from cape_webservices.app.app_user_endpoints import app_user_endpoints
from cape_webservices import webservices_settings

app = Sanic(__name__)
app.blueprint(app_endpoints)
app.blueprint(app_annotation_endpoints)
app.blueprint(app_document_endpoints)
app.blueprint(app_saved_reply_endpoints)
app.blueprint(app_inbox_endpoints)
app.blueprint(app_user_endpoints)
app.blueprint(errors_endpoints)
app.blueprint(configuration_endpoints)
app.static('/', file_or_directory=webservices_settings.STATIC_FOLDER)
app.static('/', file_or_directory=webservices_settings.HTML_INDEX_STATIC_FILE)

app.config.update(webservices_settings.WEBAPP_CONFIG)

info(f"List of active endpoints { app.router.routes_all.keys() }")


def run(port: Union[None, int] = None):
    if port is not None:
        webservices_settings.CONFIG_SERVER['port'] = int(port)
    info("Using port: %d", webservices_settings.CONFIG_SERVER['port'])
    app.config.LOGO = None
    app.run(**webservices_settings.CONFIG_SERVER)
