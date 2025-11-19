import secrets
import string
import re

def generate_temporary_password(length=12):
    """Generate a temporary password satisfying policy:
    - min length 8 (caller can request longer)
    - at least 1 uppercase, 1 lowercase, 1 digit, 1 special char
    """
    if length < 8:
        length = 8

    specials = '!@#$%&*()-_=+[]{}<>?'
    categories = [string.ascii_uppercase, string.ascii_lowercase, string.digits, specials]

    # ensure at least one from each category
    password_chars = [secrets.choice(cat) for cat in categories]

    all_chars = string.ascii_letters + string.digits + specials
    while len(password_chars) < length:
        password_chars.append(secrets.choice(all_chars))

    # shuffle
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)


def validate_password_policy(pwd):
    """Return (valid:bool, message:str)."""
    if not pwd or len(pwd) < 8:
        return False, 'La contraseña debe tener al menos 8 caracteres.'
    if not re.search(r'[A-Z]', pwd):
        return False, 'La contraseña debe incluir al menos una letra mayúscula.'
    if not re.search(r'[a-z]', pwd):
        return False, 'La contraseña debe incluir al menos una letra minúscula.'
    if not re.search(r'\d', pwd):
        return False, 'La contraseña debe incluir al menos un dígito.'
    if not re.search(r'[!@#$%&*()\-_=+\[\]{}<>?]', pwd):
        return False, 'La contraseña debe incluir al menos un carácter especial.'
    return True, ''
