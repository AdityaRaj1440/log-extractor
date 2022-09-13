from tkinter import *
from tkinter import scrolledtext as st
import time
import os
import psutil
import re

res="Hi"
location=""
isoDatUpper=""
isoDatLower= ""

def getDetails():
    res=""
    ts= time.time()
    isoDatLower= e1.get()
    isoDatUpper= e2.get()
    location= e3.get()

    pattern = re.compile(r'\d{4}[-]\d{2}[-]\d{2}[T]\d{2}[:]\d{2}[:]\d{2}[Z]')
    mo= pattern.findall(isoDatLower)
    mo1= pattern.findall(isoDatUpper)
    if len(mo)==0 or len(mo1)==0:
        res= "Invalid Data and Time Format"
        print(res)
        text_area.delete('1.0',END)
        text_area.insert(INSERT,res)
    else:
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

        if isoDatLower<=isoDatUpper:
            #file scanning process
            while (not done) and (fileNumber<=18203):
                # logList= []                                                     #fetches logs from the current file
                #go to next file
                fileNumber+=1
                if(fileNumber>18203):
                    continue
                done= checkFirstTime(start,isoDatUpper)
                if(not done):
                    done= checkLastTime(end,isoDatLower)
                    if(not done):
                        currentFile= getFileName(fileName,fileNumber,fileExtension)     #current file name
                        if(checkLastTime(currentFile,isoDatLower)):
                            continue
                        try:
                            logFile= open(currentFile,"r")
                            logLine= logFile.readline()
                            while logLine:
                                try:
                                    # logList.append(logLine)
                                    if(logLine.split(",")[0]>isoDatUpper):
                                        done= True
                                    if logLine.split(",")[0]>=isoDatLower and logLine.split(",")[0]<=isoDatUpper:
                                        filteredLog.append(logLine)
                                except ValueError:
                                    print("Error in line :"+logLine)
                                logLine= logFile.readline()
                        except FileNotFoundError:
                            print("hello")
        if len(filteredLog)==0:
            res= "No log for the specified time range found"
        else:
            res= filteredLog
            te= time.time()         #ending time
            res.append("Logs fetched in "+str(te-ts)+" seconds")
            # memory= 'RAM memory % used:'+str(psutil.virtual_memory()[2])
            # CPU= 'The CPU usage is: '+ str(psutil.cpu_percent(4))
            # res.append(memory)
            # res.append(CPU)
            res= "\n".join(res)
        # print(res)
        text_area.delete('1.0',END)
        text_area.insert(INSERT,res)
        # top.destroy()



# le.sys.argv.append(["-f", "2015-10-18T18:10:47Z","-t", "2015-10-18T23:10:51Z", "-i" ,"D:\\project\\Achieve.ai\\[DSATM]ADITYA_RAJ-SDE_SUBMISSION\\data\\"])
top = Tk()
# Code to add widgets will go here...
top.title("Log Extractor GUI")
inputFrame= Frame(top)
inputFrame.pack(side= "top")
Label(inputFrame, text='From Time').grid(row=0)
Label(inputFrame, text='To Time').grid(row=1)
Label(inputFrame, text='Log Directory Location').grid(row=2)
e1 = Entry(inputFrame)
e2 = Entry(inputFrame)
e3= Entry(inputFrame)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
executeFrame= Frame(top)
executeFrame.pack(side= "top")
w=Button(executeFrame, text="Fetch Logs", width= 25, command= getDetails)
w.pack()
outputFrame= Frame(top)
outputFrame.pack(side="top")
text_area = st.ScrolledText(outputFrame,
                            width = 140, 
                            height = 35, 
                            font = ("Times New Roman",
                                    10))
  
text_area.grid(column = 0, pady = 10, padx = 10)
  
# Inserting Text which is read only
# text_area.insert(INSERT,res)
  
# Making the text read only
# text_area.configure(state ='disabled')
top.mainloop()
