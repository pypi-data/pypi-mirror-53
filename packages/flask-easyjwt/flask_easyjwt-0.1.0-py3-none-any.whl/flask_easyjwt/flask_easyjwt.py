#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Definition of the token base class for use in Flask applications.
"""

from typing import cast
from typing import Iterable
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from datetime import datetime
from datetime import timedelta
from warnings import warn

from easyjwt import EasyJWT
from easyjwt import EasyJWTError
from flask import current_app

FlaskEasyJWTClass = TypeVar('FlaskEasyJWTClass', bound='FlaskEasyJWT', covariant=True)
"""
    The type of the :class:`.FlaskEasyJWT` class, allowing subclasses.
"""


class FlaskEasyJWT(EasyJWT):
    """
        The base class for representing JSON Web Tokens (JWT).

        To use a JWT, you have to create a subclass inheriting from :class:`FlaskEasyJWT`. All public instance variables
        of this class (that is, all instance variables not starting with an underscore) will make up the claim set of
        your token (there will be a few meta claims in the token as well that :class:`FlaskEasyJWT` needs to verify the
        token). For details, see the documentation of `EasyJWT <https://easyjwt.readthedocs.io/en/latest/>`__.

        :class:`FlaskEasyJWT` simplifies the usage of `EasyJWT` in Flask applications by allowing to specify a few
        common settings in the application's configuration:

        * The key used for encoding and decoding a token can be specified in the configuration key :attr:`EASYJWT_KEY`.
        * The validity of a token can be specified in the configuration key :attr:`EASYJWT_TOKEN_VALIDITY`. The
          expiration date will be set at the time of creation of a token to the current time plus the specified duration
          (in seconds).
    """

    # region Initialization

    def __init__(self, key: Optional[str] = None) -> None:
        """
            :param key: If set, the given string will be used to encrypt tokens when they are created. If not given,
                        the key defined in the application's configuration will be used. Defaults to `None`.
            :raise EasyJWTError: If no key is given and there is no key defined in the application's configuration.
        """

        self.expiration_date: Optional[datetime]

        if key is None:
            key = self._get_config_key()

        # Perform the default initialization with the chosen key.
        super().__init__(key)

    # endregion

    # region Creation

    def create(self, issued_at: Optional[datetime] = None) -> str:
        """
            Create the actual token from the :class:`EasyJWT` object. Empty optional claims will not be included in the
            token. Empty non-optional claims will cause a :class:`MissingRequiredClaimsError`.

            :param issued_at: The date and time at which this token was issued. If not given, the current date and time
                              will be used. Must be given in UTC. Defaults to `None`.
            :return: The token represented by the current state of the object.
            :raise IncompatibleKeyError: If the given key is incompatible with the algorithm used for encoding the
                                         token.
            :raise MissingRequiredClaimsError: If instance variables that map to non-optional claims in the claim set
                                               are empty.
        """

        # If the expiration date is not set, set it from the application's configuration.
        if self.expiration_date is None:
            self.expiration_date = self._get_config_expiration_date()

        token: str = super().create(issued_at)
        return token

    # endregion

    # region Verification

    @classmethod
    def verify(cls: Type[FlaskEasyJWTClass],
               token: str,
               key: Optional[str] = None,
               issuer: Optional[str] = None,
               audience: Optional[Union[Iterable[str], str]] = None
               ) -> FlaskEasyJWTClass:
        """
            Verify the given JSON Web Token.

            :param token: The JWT to verify.
            :param key: The key used for decoding the token. This key must be the same with which the token has been
                        created. If left empty, the key set in the application's configuration will be used.
            :param issuer: The issuer of the token to verify.
            :param audience: The audience for which the token is intended.
            :return: The object representing the token. The claim values are set on the corresponding instance
                     variables.
            :raise EasyJWTError: If no key is given and there is no key defined in the application's configuration.
            :raise ExpiredTokenError: If the claim set contains an expiration date claim ``exp`` that has passed.
            :raise ImmatureTokenError: If the claim set contains a not-before date claim ``nbf`` that has not yet been
                                       reached.
            :raise IncompatibleKeyError: If the given key is incompatible with the algorithm used for decoding the
                                         token.
            :raise InvalidAudienceError: If the given audience is not specified in the token's audience claim, or no
                                         audience is given when verifying a token with an audience claim, or the given
                                         audience is not a string, an iterable, or `None`.
            :raise InvalidClaimSetError: If the claim set does not contain exactly the expected (non-optional) claims.
            :raise InvalidClassError: If the claim set is not verified with the class with which the token has been
                                      created.
            :raise InvalidIssuedAtError: If the claim set contains an issued-at date ``iat`` that is not an integer.
            :raise InvalidIssuerError: If the token has been issued by a different issuer than given.
            :raise InvalidSignatureError: If the token's signature does not validate the token's contents.
            :raise UnspecifiedClassError: If the claim set does not contain the class with which the token has been
                                          created.
            :raise UnsupportedAlgorithmError: If the algorithm used for encoding the token is not supported.
            :raise VerificationError: If a general error occurred during decoding.
        """

        if key is None:
            key = cls._get_config_key()

        return cast(FlaskEasyJWTClass, super().verify(token, key, issuer, audience))

    # endregion

    # region Configuration Values

    @staticmethod
    def _get_config_expiration_date() -> Optional[datetime]:
        """
            Get the expiration date based on the token's validity defined in the current Flask app's configuration.

            The token's validity is read from the configuration key `EASYJWT_TOKEN_VALIDITY`. The value can either be
            a string castable to an integer, an integer (both interpreted in seconds), or a `datetime.timedelta`
            object.

            :return: `None` if no token validity is defined in the application's configuration or if the value has a
                     wrong type. A `datetime` object otherwise, in UTC and the defined amount of time from now.
        """

        # If no token validity is defined, the token won't have an expiration date.
        validity = current_app.config.get('EASYJWT_TOKEN_VALIDITY', None)
        if validity is None:
            return None

        # If the validity is specified as a string, convert it to an integer.
        if isinstance(validity, str):
            try:
                validity = int(validity)
            except ValueError:
                # If the string cannot be parsed to an integer, the validity is invalid.
                # In this case, let the validity as is; the following checks will fail as well,
                # and thus, a warning will be issued without having to duplicate the warning code.
                pass

        # If the validity is specified as an integer or has been parsed to one, convert it to a timedelta object.
        if isinstance(validity, int):
            validity = timedelta(seconds=validity)

        # If the validity still is not a timedelta object, issue a warning.
        if not isinstance(validity, timedelta):
            warn('EASYJWT_TOKEN_VALIDITY must be an int, a string castable to an int, or a datetime.timedelta.')
            return None

        # The expiration date of the token is the given amount of time from now.
        return datetime.utcnow().replace(microsecond=0) + validity

    @staticmethod
    def _get_config_key() -> str:
        """
            Get the key for encrypting and decrypting tokens from the current Flask app's configuration.

            :return: The key defined in the application's configuration. `None` if none is set.
            :raise EasyJWTError: If there is no key defined in the application's configuration.
        """

        # If there is a key defined in the EasyJWT configuration key, use this. Otherwise, fall back to the app' secret
        # key.
        key: Optional[str] = current_app.config.get('EASYJWT_KEY', None)
        if key is not None:
            return key

        # Fall back to the application's secret key.
        key = current_app.config.get('SECRET_KEY', None)
        if key is not None:
            return key

        raise EasyJWTError('No key set for encrypting tokens. Set EASYJWT_KEY or SECRET_KEY.')

    # endregion
