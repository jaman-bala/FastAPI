from passlib.context import CryptContext # pip install passlib
import jwt# pip install python-jose

from app.user.models import UserModel


JWT_SECRET = "liusaehfliu54feswa8v418ab4^&$*"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # pip install bcrypt


#create Token
def create_access_token(user):
    try:
        payload = {
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "active": user.is_active,
        }
        return jwt.encode(payload, key=JWT_SECRET, algorithm=ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex


# Схожость имен в базе
def get_password_hash(password):
    return pwd_context.hash(password)
