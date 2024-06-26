# tornado-authz

[![Discord](https://img.shields.io/discord/1022748306096537660?logo=discord&label=discord&color=5865F2)](https://discord.gg/S5UjpzGZjN)

## Installation

Clone this repo

```bash
git clone https://github.com/pycasbin/tornado-authz
```

## Simple Example

```python
import asyncio
import tornado
from casbin import Enforcer

from tornado_authz import CasbinMiddleware


# Create a CasbinMiddleware instance with the enforcer
enforcer = Enforcer("../examples/authz_model.conf", "../examples/authz_policy.csv")
middleware = CasbinMiddleware(enforcer)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = None
        if self.get_secure_cookie("user"):
            user = self.get_secure_cookie("user").decode('utf-8')
        return user

    def prepare(self):
        # Check the permission for the current request
        middleware(self)


class MainHandler(BaseHandler):
    def get(self):
        self.write("Main Page")


class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/dataset1/")


class DatasetHandler(BaseHandler):
    def get(self):
        self.write("You must be alice to see this.")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/dataset1/.*", DatasetHandler),
    ], cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")


async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

```

## Documentation

The authorization determines a request based on ``{subject, object, action}``, which means what ``subject`` can perform
what ``action`` on what ``object``. In this plugin, the meanings are:

1. ``subject``: the logged-in username
2. ``object``: the URL path for the web resource like `dataset1/item1`
3. ``action``: HTTP method like GET, POST, PUT, DELETE, or the high-level actions you defined like "read-file", "write-blog"

For how to write authorization policy and other details, please refer to [the Casbin's documentation](https://casbin.org).

## Getting Help

- [Casbin](https://casbin.org)

## License

This project is under Apache 2.0 License. See the [LICENSE](LICENSE) file for the full license text.