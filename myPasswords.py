import os
from dotenv import load_dotenv
import json
import random
import string
import qrcode
import pyperclip
from cryptography.fernet import Fernet


def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def check_existing_accounts(website, email, data):
    for entry in data:
        if website in entry and entry[website]['email'] == email:
            return entry
    return None


def save_passwords(data, encryption_key):
    # Encrypt the data
    encrypted_data = encrypt_data(json.dumps(data), encryption_key)

    # Save encrypted data to JSON file
    with open('passwords.json', 'w') as file:
        file.write(encrypted_data)

def edit_password(data, encryption_key):
    #Encrypt the data
    encrypted_data = encrypt_data(json.dumps(data), encryption_key)


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


    
    # # DISPLAYING JSON AT LAUNCH
    # # Load encrypted data from JSON file
    # try:
    #     with open('passwords.json', 'r') as file:
    #         encrypted_data = file.read()
    #         decrypted_data = decrypt_data(encrypted_data, encryption_key)
    #         data = json.loads(decrypted_data)
    #         print(json.dumps(data, indent=2))  # Print decrypted data with indentation
    #         # for dictionary in data:
    #         #     json_data = json.dumps(dictionary, indent=4)
    #         #     print(json_data, ",")
    #             # print()
    # except (FileNotFoundError, json.JSONDecodeError):
    #     data = []





    action = input("What do you want to do?\n 1. Get a password\n 2. Generate passwords\n 3. Edit a password\n 4. Delete a password\nAnswer: ")

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

        existing_account = check_existing_accounts(website, email, data)
        if existing_account:
            print("\n### Your info ###")
            # print(f"Website: {website}")
            # print(f"Email: {email}")
            # print(f"Password: {existing_account[website]['password']}")

            # Generate QR code
            qr_code = qrcode.QRCode()
            qr_code.add_data(existing_account[website]['password'])
            qr_code.make()

            # Display QR code in the terminal
            qr_code.print_ascii()

            pyperclip.copy(existing_account[website]['password'])

            print("### END OF PROGRAM ###\n")
        else:
            print("No account found with the given data.\nExiting...")


    elif action == "2":
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
                    # print(data)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []

            email = input("Enter the email linked to the website: ")

            existing_password = check_existing_accounts(website, email, data)
            if existing_password:
                print("You already have an account for this website:")
                print(f"Email: {email}")
                # Generate QR code
                qr_code = qrcode.QRCode()
                qr_code.add_data(existing_account[website]['password'])
                qr_code.make()

                # Display QR code in the terminal
                qr_code.print_ascii()

                pyperclip.copy(existing_account[website]['password'])
                continue

            action = input("What do you want to do?\n 1. Generate a random password\n 2. Customized password\nAnswer: ")

            if action == "1":
                password = generate_password(25)

                password_data = {
                    website: {
                        "email": email,
                        "password": password
                    }
                }

                data.append(password_data)
                passwords = data

                save_passwords(passwords, encryption_key)
                
                # Generate QR code
                qr_code = qrcode.QRCode()
                qr_code.add_data(password_data[website]['password'])
                qr_code.make()

                # Display QR code in the terminal
                qr_code.print_ascii()

                pyperclip.copy(password_data[website]['password'])

                print("Passwords successfully generated.")

            if action == "2":
                password = input("Enter the password: ")

                password_data = {
                    website: {
                        "email": email,
                        "password": password
                    }
                }

                data.append(password_data)
                passwords = data
                save_passwords(passwords, encryption_key)

                # Generate QR code
                qr_code = qrcode.QRCode()
                qr_code.add_data(password_data[website]['password'])
                qr_code.make()

                # Display QR code in the terminal
                qr_code.print_ascii()

                pyperclip.copy(password_data[website]['password'])

                print("Password successfully created.")


    elif action == "3":
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

        existing_account = check_existing_accounts(website, email, data)
        if existing_account:
            data.remove(existing_account)
            action = input("What do you want to do?\n 1. Generate a new password\n 2. Edit the password\nAnswer: ")

            if action == "1": 
                new_password = generate_password(25)
                existing_account[website]['password'] = new_password

                password_data = {
                    website: {
                        "email": email,
                        "password": new_password
                    }
                }

                data.append(password_data)
                save_passwords(data, encryption_key)

                # Generate QR code
                qr_code = qrcode.QRCode()
                qr_code.add_data(password_data[website]['password'])
                qr_code.make()

                # Display QR code in the terminal
                qr_code.print_ascii()

                pyperclip.copy(password_data[website]['password'])

                print("Password successfully generated.")

            elif action == "2":
                new_password = input("Enter the new password: ")
                existing_account[website]['password'] = new_password

                password_data = {
                    website: {
                        "email": email,
                        "password": new_password
                    }
                }

                data.append(password_data)
                save_passwords(data, encryption_key)
                
                # Generate QR code
                qr_code = qrcode.QRCode()
                qr_code.add_data(password_data[website]['password'])
                qr_code.make()

                # Display QR code in the terminal
                qr_code.print_ascii()

                pyperclip.copy(password_data[website]['password'])

                print("Password successfully edited.")
        else:
            print("No account found with the given data.\nExiting...")
        
    elif action == "4":
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

        existing_account = check_existing_accounts(website, email, data)
        if existing_account:
            data.remove(existing_account)
            save_passwords(data, encryption_key)

            print("Password successfully deleted.")
        else:
            print("No account found with the given data.\nExiting...")


if __name__ == '__main__':
    main()
