#LogHawk3.2
import re
import datetime
from collections import Counter
print (" <<<<< Welcome to LogHawk v3.1 >>>>>")

#region User Customized Input/Output (optional)
### Allow User to input their own log file paths by activating lines below (must comment out default log file paths):

#httpLogFilePath = input("What is the file path for the web server log you would like to check? (ex:/var/log/apache2.log)\n")
#sshLogFilePath = input("What is the file path for the SSH log you would like to check? (ex:/var/log/auth.log)\n")
#errorLogFilePath = input("What is the file path for the error log you would like to check? (ex:/var/log/kern.log)\n")
#cronLogFilePath = input("What is the file path for the Cron log you would like to check? (ex:/var/log/cron)\n")

#outputPath = input("please enter the preferred file output path (ex: C:/Users/User/Documents/LogHawkLogs)\n")

#endregion

#region Default Input/Output (optional)
### Configure default log file paths and output folders (must be commented out if using User Customized version)
httpLogFilePath = "/var/log/apache2.log"
sshLogFilePath = "/var/log/auth.log"
errorLogFilePath = "/var/log/kern.log"
cronLogFilePath = "/var/log/cron.log"

outputPath = "user/Documents/LogHawkLogs" #folder location must exist

#endregion

#region Script Options - Allows for script customization
fileDetail = input("would you like to included detailed results? (y|n)\n")
printToTerminal = input("would you like to print the results to this terminal? (y|n)\n")
#endregion

#region Variables
##HTTP Variables (add or change as needed)
count404 = 0
count401 = 0
count200 = 0
ipAddresses = []
##SSH Variables (add or change as needed)
countsudo = 0
countfailure = 0
count3fails = 0
##SSH Variables (add or change as needed)
countErr = 0
countCrit =0
##SSH Variables (add or change as needed)

#endregion

#region Data Retrieval
httpFile = open(httpLogFilePath, "r")
httpLines = httpFile.readlines()
httpFile.close()

sshFile = open(sshLogFilePath, "r")
sshLines = sshFile.readlines()
sshFile.close

errFile = open(errorLogFilePath, "r")
errLines = errFile.readlines()
errFile.close

cronFile = open(cronLogFilePath, "r")
cronLines = cronFile.readlines()
cronFile.close

#endregion

#region File Output Creation
from datetime import datetime
fileName = outputPath + "\\" + "LogHawk3.2_" + datetime.now().strftime("%Y-%m-%d_%H-%M") + ".txt"

#endregion

#region Run HTTP Code Checks
##count code instances (add or change as needed)
for line in httpLines:
    if " 404 " in line:
        count404 +=1
    if " 401 " in line:
        count401 +=1
    if " 200 " in line:
        count200 +=1

##count IP address occurances

for line in httpLines:
    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',line)
    if match:
        ip = match.group()
        ipAddresses.append(ip)
ipCounts = Counter(ipAddresses)
ipSort = sorted(ipCounts, key=ipCounts.get, reverse=True)
#endregion

#region Run SSH Count Checks

##count instances (add or change as needed)
for line in sshLines:
    if "failure" in line:
        countfailure +=1
    if "3 incorrect password attempts" in line:
        count3fails +=1
    
#endregion

#region Run Critical/Error Check
##count errors and crits(add or change as needed)
for line in errLines:
    if "*ERROR*" in line:
        countErr +=1
    if "*CRITICAL*" in line:
        countCrit +=1
 
#endregion

#region Run Suspicious Script Activity Check


#endregion

#region Output
##write file log
with open(fileName, "a") as file:
    file.write(f"<<<<< LogHawk v3.2 >>>>>\n")
    file.write(f"\n")
    file.write(f"   Results Summary   \n")
    file.write(f"\n")
    #HTTP Summary
    file.write(f" < HTTP Code and IP Address Summary > \n")
    file.write(f"\n")
    file.write(f"HTTP Code Occurences:\n")
    file.write(f"Code 404: {count404}\n")
    file.write(f"Code 401: {count401}\n")
    file.write(f"Code 200: {count200}\n")
    file.write(f"\n")
    file.write(f"Unique IP Address Occurences:\n") #sorted most frequent to least frequent
    for ip in ipSort:
        file.write(f"{ip}: {ipCounts[ip]}\n")
    file.write(f"\n")
    #SSH Summary
    file.write(f" < SSH Login Attempt Failure Summary > \n")
    file.write(f"\n")
    file.write(f"Authentication Failure occurences: {countfailure}\n")
    file.write(f"3 incorrect password attempts occurences: {count3fails}\n")   
    file.write(f"\n")
    #Error/Critical Summary
    file.write(f" < Kernel Errors and Criticals Summary > \n")
    file.write(f"\n")
    file.write(f"Error Codes: {countErr}\n")
    file.write(f"Critical Codes: {countCrit}\n") 
    file.write(f"\n")
    #detailed results (optional)
    if fileDetail == "y":
        file.write(f"\n\n")
        file.write(f"<<< Detailed Results >>>\n")
        file.write(f"\n")
        file.write(f"Authentification Failures:\n")
        for line in sshLines:
            if "failure" in line:
                file.write(f"{line}")
        file.write(f"\n")        
        file.write(f"3 Failed Logins Attempted:\n")
        for line in sshLines:
            if "3 incorrect password attempts" in line:
                file.write(f"{line}")
        file.write(f"\n")
        file.write(f"Kernal Error Alerts:\n")
        for line in errLines:
            if "*ERROR*" in line:
                file.write(f"{line}")
        file.write(f"\n")
        file.write(f"Kernal Critical Alerts:\n")
        for line in errLines:
            if "*CRITICAL*" in line:
                file.write(f"{line}")
        file.write(f"\n")
##close file
file.close()
##print output         
print("Output File: " + fileName + "\n")
if printToTerminal == "y":
    fileRead = open(fileName, "r")
    print(fileRead.read())

#endregion
