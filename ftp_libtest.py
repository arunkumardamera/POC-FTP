 from ftplib import FTP
import time
from dateutil import parser

class FTPsession():
    def __init__(self,
                 hostname="",
                 username="",
                 password=""):
        print("Ftp Login Started...")
        self.ftp=None
        try:
            self.ftp= FTP(hostname)
            self.ftp.login(username,password) 
        except:
            print("Ftp Login Failed")
            
    def get_latest_file_name(self):
        data = []
        if self.ftp:
            #self.ftp.dir('-t',data.append)
            self.ftp.dir("",data.append)
            latest_time = None
            latest_name = None
            
            for line in data:
                tokens = line.split()
                time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
                # date utils are used here to parse the time string
                time = parser.parse(time_str)
                if (latest_time is None) or (time > latest_time):
                    latest_name = tokens[8]
                    latest_time = time
            self.latest_file=latest_name
            return latest_name
    def download_latest_file(self):
        fpath = '/opt/' + self.latest_file
        handle = open(fpath, 'wb')
        try:
            self.ftp.retrbinary('RETR %s' % self.latest_file, handle.write)
        except:
            print("Ftp download Failed")
            handle.close()
            return False
        return True
    
    def is_dir_exist(self,dir = ''):
        filelist = []
        self.ftp.retrlines('LIST',filelist.append)
        for f in filelist:
            if f.split()[-1] == dir and f.upper().startswith('D'):
                return True
    
    def create_dir_in_ftp_server(self, dir='upload_folder'):
        if not self.is_dir_exist (dir):
            self.ftp.mkd('upload_folder')
        self.ftp.cwd(dir)

    def upload_files_cwd(self, file_name, file_path):
        self.ftp.storbinary('STOR ' + file_name, open(file_path,'rb') )
        
    
        
        
            
if  __name__=='__main__':
    ftp1= FTPsession('ftp.pfainc.com','CoreLogic',"#C0r3106!c@m@d0r!")
    print(ftp1.get_latest_file_name())