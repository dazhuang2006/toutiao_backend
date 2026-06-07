from passlib.context import CryptContext
#创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#获得哈希密码
def get_password_hash(password):
    return pwd_context.hash(password)