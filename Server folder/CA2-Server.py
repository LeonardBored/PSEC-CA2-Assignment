# StudentID:    P2006264
# Name:	        Soh Kai Meng Leonard
# Class:		DISM/FT/1B/05 
# Assessment:	CA2 
# 
# Script name:	CA2-Server.py
# 
# Purpose:	For processing of client's (user.py) inputs and writing to files 
#
#           The server will be constantly running and wil be awaiting for connections made by the client
#           when a connection is made, the client would sent over a request, asking for specific data. Server
#           wil then send that data over to client and close the connection
#
#           Once client is done with quiz, they will submit the attempt over to server for processing
#           After processing it, the server will write the user's attempt in quiz_results.csv
#
#
# Usage syntax:	Run with play button 
#
# Alternate usage syntax: 1. Type in terminal : cd '.\Server folder\'
#                         2. Type in terminal : py .\CA2-Server.py
# Input file:	
#  
# './Server folder/userid_pswd.txt'
# './Server folder/question_pool.txt'
# './Server folder/quiz_setting.txt'
# './Server folder/quiz_results.csv'
# 
# Output file:	
#
# './Server folder/userid_pswd.txt'
# './Server folder/question_pool.txt'
# './Server folder/quiz_setting.txt'
# './Server folder/quiz_results.csv'
# 
# Python ver:	Python 3
#
# Reference:
#       
#
#       (a) Working with csv files in Python 
#           https://www.geeksforgeeks.org/working-csv-files-python/ 
#           accessed on 19 Nov 2021
#
#       (b) Python CSV 
#           https://www.programiz.com/python-programming/csv 
#           accessed on 19 Nov 2021
#
#       (c) Python ast eval
#           https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary
#           accessed on 20 Jan 2022
#
#       (d) Python Socket Programming
#           https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python
#           accessed on 20 Jan 2022
#       
# Library/:	
# package/:	
# Module/:
# 
# socket module
# sys module
# traceback module
# thread module
# csv module
# ast Module
#
# Known issues:	eg. no validation of input value
# 
# None
#
# ****************************** User-defined functions ***************************
# Describe the purpose of user-defined functions, parameters and return values

# This function creates a list that stores dictionaries from the chosen csv file
# This function takes in a chosen csv file's path as its argument
# It returns a list containing dictionaries where each dictionary represents a row in the csv file
def readCSV(csvFile):
    # list that contains all previous attempts stored in csv file
    dataList = []

    try: 
        # Reading of previously stored data in csv file and store in a list
        with open(csvFile,'r') as file: # Read mode
            writer = csv.DictReader(file)
            for line in writer:
                # Appends each attempt into list as a dictionary
                dataList.append(dict(line))
    
    # for when running script by changing dir to server on terminal and py .\CA2-server.py
    # This changes the file paths of the text files
    except FileNotFoundError:
        if csvFile == resultsCsv:
            csvFile = './quiz_results.csv'

        with open(csvFile,'r') as file: # Read mode
            writer = csv.DictReader(file)
            for line in writer:
                # Appends each attempt into list as a dictionary
                dataList.append(dict(line))
    
    # Returns created dataList
    return dataList

# This function creates a dictionary. The number of key = the number of lines of the given txt file
# In each key, there will be a list of items, made by .split('|')
# The argument of this function takes in a textfile's pathway
# It returns a dictionary created based on the data stored in the text file
def readFile(txtFile):
    try: 
        dict = {}
        with open(txtFile,'r') as fn:       # Opens the given text file in read mode
            for i, line in enumerate(fn):   # For each line in the given txt file
                line = line.strip()         # Removes any spaces + '\n'
                dict[f'{i + 1}'] = line.split('|')    # Creates a list with the seperator '|' seperating each element

    # for when running file after changing dir to server on terminal and py .\CA2-server.py
    # This changes the file paths of the text files
    except FileNotFoundError:
        # Changing of file paths
        if txtFile == questionPoolTxt:
            txtFile = './question_pool.txt'
            
        elif txtFile == quizSettingTxt:
            txtFile = './quiz_setting.txt'

        elif txtFile == userID_pwdTxt:
            txtFile = './userid_pswd.txt'

        elif txtFile == coursesTxt:
            txtFile = './courses.txt'

        dict = {}
        with open(txtFile,'r') as fn:       # Opens the given text file in read mode
            for i, line in enumerate(fn):   # For each line in the given txt file
                line = line.strip()         # Removes any spaces + '\n'
                dict[f'{i + 1}'] = line.split('|')    # Creates a list with the seperator '|' seperating each element
    
    finally:
        # Checks for any empty list that were stored in dictionary keys
        emptyKeyList = []
        for key in dict:
            if dict[key] == ['']:
                emptyKeyList.append(key)
        
        # Deletes dict key that contains empty list as it is invalid
        for key in emptyKeyList:    
            del dict[key]
        
        return dict   # Returns the created dictionary
    

