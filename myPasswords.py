import json
import random
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_existing_accounts(website, email, data):
    for entry in data:
        if website in entry and entry[website]['email'] == email:
            return entry[website]['password']
    return None

def save_passwords(passwords):
    # Load existing data from JSON file if it exists
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
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

    # Save data to JSON file
    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)

    # Save data to text file
    with open('passwords.txt', 'a') as file:
        for password in passwords:
            for website, details in password.items():
                file.write(f"{website} :\n")
                file.write(f"  email: {details['email']}\n")
                file.write(f"  password: {details['password']}\n\n")

def main():
    action = input("What do you want to do ?\n 1. Get a password\n 2. Create passwords\n\nAnswer : ")

    if action == "1":
        website = input("Enter the name of the website: ")
        email = input("Enter the email linked to the website: ")
        
        # Load existing data from JSON file if it exists
        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        existing_password = check_existing_accounts(website, email, data)
        if existing_password:
            print("\n### Your infos ###")
            print(f"  Website : {website}")
            print(f"  Email : {email}")
            print(f"  Password : {existing_password}")
            print("### END OF PROGRAM ###\n")

    if action == "2":
        num_passwords = int(input("How many passwords do you want to generate? "))

        passwords = []
        for _ in range(num_passwords):
            website = input("Enter the name of the website: ")

            # Load existing data from JSON file if it exists
            try:
                with open('passwords.json', 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
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

            save_passwords(passwords)

            print("Passwords saved successfully.")

if __name__ == '__main__':
    main()
