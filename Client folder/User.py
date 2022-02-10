# StudentID:    P2006264
# Name:	        Soh Kai Meng Leonard
# Class:		DISM/FT/1B/05 
# Assessment:	CA2 
# 
# Script name:	User.py
# 
# Purpose:	For user to take quiz and store their attempt in quiz_results.csv
#
#   Firstly user will be prompted to login using their userID and password. 
#   Programme will only accept valid userIDs and their respective passwords stored in userid_pswd.txt
#   User can also choose to forget password in order to reset password. User will have to enter appropriate userID
#   and email address allocated to it in userid_pswd.txt in order to be able to reset their password
#   
#   After successful Login, User can choose to take quiz or view their previous attemptsS
#   Once user have finished taking the quiz, results will be printed for user and attempt 
#   will be sent over to server for processing
#
#
# Usage syntax:	Run with play button
# 
# Alternate Usuage syntax: 1. Type in terminal: cd '.\Client folder\'
#                          2. Type in terminal: py .\User.py
#
# Input file:	None
#  
# Output file:	None
#   
# 
# Python ver:	Python 3
#
# Reference:
#       
#       (a) Python time Module 
#           https://www.programiz.com/python-programming/time 
#           accessed on 20 Nov 2021
#
#       (b) Working with csv files in Python 
#           https://www.geeksforgeeks.org/working-csv-files-python/ 
#           accessed on 19 Nov 2021
#
#       (c) Python CSV 
#           https://www.programiz.com/python-programming/csv 
#           accessed on 19 Nov 2021
#
#       (d) Python Random shuffle() Method 
#           https://www.w3schools.com/python/ref_random_shuffle.asp
#           accessed on 15 Nov 2021
#
#       (e) Python Regex 
#           https://www.w3schools.com/python/python_regex.asp
#           accessed on 18 Dec 2021
#       
#       (f) Python ast eval
#           https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary
#           accessed on 20 Jan 2022
#       
# Library/:	
# package/:
# Module/:
# 
# Random Module 
# Time Module
# re Module
# getpass Module
# ast Module
# socket Module
# sys Module
#
# Known issues:	eg. no validation of input value
#   
# Please ensure that server is running before attempting to login to user.
# If server is not running, the programme will be terminnated after 
# printing the message :  "[ERROR] Connection Error. Cannot connect to server" 
#
# ****************************** User-defined functions ***************************
# Describe the purpose of user-defined functions, parameters and return values

# This function checks for userInput and only accepts if userInput is within the range specified
# The argument of this function takes in the start and end integer values and finally the question being asked
# The function returns a valid integer number between the range specified in the argument
def validationRange(start,end,question): 
    while True:
        try:
            checkInput = int(input(question))
            if checkInput < start or checkInput > end:
                raise OverflowError
            else:
                return checkInput
        except OverflowError:   # for out of range
            print('\33[41m' +f'Out of range! Please enter an integer number between {start} and {end}'+ '\33[0m' +'\n')
        
        except ValueError:      # for not int number input 
            print('\33[41m'+ f'Invalid, not int. Please enter an integer number between {start} and {end}'+'\33[0m' + '\n')

        except EOFError:        # error for when user enters ctrl + z
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
        except KeyboardInterrupt:   # Error for when user enters ctrl + c
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')


# This function checks for any illegal char used in user inputs and rejects it if it is found. 
# The argument of this function takes in the question being asked
# The function returns a valid string that does not contain illegal char in the specialCharList
def stringValidation(question):
    specialCharList = ['~','`','`','\ ','|',':',',']
    while True: 
        try:
            counter = 0   
            checkInput = input(question)
            checkInput = checkInput.strip() # Removes spaces
            if checkInput == '':
                counter += 1
                print('\33[41m' + 'Empty input! Please re-enter again' + '\33[0m' + '\n')

                
            for char in specialCharList:
                # Ensure user input no special char
                if checkInput.find(char) != -1:   # If input contains special char : reject it
                    print('\33[41m' + f'Invalid char {char} entered! Please re-enter again' + '\33[0m' + '\n')
                    counter += 1
                    break

            if counter == 0:                
                return checkInput   # Validated after no special char in input

        except EOFError:            # error for when user enters ctrl + z
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
        except KeyboardInterrupt:   # Error for when user enters ctrl + c
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')

# This function takes in a list and question as parameters and ensures that user Input is an element in the given list
# The argument of this function takes in a list and the question being asked
# It returns a valid input that is inside the specified list in the argument
def listRangeValidation(list,question):
    while True: 
        try: 
            checkInput = input(question)
            checkInput = checkInput.strip()
            for char in list:
                if checkInput == char:      # if input is found within the list
                    return checkInput       # Returns input
            print('\33[41m' + f'Invalid char entered! Please re-enter a option from {list}'+ '\33[0m' +'\n')

        except EOFError:            # error for when user enters ctrl + z
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
        except KeyboardInterrupt:   # Error for when user enters ctrl + c
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')


# This function prints the selected question in the questionPool dict
# The argument of this function is the key of the selected question, its question pool dictionary and index (used for indexing of question)
def printSelectedQuestion(selectedQuestion,dictionary,index):
    print('\n---------------------------------------------\n')
    print('\n'+ '\33[32m' +f'Question {index}: ' + '\33[0m' f'\n{dictionary[selectedQuestion][0]} ({dictionary[selectedQuestion][6]}m)')
    for i in range(4):   # Printing of options 
        print(f'{dictionary[selectedQuestion][i+1]}')
    
    print('\n---------------------------------------------\n')

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