# This function receives the binary input sent from a client
# It then checks for the size of the message and ensures that it is not more than the specified max buffer size
# It then decodes the message and returns it as a string
# The arguments of this function are connection which is the socket connection and the max buffer size 
def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))
    decodedInput = client_input.decode("utf8").rstrip()
    return decodedInput
    
# modules Imported from python's library
import socket
import sys
import traceback
from threading import Thread
import csv
import ast

# Global variabes that contains the pathway to individual text files (works when pressing the run button)
questionPoolTxt = './Server folder/question_pool.txt'
quizSettingTxt = './Server folder/quiz_setting.txt'
userID_pwdTxt = './Server folder/userid_pswd.txt'
resultsCsv = './Server folder/quiz_results.csv'
coursesTxt = './Server folder/courses.txt' 

#
# ******************************* Main program ***********************************

def main():
    start_server()

# This function starts the server
def start_server():
    host = "127.0.0.1"
    port = 8000 # arbitrary non-privileged port
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    soc.listen(6) # queue up to 6 requests
    print("Socket now listening")
    # infinite loop- do not reset for every requests
    while True:
            connection, address = soc.accept()
            ip, port = str(address[0]), str(address[1])
            print('-------------------------------------------------')
            print('\n' + '\33[42m' + "Connected with " + ip + ":" + port + '\33[0m')
            
            try:
                Thread(target=clientThread, args=(connection, ip, port)).start()
            except:
                print("Thread did not start.")
                traceback.print_exc()

# This function listens and receives the client's input for the userID and password.
# It then processes it by checking it against the user dictionary
# the arguments in this function are the connection, the max buffer size of the message received and 
# the ip and port of the client and the user dictionary which was made based on the userid_pswd.txt
# Once the user enters both a valid username and password, it will then send the userID and module to the client, 
# allowing it to continue into the main user menu and then it will terminate the connection.
# To terminate the connection, it returns a False boolean value
def loginUser(connection, max_buffer_size, dict, ip,port):
    
    connection.send(b'Checking information...')
    # receiving clients input (String with userID and password or --Quit Login--)
    # e.g. 'userID|Password'
    client_input = receive_input(connection, max_buffer_size)

    # Intializing values
    checkLogin = client_input.split('|')
    checkUserID = checkLogin[0]
    checkPwd = checkLogin[1]
    module = None

    del dict['1'] # deletes admin user from dictionary 

    # For each username and password stored in userDict, check if userID and password both matches
    for key in dict:
        if checkUserID == dict[key][0]: # Checks if username is equal to stored password
            correctUserID = True
            if checkPwd == dict[key][1]: # Checks if password is equal to stored password
                correctPwd = True
                module = dict[key][3] # Assign the module based on the successful logged in user
                break
            else: 
                correctPwd = False
        else: 
            correctUserID = False
            correctPwd = False

    if correctPwd == True and correctUserID == True:
        # sends a string : True,{module assigned to user}
        print('\n'+ '\33[32m' + f'Client {ip}:{port} Successful Login!' + '\33[0m')
        connection.send(f'True|{module}'.encode("utf8"))
        connection.close() # Close connection
        print('\n'+ '\33[41m' +"Connection " + ip + ":" + port + " closed" +'\33[0m')
        print('-------------------------------------------------')
        return False # To terminate connection

    else:
        print('\n'+ '\33[41m' + f'Client {ip}:{port} Unsuccessful Login!' + '\33[0m')
        connection.send(b'False')
        connection.close() # Close connection
        print('\n'+ '\33[41m' +"Connection " + ip + ":" + port + " closed" +'\33[0m')
        print('-------------------------------------------------')

