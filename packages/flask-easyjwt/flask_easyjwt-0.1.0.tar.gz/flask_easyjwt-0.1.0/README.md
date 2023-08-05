# Flask-EasyJWT


[![PyPI](https://img.shields.io/pypi/v/flask_easyjwt.svg)](https://pypi.org/project/flask_easyjwt/)
[![PyPI - License](https://img.shields.io/pypi/l/flask_easyjwt.svg)](https://github.com/BMeu/Flask-EasyJWT/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/BMeu/Flask-EasyJWT.svg?branch=master)](https://travis-ci.org/BMeu/Flask-EasyJWT)
[![codecov](https://codecov.io/gh/BMeu/Flask-EasyJWT/branch/master/graph/badge.svg)](https://codecov.io/gh/BMeu/Flask-EasyJWT)
[![Documentation Status](https://readthedocs.org/projects/flask-easyjwt/badge/?version=latest)](https://flask-easyjwt.readthedocs.io/en/latest/?badge=latest)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask_easyjwt.svg)

Flask-EasyJWT provides a simple interface to creating and verifying
[JSON Web Tokens (JWTs)](https://tools.ietf.org/html/rfc7519) in Python. It allows you to once define the claims of the
JWT, and to then create and accept tokens with these claims without having to check if all the required data is given
or if the token actually is the one you expect.

Flask-EasyJWT is a simple wrapper around [EasyJWT](https://github.com/BMeu/EasyJWT) for easy usage in
[Flask](http://flask.pocoo.org/) applications. It provides configuration options via Flask's application configuration
for common settings of all tokens created in a web application. For detailed information on how to use
[EasyJWT](https://github.com/BMeu/EasyJWT), see [its documentation](https://easyjwt.readthedocs.org/en/latest/).

```python
from flask_easyjwt import FlaskEasyJWT
from flask import Flask

# Define the claims of your token.
class MySuperSimpleJWT(FlaskEasyJWT):

    def __init__(self, key):
        super().__init__(key)
        
        # Define a claim `name`.
        self.name = None

# Define the default configuration options for FlaskEasyJWT
# in the configuration of your Flask app.
app = Flask(__name__)
app.config.from_mapping(
    # The default key for encoding and decoding tokens.
    EASYJWT_KEY='Super secret key',

    # Tokens will be valid for 15 minutes after creation by default.
    EASYJWT_TOKEN_VALIDITY=15 * 60
)

@app.route('/token/<name>')
def get_token(name):
    """ This view returns a token with the given name as its value. """
    token_object = MySuperSimpleJWT()
    token_object.name = name
    return token_object.create()

@app.route('/verify/<token>')
def verify_token(token):
    """ This view verifies the given token and returns the contained name. """
    verified_token_object = MySuperSimpleJWT.verify(token)
    return verified_token_object.name
```

## Features

 * Integrates [EasyJWT](https://github.com/BMeu/EasyJWT) into Flask for easy configuration of default options for
   creating and verifying JWTs.
 * Define the claims of your token once as a class, then use this class to easily create and verify multiple tokens.
 * No worries about typos in dictionary keys: the definition of your claim set as a class enables IDEs to find those
   typos for you.
 * Multiple tokens may have the same claims, but different intentions. Flask-EasyJWT will take care of this for you: you
   can define a token for account validation and one for account deletion, both with the account ID as a claim, and you
   don't need to worry about accidentally deleting a newly created account instead of validating it, just because
   someone mixed up the tokens.
 * All registered JWT claims are supported: `aud`, `exp`, `iat`, `iss`, `jti`, `nbf`, and `sub`.

For a full list of features, see [the features of EasyJWT](https://easyjwt.readthedocs.org/en/latest/#features).

## System Requirements & Installation

Flask-EasyJWT requires Python 3.6 or newer.

Flask-EasyJWT is available [on PyPI](https://pypi.org/project/flask_easyjwt/). You can install it using your favorite
package manager.

 * PIP:

    ```bash
    python -m pip install flask_easyjwt
    ```

 * Pipenv:

    ```bash
    pipenv install flask_easyjwt
    ```

## Usage

Flask-EasyJWT is used exactly as [EasyJWT](https://github.com/BMeu/EasyJWT). Therefore, this section only describes the
specific features of Flask-EasyJWT and the basic usage. For detailed explanations on how to use EasyJWT (for example,
optional claims, registered claims such as `aud`, `iat`, and `sub`, or verifying third-party tokens), see
[its documentation](https://easyjwt.readthedocs.org/en/latest/#usage).

### Application Setup

You do not need to initialize Flask-EasyJWT with your Flask application. All you have to do (although even this is,
strictly speaking, not required), is to specify some default settings for all of your tokens in the configuration of
your Flask application. These settings are:


| Configuration Key        | Description |
|--------------------------|-------------|
| `EASYJWT_KEY`            | The key that will be used for encoding and decoding all tokens. If `EASYJWT_KEY` is not specified, Flask-EasyJWT will fall back to Flask's `SECRET_KEY` configuration value. |
| `EASYJWT_TOKEN_VALIDITY` | The validity of each token after its creation. This value can be given as a string (that is parsable to an integer), an integer, or a `timedelta` object. The former two are interpreted in seconds. |

You can specify these configuration values as any other configuration values in your Flask application, for example,
using a mapping in your code:

```python
from datetime import timedelta
from flask import Flask

app = Flask(__name__)
app.config.update(
    EASYJWT_KEY='Super secret key',
    EASYJWT_TOKEN_VALIDITY=timedelta(minutes=7)
)
```

In this example, all tokens will (by default) be encoded using the (not so secure) string `Super secret key` and will
be valid for seven minutes after they have been created (i.e., after the `create()` method has been called on the token
object).

Of course, any other way of specifying the configuration values will work as well (see
[Flask's documentation](https://flask.palletsprojects.com/en/1.1.x/config/)).

### Token Specification & Usage

Tokens are specified and used exactly as with [EasyJWT](https://easyjwt.readthedocs.org/en/latest/#usage):

```python
from flask_easyjwt import FlaskEasyJWT

# Define the claims of your token.
class MySuperSimpleJWT(FlaskEasyJWT):

    def __init__(self, key):
        super().__init__(key)
        
        # Define a claim `name`.
        self.name = None

# Assuming we are within a Flask app context. 

# Create a token with some values.
token_object = MySuperSimpleJWT()
token_object.name = 'Zaphod Beeblebrox'
token = token_object.create()

# Verify the created token.
verified_token_object = MySuperSimpleJWT.verify(token)
assert verified_token_object.name == 'Zaphod Beeblebrox'
```

The only difference is that you do not have to pass the key for encoding or decoding the token to the constructor and
`verify()` method, respectively (you still can do so if you do not want to use the default key defined in your
application's configuration).

Additionally, if the configuration value `EASYJWT_TOKEN_VALIDITY` is set, the token will
be valid for the amount specified in this configuration value after it has been created with `create()`. If this
configuration value is not set tokens will not expire. If you explicitly set the expiration date on a token object
this value will always take precedence (if it is not `None`):

```python
import datetime

from flask_easyjwt import FlaskEasyJWT
from flask import Flask

# Define the claims of your token.
class MySuperSimpleJWT(FlaskEasyJWT):

    def __init__(self, key):
        super().__init__(key)
        
        # Define a claim `name`.
        self.name = None

# Define the default configuration options for FlaskEasyJWT
# in the configuration of your Flask app.
app = Flask(__name__)
app.config.from_mapping(
    EASYJWT_KEY='Super secret key',
    EASYJWT_TOKEN_VALIDITY=datetime.timedelta(minutes=7)
)

# Assuming we are within a Flask app context.

token_object = MySuperSimpleJWT()
token_object.name = 'Zaphod Beeblebrox'

# This token will expire in 15 minutes, even though the default token validity is set to 7 minutes.
token_object.expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
```

Initializing token objects and creating and verifying tokens must be executed within a
[Flask application context](https://flask.palletsprojects.com/en/1.1.x/appcontext/) if you want to use the configuration
values from the application's configuration.

## Acknowledgements

Flask-EasyJWT is just an easy-to-use abstraction layer around José Padilla's
[PyJWT library](https://pypi.org/project/PyJWT/) that does the actual work of creating and verifying the tokens
according to the JWT specification. Without his work, Flask-EasyJWT would not be possible.

## License

Flask-EasyJWT is developed by [Bastian Meyer](https://www.bastianmeyer.eu)
<[bastian@bastianmeyer.eu](mailto:bastian@bastianmeyer.eu)> and is licensed under the
[MIT License]((http://www.opensource.org/licenses/MIT)). For details, see the attached [LICENSE](LICENSE) file. 
