from passlib.context import  CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])
# deprecated 弃用 ， false 不弃用

class Hash() :
    @staticmethod
    def bcrypt(password : str):
        return pwd_context.hash(password)

    @staticmethod
    def verify(   plain_password , hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
