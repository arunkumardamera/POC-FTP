 from ftp_lib import FTPsession
import shutil
import threading
import time
import os
import subprocess

class ftpTask (threading.Thread):
    def __init__(self, threadID, name, host, username,password):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name # county name
        self.host = host
        self.username=username
        self.password = password

    def run(self):
        print ("Starting tasks for " + self.name )
        time.sleep(3)
        ftp1 = FTPsession(self.host, self.username , self.password)
        latest_file = ftp1.get_latest_file_name()
        # Not needed for the first time
        rmtar = 'rm -rf /opt/' + self.name + '/*'
        if os.path.exists('/opt/' + self.name):
            result = subprocess.check_output(rmtar, shell=True)
            print(result)
        if(ftp1.download_latest_file()):
            fpath = '/opt/' + latest_file
            os.chdir('/opt/')
            if not os.path.exists(self.name):
                os.makedirs(self.name)
            dpath= '/opt/' + self.name
            shutil.move(fpath,dpath)
            untarcmd = 'tar -xvf ' + dpath + '/*.tar* -C /opt/' + self.name + '/'
            result = subprocess.check_output(untarcmd, shell=True)
            print(result)
            ftp1.create_dir_in_ftp_server()
            ft = None
            for files in  os.walk(dpath):
                ft = files
            print(ft)
            if ft:
                for item in  ft[2]:
                    item_path =  dpath + '/' + item
                    print(item_path)
                    ftp1.upload_files_cwd(item,item_path)
        else:
            #Send out the mail we should return an error
            print("File Download Fails..")
    
def main():
    
    threads = []
    timeoutval = 300

    #In production code the values will be taken out from db
    #DB coulmns will be county (ca_amador will be unique), type (ftp/email/web), host, username, password
    #Seperate script will be provided to update db params
    #Below line create a new thread for ca_amador ftp
    t_id = ftpTask(1,"ca_amador",'ftp.pfainc.com','CoreLogic',"#C0r3106!c@m@d0r!")

    time.sleep(1)
    #in production code these two will be done inside a loop
    if t_id:
        print('Starting...')
        t_id.start()
        time.sleep(1)
        threads.append(t_id)
        
    for t in threads:
        t.join(timeout=timeoutval)

if __name__ == "__main__":
    main()