# This function listens and receives a username with their email
# It then checks whether it is valid and then sends the client for further prompts to reset password
# Once the client sends the new password, it will then process it and update userid_pswd.txt accordingly
# The arguments in this function are the connection, the max buffer size of the message received and 
# the ip and port of the client and the user dictionary which was made based on the userid_pswd.txt
# once done, it will terminate the connection 
def resetPwd(connection, max_buffer_size, dict, ip,port):
    
    connection.send(b'Checking information...')
    # receiving clients input (String with userID and password or --Quit Login--)
    # e.g. 'userID|Email'
    client_input = receive_input(connection, max_buffer_size)

    checkAccount = client_input.split('|')
    checkUserID = checkAccount[0]
    accountEmail = checkAccount[1]

    # Checks if userID entered by user is valid + store account email into accountEmail
    for key in dict:
        if int(key) > 1: # Key 1 is for admin user
            if checkUserID == dict[key][0] and accountEmail == dict[key][2] :
                correctUserID = True
                dictKey = key                      # Storing of dict key for writing later
                break
            else: 
                correctUserID = False

    # if both userid and email is correct, allow for reset password
    if correctUserID == False:
        print('\n'+ '\33[41m' + f'Client {ip}:{port} Wrong UserID or Email!' + '\33[0m')
        connection.send(b'Fail')
        connection.close() # Close connection
        print('\n'+ '\33[41m' +"Connection " + ip + ":" + port + " closed" +'\33[0m')
        print('-------------------------------------------------')

    # If email and username is correct, continue and receive new password
    else: 
        connection.send(b'Success!')
        print('\n'+ '\33[42m' + f'Client {ip}:{port} Entered Correct UserID and Email!' + '\33[0m')

        # receive new pwd or '--User Quit Reset Password--'
        newPwd = receive_input(connection,max_buffer_size)
        
        if newPwd != '--User Quit Reset Password--':
            # Reformatting of new password
            dict[dictKey][1] = ' pwd: wla' + newPwd[::-1] 
            
            try: 
                fn = open(userID_pwdTxt,'w') # Write mode
                # Writing of old account details stored onto old txt file + new password
                for key in dict:       
                        # Writes UserID | Password | Email | module
                        # For admin, only userID | Password
                        try:
                            fn.write(dict[key][0])
                            fn.write( '|' + dict[key][1])
                            fn.write( '|' + dict[key][2])
                            fn.write( '|' + dict[key][3] + '\n')
                        
                        # for admin account 
                        except IndexError:
                            fn.write('\n')  # new linefeed
                        
                    # Writing of new account being added
                fn.close()
            
            # for when runnning file by changing dir and py .\CA2-Server.py
            # This changes the file paths of all files
            except FileNotFoundError:
                txtFile = './userid_pswd.txt'
                fn = open(txtFile,'w') # Write mode
                # Writing of old account details stored onto old txt file + new password
                for key in dict:       
                        # Writes UserID | Password | Email | module
                        # For admin, only userID | Password
                        try:
                            fn.write(dict[key][0])
                            fn.write( '|' + dict[key][1])
                            fn.write( '|' + dict[key][2])
                            fn.write( '|' + dict[key][3] + '\n')
                        
                        # for admin account 
                        except IndexError:
                            fn.write('\n')  # new linefeed
                        
                    # Writing of new account being added
                fn.close()
                        
            print('\n' + '\33[32m' + 'Successfully changed password!' + '\33[0m')

        # user quits when changing password
        else: 
            print('\n' + '\33[41m' + 'User Quitted when changing password' + '\33[0m')

        connection.close() # Close connection
        print('\n'+ '\33[41m' +"Connection " + ip + ":" + port + " closed" +'\33[0m')
        print('-------------------------------------------------')


# This function sends both the strings of the quizSetting dictionary and the questionPool dictionary
# to client in order for client to continue taking the quiz
# The arguments in this function are the connection, the max buffer size of the message received and 
# the ip and port of the client.
def takeQuiz(connection, max_buffer_size,ip,port):
    
    # Reading of question Settings
    quizSettings = readFile(quizSettingTxt)
    # Reading of question pool
    questionPool = readFile(questionPoolTxt)
    # Reading of courses file to get the different modules
    courseDict = readFile(coursesTxt)   

    # Sending a string of the course dictionary to client
    connection.send(str(courseDict).encode("utf-8"))
    print('\n' + '\33[32m' + 'Sending Course Dictionary....' + '\33[0m')
    clientInput = receive_input(connection,max_buffer_size)
    print('\n' + '\33[32m' + clientInput + '\33[0m')
    
    # Sending a string of the quizSettings to client
    connection.send(str(quizSettings).encode("utf-8"))
    print('\n' + '\33[32m' + 'Sending Quiz Settings....' + '\33[0m')
    clientInput = receive_input(connection,max_buffer_size)
    print('\n' + '\33[32m' + clientInput + '\33[0m')

    # Sending a string of the questionPool to client
    connection.send(str(questionPool).encode("utf-8"))
    print('\n' + '\33[32m' + 'Sending Question Pool....' + '\33[0m')
    clientInput = receive_input(connection,max_buffer_size)
    print('\n' + '\33[32m' + clientInput + '\33[0m')

    connection.close() # Close connection
    print('\n'+ '\33[41m' +"Connection " + ip + ":" + port + " closed" +'\33[0m')
    print('-------------------------------------------------')
    return False

