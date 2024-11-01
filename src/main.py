from .database_connection import DatabaseConnection
from .user import User
from .hashing_algorithm import HashingAlgorithm
from .auth import Auth

# Main function
def main():
    # Ensure the user table exists
    DatabaseConnection.create_user_table()

    while True:
        # Prompt the user for a username
        username = input("Enter a username: ")

        # Check if the username already exists in the database
        found_user = DatabaseConnection.find_user_by_username(username)

        if found_user:
            # Username exists, prompt for password to log in
            print("Username exists. Please log in.")
            stored_password = found_user.hashed_password
            password = input("Enter your password: ")

            # Verify the password
            if stored_password == Auth.hash_md5(password) or stored_password == Auth.hash_sha512(password) or stored_password == Auth.hash_pbkdf2(password) or stored_password == Auth.hash_argon2(password) or stored_password == Auth.hash_bcrypt(password) or stored_password == Auth.hash_scrypt(password):
                print("Login successful.")
            else:
                print("Incorrect password. Try again.")
                continue
        else:
            # Username is new, prompt to create a password
            print("Username created.")
            password = input("Enter a password: ")

        while True:
            # If the user successfully logs in, present the options
            if found_user:
                print("Do you want to:")
                print("1. Log out")
                print("2. Hash the password with a different algorithm")
                print("3. Change the password")
                next_action = input("Enter the number of your choice: ")

                if next_action == '1':
                    return
                elif next_action == '2':
                    pass  # Continue to the hashing algorithm selection
                elif next_action == '3':
                    # Prompt the user for a new password
                    password = input("Enter a new password: ")
                else:
                    print("Invalid choice, please try again.")
                    continue

            hashing_algorithm = get_algorithm_user_choice()

            hashed_password = get_hashed_password(password, hashing_algorithm)

            # Insert or update the username and hashed password in the database
            new_user = User(username, password, hashing_algorithm.name, hashed_password, None)
            if found_user:
                DatabaseConnection.add_user(new_user)
            else:
                DatabaseConnection.add_user(new_user)

            # Output the hashed password
            print("Username and hashed password stored in the database successfully.")
            print(f"Hashed password: {hashed_password}")

            # Ask the user if they want to log out, hash the password with a different algorithm, or change the password
            while True:
                print("Do you want to:")
                print("1. Log out")
                print("2. Hash the password with a different algorithm")
                print("3. Change the password")
                next_action = input("Enter the number of your choice: ")

                if next_action == '1':
                    return
                elif next_action == '2':
                    break
                elif next_action == '3':
                    # Prompt the user for a new password
                    password = input("Enter a new password: ")
                    break
                else:
                    print("Invalid choice, please try again.")

            if next_action == '2':
                continue
            elif next_action == '3':
                while True:

                    hashing_algorithm = get_algorithm_user_choice()

                    hashed_password = get_hashed_password(password, hashing_algorithm)

                    # Update the password for the existing username in the database
                    new_user = User(username, password, hashing_algorithm.name, hashed_password, None)
                    DatabaseConnection.add_user(new_user)

                    # Output the hashed password
                    print("Password updated successfully.")
                    print(f"New hashed password: {hashed_password}")

                    # Ask the user if they want to log out, hash the password with a different algorithm, or change the password
                    break


def get_algorithm_user_choice():

    while True:
        # Display a menu for selecting a hashing algorithm
        print("Select a hashing algorithm:")
        print("1. MD5")
        print("2. SHA-512")
        print("3. PBKDF2")
        print("4. Argon2")
        print("5. bcrypt")
        print("6. scrypt")
        choice = input("Enter the number of the hashing algorithm: ")

        if not choice.isdigit() or int(choice) > len(HashingAlgorithm) or int(choice) < 1:
            print("Invalid choice")
        else:
            return HashingAlgorithm(int(choice))


def get_hashed_password(password: str, hashingAlgorithm: HashingAlgorithm):

    hashed_password = None

    if hashingAlgorithm == HashingAlgorithm.MD5:
        hashed_password = Auth.hash_md5(password)
    elif hashingAlgorithm == HashingAlgorithm.SHA512:
        hashed_password = Auth.hash_sha512(password)
    elif hashingAlgorithm == HashingAlgorithm.PBKDF2:
        hashed_password = Auth.hash_pbkdf2(password)
    elif hashingAlgorithm == HashingAlgorithm.ARGON2:
        hashed_password = Auth.hash_argon2(password)
    elif hashingAlgorithm == HashingAlgorithm.BCRYPT:
        hashed_password = Auth.hash_bcrypt(password)
    elif hashingAlgorithm == HashingAlgorithm.SCRYPT:
        hashed_password = Auth.hash_scrypt(password)

    if hashed_password:
        return hashed_password  
    else: 
         raise Exception("There was an error with hashing the password.")        


if __name__ == "__main__":
    main()
