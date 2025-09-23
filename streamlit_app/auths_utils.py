import jwt
import datetime
import secrets
import os

JWT_SECRET = "sua_chave_secreta_super_segura"
JWT_ALGORITHM = "HS256"
TOKEN_PATH = "sessao.jwt"

def gerar_token(email, fisioterapeuta):
    payload = {
        "email": email,
        "fisioterapeuta": fisioterapeuta,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def validar_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["email"], payload["fisioterapeuta"]
    except jwt.ExpiredSignatureError:
        return None, None
    except jwt.InvalidTokenError:
        return None, None

def salvar_token_local(token):
    with open(TOKEN_PATH, "w") as f:
        f.write(token)

def carregar_token_local():
    try:
        with open(TOKEN_PATH, "r") as f:
            return f.read()
    except:
        return None

def limpar_token_local():
    if os.path.exists(TOKEN_PATH):
        os.remove(TOKEN_PATH)