# This function creates a new connection with the server
# it returns the socket being connected
def newConnection():
    # Connecting to server
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8000

    try:
        soc.connect((host, port))
    except:
        print('\n' + '\33[41m' + "[ERROR] Connection Error. Cannot connect to server" + '\33[0m' )
        sys.exit()
    
    return soc

#
# ******************************* Main program ***********************************


import random
import time
import re
import getpass
import ast

import socket
import sys


# This function calculates the results of the quiz based on user input in answerList and answer that was inside the quesion pool.
# It will then collate the total marks and give a report + grade
# It then data into quiz_results.csv the attempt
# The argument of this function takes in the userID of the user, the module assigned to the user, course, module, the quiz name,
# the topic tested for the quiz, the answerlist, the key of tested questions, the question pool, time taken and the number of question answered
# the selected questions key used in the list and the question pool dict, time used for quiz, and the number of questions answered
def calculateResults(userID,course,module,quizName,topic,answer,selectedQuestionKey,questionpoolDict,timeUsed,numOfAnswered):
    correctAnswerList = []
    totalPossibleMarks = 0
    totalMarks = 0
    numOfCorrect = 0
    timeSubmitted = time.ctime(time.time())   # Gets time when quiz was submitted
    
    # Storing of correct answers + total possible marks
    for i in selectedQuestionKey:
        correctAnswerList.append(questionpoolDict[f'{i}'][5])   # Make a list filled with the correct answers
        totalPossibleMarks += int(questionpoolDict[f'{i}'][6])  # Collate total marks
    
    # Checks for correct answer and add marks accordingly
    for i, s in enumerate(correctAnswerList):
        if s == answer[i]:
            totalMarks += int(questionpoolDict[f'{selectedQuestionKey[i]}'][6]) # If answer is correct, add that marks allocated to the question to total marks
            numOfCorrect += 1                     # Adds 1 to the number of correct answer
    
    scorePercent = (totalMarks / totalPossibleMarks) * 100

    # Formatting of quiz results printing
    resultsMenu =  '\33[32m' + 'Results' + '\33[0m' +f'\n==============================================\n{userID}\nModule: {module.strip()}\n' 
    resultsMenu += '\nModule : ' + '\33[32m' + f'{module}' + '\33[0m' 
    resultsMenu += '\nTopic Tested : ' + '\33[32m' + f'{topic}' + '\33[0m' 
    resultsMenu += '\nResults : ' + '\33[32m' + f'{scorePercent:.2f} %' + '\33[0m' 
    resultsMenu += f'\nNumber of questions answered: {numOfAnswered} / {len(correctAnswerList)}'
    resultsMenu += f'\nNumber of correct answers {numOfCorrect} / {len(correctAnswerList)}' + '\n'
    resultsMenu += f'\nTotal Marks: {totalMarks:.2f} / Total Possible Marks : {totalPossibleMarks:.2f}'
    resultsMenu += f'\nTime Taken: {timeUsed} min\n'
    resultsMenu += f'\nTime Submitted: {timeSubmitted}\n'

    if scorePercent <= 40:
        resultsMenu += '\n' + '\33[41m' + 'Poor! You will have to work harder.' + '\33[0m'
    
    elif scorePercent < 80: 
        resultsMenu += '\n' + '\33[46m' + 'Fair. You can do better with more effort.' + '\33[0m'
    
    # For percentage 80% to 100%
    else: 
        resultsMenu += '\n' + '\33[42m' + 'Good! Well done.'  + '\33[0m'
    
    resultsMenu += '\n==============================================\n'
    print(resultsMenu)
    input('\33[42m' + 'Press enter to continue...' + '\33[0m' + '\n')

    # Creates a dictionary to store all of quiz data for the current attempt
    resultDict = {  'UserID' : userID,
                    'Course' : course,
                    'Module' : module.strip(),
                    'Quiz Name' : quizName,
                    'Topic Tested': topic,
                    'Grade (%)' : f'{scorePercent:.2f}',
                    'Number of Question Tested' : str(len(correctAnswerList)),
                    'Number of Question Answered' : numOfAnswered,
                    'Number of Correct Answer' : str(numOfCorrect),
                    'Total Marks' : f'{totalMarks:.2f}',
                    'Total Possible Marks': f'{totalPossibleMarks:.2f}',
                    'Time Used (min)' : timeUsed,
                    'Time Submitted' : timeSubmitted }

    # Create a new connection
    connection = newConnection()
    connection.send(b'--Write Attempt--') # Telling it to go into the writeAttempt function in server

    serverReply = receive_input(connection,max_buffer_size=5120)
    
    # Sends the resultDict over to server for it to update the quiz_results.csv
    connection.send(str(resultDict).encode("utf-8"))

    serverReply = receive_input(connection,max_buffer_size=5120)

    # sending the questionPoolDict over to server as a string
    connection.send(str(questionpoolDict).encode("utf-8"))

    # Makes a list that contains this 3 data to be sent over to server for processing
    topic_answer_selectedQuestionKey = [topic,answer,selectedQuestionKey]

    serverReply = receive_input(connection,max_buffer_size=5120)
    
    # sending over to server
    connection.send(str(topic_answer_selectedQuestionKey).encode("utf-8"))

# This function checks whether user has any attempts left and returns the number of attempts user has made
# It takes in the current user ID, module and the topic as the argument
def checkAttempt(userID,module,topic):
    # Number of attempts user have used
    numOfAttempts = 0

    # new connection
    connection = newConnection()
    connection.send(b'--Request results.csv--')

    # Receiving "--OK--" from server
    serverReply = receive_input(connection,max_buffer_size=5120)

    # Sending of userID
    connection.send(userID.encode("utf-8"))

    # Datalist is a list that contains each attempts in dictionaries
    # Need a very big buffer size as the data is quite long and big
    serverReply = receive_input(connection,max_buffer_size=30000)

    # converts the string into a list containing dictionaries
    dataList = ast.literal_eval(serverReply)

    # For each attempt, under the key 'UserID', if both userIDs matches add one to numOfAttempts
    for dictionary in dataList:
        if userID == dictionary['UserID'] and topic == dictionary['Topic Tested'] and module == dictionary['Module']:
            numOfAttempts += 1

    return numOfAttempts

