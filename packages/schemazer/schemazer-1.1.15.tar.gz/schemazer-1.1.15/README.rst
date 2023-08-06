Schemazer (Flask-Schemazer)
===========================
*Created by Dmitriy Danshin:*

https://gitlab.tingerlink.pro/tingerlink/schemazer

Introduction
------------
Project which allows to describe the schema API. To set input parameters, binding, limitations, ranges, pattern of verification values, and to tie it to the route of the flask view.

Using Schemazer check decorator::

  @schemazer.check(Schema.auth.signIn)

Installation
------------
To install Schemazer, simply::

    pip install schemazer

Examples
--------


Create custom schema API or use ``commons.schema.BaseSchema``::

    class Schema:
        auth = AuthGroup


Create custom methods groups::

    class AuthGroup(SchemazerGroup):
        __group_name__ = 'auth'

        signInEmail = SchemazerMethod(
            group_name=__group_name__,
            name='signInEmail',
            description='Sign in by email.',
            parameters=[
                AuthParameters.Email(),
                AuthParameters.Password()
            ],
            response=SchemazerResponse(schema=TokenField()),
            errors=[AuthErrors.UserNotFound,
                    AuthErrors.AuthTokenExpired],
            limits=[AllLimit()]
        )

Parameters::

    class Email(SchemazerParameter):
        name = 'email'
        description = 'Email'
        type = str
        required = True
        example = 'example@gmail.ru'
        validator = Validator(EmailFormat)

SchemazerResponse schema::

    class AuthTokenResponse(SchemazerResponse):
        description = 'Token'

        schema = SchemazerResponseObjectField(
            name='auth_token',
            fields=[TokenField(), ExpiresInField()]
        )

SchemazerResponse field schema::

    class TokenField(StringField):
        name = 'token'
        description = 'Unique auth token.'
        example = '1q2w3e4r5t6y7u8i9o0p1q2w3e4r5t6y7u8i9o0p'

Init schema::

    Schemazer(app, Schema())

Documentation
-------------

For add documentation by api add::

    from schemazer.docs_view import doc_bp
    app = Flask(__name__)
    app.register_blueprint(doc_bp)


SchemazerResponse examples
-----------------

Error response schema::

    {
        "error":
            {
                "code": "ErrorClass.ErrorName",
                "msg": "Error in param `param1`",
                "failure_param": "param1",
                "params": {
                    "param1": "1234",
                    "param2": "****"
                }
            }
    }


Schemazer configuration
------------------------

Add config for you flask app after Schemazer init::

    app.config.update({'SCHEMAZER_...': '...'})

Schemazer config params start with ``SCHEMAZER_`` prefix::

    SCHEMAZER_VERSION = 1.0

Config parameters
===================

Override in your flask app::

    SCHEMAZER_QUERY_TOKEN = token
    SCHEMAZER_HEADER_TOKEN = Authentication-Token
    SCHEMAZER_COOKIE_TOKEN = auth_token

    SCHEMAZER_QUERY_APIKEY = apikey
    SCHEMAZER_HEADER_APIKEY = Apikey
    SCHEMAZER_COOKIE_APIKEY = apikey

    SCHEMAZER_ERROR_HTTP_CODE = 200
    SCHEMAZER_HOST = localhost
    SCHEMAZER_HTTP_SCHEMA = http
    SCHEMAZER_VERSION = schemazer

DEFAULT ERRORS
==============
Schemazer have default errors objects.

Import objects from::

    from schemazer.commons.errors import *


Default errors objects::

    RequestErrors
        BadRequest
        NotFound
        Undefined

    AccessErrors
        ApiKeyInvalid
        ApiKeyNotFound

    AuthErrors
        UserNotFound
        UserNotVerify
        AuthTokenExpired

