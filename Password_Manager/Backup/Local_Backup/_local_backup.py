from Password_Manager.Essentials.utilities import is_windows, create_dir
from pathlib import Path
import shutil
import glob
import json
import os

if is_windows():
    defaultBackupPath = Path("C:/ProgramData/iThACK-PassMag")
    defaultBackedUp_key_location = defaultBackupPath / "00003.1.KEY.bin"
    defaultBackedUp_salt_location = defaultBackupPath / "00003.1.SALT.bin"
    defaultBackedUp_database_location = defaultBackupPath / "user.db"
else:
    defaultBackupPath = Path("/var/lib/iThACK-PassMag")
    defaultBackedUp_key_location = defaultBackupPath / "00003.1.KEY.bin"
    defaultBackedUp_salt_location = defaultBackupPath / "00003.1.SALT.bin"
    defaultBackedUp_database_location = defaultBackupPath / "user.db"

def backup_Database_And_Config(backupPath=defaultBackupPath):
    try:
        # create path, if it doesn't exist'
        location = Path(backupPath)
        create_dir(location)

        # copy *level files to backup location
        shutil.copy("Password_Manager/User/leveldb/user.db", location)
        files_to_backup = glob.glob("Password_Manager/User/masterlevel/*.bin")
        for filename in files_to_backup:
            shutil.copy(filename, location)
    
    except Exception as e:
        print(e)
        print("\nāāā ErRoR OcCuRrEd š Unable To Backup Passwords And Configurations āāā")



def restore(backedUp_key=defaultBackedUp_key_location, backedUp_salt=defaultBackedUp_salt_location, backedUp_database=defaultBackedUp_database_location):
    try:
        '''
        This function will restore previously backed up master password files and password database.
        '''

        restoreMasterlevelLocation = Path("Password_Manager/User/masterlevel")
        restoreMasterlevelLocation.mkdir(parents=True, exist_ok=True)

        restoreLeveldbLocation = Path("Password_Manager/User/leveldb")
        restoreLeveldbLocation.mkdir(parents=True, exist_ok=True)

        if os.path.exists(backedUp_key and backedUp_salt and backedUp_database):
            shutil.copy(backedUp_key,restoreMasterlevelLocation)
            shutil.copy(backedUp_salt,restoreMasterlevelLocation)
            shutil.copy(backedUp_database,restoreLeveldbLocation)
            print("\nš¤ Successfully Restored To The Previous Stage š¬")
        else:
            print("\nā Backup Configuration Not Found š\n")
    except Exception as e:
        print("\nāāā ErRoR OcCuRrEd š Can't Restore Backed Up State āāā")
    

def deleteLocalBackup():
    try:
        print('\nāāā deleting backup āāā')

        backedUp_folder = defaultBackupPath
        if os.path.exists(backedUp_folder):
            shutil.rmtree(backedUp_folder)

        with open("Password_Manager/config.json", "r+") as config_file:
            backupConfig = json.load(config_file)
            backupConfig['Automatic Backup'] = False
            config_file.seek(0)
            json.dump(backupConfig, config_file)
            config_file.truncate()
        print("\n[-] records deleted")
    except Exception as e:
        print("\nāāā ErRoR OcCuRrEd š Unable Delete Local Backup Files āāā")