# This function randomizes the options for all questions in the question pool and returns the newly edited dictionary
# It takes in the questionPool dict as its argument
def randomizeQuestionOption(dict):
    for key in dict:
        oldOptionList = dict[str(key)][1:6]  # Set oldOptionList a list with all options from a to d + answer
        optionList = dict[str(key)][1:5]     # set optionList as a list with all options from a to d
        optionStrList = []
        correctOption = ''

        # For each option among the 4 options form a) to d), find the correct answer and store in a str
        for option in optionList:                 
            if option.find(dict[str(key)][5]) != -1:
                optionStrList = option.split()     # append each word into a list
                optionStrList.pop(0)               # Removes a) to d)

                # Formatting of correct answers without a) to d)
                for char in optionStrList :
                    correctOption += char + ' ' 

        random.shuffle(optionList)
        
        if oldOptionList[4] == 'a)':
            index = 0
        elif oldOptionList[4] == 'b)':
            index = 1
        elif oldOptionList[4] == 'c)':
            index = 2
        elif oldOptionList[4] == 'd)':
            index = 3

        count = 0
        # Ensures that correct answer will be changed
        while optionList[index].find(correctOption) != -1:
            if count > 100:
                break
            random.shuffle(optionList)
            count += 1
        
        # Removes the optionNumbering for each option and replace with a) to d)
        for i , numbering in enumerate(['a','b','c','d']):
            optionStrList = optionList[i].split()        # append each word into a list
            optionStrList.pop(0)                         # Removes a) to d) it was initialized with
            newOption = numbering + ') '                 # Adds a) to d) respectively to match the order
            for char in optionStrList:
                newOption += char + ' '                  # Format the option as a) option....
            dict[str(key)][i+1] = newOption     # update new option into dict

        # Find the correct answer's option Numbering using plain text answer
        for option in dict[str(key)][1:5]:      # For each option in dict
            if option.find(correctOption) != -1:         # Find the correctOption with just the substring of the plain text option without its numbering a) to d)
                dict[str(key)][5] = option[0:2] # Adds the appropriate option numbering, a) to d) to inidicate the new correct answer
                
    return dict

