from graphql_jwt.settings import jwt_settings
import jwt


def jwt_encode(payload, context=None):
    return jwt.encode(
        payload,
        jwt_settings.JWT_PRIVATE_KEY or jwt_settings.JWT_SECRET_KEY,
        jwt_settings.JWT_ALGORITHM,
    )
