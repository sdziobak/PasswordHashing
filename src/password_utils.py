from enum import Enum

class PasswordUtils:

    def generate_super_strong_password() -> str:
        password = ""
        #
        return password

    def generate_memorable_password() -> str:
        password = ""
        return password

    def get_password_strength(password: str) -> 'PasswordStrength':
        strength: PasswordStrength = None
        # 
        return strength

class PasswordStrength(Enum):
    WEAK = 1
    MEDIUM = 2
    STRONG = 3


if __name__ == "__main__":
    PasswordUtils.generate_super_strong_password()