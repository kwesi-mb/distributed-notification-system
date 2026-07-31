from pwdlib import PasswordHash 
from hashlib import sha256

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    return password_hasher.verify(
        password,
        hashed_password,
    )

def hash_token(token: str) -> str:
    return sha256(token.encode()).hexdigest()

def verify_token_hash(token: str, token_hash: str) -> bool:
    return hash_token(token) == token_hash

