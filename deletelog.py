import os
import configparser
import datetime
import time
#today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

def deleteLogger():
    deledate = datetime.date.today() - datetime.timedelta(days=7)
    deledate = deledate.strftime("%Y-%m-%d")
    for i in os.listdir("./"):
        if os.path.splitext(i)[1] == '.log':
            filename = os.path.splitext(i)[0]
            if filename < deledate:
                os.remove("./{}.log".format(filename))
                
if __name__ == "__main__":
    deleteLogger()