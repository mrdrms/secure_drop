import dropbox
import sys
import os


frozen = 'not'
if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        print bundle_dir
else:
        # WE ARE RUNNING IN A NORMAL PYTHON ENVIRONMENT
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token


    def upload_file(self, encrypted_text, file_to=None):
        """upload a file to Dropbox using API v2
        """
        # WE CREATE A DROPBOX INSTANCE WITH OUR TOKEN, AND WE SET THE MODE AS OVERWRITE WHICH MEANS
        # IF WE TRY TO UPLOAD A FILE WITH A NAME THAT IS ALREADY IN DROPBOX, THE FILE IN DROPBOX WILL BE OVERWRITTEN
        # AFTER SETTING THE MODE, WE UPLOAD THE ENCRYPTED FILE TO DROPBOX
        dbx = dropbox.Dropbox(self.access_token)
        mode = dropbox.files.WriteMode.overwrite 
        res = dbx.files_upload(encrypted_text, file_to,mode)
        return res



    def download_file(self,filename):
        """download a file from Dropbox using API v2
        """
        # WE DOWNLOAD A FILE FROM DROPBOX AND WRITE IT TO A LOCAL FILE
        LOCAL_FILE= os.path.abspath(os.path.join(bundle_dir, filename))
        flag=0
        content = ""
        try:
            dbx = dropbox.Dropbox(self.access_token)
            metadata, res = dbx.files_download(path="/" + filename)  
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            flag =1

        if flag == 0:
            with open(LOCAL_FILE, "wb") as f:
                dbx = dropbox.Dropbox(self.access_token)
                content = res.content                          
                f.write(content)

                
            

