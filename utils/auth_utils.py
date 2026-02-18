from passlib.context import CryptContext

bycrpt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return bycrpt_context.hash(password)

def verify_password(password_passed: str, hashed_password: str) -> bool:
    return bycrpt_context.verify(password_passed, hashed_password)
