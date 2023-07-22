import tkinter
import tkinter.messagebox
import customtkinter
import tkinter.simpledialog
import tkinter.ttk as ttk
from io import BytesIO

import os
from dotenv import load_dotenv
import json
import random
import string
import qrcode
from cryptography.fernet import Fernet

ENCRYPTION_KEY = b'oYQVYml9qVlF_zxtwgq2i5LsWczAeRLoDaajDFCl1sU='

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_widget_scaling(2)  # widget dimensions and text size
customtkinter.set_window_scaling(2)  # window geometry dimensions

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        # configure window
        self.title("myPasswords")
        self.geometry(f"{600}x{580}")

        # create a main frame for the main screen
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="myPasswords", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # create website name input field
        self.website_name_label = customtkinter.CTkLabel(self.main_frame, text="Website Name or Username:")
        self.website_name_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.website_name_entry = customtkinter.CTkEntry(self.main_frame)
        self.website_name_entry.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # create email input field
        self.email = customtkinter.CTkLabel(self.main_frame, text="Website Name or Username:")
        self.email.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.email_entry = customtkinter.CTkEntry(self.main_frame)
        self.email_entry.grid(row=1, column=0, padx=20, pady=(0, 20))

        # # create password length dropdown menu
        # self.password_length_label = customtkinter.CTkLabel(self.main_frame, text="Password Length:")
        # self.password_length_label.grid(row=2, column=0, padx=20, pady=(20, 10))
        # self.password_length_var = tkinter.StringVar(value="8")
        # # Update the line below to pass the options as positional arguments
        # self.password_length_dropdown = customtkinter.CTkOptionMenu(self.main_frame, self.password_length_var, "8", "10", "12", "14", "16", "18", "20")
        # self.password_length_dropdown.grid(row=3, column=0, padx=20, pady=(0, 20))

        def optionmenu_callback(choice):
            print("optionmenu dropdown clicked :", choice)

        optionmenu = customtkinter.CTkOptionMenu(App, values=["option 1", "option 2"],
                                                command=optionmenu_callback)
        optionmenu.set("option 2")


        # create generate password button
        self.generate_password_button = customtkinter.CTkButton(self.main_frame, text="Generate Password", command=self.generate_password)
        self.generate_password_button.grid(row=4, column=0, padx=20, pady=(20, 10))

        # create password display field
        self.password_label = customtkinter.CTkLabel(self.main_frame, text="Password:")
        self.password_label.grid(row=5, column=0, padx=20, pady=(20, 10))
        self.password_entry = customtkinter.CTkEntry(self.main_frame, show="●")
        self.password_entry.grid(row=6, column=0, padx=20, pady=(0, 20))

        # create copy password button
        self.copy_password_button = customtkinter.CTkButton(self.main_frame, text="Copy Password", command=self.copy_password)
        self.copy_password_button.grid(row=7, column=0, padx=20, pady=(20, 10))

        # create save password button
        self.save_password_button = customtkinter.CTkButton(self.main_frame, text="Save Password", command=self.save_password)
        self.save_password_button.grid(row=8, column=0, padx=20, pady=(20, 10))

        # create load passwords button
        self.load_passwords_button = customtkinter.CTkButton(self.main_frame, text="Load Passwords", command=self.load_passwords)
        self.load_passwords_button.grid(row=9, column=0, padx=20, pady=(20, 10))

        # create generate QR code button
        self.generate_qr_code_button = customtkinter.CTkButton(self.main_frame, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_qr_code_button.grid(row=10, column=0, padx=20, pady=(20, 10))




    def generate_password(self):
        # generate a random password
        password = "".join(random.choices(string.ascii_letters + string.digits, k=int(self.password_length_var.get())))
        self.password_entry.delete(0, tkinter.END)
        self.password_entry.insert(0, password)

    def copy_password(self):
        # copy the generated password to the clipboard
        password = self.password_entry.get()
        self.clipboard_clear()
        self.clipboard_append(password)

    def save_password(self):
        # save the website name, username, and password to a JSON file
        website_name = self.website_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        data = {
            "website_name": website_name,
            "email": email,
            "password": password
        }
        with open("passwordsNOCRYPT.json", "a") as f:
            f.write(json.dumps(data) + "\n")

    def load_passwords(self):
        # load the saved passwords from the JSON file
        passwords = []
        try:
            with open("passwordsNOCRYPT.json", "r") as f:
                for line in f:
                    passwords.append(json.loads(line))
        except FileNotFoundError:
            pass
        self.password_listbox.delete(0, tkinter.END)
        for password in passwords:
            self.password_listbox.insert(tkinter.END, f"{password['website_name']} - {password['username']} - {password['password']}")

    def generate_qr_code(self):
        # generate a QR code for the generated password
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        password = self.password_entry.get()
        qr.add_data(password)
        qr.make(fit=True)

        # create a PIL image from the QR code data
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image_bytes = BytesIO()
        qr_image.save(qr_image_bytes, format='png')
        qr_image_bytes.seek(0)

        # display the QR code image in a separate window
        qr_window = tkinter.Toplevel(self)
        qr_window.title("QR Code")
        qr_image_label = tkinter.Label(qr_window, image=tkinter.PhotoImage(data=qr_image_bytes.getvalue()))
        qr_image_label.pack()

    def __del__(self):
        # save the passwords to the JSON file when the program is closed
        passwords = []
        for i in range(self.password_listbox.size()):
            password = self.password_listbox.get(i)
            website_name, username, password = password.split(" - ")
            passwords.append({
                "website_name": website_name,
                "username": username,
                "password": password
            })
        with open("passwordsNOCRYPT.json", "w") as f:
            f.write(json.dumps(passwords))



# The script's main logic remains unchanged
def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()