# This function writes the attempt it receives from the client into the quiz_results.csv
# once its done, it will close connection and return a False value to break out of main client thread loop.
# The arguments in this function are the connection, the max buffer size of the message received and 
# the ip and port of the client.
def writeAttempt(connection, max_buffer_size,ip,port):
    
    connection.send(b'Writing attempt...')

    clientAttempt = receive_input(connection,max_buffer_size)
    print('\n' + '\33[32m' + 'Received Attempt' + '\33[0m')

    connection.send(b'Received Attempt')

    # this is a rather large string, need bigger buffer
    questionPoolStr = receive_input(connection,max_buffer_size=10000)
    print('\n' + '\33[32m' + 'Received Question Pool' + '\33[0m')

    connection.send(b'Received question pool')

    # Rather long string where it contains "[topic,answer,selectedQuestionKey]"
    clientInput = receive_input(connection,max_buffer_size=10000)
    print('\n' + '\33[32m' + 'Received Topic, user answers and selected questions key' + '\33[0m')

    connection.close() # Close connection
    print('\n'+ '\33[41m' +"Connection " + ip + ":" + port + " closed" +'\33[0m')
    print('-------------------------------------------------')

    # Converting strings to dictionaries
    resultDict = ast.literal_eval(clientAttempt)
    questionpoolDict = ast.literal_eval(questionPoolStr)
    clientInputList = ast.literal_eval(clientInput)

    # Some intializing
    topic = clientInputList[0]
    answer = clientInputList[1]
    selectedQuestionKey = clientInputList[2]

    # Original question pool
    OGQuestionPool = readFile(questionPoolTxt)


    # This is to change user answers back to the matching original option of the original question pool
    # Original question pool will not be the same as the question pool being tested if the options are randomized
    if OGQuestionPool != questionpoolDict:
        optionNumbering = ['a)','b)','c)','d)']
        
        i = 0
        # Go through each question in the question pool 
        for key in selectedQuestionKey:
            try: 
                optionList = questionpoolDict[key][1:5]   
                # copying the plain text of the option the user has selected as their answer
                for option in optionList:
                    if option.find(str(answer[i])) != -1:
                        optionAnswered = option[3:]
                        break
                    
                    else:
                        optionAnswered = 'false'
                    
            
                # for each question, check with randomized list and change the user answer back to its original
                for a, OG_Option in enumerate(OGQuestionPool[key][1:5]):   
                    if OG_Option.find(optionAnswered) != -1:  
                        answer[i] = optionNumbering[a]
            
                i += 1

            except IndexError:   # For when user answer list have been fully changed back to original 
                continue

    i = 0
    # Creates key and input appropriate values and generate fieldnames accordingly
    for key in questionpoolDict:
        if questionpoolDict[key][7] == topic:
            resultDict[f'Question {i+1}'] = OGQuestionPool[key][0]         # Question
            resultDict[f'Q{i+1} Correct Answer'] = OGQuestionPool[key][5]  # Correct Answer for Question
            
            # If user did this question, store the user's answer along in the list
            if key in selectedQuestionKey:
                # If question is unanswered, store it as unanswered. Else, store it as what user have answered
                # selectedQuestionKey.index(key) finds the index where key is found in selectedQuestionKey list
                # it then checks if user have attempted the question or skip it
                # len(selectedQuestionKey) == len(answer)
                if answer[selectedQuestionKey.index(key)] == None:
                    resultDict[f'Q{i+1} User Answer'] = 'Unanswered'
                else:
                    resultDict[f'Q{i+1} User Answer'] = answer[selectedQuestionKey.index(key)]
            
            else: # if key is not in selectedQuestionKey List, it means it is not tested
                resultDict[f'Q{i+1} User Answer'] = 'Not Tested'
            
            i += 1

    # Datalist is a list that contains each previous attempts in dictionaries
    dataList = readCSV(resultsCsv)

    # Header of the csv file is contained within field list
    field = []
    for dictionary in dataList:
        for key in dictionary:
            # Appends all keys that attempt 1 has if it exists in csv file
            field.append(key)
        break
    
    # For when headers is empty (csv file is empty) or if headers contains lesser values than current attempt (new question added)
    if field == [] or len(field) < len(resultDict.keys()):
        field.clear()              # Resets field list to []
        for key in resultDict:
            field.append(key)      # Appending of old header

    # Appends the current attempt into the dataList(contains all previous known attempts)
    dataList.append(resultDict)
    
    # For any key that == '', it means that a new question(column) got added previously and previous attempts will have a new column
    # Helps to indicate that question did not exist in the quiz in the first place for that attempt
    for dictionary in dataList:
        for key in dictionary:
            if dictionary[key] == '':
                dictionary[key] = 'N/A'
    try: 
        # Writing of data into csv file
        with open(resultsCsv,'w') as fn: # write mode

            # Using dict writer as data is stored in dict
            writer = csv.DictWriter(fn,fieldnames = field)

            # Writing Headers (field names)
            writer.writeheader()
            
            # Writing of data rows
            writer.writerows(dataList)

    # for when runnning file by changing dir and py .\CA2-Server.py
    # This changes the file paths of all files
    except FileNotFoundError:
        # Changing of file path
        newResultsCSV = './quiz_results.csv'
        # Writing of data into csv file
        with open(newResultsCSV,'w') as fn: # write mode

            # Using dict writer as data is stored in dict
            writer = csv.DictWriter(fn,fieldnames = field)

            # Writing Headers (field names)
            writer.writeheader()
            
            # Writing of data rows
            writer.writerows(dataList)

    return False # To break out of loop in client thread, ending it