# This function, takeQuiz first prompts the user to confirm take quiz
# If user confirms to take quiz, then it will create a random question list based on number of questions set in quiz settings\
# User will then take quiz with selected randomized questions where user answers will be stored in answerList
# This function will then go to calculateResults() function once user successfully submits to calculate results
# The argument of this function is the UserID of the successful login and the course assigned to it
def takeQuiz(userID,course):

    # Makes a new connection
    connection = newConnection()
    connection.send(b'--TAKE QUIZ--') # To go into takeQuiz() function of server file
    
    # Receiving courses dict
    courseDictStr = receive_input(connection,max_buffer_size=5120)
    connection.send(b'Client Received course dictionary')

    # Receiving quiz settings as a string from server
    quizSettingsStr = receive_input(connection,max_buffer_size=5120)
    connection.send(b'Client Received Quiz Settings')

    # Receiving Question pool from server
    questionPoolStr = receive_input(connection,max_buffer_size=10000)
    connection.send(b'Client Received Question Pool')

    # converting string back to dictionary
    questionPool = ast.literal_eval(questionPoolStr)
    quizSettings = ast.literal_eval(quizSettingsStr)
    courseDict = ast.literal_eval(courseDictStr)
    
    # Finding the course assigned to user and make a list of the modules assigned to it
    for key in courseDict:
        if courseDict[key][0] == course.strip():
            # e.g. ['PSEC', 'Fundamentals of Networking',...]
            moduleList = courseDict[key][1].split(',')
            break 

    # printing of modules assigned to the user's course
    takeQuizMenu = '\n-------------------------------------------------\n' + '\33[32m' + '\t      ' + '\33[4m'+ '\ Choose Module /' + '\33[0m' + '\n'

    for i, moduleName in enumerate(moduleList):
        takeQuizMenu += f'\n[{i+1}] ' + '\33[31m' + '\33[4m' + f'{moduleName}' + '\33[0m'

    takeQuizMenu += '\n-------------------------------------------------\nChoose a module based on its index\n[0] Cancel (Back)\n>>> '

    chosenOption = validationRange(start=0,end=len(moduleList),question=takeQuizMenu)

    if chosenOption == 0:
        return None # break out of function
    
    module = moduleList[chosenOption-1] # Selecting of module

    # Checks if question pool or quiz setting is empty
    if questionPool == {} or quizSettings == {}:
        emptyDict = True
    else:
        # Ensure that even if quiz setting is filled, it is with appropriate data and not the default empty
        if quizSettings['1'][1] == 'empty' or quizSettings['2'][1] == 'empty' or quizSettings['3'][1] == 'empty' or quizSettings['4'][1] == 'empty' or quizSettings['5'][1] == 'empty':
            emptyDict = True
        else:
            emptyDict = False


    # if both question pool and quiz setting is not empty, proceed to quiz
    if emptyDict == False:

        questionPoolKeyList = []
        timeOfQuiz = quizSettings['1'][1]              # contains a int. If not set : 'empty'. else can be 'Unlimited' as well
        noOfAttempts = quizSettings['3'][1]            # contains a int. If not set: 'empty'. Else can be 'Unlimited as well'
        randomizeOption = quizSettings['4'][1]         # 'Yes' or 'No'. If not set : 'empty'

        # A list that contains all the quizes in the module the user is assigned to
        for key in quizSettings:
            if int(key) > 5 and module == quizSettings[key][0]:
                # List contains the different quizes. e.g. ['Quiz 1:Math:Sci', 'Quiz 2:Geography:History'] for the module
                moduleQuiz = quizSettings[key][1].split(',')
                break

        # Creats a list that contains all the quiz being tested for each module 
        # e.g. ['Fundamentals of Networking: Quiz 1', 'PSEC: Quiz 1']
        moduleQuizTested = quizSettings['5'][1].split(',')
        
        quizTested = None

        for i in moduleQuizTested:
            # Creates a tmporary list that seperated the module name and the quiz being tested into a list
            # e.g. ['Fundamentals of Networking', ' Quiz 1']
            tmpList = i.split(':')
            if module == tmpList[0]:
                # e.g ' Quiz 1'
                quizTested = tmpList[1]
                break
        
        if quizTested == None or moduleQuiz == []:
            print('\n' + '\33[41m' + 'Error! No Quiz Tested Defined or No Quiz defined for module. Please contact admin' + '\33[0m')

        else: 
            for i in moduleQuiz:
                # creates a temporary list that contains the quiz and the topics it is testing 
                tmpList = i.split(':')
                # finding of quiz tested and its topics and storing it in topicTested Variable
                if quizTested == ' ' + tmpList[0]:
                    # A list that contains all topics tested in the course e.g. [topic,topic,...]
                    topicTested = tmpList[1:]
                    break

            attemptLeftList = []

            if noOfAttempts != 'Unlimited':
                # Checks for how many attempts user has made
                for i in topicTested:
                    numOfUserAttempts = checkAttempt(userID,module,topic=i)
                    print(numOfUserAttempts)
                    remainingAttempts = int(noOfAttempts)-numOfUserAttempts
                    if remainingAttempts < 0:
                        remainingAttempts = 0
                    
                    attemptLeftList.append(remainingAttempts)
            
            elif noOfAttempts == 'Unlimited':
                attemptLeftList = ['Unlimited'] * len(topicTested)

            takeQuizMenu = '\n-------------------------------------------------\n' + '\33[32m' + '\t\t' + '\33[4m'+ '\ Take Quiz /' + '\33[0m'
            # Printing of attempts left for each topic tested
            attemptStr = f'{topicTested[0]:} : ' + '\033[91m' + '\33[4m' + f'{attemptLeftList[0]}' + '\33[0m' + '\n'
            for i in range(len(attemptLeftList)-1):
                attemptStr += f'{topicTested[i+1]:>30} : ' + '\033[91m' + '\33[4m' + f'{attemptLeftList[i+1]}' + '\33[0m' + '\n'

            takeQuizMenu += f'\n\nNumber of Attempts Left -> {attemptStr}'

            noOfQuestions = []
            # Finding noOfQuestions for each topic and store it in a list
            for topic in topicTested:
                # [Math: 5,Sci: 2,Geography: 3,History: 2]
                tmpList = quizSettings['2'][1].split(',')
                for i in tmpList:
                    # creates a list that contains the topic name and its number of questions assigned to it
                    tmpList1 = i.split(':')
                    if tmpList1[0] == topic:
                        noOfQuestions.append(tmpList1)

            # Printing of details for quiz
            noOfQuestionStr = ''
            noOfQuestionStr = f'{topicTested[0]:} : ' + '\033[91m' + '\33[4m' + f'{noOfQuestions[0][1].strip()}' + '\33[0m' + '\n'
            # Printing of topics tested with its number of question being tested for the given topic
            for i in range(len(noOfQuestions)-1):
                noOfQuestionStr += f'{topicTested[i+1]:>33} : ' + '\033[91m' + '\33[4m' + f'{noOfQuestions[i+1][1].strip()}' + '\33[0m' + '\n'

            takeQuizMenu += f'\nNumber of Questions Tested -> {noOfQuestionStr}'
            quizName = quizTested.strip()
            takeQuizMenu += '\nQuiz Tested: ' + '\33[41m' + '\33[4m' + f'{quizName}' + '\33[0m'
            takeQuizMenu += f'\nTopic Tested: {topicTested}\n'
            takeQuizMenu += f'\nTime allowed: {timeOfQuiz} min'
            # Prints all topics in topicTested
            for i , topic in enumerate(topicTested):
                takeQuizMenu += f'\n[{i+1}] {topic}'
            takeQuizMenu += f'\n[0] Back'

            takeQuizMenu += '\n\n-------------------------------------------------\n>>> '

            confirmOption = validationRange(start=0,end=len(topicTested),question=takeQuizMenu)

            topic = topicTested[confirmOption-1] # Set topic chosen by user

            if attemptLeftList[confirmOption-1] != 0 and confirmOption != 0:   # ensures that user can only take quiz if attempts are not 0  
                # User will be tested quizes according to topic tested as specified in quiz_setting file
                for key in questionPool:
                    if questionPool[key][7] == topic: 
                        questionPoolKeyList.append(key)
                
                # Randomizes the question options if setting for randomize option for question is 'Yes'
                if randomizeOption == 'Yes':
                    questionPool = randomizeQuestionOption(dict = questionPool)

                # Shuffles the question key pool to randomize questions that are selected
                random.shuffle(questionPoolKeyList)
                # setting no of questions to be the number of questions assigned to the given topic
                # noOfQuestions list = [['Math', ' 5'],['Sci', ' 2'], ['Geography', ' 3'], ['History', ' 2'],....]
                noOfQuestions = noOfQuestions[confirmOption-1][1]
                # Set the no of questions in questionPoolKeyList to be that of what was stated in quiz settings 
                questionPoolKeyList = questionPoolKeyList[0:int(noOfQuestions)]
                # Makes an empty list whcih has a length equal to number of questions being tested 
                # List contains [None,None,None,...] Number of elements in list is equal to number of questions being tested
                answerList = [None]*len(questionPoolKeyList)

                print(f'\n{userID}, Please Choose the best answer for questions.\nTopic Tested: {topic}\nNumber Of Questions: {noOfQuestions}\nTime allowed: {timeOfQuiz} min\n')

                # Intializing of i and key for while True loop 
                i = 0
                key = questionPoolKeyList[i]
                
                # Calculate when the end time of the quiz should be only when time setting is not set as "Unlimited"
                if timeOfQuiz != 'Unlimited':
                    # use time module to get seconds since 1970 for storing of time quiz should end
                    endTime = time.time() + int(timeOfQuiz) * 60

                # Quiz Loop where they will ask questions chosen from randomized questionPoolKeyList. 
                # Only accept user input a,b,c,d,p,n
                # P for previous question
                # N for next question
                # User input (answer) is stored in answerList 
                while True:
                
                    # Checking of any unaswered questions for when time is out
                    unansweredQuestionList = []
                    unansweredQuestion = False

                    # Check through answerList and check if there is any value which is None. Count is used to count num of questions answered
                    count = len(questionPoolKeyList)
                    for s, userAnswer in enumerate(answerList):
                        if userAnswer == None:
                            unansweredQuestionList.append(s+1)
                            unansweredQuestion = True
                            count -= 1

                    # Only stop quiz when time is up for when time setting is not set as "Unlimited"
                    if timeOfQuiz != 'Unlimited':
                        # Gets time left in min (-0.40 as it starts from 1.00 for each min)
                        timeLeft = (endTime - time.time()) / 60 - 0.40

                        # If time is up, auto submit it after next user input
                        if timeLeft <= 0:
                            print('\n' + '\33[41m' + 'Time is up! Submitting Test now...' + '\33[0m' + '\n')
                            # The parameter takes in the userID of the user, the answerlist, the selected questions used in the list, question pool dict and time taken
                            calculateResults(userID,course,module,quizName,topic=topic,answer=answerList,selectedQuestionKey=questionPoolKeyList,questionpoolDict=questionPool,timeUsed=timeOfQuiz,numOfAnswered=count)
                            break    # Breaks out of while true loop after calculateResults function
                    
                    # if time setting is set as "Unlimited", store start time when the quiz has started.
                    elif timeOfQuiz == 'Unlimited':
                        startTime = time.time()

                    # Prints selcted question given the question key
                    printSelectedQuestion(selectedQuestion=key,dictionary=questionPool,index=i+1)
                    
                    # Only display time left if time is not set as "Unlimited" in settings
                    if timeOfQuiz != 'Unlimited':
                        print('Current Time Left: ' + '\33[32m' + f'{timeLeft:.2f} (min/s)' + '\33[0m')

                    # Shows previous submitted answer for previous questions if user presses P after entering an answer
                    if answerList[i] != None:
                        print('Previous Answer submitted: ' + '\33[32m' + f'{answerList[i]}' + '\33[0m' + '\n')
                    
                    # Gets user input for answer of quiz
                    answer = listRangeValidation(list=['a','b','c','d','p','n'],question='<Enter (a) to (d) for answer, P for previous question, N for next question>\n>>> ')

                    # If user enters answer, store it in answerList and go to next question
                    if answer.upper() != 'P' and answer.upper() != 'N':
                        answerList[i] = answer + ')'  # Storing of answer in answerList
                        i += 1                        # Adds one to i

                        # For last question, ask for submit
                        if i == len(questionPoolKeyList) :
                            print('\n\n\n\n')
                            # Printing of all questions and what user has answered for each
                            for s , key in enumerate(questionPoolKeyList):
                                printSelectedQuestion(selectedQuestion=key,dictionary=questionPool,index=s+1)
                                if answerList[s] != None:
                                    print('Answer submitted: ' + '\33[32m' + f'{answerList[s]}' + '\33[0m' + '\n')
                                else: 
                                    print('Answer submitted: ' + '\33[41m' + f'Unanswered' + '\33[0m' + '\n')
                            
                            confirmSubmitMenu = '\nEnter' + '\33[32m' + ' 0 ' + '\33[0m' + 'to submit your quiz or ' +'\33[91m' + f'[1 to {i}] ' + '\33[0m' + 'to change your answer.\n >>> '
                            
                            # Checking of any unaswered questions again for final question
                            unansweredQuestionList.clear()   # Clears list
                            unansweredQuestion = False       # Reset check

                            # Check through answerList and check if there is any value which is None. Count is used to count num of questions answered
                            count = len(questionPoolKeyList)
                            for s, userAnswer in enumerate(answerList):
                                if userAnswer == None:
                                    unansweredQuestionList.append(s+1)
                                    unansweredQuestion = True
                                    count -= 1

                            # IF there are unanswered questions, let user know
                            if unansweredQuestion == True:
                                print('\33[41m' + f'Unanswered Question(s): {unansweredQuestionList}' + '\33[0m' + '\n')  

                            confirmSubmit = validationRange(start=0,end=i,question=confirmSubmitMenu)
                            # Submission of quiz
                            if confirmSubmit == 0:
                                input('\33[42m' + '\nQuiz Submitted! Press enter to continue...' + '\33[0m' + '\n')
                                
                                # calculate time taken if time is not set as "Unlimited"
                                if timeOfQuiz != 'Unlimited':
                                    timeTaken = str(int(timeOfQuiz) - int(timeLeft))
                                
                                # Calculate time taken if time is set as "Unlimited" by taking the time submitted - start time
                                elif timeOfQuiz == 'Unlimited':
                                    timeTaken = str(int((time.time()-startTime))) 
                                
                                # The parameter takes in the userID of the user, the answerlist, the selected questions used in the list, question pool dict and time taken
                                calculateResults(userID,course,module,quizName,topic=topic,answer=answerList,selectedQuestionKey=questionPoolKeyList,questionpoolDict=questionPool,timeUsed=timeTaken,numOfAnswered=count)
                                
                                # Break out of while True loop to go all the way back to main menu page
                                break 

                            # For when user chooses to change an answer of a selected question
                            else:
                                i = confirmSubmit - 1 # -1 as for last element, there is a += 1 above

                        key = questionPoolKeyList[i]  # sets key to current question where index i is

                    # Go to next question when i < index of last question
                    elif answer.upper() == 'N' and i < len(questionPoolKeyList) -1:
                        i += 1
                        key = questionPoolKeyList[i]
                    # For when user tries to get to next question at last question when i > index of last question
                    elif answer.upper() == 'N' and i >= len(questionPoolKeyList) -1: 
                        print('\n'  + '\33[41m' + 'Error! Your are attempting last question. Cannot go to next question' + '\33[0m' + '\n')

                    # Go to previous question when i >= index of first questtion, 0
                    elif answer.upper() == 'P' and i >= 1: 
                        i -= 1
                        key = questionPoolKeyList[i]
                    
                    # For when user tries to go to previous question at Question 1 when i < index of first question,0
                    elif answer.upper() == 'P' and i < 1:
                        print('\n'  + '\33[41m' + 'Error! You are attempting first question. Cannot go back to previous question' + '\33[0m' + '\n')
            
            # For when user tries to enter quiz but has used up all attempts
            else:
                if confirmOption != 0:  # If user presses 1 instead of 0 since 0 is used to go back
                    print('\n'  + '\33[41m' + f'Error! You have used up all attempts for {topic}. Cannot attempt quiz again' + '\33[0m' + '\n')

    # Error for when quiz settting is empty or when question pool is empty
    else: 
        print('\n'  + '\33[41m' + 'Error! Quiz Setting or Question Pool is empty! Please contact administrators for help' + '\33[0m' + '\n')

