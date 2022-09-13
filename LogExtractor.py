import os
import sys
import time
import re
import psutil
  
count=0;
ts= time.time()         #starting time

#accessing arguments from command line
if len(sys.argv) > 7:
    print("You have too many arguments")
    sys.exit()

if len(sys.argv) < 7:
    print("You need to specify the path to be listed")
    sys.exit()

# initializing variable from command line arguments
location= sys.argv[6]
isoDatLower= sys.argv[2]
isoDatUpper= sys.argv[4]

# Regular expression for validating ISO 8601
pattern = re.compile(r'\d{4}[-]\d{2}[-]\d{2}[T]\d{2}[:]\d{2}[:]\d{2}[Z]')
mo= pattern.findall(isoDatLower)
mo1= pattern.findall(isoDatUpper)
if len(mo)==0 or len(mo1)==0:
    print("Invalid Data and Time Format")
    sys.exit()
#Range of date for acessing logs
# isoDatLower= "2015-10-18T18:10:47Z"
# isoDatUpper= "2015-10-18T23:10:51Z"
# location= "D:\\project\\Achieve.ai\\[DSATM]ADITYA_RAJ-SDE_SUBMISSION\\data\\"

#log file name in 3 parts
fileName= "LogFile-"
fileNumber= 0
fileExtension= ".log"

#the files will be scanned till this variable is not true
done= False

#to store the filtered logs
filteredLog= []

# First and last file
start= location+ str("LogFile-000001.log")
end=   location+ str("LogFile-0018203.log")

#to create the name of the log file to be accessed
def getFileName(filename,filenumber,fileextension):
    if filenumber<=9999:
        filenumber= str(filenumber)
        while len(filenumber)!=6:
            filenumber= "0"+filenumber
    else:
        filenumber= str(filenumber)
        while len(filenumber)!=7:
            filenumber= "0"+filenumber
    return location+filename+filenumber+fileextension

#to check if the lower date and time is lesser than the highest date and time of the file or not
def checkLastTime(filename,lowerDate):
    try:
        with open(filename, "rb") as file:
            try:
                file.seek(-2, os.SEEK_END)
                while file.read(1) != b'\n':
                    file.seek(-2, os.SEEK_CUR)
                    count+=1
            except OSError:
                file.seek(0)
            last_line = file.readline().decode()
            lastTime= last_line.split(",")[0]
            if(lowerDate>lastTime):
                return True
            else:
                return False
    except:
        print("LogFile-0018023 does not exist")

#to check if the upper date and time is greater than the lowest date and time of the file or not
def checkFirstTime(filename,upperDate):
    f= open(filename,"r")
    firstLine= f.readline()
    firstTime= firstLine.split(",")[0]
    if(upperDate<firstTime):
        return True
    else:
        return False

# if range of date is valid
if isoDatLower<=isoDatUpper:
    #file scanning process
    while (not done) and (fileNumber<=18203):
        #go to next file
        fileNumber+=1
        if(fileNumber>18203):
            continue
        # edge cases
        done= checkFirstTime(start,isoDatUpper)
        if(not done):
            done= checkLastTime(end,isoDatLower)
            if(not done):
                currentFile= getFileName(fileName,fileNumber,fileExtension)     #current file name
                # if the range does not exist in the current log file
                if(checkLastTime(currentFile,isoDatLower)):
                    continue
                try:
                    logFile= open(currentFile,"r")
                    logLine= logFile.readline()
                    while logLine:
                        try:
                            # if the upper date is lesser than the current file's oldes log, then end the scanning
                            if(logLine.split(",")[0]>isoDatUpper):
                                done= True
                            # if the file contains logs within the given range, store the log
                            if logLine.split(",")[0]>=isoDatLower and logLine.split(",")[0]<=isoDatUpper:
                                filteredLog.append(logLine)
                        except ValueError:
                            print("Error in line :"+logLine)
                        logLine= logFile.readline()
                except FileNotFoundError:
                    print("hello")
if len(filteredLog)==0:
    print("No log for the specified time range found")
else:
    for log in filteredLog:
        print(log)
    te= time.time()         #ending time
    print("Logs fetched in "+str(te-ts)+" seconds")
    # print('RAM memory % used:'+str(psutil.virtual_memory()[2]))
    # print('The CPU usage is: '+ str(psutil.cpu_percent(4)))
    print("Count="+str(len(filteredLog)))