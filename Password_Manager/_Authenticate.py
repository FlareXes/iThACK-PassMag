import hashlib
import secrets
from getpass import getpass


def checkTrust():
    try:
        masterPasswordAttempt = 0
        while masterPasswordAttempt <= 2:
            masterPassword = getpass("\nVerify Yourself To Continue (Master Password)š : ")
            if verifyMasterPassword(masterPassword) == True:
                break
            else:
                print("\nā Nope, Try Again ā")
                masterPasswordAttempt += 1
        else:
            print("\n ššššššššš To Many Invalid Attempts!! Get Out š ššššššššš\n")
            quit()
        return masterPassword
    except Exception as e:
        print("\nāāā ErRoR OcCuRrEd š Can't Verify The Trust Level āāā")
        print("\n šššššššššššššššššš\n")
        exit()


def verifyMasterPassword(masterPassword):
    with open("Password_Manager/User/masterlevel/00003.1.SALT.bin", "rb") as saltFile:
        salt = saltFile.read()
    with open("Password_Manager/User/masterlevel/00003.1.KEY.bin", "rb") as keyFile:
        key = keyFile.read()

    new_key = hashlib.pbkdf2_hmac('sha256', masterPassword.encode('utf-8'), salt, 150000, dklen=128)
    trust = secrets.compare_digest(key, new_key)
    return trust