# This function allows the user to view their previous attempts 
# User will select a previous attempt to view information about their previous chosen attempt.
# It gives the question tested in the quiz and the subsequent answers for each question.
# It also gives stats on the attempt of the chosen attempt
# It takes in the user ID of a chosen user and its course as the argument
def viewResults(userID,course):
    while True:

        connection = newConnection()
        connection.send(b'--Request results.csv--') # Requesting for each attempt in quiz_results.csv 

        # Receiving "--OK--" from server
        serverReply = receive_input(connection,max_buffer_size=5120)

        # Sending of userID
        connection.send(userID.encode("utf-8"))

        # Max buffer size is big as list could be quite big
        serverReply = receive_input(connection,max_buffer_size=30000)

        # Datalist is a list that contains each attempts in dictionaries
        userAttemptList = ast.literal_eval(serverReply) # Converts string to list that contains many dictionaries
        
        # Error message if user did not attempt quiz 
        if userAttemptList == []:        
            print('\n' + '\33[41m' + 'Error! No attempts made to quiz' + '\33[0m' + '\n') 
            break
        
        # Printing of all results
        resultsMenu = f'\n------------------------------------------------------\n\t\t' + '\33[32m' + '\33[4m' + '{ View Results }'  + '\33[0m'
        resultsMenu += f'\n\n{userID}\nCourse: {course}\n' 
        
        # Printing of each attempt done 
        for i, attempt in enumerate(userAttemptList):
            resultsMenu += f'\n[{i+1}] Attempt {i+1}: ' + 'Time Submitted: ' + attempt['Time Submitted'] + '\n'
            resultsMenu += '    Module: ' +'\33[32m' + attempt['Module'] + '\33[0m' +'\tQuiz Name: ' '\33[31m' + attempt['Quiz Name'] + '\33[0m' + '\n    Topic: ' + '\33[32m' + attempt['Topic Tested'] + '\33[0m' 
            resultsMenu += '\tGrade: ' + '\33[41m' + '\33[4m' + attempt['Grade (%)'] + ' %' + '\33[0m' + '\n'

        resultsMenu += '\n\n------------------------------------------------------\n' + '\33[41m' + '\33[4m' + 'Choose an attempt to view the questions tested' + '\33[0m'
        resultsMenu += '\n[0] Cancel (Back)\n>>> '

        checkInput = validationRange(start=0,end=len(userAttemptList),question=resultsMenu)
        
        if checkInput == 0:
            break

        chosenAttempt = userAttemptList[checkInput-1] # selecting of chosen attempt (attempt is a dictionary)
        topicTested = chosenAttempt['Topic Tested']   # getting of topic tested

        possibleUserAnswerList = ['a)','b)','c)','d)','Unanswered']
        keyList = []
        questionTestedKey = []
        userAnswer = []
        for key in chosenAttempt:
            keyList.append(key)
            if chosenAttempt[key] in possibleUserAnswerList and 'User Answer' in key:
                # Index of where question tested can be found (question Index = user answer index - 2)
                questionTestedKey.append(keyList[keyList.index(key) - 2]) # storing of question title
                userAnswer.append(chosenAttempt[key]) # Storing of user answer

        # Making another new conection to server
        connection = newConnection()
        connection.send(b'--Request Question Pool--')

        # it is a rather long string, thus buffer size is big
        serverReply = receive_input(connection,max_buffer_size=10000)

        # question pool dict that contains all questions
        questionPoolDict = ast.literal_eval(serverReply) # converts string into dictonary

        # Use for printing of the individual user answers in the loop below
        userAnswerIndex = 0
        # Printing of individual question tested and the user's answer
        for key in questionPoolDict:
            resultsMenu = ''
            for questionTested in questionTestedKey:
                if questionPoolDict[key][7] == topicTested and chosenAttempt[questionTested] == questionPoolDict[key][0]:
                    # Prints selcted question given the question key
                    printSelectedQuestion(selectedQuestion=key,dictionary=questionPoolDict,index=userAnswerIndex+1)
                    # Prints user answer for the question
                    print( '\n' +'Your Answer: ' + '\33[32m' + '\33[4m' + f'{userAnswer[userAnswerIndex]}' + '\33[0m'+ '\n\n')
                    userAnswerIndex += 1
                    input('\33[42m' + 'Press enter to continue...' + '\33[0m' + '\n') 

        # Formatting of quiz results printing
        resultsMenu =  '\n' + '\33[32m' + f'Statistics for Attempt:' + '\33[0m' +f'\n------------------------------------------------------\n{userID}\nCourse: {course}\n' 
        resultsMenu += '\nModule : ' + '\33[32m' + chosenAttempt['Module'] + '\33[0m'
        resultsMenu += '\nTopic : ' + '\33[32m' + chosenAttempt['Topic Tested'] + '\33[0m'
        resultsMenu += '\nResults : ' + '\33[32m' + chosenAttempt['Grade (%)'] +' %' + '\33[0m' 
        resultsMenu += '\nNumber of questions answered: ' + chosenAttempt['Number of Question Answered'] + ' / ' + chosenAttempt[ 'Number of Question Tested']
        resultsMenu += '\nNumber of correct answers ' + chosenAttempt['Number of Correct Answer'] + ' / ' + chosenAttempt['Number of Question Tested']
        resultsMenu += '\nTime Taken: ' + chosenAttempt['Time Used (min)'] + ' min\n'
        resultsMenu += '\nTime Submitted: ' + chosenAttempt['Time Submitted']
        resultsMenu += '\n------------------------------------------------------\n'
        print(resultsMenu)
        
        input('\33[42m' + 'Press enter to continue...' + '\33[0m' + '\n')


