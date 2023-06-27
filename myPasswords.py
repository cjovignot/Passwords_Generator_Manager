import os
from dotenv import load_dotenv
import json
import random
import string
from cryptography.fernet import Fernet


def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def check_existing_accounts(website, email, data):
    for entry in data:
        if website in entry and entry[website]['email'] == email:
            return entry[website]['password']
    return None


def save_passwords(passwords, encryption_key):
    # Load existing data from JSON file if it exists
    try:
        with open('passwords.json', 'r') as file:
            encrypted_data = file.read()
            decrypted_data = decrypt_data(encrypted_data, encryption_key)
            data = json.loads(decrypted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Check for existing accounts
    for password in passwords:
        website = list(password.keys())[0]
        email = password[website]['email']
        existing_password = check_existing_accounts(website, email, data)
        if existing_password:
            print("You already have an account for this website:")
            print(f"Email: {email}")
            print(f"Password: {existing_password}")
            continue

        # Append new passwords to the existing data
        data.append(password)

    # Encrypt the data
    encrypted_data = encrypt_data(json.dumps(data), encryption_key)

    # Save encrypted data to JSON file
    with open('passwords.json', 'w') as file:
        file.write(encrypted_data)


def encrypt_data(data, encryption_key):
    fernet = Fernet(encryption_key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()


def decrypt_data(encrypted_data, encryption_key):
    fernet = Fernet(encryption_key)
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode()


def main():
    load_dotenv()
    encryption_key = os.getenv('ENCRYPTION_KEY')

    action = input("What do you want to do?\n 1. Get a password\n 2. Create passwords\n\nAnswer: ")

    if action == "1":
        website = input("Enter the name of the website: ")
        email = input("Enter the email linked to the website: ")

        # Load encrypted data from JSON file
        try:
            with open('passwords.json', 'r') as file:
                encrypted_data = file.read()
                decrypted_data = decrypt_data(encrypted_data, encryption_key)
                data = json.loads(decrypted_data)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        existing_password = check_existing_accounts(website, email, data)
        if existing_password:
            print("\n### Your info ###")
            print(f"  Website: {website}")
            print(f"  Email: {email}")
            print(f"  Password: {existing_password}")
            print("### END OF PROGRAM ###\n")

    if action == "2":
        num_passwords = int(input("How many passwords do you want to generate? "))

        passwords = []
        for _ in range(num_passwords):
            website = input("Enter the name of the website: ")

            # Load encrypted data from JSON file
            try:
                with open('passwords.json', 'r') as file:
                    encrypted_data = file.read()
                    decrypted_data = decrypt_data(encrypted_data, encryption_key)
                    data = json.loads(decrypted_data)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            email = input("Enter the email linked to the website: ")

            existing_password = check_existing_accounts(website, email, data)
            if existing_password:
                print("You already have an account for this website:")
                print(f"Email: {email}")
                print(f"Password: {existing_password}")
                continue

            password = generate_password(25)

            password_data = {
                website: {
                    "email": email,
                    "password": password
                }
            }

            passwords.append(password_data)

            save_passwords(passwords, encryption_key)

            print("Passwords saved successfully.")


if __name__ == '__main__':
    main()