# This function is a thread that the client runs on. It waits for message sent by the client before it does
# different types of processing.
# the arguments of the function are connection, the ip and port associated with the client, and the max
# buffer size of each message. 
def clientThread(connection, ip, port, max_buffer_size = 5120):
    is_active = True
    while is_active:
        # Reads the file that contains all the userID and passwords 
        userDict = readFile(userID_pwdTxt)

        client_input = receive_input(connection, max_buffer_size)

        if "--Login--" in client_input: # For User login
            print('\n' + '\33[32m' + f"Client {ip}:{port} is requesting to login" + '\33[0m')
            is_active = loginUser(connection, max_buffer_size, dict = userDict,ip=ip,port=port)

        elif "--Reset Password--" in client_input: # for reset password
            print('\n' + '\33[32m' + f"Client {ip}:{port} is requesting to Reset Password" + '\33[0m')
            is_active = resetPwd(connection, max_buffer_size, dict = userDict,ip=ip,port=port)
        
        elif "--TAKE QUIZ--" in client_input: # For when client decides to take quiz
            print('\n' + '\33[32m' + f"Client {ip}:{port} is requesting questions" + '\33[0m')
            is_active = takeQuiz(connection, max_buffer_size,ip=ip,port=port)

        elif "--View Previous Attempt--" in client_input:
            print('\n' + '\33[32m' + f"Client {ip}:{port} is requesting previous attempts" + '\33[0m')
            pass
        
        elif "--Request results.csv--" in client_input: # For checkAttempts when requesting the data from quiz_results.csv
            dataList = readCSV(resultsCsv)
            connection.send(b'--OK--')
            # Gets userID
            userID = receive_input(connection,max_buffer_size)
            # Storing of all user attempts in a dictionary
            userAttemptList = []
            # Loop through each dictionary in dataList
            for dictionary in dataList:
                # Finds user attmpets given the userID and append the attempt to userAttemptList
                if dictionary['UserID'] == userID + ' ':
                    userAttemptList.append(dictionary)
            
            # Sending of list of the selected user's attempts
            connection.send(str(userAttemptList).encode("utf-8"))

            print('\n'+ '\33[32m'+ 'Sending dataList from quiz_results.csv' + '\33[0m')
            connection.close() # Close connection
            print('\n'+ '\33[41m' +"Connection " + ip + ":" + port + " closed" +'\33[0m')
            print('-------------------------------------------------')
            break # goes out of loop
            
        elif "--Request Question Pool--" in client_input: # To send to client the question pool
            questionPoolDict = readFile(questionPoolTxt)
            connection.send(str(questionPoolDict).encode("utf-8"))
            print('\n'+ '\33[32m'+ 'Sending Question Pool from question_pool.txt' + '\33[0m')
            connection.close() # Close connection
            print('\n'+ '\33[41m' +"Connection " + ip + ":" + port + " closed" +'\33[0m')
            print('-------------------------------------------------')
            break # goes out of loop

        elif "--Write Attempt--" in client_input: # For when client uploads the attempt
            print('\n' + '\33[32m' + f"Client {ip}:{port} uploading attempt..." + '\33[0m')
            is_active = writeAttempt(connection, max_buffer_size,ip=ip,port=port)
         
        else:
            print("Processed result: {}".format(client_input))
            connection.sendall("-".encode("utf8"))
            
if __name__ == "__main__":
    main()
