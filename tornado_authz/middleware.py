# Copyright 2024 The Casbin Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tornado.web import RequestHandler
from casbin import Enforcer


class CasbinMiddleware:
    def __init__(self, enforcer: Enforcer):
        self.enforcer = enforcer

    def __call__(self, handler: RequestHandler):
        # Check the permission for each request.
        if not self.check_permission(handler):
            # Not authorized, return HTTP 403 error.
            self.require_permission(handler)

    def check_permission(self, handler: RequestHandler):
        user = handler.current_user
        if not user:
            user = 'anonymous'
        path = handler.request.uri
        method = handler.request.method
        return self.enforcer.enforce(user, path, method)

    @staticmethod
    def require_permission(handler: RequestHandler):
        handler.send_error(403)
