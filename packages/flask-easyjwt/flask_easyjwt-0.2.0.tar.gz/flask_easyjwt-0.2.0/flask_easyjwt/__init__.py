#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Flask-EasyJWT provides a simple interface to creating and verifying
    `JSON Web Tokens (JWTs) <https://tools.ietf.org/html/rfc7519>`_ in Python. It allows you to once define the claims
    of the JWT, and to then create and accept tokens with these claims without having to check if all the required data
    is given or if the token actually is the one you expect.

    Flask-EasyJWT is a simple wrapper around `EasyJWT <https://github.com/BMeu/EasyJWT>`_ for easy usage in
    `Flask <http://flask.pocoo.org/>`_ applications. It provides configuration options via Flask's application
    configuration  for common settings of all tokens created in a web application.

    See the included README file or the `documentation <https://flask-easyjwt.readthedocs.io/en/latest/index.html>`_ for
    details on how to use Flask-EasyJWT.
"""

from easyjwt import Algorithm
from easyjwt import CreationError
from easyjwt import EasyJWTError
from easyjwt import ExpiredTokenError
from easyjwt import ImmatureTokenError
from easyjwt import IncompatibleKeyError
from easyjwt import InvalidAudienceError
from easyjwt import InvalidClaimSetError
from easyjwt import InvalidClassError
from easyjwt import InvalidIssuedAtError
from easyjwt import InvalidIssuerError
from easyjwt import InvalidSignatureError
from easyjwt import MissingRequiredClaimsError
from easyjwt import UnspecifiedClassError
from easyjwt import UnsupportedAlgorithmError
from easyjwt import VerificationError

from .flask_easyjwt import FlaskEasyJWT

__all__ = [
    # Re-exports of EasyJWT for easier usage of Flask-EasyJWT.
    'Algorithm',
    'CreationError',
    'EasyJWTError',
    'ExpiredTokenError',
    'ImmatureTokenError',
    'IncompatibleKeyError',
    'InvalidAudienceError',
    'InvalidClaimSetError',
    'InvalidClassError',
    'InvalidIssuedAtError',
    'InvalidIssuerError',
    'InvalidSignatureError',
    'MissingRequiredClaimsError',
    'UnspecifiedClassError',
    'UnsupportedAlgorithmError',
    'VerificationError',

    # Flask-EasyJWT exports.
    'FlaskEasyJWT',
]
