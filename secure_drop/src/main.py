from transferdata import TransferData
import sys
sys.path.append("/pycrypto/lib")
from functions import *
import dropbox


def main():
    # THIS IS OUR ACCESS TOKEN FOR DROPBOX API
    access_token = ''  
    # BY USING OUR TOKEN, WE CREATE TRANSFERDATA OBJECT TO BE ABLE TO UPLOAD AND DOWNLOAD BY USING DROPBOX API
    transferData = TransferData(access_token)
    # WE CREATE THE FILE WHICH WILL STORE OUR KEY
    create_key_file()
    # WE CHECK IF WE ALREADY HAVE KEY
    key_found = check_key()
    # IF WE DON'T HAVE KEY, WE ASK THE USER CREATE ONE BY USING PASSWORD MANUALLY OR AUTOMATICALLY
    if key_found == False:
        while 1:
            auto_generated = ask_to_create_key()
            if auto_generated =="1":
                auto_generate_key()
                break
            elif auto_generated =="2":
                create_key()
                break
            else:
                print "ERROR: Invalid choice."


    # WE AUTHENTICATE USER BY ASKING THE PASSWORD
    correct_key = ask_key()
    if correct_key:
        pair  = read_key()
        key = pair[1]
        while 1:
            # HERE IS THE MAIN MENU 
            #1 FOR ENCRYPTING AND PLOADING TO DROPBOX, 
            #2 FOR DOWNLOADING FROM DROPBOX AND DECRYPTING, 
            #3 FOR EXITING
            option = ask_options()

            if option == "1":
                # THIS IS THE NAME OF THE FILE THAT WILL BE ENCRYPTED AND UPLOADED TO DROPBOX
                filename = raw_input("Enter the filename:")
                try:
                    # WE CALL ENCRYPT_FILE FUNCTION WITH PARAMETERS FILENAME, AND KEY
                    # IT RETURNS EITHER 0 FOR BAD FILE SUCH AS DOES NOT EXIST OT EMPTY OR THE ENCRYPTED CONTENT
                    content = encrypt_file(filename, key)
                    if content ==0:
                        print "file is empty or does not exist.\n"
                    else:
                        # WE SAVE ENCRYPTED CONTENT AS LOCAL COPY AND WE UPLOAD ENCRYPTED CONTENT TO DROPBOX                        
                        extension = filename[-4:]
                        encrypted_name = filename[:len(filename)-4] + "_encrypted_drop" + extension
                        res = transferData.upload_file(content, '/' + encrypted_name)
                        print "ENCRYPTED file is saved as " + encrypted_name +" in the root folder of DROPBOX.\n"
                except dropbox.exceptions.ApiError as err:
                    print('*** API error', err)


            elif option =="2":
                # THIS IS THE NAME OF THE FILE THAT WILL BE DOWNLOADED AND CHECKED FOR INTEGRITY AND DECRYPTED
                filename = raw_input("Enter the filename:")
                flag = 0
                try:
                    
                    transferData.download_file(filename)
                except dropbox.exceptions.ApiError as err:
                    print('*** API error', err)
                    flag = 1
                # IF THERE IS NO ANY API RELATED ERROR SUCH AS FILE DOES NOT EXIST IN THE DROPBOX, WE CALL DECRYPT_FILE FUNCTION
                if flag == 0:
                    decrypt_file(filename, key)



            elif option =="3":
                sys.exit("Bye, bye!")
    else:
        sys.exit("Wrong password, bye!")

if __name__ == '__main__':
    main()

#    pyinstaller --onedir --name SecureDrop -p /Users/emredurmus/Documents/crypto_project2/src main.py