# this function serves as a purpose of main menu after user successfully logins
# The argument of this function is the UserID of the successful login and the course assigned to it
# and the socket connection that will help the server know that the user has logged out
def mainMenu(userID,course):
    while True:
    
        mainMenu = '\n==============================================\n' + '\33[32m' + '\t\t' + '\33[4m'+ '\ Main Menu /' + '\33[0m'
        mainMenu += f'\n\nWelcome {userID}!\nCourse: {course}\n[1] Take Quiz\n[2] View Current Results\n[0] Logout'
        mainMenu += '\n\n==============================================\n>>> '

        chosenOption = validationRange(start=0,end=2,question=mainMenu)
        if chosenOption == 0:
            break

        # Take Quiz
        elif chosenOption == 1:
            if course == ' Deleted Course':
                print('\n' + '\33[41m' + 'Error! Course Deleted. Please contact admin' + '\33[0m')
            
            else: 
                takeQuiz(userID,course)

        # View of current user Results
        elif chosenOption == 2:
            viewResults(userID,course)

# This function checks for the correct userID and password entered by user and sends the information to the server.
# If the information is correct, the server will send back a login success reply. 
# This dictionary will be used for checking user login
def loginUser():
    while True:
        checkUserID = stringValidation(question='\n'+ '\33[32m' +'\33[4m'+  'Please Enter Your User ID' + '\33[0m'  +'\n[0] Back to login page\n>>> ')

        if checkUserID == '0':
            return None, None
        
        else:
            # Formatting of userID to match it in dict. Format is UserID: .... 
            checkUserID = 'UserID: ' + checkUserID + ' '

            checkPwd = getpass.getpass(prompt='\n' +'\33[32m'+ '\33[4m' +'Please Enter Your Password' + '\33[0m' + '\n[0] Back to Entering username\n>>> ')

            if checkPwd != '0':
                # Formatting of pwd to match it in dict. Format is pwd: wla....
                checkPwd = ' pwd: wla' + checkPwd[::-1]

                connection = newConnection() # creata a new socket 
                connection.send(b'--Login--') # let server knows to go into loginUser function inside server

                # Server will reply with 'Checking information...'
                serverInput = receive_input(connection,max_buffer_size=5120)
                print('\33[31m' + serverInput + '\33[0m')
                # sends a list over to server for processing
                connection.send(f'{checkUserID}|{checkPwd}'.encode("utf8"))
                
                # SuccessLogin is a string that the server will send over confirming whether the login is successful
                # e.g. 'True|Course assigned to user' or 'False|None' for failed login
                serverInput = receive_input(connection,max_buffer_size=5120)
                checkLogin = serverInput.split('|')
                
                # When password and userID matches, accept and go to main menu
                if checkLogin[0] == 'True':
                    input('\n'+'\33[42m' + 'Login Success! Press enter to continue...' + '\33[0m' + '\n')
                    return checkUserID, checkLogin[1] # checkLogin[1] is the course

                # for when information entered is invalid, unsuccessful login
                else: 
                    print('\n'  + '\33[41m' + 'Error! UserID or Password is invalid! Please re-enter information again' + '\33[0m' + '\n')

