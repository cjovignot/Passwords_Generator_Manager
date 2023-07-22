from cx_Freeze import setup, Executable

setup(
    name="myPasswords",
    version="1.0",
    description="Generation & Management",
    executables=[Executable("myPasswords.py")]
)
