import hashlib
from argon2.low_level import hash_secret, Type
import bcrypt
import os
from .hashing_algorithm import HashingAlgorithm
from .user import User
from .database_connection import DatabaseConnection
from typing import Union, Tuple

class Auth:
    """
    Handles things related to authenticating the user, such as hashing.
    """



    """ MD5 """
    @staticmethod
    def __hash_md5(password: bytes, salt: bytes) -> bytes:
        """
        Hashes a password using the MD5 hashing algorithm.

        Args: 
            password (bytes):
            salt (bytes):
        Returns:
            bytes: The hashed password.
        """

        hashed_password = hashlib.md5(salt + password).digest()
        return hashed_password

    """ SHA-512 """
    @staticmethod
    def __hash_sha512(password: bytes, salt: bytes) -> bytes:
        """
        Hashes a password using the SHA-512 hashing algorithm.

        Args: 
            password (bytes):
            salt (bytes):
        Returns:
            bytes: The hashed password.
        """

        hashed_password = hashlib.sha512(salt + password).digest()
        return hashed_password

    """ PBKDF2 """
    @staticmethod
    def __hash_pbkdf2(password: bytes, salt: bytes) -> bytes:
        """
        Hashes a password using the PBKDF2 hashing algorithm.

        Args: 
            password (bytes):
            salt (bytes):
        Returns:
            bytes: The hashed password.
        """

        hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
        return hashed_password

    """ argon2 """
    @staticmethod
    def __hash_argon2(password: bytes, salt: bytes) -> bytes:
        """
        Hashes a password using the Argon2 hashing algorithm.

        Args: 
            password (bytes):
            salt (bytes):
        Returns:
            bytes: The hashed password.
        """

        # Use Argon2 low-level API to specify a custom salt
        hashed_password = hash_secret(
            password,
            salt,
            time_cost=2,
            memory_cost=102400,
            parallelism=8,
            hash_len=32,
            type=Type.I
        )

        return hashed_password

    """ bcrypt """
    @staticmethod
    def __hash_bcrypt(password: bytes, salt: bytes) -> bytes:
        """
        Hashes a password using the bcrypt hashing algorithm.

        Args: 
            password (bytes):
            salt (bytes):
        Returns:
            bytes: The hashed password.
        """

        # Hash the password with the generated salt
        hashed_password_and_metadata = bcrypt.hashpw(password, salt)
        hashed_password = hashed_password_and_metadata[-31:]

        return hashed_password

    """ scrypt """
    @staticmethod
    def __hash_scrypt(password: bytes, salt: bytes) -> bytes:
        """
        Hashes a password using the scrypt hashing algorithm.

        Args: 
            password (bytes):
            salt (bytes):
        Returns:
            bytes: The hashed password.
        """

        hashed_password = hashlib.scrypt(password, salt=salt, n=16384, r=8, p=1)
        return hashed_password

    @staticmethod
    def get_hashed_password(password: str, salt: Union[str, None], hashing_algorithm: HashingAlgorithm) -> Tuple[str, str]:
        """
        Returns a hashed password and salt using whatever hashing algorithm is specified.

        Args: 
            password (str): The plain text password to be hashed.
            salt (str | None): The salt to be used during the hashing. If None is passed in, a random salt will be generated.
            hashing_algorithm (HashingAlgorith): The hashing algorithm to be used on the password.
        Returns:
            tuple[str, str]: The resulting hashed password and the salt used during the hashing process.
        """

        # Changes the password and salt to bytes. If no salt
        # is given, a random one is generated.
        bytes_password = password.encode()
        if salt:
            bytes_salt = bytes.fromhex(salt)
        elif hashing_algorithm == HashingAlgorithm.BCRYPT:
            bytes_salt = bcrypt.gensalt()
        else:
            bytes_salt = os.urandom(16)

        bytes_hashed_password = None

        if hashing_algorithm == HashingAlgorithm.MD5:
            bytes_hashed_password = Auth.__hash_md5(bytes_password, bytes_salt)
        elif hashing_algorithm == HashingAlgorithm.SHA512:
            bytes_hashed_password = Auth.__hash_sha512(bytes_password, bytes_salt)
        elif hashing_algorithm == HashingAlgorithm.PBKDF2:
            bytes_hashed_password = Auth.__hash_pbkdf2(bytes_password, bytes_salt)
        elif hashing_algorithm == HashingAlgorithm.ARGON2:
            bytes_hashed_password = Auth.__hash_argon2(bytes_password, bytes_salt)
        elif hashing_algorithm == HashingAlgorithm.BCRYPT:
            bytes_hashed_password = Auth.__hash_bcrypt(bytes_password, bytes_salt)
        elif hashing_algorithm == HashingAlgorithm.SCRYPT:
            bytes_hashed_password = Auth.__hash_scrypt(bytes_password, bytes_salt)

        if bytes_hashed_password:
            # Changes the salt and hashed_password to a normal string
            # format before being returned.
            salt = bytes_salt.hex()
            hashed_password = bytes_hashed_password.hex()
            return hashed_password, salt
        else:
            raise Exception("There was an error with hashing the password.")



    @staticmethod
    def attemptLogin(stored_user: User, entered_password: str) -> bool:
        """
        This function returns True if the passed in password, when hashed with the stored user's 
        hashing algorithm and salt, matchs the stored user's hash. 

        Args:
            stored_user (User): The user in the database that matches the username the unauthenticated user inputted.
            entered_password (str): The password that was just inputted into the system by the unauthenticated user.
        Returns:
            bool: True if the user is able to authenticate, False otherwise.

        """

        hashed_entered_password, _ = Auth.get_hashed_password(entered_password, stored_user.salt, HashingAlgorithm[stored_user.hashing_algorithm] )

        if hashed_entered_password == stored_user.hashed_password:
            return True
        else: 
            return False



    @staticmethod
    def create_user(username: str, password: str, hashing_algorithm: HashingAlgorithm) -> User:
        """
        Creates a new user in the database and returns the user object.

        Args:
            username (str):
            password (str):
            hashing_algorithm (HashingAlgorithm):
        Returns:
            User: The user that was just added into the database. 

        """
        try:
            hashed_password, salt = Auth.get_hashed_password(password, None, hashing_algorithm)
            new_user = User(username, password, hashing_algorithm.name, hashed_password, salt)
            DatabaseConnection.add_user(new_user)
            return new_user
        except:
            print("There was an error creating the user.")