# This function prompts the user to enter a valid userID and its email for them to reset password
# It then sends the user inputs over to the server for processing and waits for the server to reply
# Once the server replies a successful login, it will allow the client user to reset their password
# it will then send the new password over to the server for processing
# The argument of the function takes is the socket connection
def resetPwd():
    while True:
        checkUserID = stringValidation(question='\n'+ '\33[32m' + '\33[4m' + 'Please Enter Your User ID' + '\33[0m'  +'\n[0] Back to login page\n>>> ')

        if checkUserID == '0':
            break
        
        # Check for valid user ID
        else: 
            checkUserID = 'UserID: ' + checkUserID.strip() + ' '

            email = stringValidation(question='\n'+ '\33[32m' + '\33[4m' + 'Please Enter Your Email' + '\33[0m'  +'\n[0] Back to login page\n>>> ')
            email = ' Email: ' + email.strip() 

            if email == ' Email: 0':  # If user enters 0 to quit,  email = ' Email: ' + '0'
                break
            
            # Creates a new connection to server
            connection = newConnection()
            connection.send(b'--Reset Password--') # Let server know to go into resetPwd function
            
            # Server will reply with 'Checking information...'
            serverInput = receive_input(connection,max_buffer_size=5120)
            print('\n'+ '\33[31m' + serverInput + '\33[0m')
            # Sends to server the the username and email for verification
            connection.send(f'{checkUserID}|{email}'.encode("utf-8"))

            # Wait for server reply whether its successful or not
            # for successful, server will reply with 'Success!'
            serverInput = receive_input(connection,max_buffer_size=5120)
            # For when email or username is wrong
            if serverInput != 'Success!':
                print('\n'+ '\33[41m' + f'Error! Incorrect User ID or Email. Please re-enter information again' + '\33[0m')
                
            else: 
                input('\n'+'\33[42m' + 'Success! To Reset Password, Press Enter to continue...' + '\33[0m' + '\n')
                newPwd = pwdCheck(question='\n'+ '\33[32m' + '\33[4m' + 'Please Enter new password'+'\33[0m'+'\n[0] Back to Enter User ID\n>>> ')
                
                # If user choses not to quit, reprompt to re-enter password
                # newPwd == None if 0 is entered
                if newPwd != None :
                    checkPwd = stringValidation('\n'+ '\33[32m'+ '\33[4m' + 'Please re-enter new password'+'\33[0m'+'\n[0] Back to Enter User ID\n>>> ')

                    if checkPwd != '0' and checkPwd == newPwd:
                        # Sends the password over to server for it to update the txt file
                        connection.send(checkPwd.encode("utf-8"))
                        input('\33[42m' + '\nPassword Successfully Changed! Press enter to continue...' + '\33[0m' + '\n')
                        # break out of while True loop to go back to login Menu
                        break
                    
                    # 2 passwords that user entered did not match
                    else:
                        if checkPwd != '0':
                            print('\n'  + '\33[41m' + 'Error! Passwords do not match. Please re-enter information again' + '\33[0m' + '\n')
                        
                connection.send(b'--User Quit Reset Password--')


# This function ensures that password contains special char + minimum length of 8
# The argument of this function takes in the question being used to prompt user
def pwdCheck(question):
    while True:  
        try: 
            checkInput = input(question)
            checkInput.strip()  # Removes any spaces
            
            # Quitting of entering password
            if checkInput == '0':
                break

             # checks for contain 1 a-z , 1 A-Z, 1 digit, 1 special char from [!@#$%] and is between 4 and 20 char
            regexPattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%])[A-Za-z\d!@#$%]{4,20}$'
            
            # uses regex search and returns an object if there is a match. Else, return None if there is no match
            validationPwd = re.search(regexPattern,checkInput)

            if validationPwd != None: 
                return checkInput
            else:                
                # For any errors during password Check
                print('\33[41m' + f'Error! Please ensure that password contains at least one special char : @ , # , ? , & , % , $ , !' + '\33[0m')
                print('\33[41m' + 'AND does not contain \'|\'' + '\33[0m')
                print('\33[41m' + 'AND contains 1 number' + '\33[0m')
                print('\33[41m' + 'AND contains one uppercase and one lowercase char' + '\33[0m')
                print('\33[41m' + 'AND must be between 4 and 20 characters with no spaces in it' + '\33[0m' + '\n')

        except EOFError:            # error for when user enters ctrl + z
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
        except KeyboardInterrupt:   # Error for when user enters ctrl + c
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
            


# This function prompts user for login before leading them to main menu
def loginMenu():
    while True: 
        # use time module to get seconds since 1970 and convert into Local time with .ctime
        currentTime = time.ctime(time.time())

        loginUserMenu = '\n==============================================\n' + '\33[32m' + '\t\t' + '\33[4m'+ '\ Login Page /' + '\33[0m'
        loginUserMenu += f'\n\n[1] Login\n[2] Forget Password\n[0] Quit\n\nCurrent Time: {currentTime}\n'
        loginUserMenu += '\n==============================================\n>>> '
        
        chosenOption = validationRange(start=0,end=2,question=loginUserMenu)    
        
        # Quit
        if chosenOption == 0:
            print('\33[91m' + 'Terminating Programme...' + '\33[0m')
            print('\33[32m' + 'Programme Terminated' + '\33[0m' + '\n')
            break

        # Login using userID and password
        if chosenOption == 1:
            userID , course = loginUser()
            
            if userID != None and course != None:
                # Go to mainMenu with user selected userID after successful login and its module
                mainMenu(userID,course)

        # Reset Password
        elif chosenOption == 2:
            resetPwd()
        

if __name__ == "__main__":
    loginMenu()