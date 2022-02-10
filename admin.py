# StudentID:    P2006264
# Name:	        Soh Kai Meng Leonard
# Class:		DISM/FT/1B/05 
# Assessment:	CA2
# 
# Script name:	admin.py
# 
# Purpose:	Purpose of admin script is to edit / configure the quiz
#
# In User settings, it allows admin to view user list,register users, delete users, 
# reset user password, Change user's course and delete a user attempt from quiz results
#
# In Setup Question Pool, it allows admin to choose a selected topic, add a topic. 
# After selecting a topic, it allows to view question list, add question, delete question
# and edit question property after choosing a question (allows for more complicated configurations)
#
# In editing question property, admin chooses a selected question from question pool and is 
# able to change question title, edit option, change marks for question and randomize options
#
# In Quiz Settings, admin is able to edit the settings for quiz e.g. time of quiz, question for each topic,
# maximum attempts for quiz, enabling randomze options for quiz and choosing the test being tested for 
# the selected module
#
# In Edit Modules, Admin can choose a predefined module to edit or add a module or delete a module.
# While editing a selected module, admin is able to edit the a predefined quiz, add a quiz or delete a quiz
# While editing a selected quiz, admin is able to add a topic to the quiz, remove a topic from the quiz 
# and change the quiz name
#
# In Edit Courses, Admin can choose a predefined course to edit or add a course or delete a course.
# While editing a selected course, admin can choose to add a defined module, remove a module off the course
# and change the course name
#
# Lastly, admin is able to generate a quiz report. The quiz report is based on the number of the module, quiz, 
# topic chosen with its number of questions tested and viewing of highest attempts or all attempts made in 
# the quiz. After picking the num of questions the quiz tested, it then gives a statistical report based 
# on all atttempts that fits the critera mentioned above
#
#
# Usage syntax:	Run with play button
# 
# Input file:	
#
# './Server folder/question_pool.txt'
# './Server folder/quiz_setting.txt'
# './Server folder/userid_pswd.txt'
# './Server folder/quiz_results.csv'
#  
# Output file:	
#
# './Server folder/question_pool.txt'
# './Server folder/quiz_setting.txt'
# './Server folder/userid_pswd.txt'
# './Server folder/quiz_results.csv'
#
# Python ver:	Python 3
#
# Reference:
#   (a) statistics — Mathematical statistics functions
#       https://docs.python.org/3/library/statistics.html 
#       accessed on 21 Nov 2021'
#
#   (b) Python CSV
#       https://www.programiz.com/python-programming/csv
#       accessed on 19 Nov 2021
#
#   (c) Python Random shuffle() Method 
#       https://www.w3schools.com/python/ref_random_shuffle.asp
#       accessed on 15 Nov 2021
#
#   (d) Python Regex 
#       https://www.w3schools.com/python/python_regex.asp
#       accessed on 18 Dec 2021
#	
# Module : 
#
# Random Module
# CSV Module
# Statistics Module
# re Module
# getpass Module
# Time Module
#
# Known issues:	eg. no validation of input value
# 
# None
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
    specialCharList = ['~','`','`','\ ','|',',',':']
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

# This function creates a dictionary. The number of key = the number of lines of the given txt file
# In each key, there will be a list of items, made by .split('|')
# The argument of this function takes in a textfile's pathway
# It returns a dictionary created based on the data stored in the text file
def readFile(txtFile):
    dict = {}
    with open(txtFile,'r') as fn:       # Opens the given text file in read mode
        for i, line in enumerate(fn):   # For each line in the given txt file
            line = line.strip()         # Removes any spaces + '\n'
            dict[f'{i + 1}'] = line.split('|')    # Creates a list with the seperator '|' seperating each element
    
    # Checks for any empty list that were stored in dictionary keys
    emptyKeyList = []
    for key in dict:
        if dict[key] == ['']:
            emptyKeyList.append(key)
    
    # Deletes dict key that contains empty list as it is invalid
    for key in emptyKeyList:    
        del dict[key]
        
    return dict   # Returns the created dictionary

# This function takes in a list and question as parameters and ensures that user Input is an element in the given list
# The argument of this function takes in a list and the question being asked
# It returns a valid input that is inside the specified list in the argument
def listRangeValidation(list,question):
    while True: 
        try: 
            checkInput = input(question)
            checkInput.lower()              # Lowercase the input
            for char in list:
                if checkInput == char:      # if input is found within the list
                    return checkInput       # Returns input
            print('\33[41m' + f'Please re-enter a option from {list}'+ '\33[0m' +'\n')

        except EOFError:            # error for when user enters ctrl + z
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
        except KeyboardInterrupt:   # Error for when user enters ctrl + c
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
            
# This function prints all the questions available in question_pool.txt and returns the last index of the last question
# The argument of this function takes in the question pool dict and the topic of the question
# It returns the question index where it could be found using the key of the dictionary
def printQuestions(dict,topic):
    questionsIndex = 1
    print('\33[32m' + '\n*** Current Question List ***' + '\33[0m')
    for key in dict:
        if dict[key][7] == topic:   # checks for correct topic
            print('\n' +'\33[32m' +f'Question {questionsIndex}: ' + '\33[0m' + f'{dict[key][0]} ({dict[key][6]}m) | Correct Answer: {dict[key][5]}' )    # Printing of question + answer
            for i in range(4):   # Printing of options 
                print(f'{dict[key][i+1]}')
            questionsIndex += 1  
        
    return questionsIndex 

# This function prints the selected question in the questionPool dict
# The argument of this function is the key of the selected question, its question pool dictionary
def printSelectedQuestion(selectedQuestion,dictionary):
    print('\n---------------------------------------------\n')
    print('\n'+ '\33[32m' +f'Question {selectedQuestion}: ' + '\33[0m' f'{dictionary[str(selectedQuestion)][0]} ({dictionary[str(selectedQuestion)][6]}m) | Correct Answer: {dictionary[str(selectedQuestion)][5]}')
    for i in range(4):   # Printing of options 
        print(f'{dictionary[str(selectedQuestion)][i+1]}')
    
    print('\n---------------------------------------------\n')

# This function will write onto the question_pool.txt given the updated question dictionary
# The argument of this function takes in the updated question pool dict
def writeQuestion(dict): 
    fn = open(questionPoolTxt,'w') # write mode
    for key in dict :                                # for each key in question dict
        for question in range(7):                    # Write out the element of each question except marks
          fn.write(dict[key][question] + '|') 

        fn.write(f'{dict[key][7]}\n') # Writes topic of the question has without '|' and a line feed for new line
    fn.close()

# This function writes onto userid_pswd.txt given the updated dictionary
# The argument of the function takes in the user dictionary
def writeUser(dict):
    fn = open(userID_pwdTxt,'w') # Write mode
    for key in dict:  # For each key in dict
        try: 
            # Writes UserID | Password | Email | Module
            # For admin, only userID | Password
            fn.write(dict[key][0])
            fn.write( '|' + dict[key][1])
            fn.write( '|' + dict[key][2])
            fn.write( '|' + dict[key][3] + '\n')
        except IndexError:
            fn.write('\n')
    fn.close()

# This function writes onto the quiz_setting.txt given the updated quiz setting dictionary
# The argument of the function takes in the quiz setting dictionary
def writeQuizSetting(dict):
    # Writing to quiz_setting file (Updating Quiz tested for each module)
    fn = open(quizSettingTxt,'w') # Write mode
    for key in dict:                                  # for each key in dict
        fn.write(dict[key][0] + '|' + dict[key][1])   # Write settings onto txt file
        fn.write('\n')                                # Add line feed for new line
    fn.close()

#
# ******************************* Main program ***********************************


# Insert clear description to facilitate maintenance of script in the future

import random
import csv
import statistics
import re
import getpass
import time

# Global variabes that contains the pathway to individual text files
questionPoolTxt = './Server folder/question_pool.txt'
quizSettingTxt = './Server folder/quiz_setting.txt'
userID_pwdTxt = './Server folder/userid_pswd.txt'
resultsCsv = './Server folder/quiz_results.csv'
coursesTxt = './Server folder/courses.txt' 

# This function promopts the user and allows them to create a new question and update accordingly to the question_pool.txt    
# The argument of this function takes in the question pool dict
def addQuestion(dict,topic): 
    while True: 
            newQuestionList = []
            optionNumbering = ['a','b','c','d']
            addQuestionStr = '\33[32m' + '\n*** Add Question ***\n' + '\33[0m' + 'Please enter a new Question\n[0] Back\n>>> '
            
            newQuestion = stringValidation(question=addQuestionStr)
            if newQuestion == '0':
                newQuestionList.clear()
                break
            
            newQuestionList.append(newQuestion) # Adds Question to list
            
            # Loop  for options a - d. when user inputs 0, it will break out of loop. 
            # It also ensures that there is no duplicate options
            i = 0 # for indexing
            while True:
                newOption = stringValidation(question=f'\nPlease enter question option {optionNumbering[i]})\n[0] Cancel\n>>> ')
                if newOption == '0':
                    newQuestionList.clear()   # Removes all elements in list
                    break
                
                # Checking of new option with already inputed options and ensure no duplicate
                duplicate = False
                for option in newQuestionList[1:]:
                    for s in optionNumbering:
                        if f'{s}) {newOption}' == option:
                            duplicate = True
                            break

                if duplicate == False:
                    newQuestionList.append(f'{optionNumbering[i]}) {newOption}') # Adds option to List
                    i += 1
                    if i == 4:
                        break 

                else: 
                    print('\n' + '\33[41m' + 'Error! Duplicate option. Please enter another option' + '\33[0m')
                
            if newOption != '0':            # Option == 0 is for cancel selection
                print('\33[32m' + '\n*** NEW QUESTION ***' + '\33[0m')
                for i in newQuestionList:   # Prints new question + options
                    print(i)    
                # listRangeValidation ensures that newOption will only contain a,b,c,d
                newOption = listRangeValidation(list=optionNumbering,question='\nPlease enter the correct option from (a to d)\n>>> ')
                newQuestionList.append(newOption)

                # Checks for amount of marks user wants for the question
                marks = validationRange(start=1,end=5,question='\nPlease enter the amount of marks (1 to 5 marks) for this question\n>>> ')
                newQuestionList.append(marks)

                # Makes sure that topic cannot be named as 'None'
                # Adding of new topic for when user decides to add a new question based on a new topic
                if topic == None:
                    while True:
                        newTopic = stringValidation(question='\nPlease enter the topic for the question\n>>> ')
                        if newTopic == 'None':
                            print('\n' + '\33[41m' + "Error! Cannot name topic as ['None']. Please use another name" + '\33[0m')
                        
                        else: 
                            topic = newTopic
                            break

                newQuestionList.append(topic)

                # Prints updated question with correct answer selected
                print(f'\nNew Question: \n{newQuestionList[0]} ({marks}m) | Correct Option: {newQuestionList[5]} | Topic: {topic}') 
                for i in range(4):   # Prints options
                    print(newQuestionList[i+1])

                chosenOption = validationRange(start=0,end=1,question= '\n' + '\33[41m' + '*** CONFIRMATION : Add new Question? ***' + '\33[0m' + '\n[1] YES \t [0] NO\n >>> ')
                
                if chosenOption == 0:
                    newQuestionList.clear()  # Clears list if user decides not to confirm
                else: 
                    questionStr = ''
                    for i in range(5):      # Loops through from index 0 to the last option, d)
                        questionStr += newQuestionList[i] + ' |'  # Make a str for the new Question in the format : question | options | answer
                    
                    # Adds correct answer and the amount of marks the question is at the end of the string
                    questionStr += newQuestionList[5] + ')|' + str(newQuestionList[6]) + '|' + str(newQuestionList[7])  
 
                    fn = open(questionPoolTxt,'w') # write mode
                    for key in dict :                             # for each key in question dict
                        for question in range(7):                 # Write out the element of each question except topic
                            fn.write(dict[key][question] + '|') 
                        fn.write(f'{dict[key][7]}\n')             # Writes topic of the question has without '|' and start new line
                    
                    fn.write(questionStr)               # Finally, Write the new question onto the file at the end
                    fn.close()
                    input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')
                    break

# This function allows admin to delete questions in question List
# The argument of this function takes in the question pool dict and the topic chosen
def deleteQuestion(dict,topic):
    while True: 
        lastIndex = printQuestions(dict,topic)
        chosenOption = validationRange(start=0, end=lastIndex-1, question='\nEnter the index for Question to delete\n[0]Back\n>>> ') # range is 0 to index of last question
        if chosenOption == 0:
            break
        else: 
            # Store all keys given the topic in a list
            dictKeyList = []
            for key in dict:
                if dict[key][7] == topic:
                    dictKeyList.append(key)

            # Chosen Option = dictKeyList[chosenOption-1]
            # Prints chosen option and confirms for delete question
            printSelectedQuestion(dictKeyList[chosenOption-1],dict)
            confirmDelete = validationRange(start=0, end=1, question='\n' + '\33[41m' + '*** CONFIRMATION : Delete Question? ***' + '\33[0m' + '\n[1] Yes\t [0] No (Back)\n>>> ')
            
            # Deletes question
            if confirmDelete == 1:
                # Deleting of questions
                del dict[dictKeyList[chosenOption-1]]   # This deletes the key which contain the chosen question in the dict
                writeQuestion(dict)    # Updates txt file
                input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')
                
                quizSettingDict = readFile(quizSettingTxt)
                
                # Checking to ensure that num of questions tested <= num of questions in topic

                # Contains all topic with their number of questions tested defined. 
                # e.g. ['Math: 5','Sci: 2','Geography: 3','History: 2']
                topicQuestions = quizSettingDict['2'][1].split(',')
                

                # Checking if whether whole topic is deleted. If topic is gone, update the quiz settings under 
                # Number of Question for each Topic : if the topic was defined thr
                count = 0
                dictKeyList = []
                for key in dict:
                    if dict[key][7] == topic:
                        count += 1
                        dictKeyList.append(key)
                    
                for i, topicTested in enumerate(topicQuestions):
                        # Creates a tmp list that contains topic and num of questions
                        # e.g. ['Math',' 5']
                        tmpList = topicTested.split(':')
                        if tmpList[0] == topic:
                                if int(count) < int(tmpList[1]):
                                    topicQuestions[i] = tmpList[0] + ': ' + str(count)
                                
                                else:
                                    topicQuestions[i] = tmpList[0] + ': ' + tmpList[1]

                # Reformatting
                tmpStr = ''
                for i in range(len(topicQuestions)-1):
                    tmpStr += topicQuestions[i] + ','

                tmpStr += topicQuestions[-1]

                quizSettingDict['2'][1] = tmpStr

                writeQuizSetting(dict=quizSettingDict)
                        
                # if list is empty, means that topic is fully deleted
                if dictKeyList == []:
                    
                    # Upadating of quiz settings for when topic is deleted.
                    # Modules that might potentially contain topic + num of question for topic must be updated accordingly

                    # Updating Num of question for topic setting (delete topic if topic is deleted) code

                    # Contains all topic with their number of questions tested defined. 
                    # e.g. ['Math: 5','Sci: 2','Geography: 3','History: 2']
                    topicQuestions = quizSettingDict['2'][1].split(',')
                    for i, topicTested in enumerate(topicQuestions):
                        # Creates a tmp list that contains topic and num of questions
                        # e.g. ['Math',' 5']
                        tmpList = topicTested.split(':')
                        if tmpList[0] == topic:
                            del topicQuestions[i]
                    
                    # Reformatting
                    tmpStr = ''
                    for i in range(len(topicQuestions)-1):
                        tmpStr += topicQuestions[i] + ','

                    tmpStr += topicQuestions[-1]

                    quizSettingDict['2'][1] = tmpStr
                    
                    # |--------------------------------------------------------|
                    # |Deleting deleted topic assigned to quiz in modules code |
                    # |--------------------------------------------------------|
                    moduleQuizList = []

                    for key in quizSettingDict:
                        # as modules are all stored after key 5
                        if int(key) > 5:       
                            # Appends the list of quizes for each module
                            # e.g. [['Quiz 1:Math:Sci', 'Quiz 2:Math'], ['Quiz 1:Math:Sci', 'Quiz 2:Geography:History'],...]  
                            moduleQuizList.append(quizSettingDict[key][1].split(','))  

                    # Finding of deleted topic in quizes and deleting them
                    for i, quizList in enumerate(moduleQuizList):
                        for s, quiz in enumerate(quizList):
                            # Creates a tmp List that contains the quiz name and the topics assigned to it
                            # e.g. ['Quiz 1', 'Math', 'Sci']
                            tmpList = quiz.split(':')

                            # Finding of deleted topic in quiz
                            for a, topicTested in enumerate(tmpList[1:]):
                                if topicTested == topic:
                                    del tmpList[a+1] # +1 because we did not count in quiz name
                                    break 
                            
                            # Reformatting
                            tmpStr = ''
                            for l in range(len(tmpList)-1):
                                tmpStr += tmpList[l] + ':'
                            tmpStr += tmpList[-1]

                            # Update quizList 
                            quizList[s] = tmpStr 

                    # Reformat again
                    i = 0
                    for key in quizSettingDict:
                        # as modules are all stored after key 5
                        if int(key) > 5:    
                            # Reformatting and updating dictionary
                            quizList = moduleQuizList[i]
                            tmpStr = ''
                            for s in range(len(quizList)-1):
                                tmpStr += quizList[s] + ','
                            tmpStr += quizList[-1]
                            quizSettingDict[key][1] = tmpStr
                            i += 1

                    # update quiz settings
                    writeQuizSetting(dict=quizSettingDict)
                
                break

# This function allows user to navigate on what they want to do for different settings affecting the questions            
def setupQuestion():
    while True:
        # Creats a question pool dict and read file
        questionDict = readFile(questionPoolTxt)
        if questionDict == {}:      # Ensures that question dictionary is not empty
            emptyQuestionPool = True 
        else: 
            emptyQuestionPool = False
        
        topicList = []
        topicMenu = '\n---------------------------------------------\n' + '\33[32m' + '\t\t' + '\33[4m'+ '{ Topic List }' + '\33[0m' + '\n'

        # Store all possible topics from question pool file
        for key in questionDict:
            if questionDict[key][7] not in topicList:
                topicList.append(questionDict[key][7])

        # Prints out all topics stored in question pool file
        for i, topic in enumerate(topicList):
            topicMenu += f'\n[{i+1}] ' + '\33[91m' + '\33[4m' + f'{topic}' + '\33[0m'
        
        if emptyQuestionPool == True:
            topicMenu += '\n' + '\33[41m' + 'Error! Empty Question Pool! Please add a question with a new topic.' + '\33[0m'
        
        topicMenu += '\n\n---------------------------------------------\nPlease Choose a topic according to the index\n[-1] Add a new Question (with new/old topic)\n[0] Back\n>>> '
        
        chosenTopic = validationRange(start=-1,end=len(topicList),question=topicMenu)
        if chosenTopic == 0: # Exits setupQuestion() to go back to main menu
            break
        
        # For when there is no topics or adding of new question with new topic
        elif chosenTopic == -1:
                addQuestion(dict = questionDict, topic = None)
    
        else:
            chosenTopic = topicList[chosenTopic-1] # set the chosen topic as string of the selected topic
    
            while True:
                questionDict = readFile(questionPoolTxt)   # updates dictionary accordingly
                # Check if topic has any more questions left
                counter = 0
                for key in questionDict:
                    if questionDict[key][7] == chosenTopic:
                        counter += 1
                        break
                # If topic no longer has any questions, break out of while true loop and back to choosing of topics again
                if counter == 0:
                    print('\33[41m' + 'Topic is deleted as there are no questions left! Please choose another topic or make a new one' + '\33[0m' + '\n')
                    break

                # formatting of menu prompt for setup question
                setupQuestionMenu = '\n---------------------------------------------\n' + '\33[32m' + '\t ' + '\33[4m'+ '{ Setup Quiz Questions }' + '\33[0m'
                setupQuestionMenu += '\n\nCurrent Topic: ' + '\33[41m' + '\33[4m' +f'{chosenTopic}' + '\33[0m'
                setupQuestionMenu += '\n\n[1] View Question List\n[2] Add Question\n[3] Delete Question\n[4] Edit Question Property\n[0] Back'
                setupQuestionMenu += '\n\n---------------------------------------------\n>>> '

                chosenOption = validationRange(start=0,end=4,question=setupQuestionMenu)
                if chosenOption == 0:           # Exits setupQuestion() to go back to main menu
                    break

                elif chosenOption == 1:  # Viewing of question List
                    printQuestions(dict = questionDict,topic=chosenTopic)
                        
                elif chosenOption == 2:  # Addition of questions, do not need any questions in question pool
                    addQuestion(dict = questionDict,topic=chosenTopic)
                
                elif chosenOption == 3:  # Delete Questions
                    deleteQuestion(dict = questionDict,topic=chosenTopic)
            
                elif chosenOption == 4:  # Editing of question properties
                    editQuestionMenu(dict = questionDict,topic=chosenTopic)


# This function allows admin to edit question titles of the selected question
# The argument of this function takes in the selected question and the question pool dict
def editQuestionTitle(chosenOption,dict):
    newQuestion = stringValidation(question=f'\nOriginal Question Title: {dict[str(chosenOption)][0]}\nEnter new Question Title\n>>> ')

    # Below Prints the updated Question 
    print(f'\nQuestion {chosenOption}. {newQuestion}' + '\33[41m' + '(New!)' + '\33[0m' + f'({dict[str(chosenOption)][6]}m)| Correct Answer: {dict[str(chosenOption)][5]}')    
    for i in range(4):   # Printing of options 
        print(f'{dict[str(chosenOption)][i+1]}')
    # Confirms to change question

    checkOption = validationRange(start=0,end=1,question='\n' + '\33[41m' + '*** CONFIRMATION : change to new edited question? ***'+ '\33[0m' +'\n\n[1] YES \t [0] NO (back)\n>>> ')
    if checkOption == 1: 
        dict[str(chosenOption)][0] = newQuestion + ' '  # Changes to new question in question dict
        writeQuestion(dict)                             # Updates txt file
        input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')

# This function allows admin to edit and change the options
# It also allows the admin to change the correct answer (optional)
# The argument of this function takes in the selected question and the question pool dict
def editOption(chosenOption,dict):
    optionNumbering = ['a','b','c','d','0']
    checkOption = listRangeValidation(list=optionNumbering,question=f'\n{dict[str(chosenOption)][1:5]}\nPlease choose an option to edit\n[0] Cancel\n>>> ')
    
    # if user never presses 0 for cancel
    if checkOption != '0':
        # finds index of checkOption in optionNumbering list + store old value of option in oldOption
        indexOfOption = optionNumbering.index(checkOption) + 1  # Gives the index of the option selected and +1 as index 0 in list in dict contains question
        oldOption = dict[str(chosenOption)][indexOfOption]      # Stores old value of option selected
        correctOption = dict[str(chosenOption)][5]              # Stores the correct option's numbering such as a) to d)   
        oldCorrectOption = correctOption                        # Stores old correct option
        
        # Ask to enter new option given the old option
        newOption = stringValidation(question=f'\nOriginal option: {oldOption}\nEnter new option\n>>> ')
        dict[str(chosenOption)][indexOfOption] = checkOption + ') ' + newOption + ' (New!)' # Sets selected option to new option user has inputed
        
        checkOption = validationRange(start=0,end=1,question='\33[41m' +'\nChange correct answer?' + '\33[0m' + '\n[1] YES \t[0] NO\n>>> ')
        
        # if user chooses to change correct answer
        if checkOption == 1:
            # Prints out updated question and asks for new correct answer between a-d
            checkOption = listRangeValidation(list=optionNumbering,question=f'\nQuestion:{dict[str(chosenOption)][0]}\n\nOptions:{dict[str(chosenOption)][1:5]}\n\nOriginal Correct Answer: {dict[str(chosenOption)][5]}\n\nChoose a new correct answer\n[0] Cancel\n>>> ')
            #If user never input 0 for cancel
            if checkOption != '0':
                correctOption = checkOption + ')'  # Adds a ) to the new correctOption str
                dict[str(chosenOption)][5] = correctOption + '\33[41m' + '(New!)' + '\33[0m'
        
        #printing of question with new option
        printSelectedQuestion(selectedQuestion=chosenOption,dictionary=dict)
        
        # Confirm if user wants to change option
        checkOption = validationRange(start=0,end=1,question='\n' + '\33[41m' + '*** CONFIRMATION : save new edited option? ***' + '\33[0m' '\n\n[1] YES \t [0] NO (back)\n>>> ')
        # If user confirms to change option
        if checkOption == 1: 
            # Remove the (New!) added previously OR Take in the intialized correctOption that remained unchanged if user did not change correct option
            dict[str(chosenOption)][5] = correctOption 
            # Remove the (New!) added previously
            dict[str(chosenOption)][indexOfOption] = optionNumbering[indexOfOption - 1] + ') ' + newOption + ' '
            writeQuestion(dict)
            input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')
        # User presses 0 at end to cancel all
        else: 
            # Reset to old option if user presses 0 to cancel changing of options
            dict[str(chosenOption)][indexOfOption] = oldOption # Changes back to old option
            dict[str(chosenOption)][5] = oldCorrectOption # Changes back to old answer


# This function changes the mark allocation to the selected question from 1 to 5
# The argument of this function takes in the selected question and the question pool dict
def changeMarks(chosenOption,dict): 
    newMarks = validationRange(start=0,end=5,question=f'Old Marks: {dict[str(chosenOption)][6]}m\n\nPlease Enter new marks from 1-5\n[0] Cancel (Back)\n>>> ')
    
    if newMarks != 0:
        oldMarks = dict[str(chosenOption)][6]                         # Stores old marks
        dict[str(chosenOption)][6] = str(newMarks) + '\33[41m' + '[New!]' + '\33[0m' # formatting of new Marks for printing
        
        # Prints updated question with new marks
        printSelectedQuestion(selectedQuestion=chosenOption,dictionary=dict)

        # Resetting formatting for newMarks in dict
        dict[str(chosenOption)][6] = str(newMarks)

        # Confirmation for changing of marks
        checkOption = validationRange(start=0,end=1,question='\n' + '\33[41m' + '*** CONFIRMATION : Change to new marks? ***'+'\33[0m' '\n\n[1] YES \t [0] NO (Back)\n>>> ')

        # If user input 1, to confirm changing of marks
        if checkOption != 0:
            writeQuestion(dict)        # Update to text file
            input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')
        # For user input 0, cancel of marks
        else :
            # Reset back to old marks
            dict[str(chosenOption)][6] = oldMarks

# This function randomizes the options in the question specified by the user
# The argument of this function takes in the selected question and the question pool dict
def randomOption(chosenOption,dict): 
    checkOption = validationRange(start=0,end=1,question='Randomise option arrangement?\n\n[1] YES \t [0] NO (Back)\n>>> ')
    # user presses 1 for confirmation to randomize option arrangement
    if checkOption == 1:
        oldOptionList = dict[str(chosenOption)][1:6]  # Set oldOptionList a list with all options from a to d + answer
        optionList = dict[str(chosenOption)][1:5]     # set optionList as a list with all options from a to d

        optionStrList = []
        correctOption = ''

        # For each option among the 4 options form a) to d), find the correct answer and store in a str
        for option in optionList:                 
            if option.find(dict[str(chosenOption)][5]) != -1:
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

        # Ensures that correct answer will be changed
        while optionList[index].find(correctOption) != -1:
            random.shuffle(optionList)
        
        # Removes the optionNumbering for each option and replace with a) to d)
        for i , numbering in enumerate(['a','b','c','d']):
            optionStrList = optionList[i].split()        # append each word into a list
            optionStrList.pop(0)                         # Removes a) to d) it was initialized with
            newOption = numbering + ') '                 # Adds a) to d) respectively to match the order
            for char in optionStrList:
                newOption += char + ' '                  # Format the option as a) option....
            dict[str(chosenOption)][i+1] = newOption     # update new option into dict

        # Find the correct answer's option Numbering using plain text answer
        for option in dict[str(chosenOption)][1:5]:      # For each option in dict
            if option.find(correctOption) != -1:         # Find the correctOption with just the substring of the plain text option without its numbering a) to d)
                dict[str(chosenOption)][5] = option[0:2] # Adds the appropriate option numbering, a) to d) to inidicate the new correct answer

        #Print question with randomized options
        print('\n*** Questions with new randomized options ***\n')
        printSelectedQuestion(selectedQuestion=chosenOption,dictionary=dict)

        checkOption = validationRange(start=0,end=1,question='\n' + '\33[41m'+'*** CONFIRMATION *** : Accept new question?'+'\33[0m' +'\n\n[1] YES \t [0] NO (Back)\n>>> ')
        
        # If user confirms new question with randomized options
        if checkOption == 1:
            writeQuestion(dict)
            input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')
            
        # If user cancels, assign options + answer back to old value
        else :
            # Assign options back to old values
            for i in range(4):   
                dict[str(chosenOption)][i+1] = oldOptionList[i]

            dict[str(chosenOption)][5] = oldOptionList[4]   # Assign answer back to old value     

# This function allows user to edit question properties
# The argument of this function takes in the question pool dict
def editQuestionMenu(dict,topic):
    while True:
        lastIndex = printQuestions(dict,topic)
        # range is 0 to index of last question
        checkOption = validationRange(start=0, end=lastIndex-1, question=f'\nEnter the index for Question to edit (1 to {lastIndex-1})\n[0]Back\n>>> ') 
        if checkOption == 0: 
            break
        # Creates a list that contains all the questions keys given the topic
        dictKeyList = []
        for key in dict:
            if dict[key][7] == topic:
                dictKeyList.append(key)

        chosenOption = dictKeyList[checkOption-1]  # Sets correct chosen option given the topic
        # Prints the selected question with its options 
        while True:

            printSelectedQuestion(selectedQuestion=chosenOption , dictionary = dict)

            checkOption = validationRange(start=0,end=4,question='\n[1] Edit Question Title\n[2] Edit Option\n[3] Change Marks for Question\n[4] Randomize Options\n[0] Back\n>>> ')
            
            # Editing Question (title)
            if checkOption == 1:  
                editQuestionTitle(chosenOption,dict)

            # Editing Question options
            elif checkOption == 2:  
                editOption(chosenOption,dict)

            # Change marks for question
            elif checkOption == 3:     
                changeMarks(chosenOption,dict)

            # Randomise option arrangement
            elif checkOption == 4:  
                randomOption(chosenOption,dict)
            
            elif checkOption == 0: # Exits loop
                break

# This function asks for user input for selected quiz setting and updates it to quiz_setting.txt
# The argument of this function takes in the quizSetting Dict, its selected quiz setting (key),its question and an optional string for additional formatting
def writeSetting(dict,key,checkQuestion): 
    # Validation for input for it to be an integer and for number of questions for quiz
    while True:
        counter = 0
        
        # Makes a dict from question pool that contains all questions
        questionDict = readFile(questionPoolTxt)
        
        # Printing of topics as question
        topicList = []
        topicMenu = '\n---------------------------------------------\n' + '\33[32m' + '\t\t' + '\33[4m'+ '{ Topic List }' + '\33[0m' + '\n'

        # Store all possible topics from question pool file
        for keys in questionDict:
            if questionDict[keys][7] not in topicList:
                topicList.append(questionDict[keys][7])

        # Prints out all topics stored in question pool file
        for i, topic in enumerate(topicList):
            topicMenu += f'\n[{i+1}] ' + '\33[91m' + '\33[4m' + f'{topic}' + '\33[0m'

        # For when editing setting for number of question tested.
        if key == '2':
            
            topicMenu += '\n\n---------------------------------------------\nPlease Choose a topic according to the index\n[0] Back\n>>> '
            chosenTopic = validationRange(start=0,end=len(topicList),question=topicMenu)
            
            if chosenTopic == 0: # Exits loop for if user decides to quiz
                checkInput = 0   # for exiting
                break
            # User chooses a topic
            else:
                chosenTopic = topicList[chosenTopic-1] # set the chosen topic as string of the selected topic
                with open(questionPoolTxt,'r') as fn:
                    for line in fn:
                        line = line.strip()
                        tempList = line.split('|')
                        # Checks topic selected
                        if tempList[7] == chosenTopic:
                            counter += 1  # Counts the number of question in question pool
                
                NumQuestion = f'\nNumber of questions in Question Pool: {counter}'
                
                # Makes a list to store all quizes with its respective number of questions tested.
                # e.g. ['Math: 5', 'Sci: 2', 'Geography: 3', 'History: 2',...]
                quizList = dict['2'][1].split(',')
                
                # To check if the number of questions for the selected topic is defined
                quizNumQuestion = False

                for i in quizList:
                    # Makes a temporary list to store the quiz name and its respective number of questions tested
                    # e.g. ['Math', ' 5']
                    tmpList = i.split(':')
                    if tmpList[0] == chosenTopic:
                        currentQuestionSetting = tmpList[1]
                        quizNumQuestion = True

                # for when number of questions for chosen topic is not yet defined
                if quizNumQuestion == False:
                    currentQuestionSetting = 'Not Set'

                checkQuestion = f'\nCurrent Question setting : {currentQuestionSetting}\n\nPlease Enter new number of questions\n[0] Cancel (Back)\n>>> '
                
                # Ensures that user input will be within total number of questions of a selected topic
                checkNum = validationRange(start=0,end=counter,question=NumQuestion+checkQuestion)
                if checkNum == 0:
                    checkInput = 0
                    break

                checkInput = ''
                if dict['2'][1] == 'empty':
                    for i in range(len(topicList)-1):
                        questionNum = 'empty'
                        # Sets to inputed num 
                        if topicList[i] == chosenTopic:
                            questionNum = checkNum
                        checkInput += topicList[i] + f': {questionNum}' + ','

                    # Adding of last topic in str
                    checkInput += topicList[-1] + f': empty'
                
                else:
                    # Seperates the different topics e.g. [topic: num of attempts, topic: num of attempts, ...]
                    topicWithNumQuestionList = dict['2'][1].split(',')
                    topicInSetting = False 
                    for i , topic in enumerate(topicWithNumQuestionList):
                        # if found chosen topic, replace the value of num of attempts
                        if topic.find(chosenTopic) != -1:
                            tmpList = topic.split(':')
                            # Setting of new num of question for the topic
                            topicWithNumQuestionList[i] = f'{tmpList[0]}: {checkNum}'
                            topicInSetting = True
                    
                    # if topic is not found in the setting, append it to the list
                    if topicInSetting == False:
                        topicWithNumQuestionList.append(f'{chosenTopic}: {checkNum}')


                    # Adding of all topics with its respective num of questions in a str
                    for i in range(len(topicWithNumQuestionList)-1):
                        checkInput += topicWithNumQuestionList[i] + ','
                    
                    # Adding of last topic in str
                    checkInput += topicWithNumQuestionList[-1]
            break

        # For when editing setting for randomize option
        elif key == '4':
            checkInput = validationRange(start=0,end=2,question=checkQuestion)
            if checkInput == 0:
                break

            elif checkInput == 1:
                checkInput = 'Yes'
                break

            elif checkInput == 2:
                checkInput = 'No'
                break
        
        # For keys 1 and 3
        try:

            # Allows for time & attempts to be set as unlimited 
            checkInput = validationRange(start=0,end=2,question=checkQuestion)

            # When admin chooses unlimited
            if checkInput == 1:
                checkInput = 'Unlimited'
                break

            # User specifying own setting
            elif checkInput == 2:
                
                if key == '1':
                    questionAsked = '\nPlease Enter new time (in minutes). Anything entered >= 999 = Unlimited\n[0] Cancel (Back)\n>>> '
                elif key =='3':
                    questionAsked = '\nPlease Enter new number of attempts. Anything entered >= 999 = Unlimited\n[0] Cancel (Back)\n>>> '

                checkInput = int(input(questionAsked)) # try to int a string

                if checkInput >= 0:
                    if checkInput >= 999:  # For if user enter more or equal than 999
                        checkInput = 'Unlimited'
                    
                    break  # For normal inputs if they are >= 0
                
                elif checkInput < 0:
                    print('\33[41m'+f'error! Please enter an integer greater than or equal to 0'+'\33[0m' + '\n')
            
        # if user key in a string, reject it and prompt question again
        except ValueError:
            print('\33[41m' + 'Invalid char entered! Please re-enter an integer number!' + '\33[0m' + '\n')
        except EOFError:            # error for when user enters ctrl + z
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
        except KeyboardInterrupt:   # Error for when user enters ctrl + c
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')


    # Convert int to str if checkInput is int
    checkOption = str(checkInput)
    # Ensure that user does not cancel. Canceling will exit out of function
    if checkOption != '0':
        # Will update the settings dictionary according to the key given in the parameter
        dict[key][1] = checkOption
        
        # Writing to quiz_setting file
        writeQuizSetting(dict=dict)
        input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')

# This function allows the user to add a quiz for a selected module.
# It takes in moduleQuizes as its argument, a list that contains all the quizes that the modules 
# contains e.g. ['Quiz 1:Sci:Math', 'Quiz 2:Sci', ...] 
# It will return a string with the newly added quiz inside on it 
def addQuiz(moduleQuizes):
    while True:
        addQuizMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t' + '\33[4m' + '{ Adding of New Quiz }' + '\33[0m' + '\n\n'
        addQuizMenu += '\33[41m' + '\33[4m' + 'Current Quizes' + '\33[0m' + '\n'
        
        quizNameList = []
        for i, quiz in enumerate(moduleQuizes):
            quiz_topics = quiz.split(':')
            addQuizMenu += f'\n{i+1}. Quiz Name: {quiz_topics[0]}\tTopics: {quiz_topics[1:]}'
            quizNameList.append(quiz_topics[0])

        # for when no quizes are defined
        if moduleQuizes == []:
            addQuizMenu += '\n' + '\33[41m' + 'No quizes defined in module' + '\33[0m'

        addQuizMenu += '\n\n' + '\33[32m' + '\33[4m' + 'Please Enter New Quiz Name' + '\33[0m' + '\n[0] Cancel (Back)\n>>> '
        newQuizName = stringValidation(question=addQuizMenu)
        if newQuizName == '0':
            break
        
        if newQuizName in quizNameList:
            print('\n' + '\33[41m' + 'Error! There is already a existing quiz with the same name! Please enter a different Quiz Name' +'\33[0m' +'\n' )
        
        else:
            checkInput = validationRange(start=0,end=1,question= '\n' + '\33[41m' + f'*** CONFIRMATION : Add new Quiz | {newQuizName} | ? ***' + '\33[0m' + '\n[1] YES \t [0] NO\n >>> ')
            # for Quitting
            if checkInput == 0:
                break
            
            # Converting elements in list into string and return it
            moduleQuizes.append(newQuizName +':None')

            checkInput = ''
            for i in range(len(moduleQuizes)-1):
                checkInput += moduleQuizes[i] + ','
            
            checkInput += moduleQuizes[-1]
            
            return checkInput

# This function allows admin to delete a quiz of a selected module
# The function takes in moduleQuizes as the argument.
# moduleQuizes is a list that contains all the quizes that the modules contains
# e.g. ['Quiz 1:Sci:Math', 'Quiz 2:Sci', ...]
# The function returns the newly changed value of a module's quiz as a string
# If user quits, the value returned will be None
def deleteQuiz(moduleQuizes):
    while True:
        deleteQuizMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t' + '\33[4m' + '{ Deleting Quiz }' + '\33[0m' + '\n\n'
        deleteQuizMenu += '\33[41m' + '\33[4m' + 'Current Quizes' + '\33[0m' + '\n'
        
        quizNameList = []
        for i, quiz in enumerate(moduleQuizes):
            quiz_topics = quiz.split(':')
            deleteQuizMenu += f'\n{i+1}. Quiz Name: {quiz_topics[0]}\tTopics: {quiz_topics[1:]}'
            quizNameList.append(quiz_topics[0])

        deleteQuizMenu += '\n\n' + '\33[32m' + '\33[4m' + 'Please choose a quiz to delete according to its index' + '\33[0m' + '\n[0] Cancel (Back)\n>>> '
        chosenQuiz = validationRange(start=0,end=len(moduleQuizes),question=deleteQuizMenu)
        # for quitting
        if chosenQuiz == 0:
            break
        
        checkInput = validationRange(start=0,end=1,question= '\n' + '\33[41m' + f'*** CONFIRMATION : Delete Quiz | {moduleQuizes[chosenQuiz-1]} | ? ***' + '\33[0m' + '\n[1] YES \t [0] NO\n >>> ')
        # for Quitting
        if checkInput == 0:
            break
        
        del moduleQuizes[chosenQuiz-1] # deleting of chosen quiz in the list
        checkInput = ''

        if moduleQuizes != []:
            # for when there is more than 1 quiz left in the module after deleting
            if len(moduleQuizes) > 1:
                for i in range(len(moduleQuizes)-1):
                    checkInput += moduleQuizes[i] + ','
                
                    checkInput += moduleQuizes[-1]
            # for when there is only 1 quiz left in the module after deleting
            else:
                checkInput = moduleQuizes[0]

        # for when last quiz is deleted
        else: 
            checkInput = 'None'

        return checkInput
        
# This function allows the user to add and remove a topic of a given quiz in a module
# The function's argument are moduleQuizes, a list that contains all the quizes that the modules contains
# e.g. ['Quiz 1:Sci:Math', 'Quiz 2:Sci', ...] , chosenQuiz (index of quiz chosen in moduleQuizes)
# and the module that it is currently editing
# The function returns the newly changed value of a module's quiz as a string
# If user quits, the value returned will be None
def editQuizTopic(moduleQuizes,chosenQuiz,chosenmodule):
    while True:
        # Contains the chosen quiz and its topics e.g. [quiz1,topic,topic,...]
        chosenQuiz_Topic = moduleQuizes[chosenQuiz-1].split(':')

        moduleSettingMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t   ' + '\33[4m' + '{ Module Quiz Settings }' + '\33[0m' + '\n\n'
        moduleSettingMenu += 'Current Module: ' + '\33[91m' + '\33[4m' + f'{chosenmodule}' + '\33[0m' + '\n'
        moduleSettingMenu += f'Chosen Module Quiz: {chosenQuiz_Topic[0]}\n'
        moduleSettingMenu += '\nCurrent Topics in Quiz: ' + '\33[32m' + f'{chosenQuiz_Topic[1:]}' + '\33[0m'
        moduleSettingMenu += '\n[1] Add Topic\n[2] Remove Topic\n[3] Change Quiz Name\n[0] Cancel (Back)\n---------------------------------------------\n>>> '
        
        checkInput = validationRange(start=0,end=3,question=moduleSettingMenu)
        if checkInput == 0:
            break

        # Adding of topics to quiz
        elif checkInput == 1:
            # Makes a dict from question pool that contains all questions
            questionDict = readFile(questionPoolTxt)
            
            # Printing of topics as question
            topicList = []
            topicMenu = '\n---------------------------------------------\n' + '\33[32m' + '\t\t' + '\33[4m'+ '{ Topic List }' + '\33[0m' + '\n'

            # Store all possible topics from question pool file
            for keys in questionDict:
                if questionDict[keys][7] not in topicList:
                    topicList.append(questionDict[keys][7])

            # Prints out all topics stored in question pool file
            for i, topic in enumerate(topicList):
                topicMenu += f'\n[{i+1}] ' + '\33[91m' + '\33[4m' + f'{topic}' + '\33[0m'

            topicMenu += '\n\n---------------------------------------------\nPlease Choose a topic to add according to its index\n[0] Back\n>>> '
            checkInput = validationRange(start=0,end=len(topicList),question=topicMenu)
            
            # User does not quit
            if checkInput != 0:

                chosenTopic = topicList[checkInput-1] # set the chosen topic as string of the selected topic

                if chosenTopic in chosenQuiz_Topic[1:]:  
                    print('\33[41m' + 'Error! Topic has already been selected' + '\33[0m'+'\n')
                
                # if chosen topic is not in quiz, add it
                else: 
                    # Adds the new topic into the quiz 
                    if chosenQuiz_Topic[1] == 'None':
                        chosenQuiz_Topic[1] = chosenTopic
                    else:                       
                        chosenQuiz_Topic.append(chosenTopic)

                    tmpStr = ''
                    for i in range(len(chosenQuiz_Topic)-1):
                        tmpStr += chosenQuiz_Topic[i] + ':'

                    tmpStr += chosenQuiz_Topic[-1]                        
                    # Updating new topics in list (reformatting back and updating dict)
                    moduleQuizes[chosenQuiz-1] = tmpStr

                    checkInput = ''
                    for i in range(len(moduleQuizes)-1):
                        checkInput += moduleQuizes[i] + ','
                    
                    checkInput += moduleQuizes[-1]
                    
                    return checkInput


        # Removing of topics from setting
        elif checkInput == 2:
            
            # Topics in current setting in a list
            settingTopicList = chosenQuiz_Topic[1:]

            # Ensures that setting is not empty before deleting
            if settingTopicList == ['None']:
                print('\33[41m' + 'Error! No Topics being tested! Please add a topic before removing topic!' + '\33[0m'+'\n')

            else:
                settingTopicMenu = '\n---------------------------------------------\n' + '\33[32m' + '\t' + '\33[4m'+ '{ Current Topics }' + '\33[0m' + '\n'
                
                for i, topic in enumerate(settingTopicList):
                    settingTopicMenu += f'\n[{i+1}] ' + '\33[91m' + '\33[4m' + f'{topic}' + '\33[0m'

                settingTopicMenu += '\n\n---------------------------------------------\nPlease Choose a topic to remove according to its index\n[0] Back\n>>> '

                checkInput = validationRange(start=0,end=len(settingTopicList),question=settingTopicMenu)

                # user does not quit
                if checkInput != 0:

                    del chosenQuiz_Topic[checkInput] # Deletes chosen topic
                    if len(chosenQuiz_Topic) == 1:
                        chosenQuiz_Topic.append('None')

                    tmpStr = ''
                    # Loops through from start of list till index -2
                    for i in range(len(chosenQuiz_Topic)-1):
                        tmpStr += chosenQuiz_Topic[i] + ':' # Adds all current topic in setting until second last
                    
                    tmpStr += chosenQuiz_Topic[-1] # Adds the last topic of the setting without any commas after it
                    
                    # Updating new topics in list (reformatting back and updating dict)
                    moduleQuizes[chosenQuiz-1] = tmpStr
                    checkInput = ''
                    for i in range(len(moduleQuizes)-1):
                        checkInput += moduleQuizes[i] + ','
                    
                    checkInput += moduleQuizes[-1]
                    
                    return checkInput

        # Editing Quiz Name
        elif checkInput == 3: 
            moduleSettingMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t ' + '\33[4m' + '{ Change Quit Name }' + '\33[0m' + '\n\n'
            moduleSettingMenu += f'\nCurrent Quiz Name: {chosenQuiz_Topic[0]}\n'
            moduleSettingMenu += f'Current Topics in Quiz: {chosenQuiz_Topic[1:]}'
            moduleSettingMenu += '\n\n' + '\33[91m' + '\33[4m'  + 'Please enter new Quiz Name' + '\33[0m'
            moduleSettingMenu += '\n[0] Cancel (Back)\n---------------------------------------------\n>>> '

            newQuizName = stringValidation(question=moduleSettingMenu)

            # if user does not quit
            if newQuizName != '0':
                # Confirms with user
                checkInput = validationRange(start=0,end=1,question= '\n' + '\33[41m' + f'*** CONFIRMATION : Change Quiz Name to | {newQuizName} | ? ***' + '\33[0m' + '\n[1] YES \t [0] NO\n >>> ')

                if checkInput == 1:
                    # Store old quiz name. This will be used for later to update the quiz name in the setting files
                    oldQuizName = chosenmodule + ': ' + chosenQuiz_Topic[0]

                    # Setting of new quiz name
                    chosenQuiz_Topic[0] = newQuizName 
                    
                    # creates a tmp quiz setting dictionary
                    tmpQuizSettingDict = readFile(quizSettingTxt)
                    # Creates a list that contains all the quiz tested for each module
                    # e.g. ['Fundamentals of Networking: Quiz 2', 'PSEC: Quiz 1', ...]
                    quizTestedList = tmpQuizSettingDict['5'][1].split(',')
                    
                    # Changing list value to new one 
                    for i , quiz in enumerate(quizTestedList):
                        if oldQuizName in quiz:
                            quizTestedList[i] = chosenmodule + ': ' + newQuizName
                    
                    # Reformatting back
                    tmpStr = ''
                    for i in range(len(quizTestedList)-1):
                        tmpStr += quizTestedList[i] + ','

                    tmpStr += quizTestedList[-1]
                    tmpQuizSettingDict['5'][1] = tmpStr
                    
                    # updates quiz_setting.txt file and changing the old quiz name if it is in the 
                    # (Quiz tested for each Module:) to the new quiz name
                    fn = open(quizSettingTxt,'w')           # Write mode
                    for key in tmpQuizSettingDict:          # for each key in dict
                        # Write settings onto txt file
                        fn.write(tmpQuizSettingDict[key][0] + '|' + tmpQuizSettingDict[key][1])   
                        fn.write('\n')                      # Add line feed for new line
                    fn.close()

                    # for reformatting back under the module
                    tmpStr = ''
                    # Loops through from start of list till index -2
                    for i in range(len(chosenQuiz_Topic)-1):
                        tmpStr += chosenQuiz_Topic[i] + ':' # Adds all current topic in setting until second last
                    
                    tmpStr += chosenQuiz_Topic[-1] # Adds the last topic of the setting without any commas after it
                    
                    # Updating new topics in list (reformatting back and updating dict)
                    moduleQuizes[chosenQuiz-1] = tmpStr
                    checkInput = ''
                    for i in range(len(moduleQuizes)-1):
                        checkInput += moduleQuizes[i] + ','
                    
                    checkInput += moduleQuizes[-1]
                    
                    return checkInput


# This function does the configuration for the modules stored in the quiz_setting.txt after line 4
# The function allows to add a new Module, delete Module. It will also allow for editing of chosen module's quiz(s) 
# and does so by directing to the appropriate functions: editQuizTopic(), addQuiz(), deleteQuiz()
# The function takes in the quiz setting dictionary
def moduleSetting(dict):
    while True:
        delmodule = False   # used for the ending when checking to edit chosen module & write to file or just write to file updated dict
        moduleSettingMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t      ' + '\33[4m' + '{ module Setting }' + '\33[0m' + '\n\n'
        moduleSettingMenu += '\33[41m' + '\33[4m' + f'Choose a module to edit' + '\33[0m' + '\n\n'
        
        # Creates a list that contains all modules based on what is already in quiz_setting.txt
        moduleList = []
        # Prints out all modules available 
        i = 1
        for key in dict:
            if int(key) > 5:
                moduleSettingMenu += f'{i}. ' + '\33[91m' + '\33[4m' f'{dict[key][0].strip()}' + '\33[0m' + '\n' 
                moduleList.append(dict[key][0])
                i += 1
        
        if moduleList == []:
            moduleSettingMenu += '\33[41m' + 'No Modules Defined' + '\33[0m' + '\n'

        # There will be no modules if len of setting dict == 4, modules are stored right below after key 4 of setting dict
        if len(dict) == 4: 
            moduleSettingMenu += '\33[41m' + 'No current modules defined! Please add a module' + '\33[0m'

        moduleSettingMenu += '\n---------------------------------------------\n[-1] Add a module\n[-2] Delete a module\n[0] Cancel (Back)\n>>> '

        checkInput = validationRange(start=-2,end=len(moduleList),question=moduleSettingMenu)

        # Quitting from function
        if checkInput == 0:
            break
        
        # Adding of new module
        elif checkInput == -1:
            # set module string as a new key
            moduleKey = str(len(dict) + 1)
            
            newmoduleMenu = '\n' + '\33[32m' + '\33[4m' + 'Adding of new module' + '\33[0m' + '\n[0] Cancel (Back)\n>>> '
            newmodule = stringValidation(question=newmoduleMenu)
            
            # newmodule cannot be saved as none as it will mess up data in courses.txt
            if newmodule != '0' and newmodule not in moduleList and newmodule != 'None':
                checkInput = validationRange(start=0,end=1,question= '\n' + '\33[41m' + f'*** CONFIRMATION : Add new module | {newmodule} | ? ***' + '\33[0m' + '\n[1] YES \t [0] NO\n >>> ')
                
                if checkInput != 0:
                    dict[moduleKey] = [None,None]   # Creates a empty list
                    dict[moduleKey][0] = newmodule  # New Topic
                    checkInput = 'None'             # Topics for module

            else: 
                checkInput = 0
                # If user decides to add a module but a module already exists.
                if newmodule in moduleList:
                    print('\33[41m' + 'Error! module already exists!' + '\33[0m'+'\n')
                
                elif newmodule == 'None':
                    print('\33[41m' + "Please choose another name. Cannot Name Module as ['None']" + '\33[0m'+'\n')

        # Deleting of modules
        elif checkInput == -2:
            # Ensure that there is modules before deleting
            if len(moduleList) == 0:
                print('\33[41m' + 'Error! There is no modules! Please add a module before deleting them' + '\33[0m'+'\n')
                checkInput = 0  # For quitting loop

            else: 
                newmoduleMenu = '\n' + '\33[32m' + '\33[4m' + 'Delete module according to their Index' + '\33[0m' + '\n'
                
                # Prints out all modules available 
                i = 1
                for key in dict:
                    if int(key) > 5:
                        newmoduleMenu += f'{i}. ' + '\33[91m' + '\33[4m' f'{dict[key][0].strip()}' + '\33[0m' + '\n' 
                        moduleList.append(dict[key][0])
                        i += 1
                newmoduleMenu += '\n[0] Cancel (Back)\n>>> '
                chosenOption = validationRange(start=0,end=len(moduleList),question=newmoduleMenu)
                
                # user chooses a module and does not quit
                if chosenOption != 0:
                    checkInput = validationRange(start=0,end=1,question= '\n' + '\33[41m' + f'*** CONFIRMATION : Delete module ? ***' + '\33[0m' + '\n[1] YES \t [0] NO\n >>> ')

                    # User does not quit and confirms to delete module
                    if checkInput != 0:
                        chosenmodule = moduleList[chosenOption-1]  # Setting of chosen module
                        for key in dict:
                            # Finds the key in the dict that contains the module name and delete the key
                            if dict[key][0] == chosenmodule:
                                del dict[key]
                                break
                        
                        # Updating and deleting the module under Quiz tested for each Module:

                        # creates a list of all quiz tested for each module
                        # e.g. ['PSEC: Quiz 2','Fundamentals of Networking: Quiz 1']
                        quizTestedList = dict['5'][1].split(',') 

                        for i, quiz in enumerate(quizTestedList):
                            # Creates a tmp list that has module name and the quiz tested
                            # e.g. ['PSEC',' Quiz 2']
                            tmpList = quiz.split(':')
                            if tmpList[0] == chosenmodule:
                                del quizTestedList[i] # Deletes the module from quizTested List
                                break

                        # Reformatting 
                        tmpStr = ''
                        for i in range(len(quizTestedList)-1):
                            tmpStr += quizTestedList[i] + ','                    

                        tmpStr += quizTestedList[-1]
                        
                        # Updating Dictionary
                        dict['5'][1] = tmpStr
                        delmodule = True
                
                else:
                    checkInput = 0  # For quitting and preventing of writing to file
                        

        # Editting of chosen module (view quizes tested for each module and its subsequent topics)
        else:
            chosenmodule = moduleList[checkInput-1]  # Setting of chosen module
            for key in dict:
                # Finds the key in the dict that contains the module name
                if dict[key][0] == chosenmodule:
                    moduleKey = key

            moduleSettingMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t   ' + '\33[4m' + '{ Module Quiz Settings }' + '\33[0m' + '\n\n'
            moduleSettingMenu += 'Current Module: ' + '\33[91m' + f'{chosenmodule}' + '\33[0m' + '\n\n' 
            
            
            # a list that contains all the quizes that the modules contains
            # e.g. ['Quiz 1:Sci:Math', 'Quiz 2:Sci', ...]
            moduleQuizes = dict[moduleKey][1].split(',')
            
            if moduleQuizes != ['None']:
                for i, quiz in enumerate(moduleQuizes):
                    # Contains the quiz with its topic associated with it e.g. [quiz1,topic,topic,...]
                    quizTopicList = quiz.split(':')
                    moduleSettingMenu += f'{i+1}. Quiz Name: {quizTopicList[0]}\t\t' + '\33[91m' + f'Topics: {quizTopicList[1:]}' + '\33[0m' + '\n'

            else: 
                # Resets the list for the chosenQuiz validation later such that user is forced to only be able to add quiz
                moduleQuizes.clear() 
                moduleSettingMenu += '\33[41m' + 'No Quizes Defined in Module yet! Please add a Quiz' + '\33[0m'+'\n'

            moduleSettingMenu += '\n' +'\33[41m' + '\33[4m' + 'Edit a quiz according to its index' + '\33[0m' 
            moduleSettingMenu += '\n[-1] Add Quiz\n[-2] Delete Quiz\n[0] Cancel (Back)'
            moduleSettingMenu += '\n---------------------------------------------\n>>> '
            
            # Edit quiz topics (add/delete topic from quiz)
            while True:
                chosenQuiz = validationRange(start=-2,end=len(moduleQuizes),question=moduleSettingMenu)
                if chosenQuiz == 0:
                    checkInput = 0
                    break
                # Adding of quiz
                elif chosenQuiz == -1:
                    # it will return a none value for quitting inside the function
                    checkInput = addQuiz(moduleQuizes)
                    if checkInput != None:
                        break
                # Deleting of quiz
                elif chosenQuiz == -2:
                    if moduleQuizes != []:
                        # it will return a none value for quitting inside the function
                        checkInput = deleteQuiz(moduleQuizes)
                        if checkInput != None:
                            break
                    else:
                        print('\n' +'\33[41m' + 'Error! Cannot Delete Quiz as no quiz(s) are defined. Please add a quiz before deleting them.' + '\33[0m')

                # Editing of quiz topics (Adding and deleting topics)
                else: 
                    # it will return a none value for quitting inside the function
                    checkInput = editQuizTopic(moduleQuizes,chosenQuiz,chosenmodule)
                    if checkInput != None:
                        # Resetting of dict and look at updated txt file
                        # Txt file will be updated if admin changes the name for one of the quizes
                        dict.clear()  
                        dict = readFile(quizSettingTxt)
                        break

        # Convert int to str if checkInput is int
        checkOption = str(checkInput)
        # Ensure that user does not cancel. Canceling will exit out of function
        if checkOption != '0':
            if  delmodule == False:
                # Will update the selected module given the selected module's key
                dict[moduleKey][1] = checkOption
            # Writing to quiz_setting file
            writeQuizSetting(dict=dict)
        
            input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')

# This function allows admin to choose which quiz in each module will be tested
# Admin will first a module and then choose which quiz will be tested in that module.
# Quizes should be already defined before selection of quizes to be tested
# The function takes in the quiz setting dict as its argument
# It will update the quiz_setting.txt under "Quiz tested for each Module: "
def chooseQuiz(dict):
    while True:
        # moduleList will contain all the modules with its subsequent quizes and the topics in each quiz
        # e.g. [[module,'Quiz 1:Math:Sci, Quiz 2:Math:History'], [module,'Quiz 1:Math:Sci'],...]
        ModuleList = []
        # for printing of all modules
        chooseQuizMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t' + '\33[4m' + '{ Choosing Quiz for Module }' + '\33[0m' + '\n\n'
        
        i = 1
        for key in dict:
            if int(key) > 5:
                chooseQuizMenu += f'{i}. ' + '\33[91m' + '\33[4m' f'{dict[key][0].strip()}' + '\33[0m' + '\n' 
                ModuleList.append(dict[key])
                i += 1

        if ModuleList == []:
            chooseQuizMenu += '\33[41m' + 'Error! No quizes Defined. Please define a quiz in [4] Edit Module' + '\33[0m' + '\n'
        
        chooseQuizMenu += '\n---------------------------------------------\n'
        chooseQuizMenu += '\33[41m' + '\33[4m' + f'Choose a Module According to its index' + '\33[0m' + '\n[0] Cancel (Back)\n>>> '

        chosenOption = validationRange(start=0,end=len(ModuleList),question=chooseQuizMenu)
        if chosenOption == 0:
            break
        
        # chosenModule is a list that contains the chosen module and its quizes.
        # e.g. [module,'Quiz 1:Math:Sci, Quiz 2:Math:History', ....]
        chosenModule = ModuleList[chosenOption-1]   # setting of chosen Module

        # for when no quizes have been defined for the module
        # chosenModule will only contain module name and None
        # e.g. ['moduleName', 'None']
        if chosenModule[1] == 'None':
            print('\n' + '\33[41m' + 'Error! No quizes defined! Please define quizes in [4] Edit Modules!' + '\33[0m')
            break
        
        # list that contains all quizes for the module
        # e.g. [Quiz 1:Math:Sci, Quiz 2:Math:History, ....]
        quizList = chosenModule[1].split(',')

        # Printing of all quizes for the selected module
        chooseQuizMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t' + '\33[4m' + '{ Choosing Quiz for Module }' + '\33[0m' + '\n'
        for i, quiz in enumerate(quizList):
            # A temprorary list that will store the quiz name an its topics
            # e.g. [Quiz1,'Math',Sci',...]
            tmpList = quiz.split(':') 
            chooseQuizMenu += f'\n{i+1}. Quiz Name: {tmpList[0]:<15}' + '\33[91m' + '\33[4m' + f'Topics: {tmpList[1:]}' + '\33[0m'  
        
        
        # To find out if a quiz has been assigned to the module.
        quizAssigned = False
        # To find out the quiz that is tested for the module
        # Makes a list that stores all the quiz tested in all modules 
        # e.g. ['PSEC: Quiz 1', 'Fundamentals of Networking: Quiz 2',...]
        for i in dict['5'][1].split(','):
            # A temporary list that contains the Module and the quiz being tested for the module
            # e.g. [Module Name, 'Quiz 1']
            tmpList = i.split(':')
            if tmpList[0] == chosenModule[0]:
                quizTested = tmpList[1]
                quizAssigned = True
            
        if quizAssigned == False:
            quizTested = 'No Quiz Assigned'

        chooseQuizMenu += '\n---------------------------------------------\n\nCurrent Module: ' + '\33[91m' + '\33[4m' + f'{chosenModule[0]}' + '\33[0m'
        chooseQuizMenu += f'\nCurrent Quiz Tested: {quizTested}\nChoose a quiz to be tested according to its index.\n[0] Cancel (Back)\n>>> '
        
        checkInput = validationRange(start=0,end=len(quizList),question=chooseQuizMenu)
        
        # for user does not quit
        if checkInput != 0:
            # Creates a list that contains the chosen quiz (index 0) with its topics (index 1 onwards)
            # e.g. ['Quiz 1', 'Math', 'Sci']
            chosenQuizList = quizList[checkInput-1].split(':') 

            #chosenQuiz is a string that contains the module and the quiz being tested for that module
            # e.g. 'PSEC:Quiz 1'
            chosenQuiz = chosenModule[0] + ': ' + chosenQuizList[0]  # selecting of chosen quiz and putting it into a string
            
            if dict['5'][1] == 'empty':
                dict['5'][1] = chosenQuiz

            # If there is already defined quiz tested for modules
            else:
                # Creates a list that has existing modules and quiz being tested defined in quiz_setting.txt
                # e.g. ['PSEC:Quiz 1','Fundamentals of Networking:Quiz 2',...]
                tmpList = dict['5'][1].split(',')
                
                # check if quiz is already defined. if it is already defined, replace the value in the list
                # If it is not defined, add into list
                quizAlreadyDefined = False

                for i , module in enumerate(tmpList):
                    # creates a tmp list that contains module + quiz e.g. ['PSEC','Quiz 1']
                    tmpList1 = module.split(':')
                    if tmpList1[0] == chosenModule[0]:
                        tmpList[i] = chosenQuiz     # Updating List 
                        quizAlreadyDefined = True
                
                # Add into list as quiz teste with module was not defined in the setting
                if quizAlreadyDefined == False:
                    tmpList.append(chosenQuiz)

                # Putting all elements in the list into a string
                tmpStr = ''
                for i in range(len(tmpList)-1):
                    tmpStr += tmpList[i] + ','
                
                tmpStr += tmpList[-1]
                # Update dictionary with new values
                dict['5'][1] = tmpStr

        # for above when user quits, ensure that it does not write to quiz_setting.txt
        if checkInput != 0:
            # Writing to quiz_setting file (Updating Quiz tested for each module)
            writeQuizSetting(dict=dict)
            
            input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')
            break  # Breaks out of loop

# This function allows user to change properties of quiz_settings.txt to change quiz settings
def quizSetting():
    while True:
        # Creats a dict of quiz settings by reading file quiz_setting.txt
        settingsDict = readFile(quizSettingTxt)

        if settingsDict == {}:   # If dictionary is empty,
            settingsDict['1'] = ['Time for quiz: ','empty']
            settingsDict['2'] = ['Number of Question for each Topic: ','empty']
            settingsDict['3'] = ['Maximum number of attempts for each quiz: ','empty']
            settingsDict['4'] = ['Randomize Options for quiz: ','empty']
            settingsDict['5'] = ['Quiz tested for each Module: ','empty']
            fn = open(quizSettingTxt,'w') # Write mode
            for key in settingsDict:                                  # for each key in dict
                fn.write(settingsDict[key][0] + '|' + settingsDict[key][1])   # Write settings onto txt file
                fn.write('\n')                                # Add line feed for new line
            fn.close()

        # Adds a min after time for printing
        oldTime = settingsDict['1'][1]
        settingsDict['1'][1] = settingsDict['1'][1] + ' min'


        # formatting of current quiz settings to print to user
        quizSettingsMenu = '\n---------------------------------------------\n'+ '\33[32m' +  '\t' + '\33[4m' + '{ Current Quiz Settings }' + '\33[0m' '\n'

        for i in range(5):
            # '\033[91m' is for red color text and to end red text is '\033[0m'
            if i != 1 and i != 4:
                quizSettingsMenu += f'\n{i+1}. {settingsDict[str(i+1)][0]}' + '\033[91m' + '\33[4m' + settingsDict[str(i+1)][1] + '\033[0m'
            else: 
                quizSettingsMenu += f'\n{i+1}. {settingsDict[str(i+1)][0]}' + '\33[32m' + 'Go in for more details' + '\33[0m'

        quizSettingsMenu += '\n---------------------------------------------\nPlease Choose a setting to edit according to its index\n[0] Back\n>>> '
    
        # Resesting of time setting by setting it back to old one
        settingsDict['1'][1] = oldTime

        chosenOption = validationRange(start=0,end=5,question=quizSettingsMenu)

        if chosenOption == 0:
            break
        # Editing of time for quiz
        elif chosenOption == 1:
            writeSetting(dict = settingsDict,key='1',checkQuestion=f'\nCurrent Time setting : {settingsDict[str(1)][1]}\n[1] Unlimited\n[2] Set new specified Time\n\n[0] Cancel (Back)\n>>> ')
        # Editing Number of questions in quiz
        elif chosenOption == 2:
            writeSetting(dict=settingsDict,key='2',checkQuestion='')

        # Editing Number of attempts for quiz
        elif chosenOption == 3:
            writeSetting(dict=settingsDict,key='3',checkQuestion=f'\nCurrent Attempts for quiz : {settingsDict[str(3)][1]}\n[1] Unlimited\n[2] Set new specified Attempt\n\n[0] Cancel (Back)\n>>> ')

        # Editting randomizing options for quiz
        elif chosenOption == 4:
            writeSetting(dict=settingsDict,key='4',checkQuestion=f'\nCurrent setting for randomized options : {settingsDict[str(4)][1]}\nRandomize Options?\n\n[1] Yes\n[2] No\n[0] Cancel (Back)\n>>> ')
        
        # choosing of quizes for each module
        elif chosenOption == 5:
            chooseQuiz(dict=settingsDict)

# This function ensures that password contains special char + minimum length of 4 + max length of 20 + 1 num + lower and upper
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
                print('\33[41m' + f'Error! Please ensure that password contains at least one special char : ! , @ , # , $ , %' + '\33[0m')
                print('\33[41m' + 'AND contains 1 number' + '\33[0m')
                print('\33[41m' + 'AND contains one uppercase and one lowercase char' + '\33[0m')
                print('\33[41m' + 'AND must be between 4 and 20 characters with no spaces in it' + '\33[0m' + '\n')
        
        except EOFError:            # error for when user enters ctrl + z
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
        except KeyboardInterrupt:   # Error for when user enters ctrl + c
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')

# This Function helps register users by updating user list in userid_pswd.txt
# The user enters username, password, email
# The argument of this function takes in the users dict
def registerUser(dict):

    courseDict = readFile(coursesTxt)
    # contains all courses. E.g. ['DISM','DAAA',...]
    courseList = []
    # Appends Module from quiz_setting.txt into ModuleList
    i = 1
    # For printing of Modules later on
    courseSettingMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t      ' + '\33[4m' + '{ Module Setting }' + '\33[0m' + '\n\n'
    for key in courseDict:
        courseSettingMenu += f'{i}. ' + '\33[91m' + '\33[4m' f'{courseDict[key][0].strip()}' + '\33[0m' + '\n' 
        courseList.append(courseDict[key][0])
        i += 1
    
    courseSettingMenu += '\n---------------------------------------------\n'
    courseSettingMenu += '\33[41m' + '\33[4m' + f'Choose a Course for user according to its index' + '\33[0m' + '\n[0] Cancel (Back)\n>>> '
    
    # For when there are no Modules defined in quiz_setting.txt
    if len(courseList) == 0:
        print('\n' + '\33[41m' + 'Error! No Courses Defined!' +'\33[0m')

    # For when Modules are defined
    else: 
        registerUserMenu = '\n' + '\33[32m' + '\33[4m' +'Register New User' + '\33[0m'
        while True:
            newUser = stringValidation(question=registerUserMenu + '\nPlease Enter a User ID\n[0] Cancel (Back)\n>>> ')
            accountDetails = 'UserID: ' + newUser

            # Check if there is any duplicate user ID and reject it
            duplicateUserID = False
            for account in dict:
                if dict[account][0].strip().upper() == accountDetails.upper():
                    duplicateUserID = True
                    break

            if newUser == '0':
                break
            elif len(newUser) < 5:
                print('\33[41m' + '\nPlease input a username with minimum of 5 characters' + '\33[0m' + '\n')

            # Continue to check and enter passwords
            elif duplicateUserID == False :
                # Formatting of account details for when writing onto txt file
                accountDetails = 'UserID: ' + newUser + ' | '
                # Password validation
                newPwd = pwdCheck(question= registerUserMenu + '\nPlease enter password\n[0] Cancel (Back)\n>>> ')
                # If user does not cancel. If user cancels, newPwd = None
                if newPwd != None:
                    checkPwd = stringValidation(question=registerUserMenu + '\nPlease re-enter password\n[0] Cancel (Back)\n>>> ')

                    # Checking whether the 2 passwords entered are the same
                    if checkPwd == newPwd:
                        while True:
                            # Email account used for forgetten password in user.py
                            accountEmail = stringValidation(question=registerUserMenu+'\nPlease Enter email for account\n[0] Cancel (Back)\n>>> ')
                            quitEmail = False  # for exiting loop and going into confirmation of adding account
                            # Quitting of loop
                            if accountEmail == '0':
                                quitEmail = True
                                break
                            regexPattern = r'\w+@+\w+[.]+\w'
                            validateEmail = re.search(regexPattern,accountEmail)
                            
                            if validateEmail == None:
                                print('\n'+'\33[41m'+'Error! Please enter a valid email' + '\33[0m')

                            # Adding of Module to account
                            else: 
                                checkInput = validationRange(start=0,end=len(courseList),question=courseSettingMenu)
                                # for quitting 
                                if checkInput == 0:
                                    quitEmail = True

                                chosenCourse = courseList[checkInput-1]  # Selecting chosen Module
                
                                break # Break if email is valid (xxxx@xxxxx.xxx) format with no spaces

                        if quitEmail == False:
                            confirmRegister = validationRange(start=0,end=1,question='\33[41m' + '\n*** CONFIRMATION *** : Create new account?' + '\33[0m' + '\n\n[1] Yes \t [0] NO (Back)\n>>> ')
                            # If user confirms to register, write to file
                            if confirmRegister == 1:
                                # stored password is reverse of password + adding of wla at the front of it
                                accountDetails += 'pwd: wla' + newPwd[::-1] + '| '
                                # Adds email 
                                accountDetails += 'Email: ' + accountEmail + '| '
                                # Adds Module at the end
                                accountDetails += chosenCourse
                                
                                fn = open(userID_pwdTxt,'w') # Write mode
                                # Writing of old account details stored onto old txt file
                                for key in dict:       
                                    # Writes UserID | Password | Email | Module
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
                                fn.write(accountDetails)
                                fn.close()
                                input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')
                                break
                    # If passwords do not match
                    else:
                        if checkPwd != '0': # Error message for when passwords dont match
                            print('\33[41m' + 'Password do not match! Please re-enter information again' + '\33[0m')
            
            # Error for duplicate userIDs
            else:
                print('\33[41m'+'Error! User ID already exists! Please enter another userID' + '\33[0m' + '\n')


# This function allows the admin to delete the user selected 
# The argument of this function takes in the users dict
def deleteUser(dict):
    print()
    # Printing of current user list excluding admin account
    for key in dict:
        if key != '1':
            print('\33[32m' + str(int(key)-1) + ' : ' + '\33[0m' + dict[key][0])

    deleteUserQuestion = f'Enter the index of the user to delete [1 to {int(key)-1}]\n[0] Cancel (Back)\n>>> '
    chosenOption = validationRange(start=0,end=int(key)-1,question=deleteUserQuestion)

    if chosenOption != 0:
        confirmDeleteQuestion = '\n'+'\33[41m' + '*** CONFIRMATION *** : Delete User?' + '\33[0m' + '\n\n[1] YES \t [0] Cancel (Back)\n>>> '
        checkOption = validationRange(start=0,end=1,question=confirmDeleteQuestion)
        if checkOption != 0:
            del dict[str(chosenOption+1)] # Deletes the selected userID with its pwd from dict
            
            writeUser(dict=dict)
            
            input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')

# This function allows admin to reset password of a selected user from user list
# The argument of this function takes in the users dict
def resetPwd(dict):

    # Printing of Indexes with User ID
    for key in dict:
        print('\33[32m' +key + ' : ' + '\33[0m' + dict[key][0])
    resetPwdQuestion = f'Enter the index of user to reset password [1 to {key}]\n[0] Cancel (Back)\n>>> '

    chosenOption = validationRange(start=0,end=int(key),question=resetPwdQuestion)
    
    if chosenOption != 0:
        while True:
            newPwd = pwdCheck('\nPlease enter new password\n[0] Cancel (Back)\n>>> ')
            # If user does not cancel
            # newPwd == None when 0 is entered
            if newPwd != None:
                checkPwd = stringValidation(question='\nPlease re-enter new password\n[0] Cancel (Back)\n>>> ')

                if checkPwd == newPwd:
                    confirmRegister = validationRange(start=0,end=1,question='\n'+'\33[41m' + '*** CONFIRMATION *** : Create new account?' + '\33[0m' + '\n\n[1] Yes \t [0] NO (Back)\n>>> ')
                    # If user confirms to register, write to file
                    if confirmRegister == 1:
                        dict[str(chosenOption)][1] = ' pwd: wla' + newPwd[::-1]   # Set to new password
                        
                        writeUser(dict=dict)

                        input('\33[42m' + '\nSuccess! Press enter to continue...' + '\33[0m' + '\n')
                        break
                # If passwords do not match
                else: 
                    if checkPwd != '0': # Error message for when passwords dont match
                        print('\n'+'\33[41m' + 'Password do not match! Please re-enter information again' + '\33[0m')

            else:   # For user quitting
                break

# This function allows the admin user to changes the course of a user
# This function takes in the user dictionary that contains the user, password,email and courses
def changeCourse(dict):
    while True:
        changeCourseMenu = '\n' + '\33[32m' + '\33[4m' + 'Current User List' + '\33[0m' + '\n\n'
        
        i = 1
        for key in dict:
            try: 
                changeCourseMenu += '\33[32m' + f'{i} : ' + '\33[0m' + dict[key][0] + '\tCourse: ' + dict[key][3] + '\n'
                i += 1
            # For admin account as admin does not have Module assigned to it
            except IndexError:
                continue
        
        changeCourseMenu += '\nChoose an account to change module according to its index\n[0] Cancel (Back)\n>>> '
        
        chosenOption = validationRange(start=0,end=len(dict)-1,question=changeCourseMenu)

        # Quitting of loop 
        if chosenOption == 0:
            break
        
        # Chosen user contains [userid, password, email, module]
        chosenUser = dict[str(chosenOption+1)]

        # Current user module and its topics
        changeCourseMenu = f'\nCurrent {chosenUser[0]}\nCurrent Course: {chosenUser[3]}\n'

        courseDict = readFile(coursesTxt)

        # Contains all the modules and its quizes with topics
        # e.g. ['couse1','course2','course3',....]
        courseList = []

        # Printing of all modules with its topics
        for i, key in enumerate(courseDict):
            changeCourseMenu += f'\n[{i+1}] ' + '\33[31m' + '\33[4m' + f'{courseDict[key][0]}' + '\33[0m'
            courseList.append(courseDict[key][0])
        
        changeCourseMenu += '\n\nChange to new module according to its index\n[0] Cancel (Back)\n>>> '
        checkInput = validationRange(start=0,end=len(courseList),question=changeCourseMenu)

        # Quitting
        if checkInput == 0:
            break
        
        # contains the chosen Course
        chosenCourse = courseList[checkInput-1]

        # Changing of user module value in dict
        dict[str(chosenOption+1)][3] = ' ' + chosenCourse

        writeUser(dict=dict)

        input('\33[42m' + '\nCourse Changed Successfully! Press enter to continue...' + '\33[0m' + '\n')



# This function deletes an attempt from a user in quiz_results.csv
# This function takes in attempts stored in the quiz_result.csv 
# Attempts is a list and each user attempt is stored as a dictionary in this list
def deleteAttempt(attempts):
    
    deleteAttemptQuestion = '\n==============================================================\n'
    # Loops through dict in list and prints out userID,grade,time submitted for each attempt
    for i, userAttempt in enumerate(attempts):
        deleteAttemptQuestion += f'\n[{i+1}]: ' + userAttempt['UserID'] + '\tCourse: ' + userAttempt['Course'] + '\n'
        deleteAttemptQuestion += '     Module: ' +'\33[32m' + userAttempt['Module'] + '\33[0m' +'\tQuiz Name: ' '\33[31m' + userAttempt['Quiz Name'] + '\33[0m' + '\n     Topic: ' + '\33[32m' + userAttempt['Topic Tested'] + '\33[0m' 
        deleteAttemptQuestion += '\tGrade: ' + '\33[41m' + '\33[4m' + userAttempt['Grade (%)'] + ' %' + '\33[0m' +'\tTime Submitted: ' + userAttempt['Time Submitted'] +'\n'
        
    deleteAttemptQuestion += '\n==============================================================\n'
    
    deleteAttemptQuestion += f'\nEnter the index of the attempt to delete attempt [1 to {i+1}]\n[0] Cancel (Back)\n>>> '
    chosenOption = validationRange(start=0,end=i+1,question=deleteAttemptQuestion)

    # Double check if admin really wants to delete attempt
    if chosenOption != 0:
        checkOption = validationRange(start=0,end=1,question='\n' + '\33[41m' + '*** CONFIRMATION : Delete Attempt? ***' + '\33[0m' + '\n\n[1] Yes\t [0] No (Back)\n>>> ')

        # if admin confirms to delete user attempt, delete it from list and rewrite to csv files
        if checkOption == 1:
            del attempts[chosenOption-1]  # Deletes user attempt

            # Header of the csv file is contained within field list
            field = []
            for dictionary in attempts:
                for key in dictionary:
                    # Appends all keys that attempt 1 has if it exists in csv file
                    field.append(key)
                break

            with open(resultsCsv,'w') as fn: # write mode
                # Using dict writer as data is stored in dict
                writer = csv.DictWriter(fn,fieldnames = field)

                # Writing Headers (field names)
                writer.writeheader()
                
                # Writing of data rows
                writer.writerows(attempts)
            
            input('\33[42m' + '\nAttempt Deleted Successfully! Press enter to continue...' + '\33[0m' + '\n')


# This function will help to register and delete users
def userSetting():
    while True:
        # Creates a user dict by reading file userid_pswd.txt
        usersDict = readFile(userID_pwdTxt)

        if usersDict == {}:  # Checking for empty dictionary
            noUser = True
        else:
            noUser = False

        userSettingMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t      ' + '\33[4m' + '{ User Settings }' + '\33[0m'
        userSettingMenu += '\n\n[1] View User List\n[2] Register User\n[3] Delete User\n[4] Reset User Password\n[5] Change User Course\n[6] Delete User Attempt\n[0] Back'
        userSettingMenu += '\n\n---------------------------------------------\n>>> '

        chosenOption = validationRange(start=0,end=6,question=userSettingMenu)

        if chosenOption == 0:
            break

        # Viewing of current users in user list
        elif chosenOption == 1 and noUser == False:
            print('\n' + '\33[32m' + '\33[4m' + 'Current User List' + '\33[0m' + '\n')
            for key in usersDict:
                try: 
                    print('\33[32m' +key + ' : ' + '\33[0m' + usersDict[key][0] + '\tCourse: ' + usersDict[key][3])
                
                # For admin account as admin does not have Module assigned to it
                except IndexError:
                    print('\33[32m' +key + ' : ' + '\33[0m' + usersDict[key][0])
        # Register Users
        elif chosenOption == 2:
            registerUser(dict = usersDict)

        # Deleting of User
        elif chosenOption == 3 and noUser == False:
            deleteUser(dict = usersDict)

        # Resetting of pwd of selected user
        elif chosenOption == 4 and noUser == False:
            resetPwd(dict = usersDict)
        
        # Changing Module of user
        elif chosenOption == 5 and noUser == False:
            changeCourse(dict = usersDict)
        
        # Error message for when there are no users
        elif noUser == True: 
           print('\n'  + '\33[41m' + 'Error! There are no Users in database!' + '\33[0m' + '\n')
        
        elif chosenOption == 6:

            # list that contains all previous attempts stored in csv file
            dataList = []
            # Reading of previously stored data in csv file and store in a list
            with open(resultsCsv,'r') as file: # Read mode
                writer = csv.DictReader(file)
                for line in writer:
                    # Appends each attempt into list as a dictionary
                    dataList.append(dict(line))

            if dataList != []: # Ensures that quiz_results.csv is not empty
                deleteAttempt(attempts = dataList)
            else:
                print('\n'  + '\33[41m' + 'Error! There are no attempts in quiz!' + '\33[0m' + '\n')

# this function allows admin to add a course in course.txt
# The function takes in the course dictionary that stores all the defined courses
def addCourse(dict):
    while True:
        #Printing of menu
        addCourseMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t      ' + '\33[4m' + '{ Add Course }' + '\33[0m' + '\n\n'
        addCourseMenu += '\33[41m' + '\33[4m' + f'Current Courses' + '\33[0m' + '\n\n'

        courseList = []
        # Printing of all defined courses in courses.txt
        for i, key in enumerate(dict):
            addCourseMenu += f'[{i+1}] ' + '\33[31m' + '\33[4m' + f'{dict[key][0]}' + '\33[0m' + '\n'
            courseList.append(dict[key][0])

        # for when no courses are defined
        if dict == {}:
            addCourseMenu += '\33[41m' + 'No Courses are defined. Please add a course!' + '\33[0m'
        
        addCourseMenu +=  '\n---------------------------------------------\n' + '\33[32m' + 'Enter New Course Name' + '\33[0m'
        addCourseMenu += '\n[0] Cancel (Back)\n>>> '
        
        newCourse = stringValidation(question=addCourseMenu)

        # Quitting
        if newCourse == '0':
            break
            
        # Checking if course already exists
        duplicateCourse = False
        for i in courseList:
            if i == newCourse.upper():
                duplicateCourse = True

        if duplicateCourse == True:
            print('\n' + '\33[41m' + 'Error! Course already exists. Please choose a different name' + '\33[0m')

        else: 
            chosenOption = validationRange(start=0,end=1,question= '\n' + '\33[41m' + '*** CONFIRMATION : Add new Course? ***' + '\33[0m' + '\n[1] YES \t [0] NO\n >>> ')
            
            if chosenOption == 1:
                # Updating courses.txt
                with open(coursesTxt,'w') as fn:
                    for key in dict:
                        fn.write(dict[key][0] + '|' + dict[key][1])
                        fn.write('\n')
                    fn.write(newCourse + '|None')

                input('\33[42m' + 'Course Added! Press enter to continue...' + '\33[0m' + '\n')
                break # get out of loop

# This function allows the admin to delete a defined course in courses.txt
# The argument of this function is the course dictionary that contains all the courses defined in courses.txt
def deleteCourse(dict):
    while True:
        #Printing of menu
        deleteCourseMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t      ' + '\33[4m' + '{ Delete Course }' + '\33[0m' + '\n\n'
        deleteCourseMenu += '\33[41m' + '\33[4m' + f'Current Courses' + '\33[0m' + '\n\n'

        courseList = []
        # Printing of all defined courses in courses.txt
        for i, key in enumerate(dict):
            deleteCourseMenu += f'[{i+1}] ' + '\33[31m' + '\33[4m' + f'{dict[key][0]}' + '\33[0m' + '\n'
            courseList.append(dict[key][0])
        
        deleteCourseMenu +=  '\n---------------------------------------------\n' + '\33[32m' + 'Choose a course to delete according to its index' + '\33[0m'
        deleteCourseMenu += '\n[0] Cancel (Back)\n>>> '

        chosenOption = validationRange(start=0,end=len(courseList),question=deleteCourseMenu)

        # For Quitting
        if chosenOption == 0:
            break
        
        chosenCourse = courseList[chosenOption-1] # Selecting of chosen course to delete

        confirmDelete = validationRange(start=0,end=1,question= '\n' + '\33[41m' + '*** CONFIRMATION : Delete Course? ***' + '\33[0m' + '\n[1] YES \t [0] NO\n >>> ')
        
        # User confirms to delete course
        if confirmDelete == 1:
            # Deleting course from dictionary
            for key in dict:
                if dict[key][0] == chosenCourse:
                    del dict[key]
                    break 

            # Updating courses.txt
            with open(coursesTxt,'w') as fn:
                    for key in dict:
                        fn.write(dict[key][0] + '|' + dict[key][1])
                        fn.write('\n')

            # Updating of courses in userid_pswd.txt
            userDict = readFile(userID_pwdTxt)
            
            for key in userDict:
                try: 
                    # If the course was deleted and a user has the module in the userid_pswd.txt, update it to say deleted module
                    if userDict[key][3] == ' ' + chosenCourse:
                        userDict[key][3] = ' Deleted Course'

                except IndexError:
                    continue
            
            writeUser(dict=userDict)

            input('\33[42m' + 'Course Deleted! Press enter to continue...' + '\33[0m' + '\n')
            break # get out of loop

# This function allows user to add a module to a course
# The function takes in the course dictionary as its argument and the 
# chosen course it is editing where chosenCourse is a list that contains the chosen course and its modules
# e.g. [course,'module1,module2,...']
def addModuleToCourse(dict, chosenCourse):
    while True:
        # Gets quiz setting to find out more info about modules stored there
        quizSettingDict = readFile(quizSettingTxt)
        # moduleList is a list where is contains all defined modules
        # e.g. ['Fundamentals of Networking','PSEC', ...]
        moduleList = []

        addModuleMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t' + '\33[4m' + '{ Add Module to Course }' + '\33[0m' + '\n\n'
    
        # Printing of all modules
        i = 1
        for key in quizSettingDict:
            if int(key) > 5: # as modules are stored after key 5
                addModuleMenu += f'\n[{i}] ' + '\33[31m' + '\33[4m' + f'{quizSettingDict[key][0]}' + '\33[0m'
                moduleList.append(quizSettingDict[key][0])
                i += 1

        # Checking if no modules are defined
        noModule = False
        if moduleList == []:
            noModule = True

        addModuleMenu += '\n\n---------------------------------------------\n' + '\33[32m' + 'Choose a module to add according to its index' + '\33[0m'
        addModuleMenu += '\n[0] Cancel (Back)\n>>> '

        # For when no modules are defined. Break out of function
        if noModule == True:
            print('\n' + '\33[41m' + 'Error! No modules defined. Please Define add a module in [4] Edit Module in Main Menu' + '\33[0m')
            break
        
        chosenOption = validationRange(start=0,end=len(moduleList),question=addModuleMenu)
        
        if chosenOption == 0:
            break

        chosenModule = moduleList[chosenOption-1] # Selecting of chosen course

        # Creates a list that contains all the modules assigned to the chosen course
        course_Modules = chosenCourse[1].split(',')

        # Checks if the module has already assigned
        moduleAlreadyAssigned = False
        for module in course_Modules:
            if chosenModule == module:
                moduleAlreadyAssigned = True
                break
        
        if moduleAlreadyAssigned == True:
            print('\n' + '\33[41m' + 'Error! Module is already assigned to course' + '\33[0m')

        # Updating dict and writing to courses.txt
        else: 

            # For when there are no modules assigned to it yet
            if course_Modules == ['None']:
                # Appends new module into list
                course_Modules[0] = chosenModule

            # For when there are already existing modules assigned to course
            else:
                course_Modules.append(chosenModule)

            # reformatting 
            tmpStr = ''

            for i in range(len(course_Modules)-1):
                tmpStr += course_Modules[i] + ','

            tmpStr += course_Modules[-1]

            # updating dictionary
            chosenCourse[1] = tmpStr 

            for key in dict:
                # Search for the chosen course and change its modules
                if dict[key][0] == chosenCourse[0]:
                    dict[key][1] = chosenCourse[1]

            # Updating courses.txt
            with open(coursesTxt,'w') as fn:
                for key in dict:
                    fn.write(dict[key][0] + '|' + dict[key][1])
                    fn.write('\n')

            input('\33[42m' + 'Module Added to Course! Press enter to continue...' + '\33[0m' + '\n')
            break # get out of loop

# This function allows admin to delete modules assigned to the course
# The arguments of this function are the course dictionary and the 
# chosen course it is editing where chosenCourse is a list that contains the chosen course and its modules
# e.g. [course,'module1,module2,...']
def deleteModuleFromCourse(dict, chosenCourse):
    deleteModuleMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t' + '\33[4m' + '{ Delete Module from Course }' + '\33[0m' + '\n\n'
    deleteModuleMenu += '\33[41m' + 'Current Modules assigned to Course' + '\33[0m' + '\n'

    # Creates a list that stores all the modules assigned to the selected course
    # e.g. ['module1', 'module2',...]
    moduleList = chosenCourse[1].split(',')

    for i, module in enumerate(moduleList):
        deleteModuleMenu += f'\n[{i+1}] {module}'

    deleteModuleMenu += '\n---------------------------------------------\nChoose a module to delete from course according to its index\n[0] Cancel (Back)\n>>> '

    chosenOption = validationRange(start=0,end=len(moduleList),question=deleteModuleMenu)
    
    # If user did not quit, Delete module assigned to course
    if chosenOption != 0: 
        chosenModule = moduleList[chosenOption-1] # Selecting of module to delete

        # Deleting of module in module list
        for i, module in enumerate(moduleList):
            if module == chosenModule:
                del moduleList[i]
                break

        # Checking for empty list (all modules are deleted)
        # If so, make moduleList = ['None']
        if moduleList == []:
            moduleList.append('None')
        
        # Reformatting
        tmpStr = ''
        for i in range(len(moduleList)-1):
            tmpStr += moduleList[i] + ','

        tmpStr += moduleList[-1]

        # finding the chosen course stored in dictionary and updating the modules
        for key in dict:
            if dict[key][0] == chosenCourse[0]:
                dict[key][1] = tmpStr
                break

        # Updating courses.txt
        with open(coursesTxt,'w') as fn:
            for key in dict:
                fn.write(dict[key][0] + '|' + dict[key][1])
                fn.write('\n')

        input('\33[42m' + 'Module Added to Course! Press enter to continue...' + '\33[0m' + '\n')
        
# This function allows admin to change the selected course's name
# It takes in the course dictionary and the chosenCourse which is a list that contains the chosen course and the modules
# assigned to it. e.g. [course,'module1,module2,...']
def changeCourseName(dict,chosenCourse): 
    while True:
        changeCourseMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t   ' + '\33[4m' + '{ Change Course Name }' + '\33[0m' + '\n\n'
        changeCourseMenu += 'Current Course Name: ' + '\33[41m' + f'{chosenCourse[0]}' + '\33[0m' + '\nModules: '

        moduleList = []
        courseList = []

        for key in dict:
            courseList.append(dict[key][0].upper())

        # printing of all modules in the current selected course
        for i, module in enumerate(chosenCourse[1:]):
            changeCourseMenu += f'\n{i+1}. {module}'  
            moduleList.append(module) 

        # for when there is no modules assigned to course yet
        if moduleList == []:
            changeCourseMenu += '\n' + '\33[31m' + 'No Modules Assigned to course' + '\33[0m'

        changeCourseMenu = '\n---------------------------------------------\nEnter New Course Name\n[0] Cancel (Back)\n>>> '    
        
        newCourseName = stringValidation(question=changeCourseMenu)

        # user quit
        if newCourseName == '0':
            break

        # newCourseName cannot be 'None' as it will mess up data in courses.txt and userid_pswd.txt
        elif newCourseName == 'None':
            print('\n' + '\33[41m' + "Error! Cannot name course as ['None']. Please use another name" + '\33[0m')

        elif newCourseName.upper() in courseList:
            print('\n' + '\33[41m' + "Error! Course already exists. Please use another name" + '\33[0m')

        else: 
            # Updating of courses in userid_pswd.txt 
            userDict = readFile(userID_pwdTxt)
            for key in userDict:
                if int(key) > 1:  # avoid admin account
                    if userDict[key][3] == ' ' + chosenCourse[0]:
                        userDict[key][3] = ' '+ newCourseName

            writeUser(dict=userDict)

            # finding selected course and changing its name in the dictionary
            for key in dict:
                if dict[key][0] == chosenCourse[0]:
                    dict[key][0] = newCourseName 
                    break 
            
            # Updating courses.txt
            with open(coursesTxt,'w') as fn:
                for key in dict:
                    fn.write(dict[key][0] + '|' + dict[key][1])
                    fn.write('\n')

            input('\33[42m' + 'Course Name Changed! Press enter to continue...' + '\33[0m' + '\n')
            break 

# This function allows admin to add, delete and choose a selected course to modify
# Courses will contain the modules allocated to it in courses.txt
# This courses will be assigned to each user when registering in admin
def courseSetting():
    while True:
        # Create a course dictionary that holds the courses and modules allocated to it
        courseDict = readFile(coursesTxt)

        # Printing of menu
        courseSettingMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t      ' + '\33[4m' + '{ Course Setting }' + '\33[0m' + '\n\n'
        courseSettingMenu += '\33[41m' + '\33[4m' + f'Choose a Course to edit' + '\33[0m' + '\n\n'

        # Printing of all defined courses in courses.txt
        for i, key in enumerate(courseDict):
            courseSettingMenu += f'[{i+1}] ' + '\33[31m' + '\33[4m' + f'{courseDict[key][0]}' + '\33[0m' + '\n'

        # for when no courses are defined
        if courseDict == {}:
            courseSettingMenu += '\33[41m' + 'No Courses are defined. Please add a course!' + '\33[0m'

        courseSettingMenu += '\n---------------------------------------------\n[-1] Add Course\n[-2] Delete course\n[0] Cancel (Back)\n>>> '

        chosenOption = validationRange(start=-2,end=len(courseDict),question=courseSettingMenu)
        
        # for user quitting
        if chosenOption == 0:
            break
        
        # Adding of courses
        elif chosenOption == -1:
            addCourse(dict = courseDict)

        # Deleting of courses
        elif chosenOption == -2:
            if len(courseDict) == 0:
                print('\n' + '\33[41m' + 'Error! Cannot delete courses if no courses are defined!' + '\33[0m')
            else: 
                deleteCourse(dict = courseDict)
        # Selected a defined course
        else: 
            while True:
                # this is a list that contains the course name and the modules assigned to it.
                # e.g. ['course', 'module1,module2']
                chosenCourse = courseDict[str(chosenOption)]
                moduleList = chosenCourse[1].split(',')  # a list that contains all the modules in the course

                # Printing of menu
                courseSettingMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t      ' + '\33[4m' + '{ Course Setting }' + '\33[0m' + '\n\n'
                courseSettingMenu += 'Current Course: ' + '\33[41m' + f'{chosenCourse[0]}' + '\33[0m' + '\n'

                for i , module in enumerate(moduleList):
                    courseSettingMenu += f'\nModule {i+1}. ' + '\33[32m' + '\33[4m' + f'[{module}]' + '\33[0m' 

                courseSettingMenu += '\n---------------------------------------------\n[1] Add Module\n[2] Delete Module\n[3] Change Course Name\n[0] Cancel (Back)\n>>> '

                checkInput = validationRange(start=0,end=3,question=courseSettingMenu)

                # Quitting
                if checkInput == 0:
                    break

                # Adding of modules to course
                elif checkInput == 1:
                    addModuleToCourse(dict = courseDict, chosenCourse = chosenCourse)
                # Deleting of modules from course
                elif checkInput == 2:
                    if moduleList == ['None']:
                        print('\n' + '\33[41m' + 'Error! Cannot delete module as no modules have been assigned to course!' + '\33[0m')
                    
                    else: 
                        deleteModuleFromCourse(dict = courseDict, chosenCourse = chosenCourse)

                # Changing of course name
                elif checkInput == 3:
                    changeCourseName(dict=courseDict, chosenCourse=chosenCourse)

# This function generates a statistical report based on user's performance in the quiz under the quiz_result.csv
# This function takes in results as an argument. Results is a list that contains all user's attempt to quiz
# each user's attempt in the quiz is stored as a dictionary
def generateReport(results):
    while True: 
        # Printing of all modules being tested
        moduleList = []
        for attempt in results:
            if attempt['Module'] not in moduleList:
                moduleList.append(attempt['Module'])

        moduleMenu = '\n---------------------------------------------\n' + '\33[32m' + '\t' + '\33[4m'+ '{ Current Module Tested }' + '\33[0m' + '\n'
        for i, module in enumerate(moduleList):
            moduleMenu += f'\n[{i+1}] ' + '\33[91m' + '\33[4m' + f'{module}' + '\33[0m'
        
        moduleMenu += '\n\n---------------------------------------------\nPlease Choose a Module to view its Quiz(s)\n[0] Back\n>>> '

        checkInput = validationRange(start=0,end=len(moduleList),question=moduleMenu)

        # if user didnt quit 
        if checkInput == 0:
            break 
        chosenModule = moduleList[checkInput-1] # Selecting of chosen module
        quizList = []   

        # Adds all quizes tested given the chosen module
        for attempt in results:
            if attempt['Module'] == chosenModule and attempt['Quiz Name'] not in quizList:
                quizList.append(attempt['Quiz Name'])

        # Printing of all quizes
        quizMenu = '\n---------------------------------------------\n' + '\33[32m' + '\t' + '\33[4m'+ '{ Quiz Tested in Module }' + '\33[0m' + '\n'
        for i, quiz in enumerate(quizList):
            quizMenu += f'\n[{i+1}] ' + '\33[91m' + '\33[4m' + f'{quiz}' + '\33[0m'
        
        quizMenu += '\n\n---------------------------------------------\nPlease Choose a Quiz to view its Topic(s)\n[0] Back\n>>> '

        checkInput = validationRange(start=0,end=len(quizList),question=quizMenu)

        # user did not quit
        if checkInput != 0:
            
            chosenQuiz = quizList[checkInput-1] # selecting of chosen quiz

            numOfQuestionTested = []    
            topicList = []

            for attempt in results:
                if attempt['Topic Tested'] not in topicList and attempt['Module'] == chosenModule and attempt['Quiz Name'] == chosenQuiz:
                    topicList.append(attempt['Topic Tested'])
            
            topicMenu = '\n---------------------------------------------\n' + '\33[32m' + '\t' + '\33[4m'+ '{ Current Topics Tested }' + '\33[0m' + '\n'
            
            for i, topic in enumerate(topicList):
                topicMenu += f'\n[{i+1}] ' + '\33[91m' + '\33[4m' + f'{topic}' + '\33[0m'

            topicMenu += '\n\n---------------------------------------------\nPlease Choose a topic to view its results\n[0] Back\n>>> '

            checkInput = validationRange(start=0,end=len(topicList),question=topicMenu)

            if checkInput != 0:
                chosenTopic = topicList[checkInput-1]   # Selects the chosen Topic
                attemptList = []
                # Appends attempts made for selected topic
                for i in results:
                    if i['Topic Tested'] == chosenTopic and i['Module'] == chosenModule and i['Quiz Name'] == chosenQuiz:
                        attemptList.append(i)

                # Appends number of question tested in quiz for the first attempt
                numOfQuestionTested.append(attemptList[0]['Number of Question Tested'])

                # different number of questions tested and append in numOfQuestionTested List
                for attempt in attemptList:
                    if attempt['Number of Question Tested'] not in numOfQuestionTested:
                        numOfQuestionTested.append(attempt['Number of Question Tested'])

                testStatistics = {}
                # Create a key based on the num of question tested and divide the attempts based off it
                for i in numOfQuestionTested:
                    testStatistics[i] = []

                # For each attempt in AttemptList, if the number of question tested is equal
                # Append that attempt according to its key which is based of the number of questions tested
                # This is so that data isint skewed or altered due to different number of questions being tested
                for questionTested in numOfQuestionTested:
                    for attempt in attemptList:
                        if questionTested == attempt['Number of Question Tested']:
                            testStatistics[questionTested].append(attempt)

                reportMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t      ' + '\33[4m' + f'[ Quiz Report for {chosenTopic} ]' + '\33[0m' + '\n'
                
                # Sorts list from ascending 
                numOfQuestionTested.sort()
                
                # Print for the different amounts of questions tested 
                for i in numOfQuestionTested:
                    reportMenu += '\nNumber of Question Tested: ' + i
                
                reportMenu += '\n\n---------------------------------------------\n'
                reportMenu += '\nPlease Enter the Number of Question Tested to view its respective report\n[0] Cancel (back)\n>>> '

                # For quitting / going back
                numOfQuestionTested.append('0')
                
                chosenOption = listRangeValidation(list=numOfQuestionTested,question=reportMenu)
               
                # if user does not quit, then go and print a statistical report based on the number of questions tested
                if chosenOption != '0': 

                    reportMenu = '\n---------------------------------------------\n' + '\33[32m' +  '\t      ' + '\33[4m' + f'[ Quiz Report for {chosenTopic} ]' + '\33[0m' + '\n'    
                    reportMenu += '\n[1] All Attempts\n[2] Only Highest Grade Attempt\n\n---------------------------------------------\n'
                    reportMenu += '\nPlease Enter which report to view\n[0] Cancel (back)\n>>> '

                    checkInput = validationRange(start=0,end=2,question=reportMenu)
                    # did not quit
                    if checkInput != 0:
                        
                        # for view highest attempt, update the list of attempts to view only each user's highest grade attempt
                        if checkInput == 2:
                            tmpList = [testStatistics[chosenOption][0]] # initialize with 1st attempt
                            userList = []       # Storing of user that has already been added in tmpList

                            for attempt in testStatistics[chosenOption]:
                                # Loops through tmpList and updates tmpList accordingly.
                                for i, storedAttempt in enumerate(tmpList):
                                    # find in tmp list if same userID has stored a <= value and update and store highest / most recent if it is equal
                                    if attempt['UserID'] == storedAttempt['UserID'] and float(storedAttempt['Grade (%)']) <= float(attempt['Grade (%)']):
                                        tmpList[i] = attempt
                                        break
                                    
                                    # If user is not stored in tmpList, append it to tmpList
                                    elif attempt['UserID'] not in userList:
                                        tmpList.append(attempt)
                                        break 
                                
                                # appends and updates the users that are stored in tmpList
                                if attempt['UserID'] not in userList:
                                    userList.append(attempt['UserID'])

                            testStatistics[chosenOption] = tmpList # updating the entire list

                        questionDict = readFile(txtFile=questionPoolTxt)

                        reportMenu = '\n=========================================================================='
                        reportMenu += f"\nFrom Date: {testStatistics[chosenOption][0]['Time Submitted']}"
                        reportMenu += f"\nTo Date: {testStatistics[chosenOption][-1]['Time Submitted']}" 
                        reportMenu += '\n\nModule Name: ' + '\33[32m' + chosenModule + '\33[0m'
                        reportMenu += '\nQuiz Name: ' + '\33[31m' + chosenQuiz +  '\33[0m'
                        reportMenu += '\nTopic: ' + '\33[41m' + chosenTopic + '\33[0m'
                        reportMenu += '\nNumber of questions Tested: ' + '\33[32m' + '\33[4m' + chosenOption + '\33[0m'
                        reportMenu += '\n=========================================================================='

                        print(reportMenu)
                        # press enter to continue for more stats
                        input('\33[42m' + 'Press enter for more statistics...' + '\33[0m' + '\n')
                        
                        # Printing of all questions given the chosen topic and returns the index of the last printed question
                        numOfQuestion = printQuestions(dict=questionDict,topic=chosenTopic) - 1
                        
                        # for dynamic bars based on number of questions
                        questionTextLength = (int(numOfQuestion) * 8) - 2
                        barLength = questionTextLength + 66
                        
                        # for when there is less that 4 questions in a topic, make the dynamic report fixed in length
                        if numOfQuestion < 4:
                            questionTextLength = (4 * 8) - 1
                            barLength = questionTextLength + 65
                            columnSpacing = (questionTextLength/numOfQuestion)-1

                        userReport = f"\n{'=':=>{barLength}}"
                        userReport += '\n|' +f" {'Username':^21}|" + '\33[41m' + f"{'Questions (Total: '+f'{numOfQuestion})':^{questionTextLength}} " + '\33[0m' + '|\33[42m' +'\33[30m' + f"{'Grade':^12}" + '\33[0m' + '|' +f"{'Time Submitted':^26}" + '|'
                        userReport += f"\n{'|':<23}|"
                        for i in range(numOfQuestion):
                            if numOfQuestion >= 4:
                                userReport += '\33[41m' + f"  {str(i+1):^3}  " + '\33[0m' + '|'
                            else: 
                                userReport += '\33[41m' + f"{str(i+1):^{columnSpacing}} " + '\33[0m' + '|'

                        userReport += '\33[42m' + f"{' ':>12}" + '\33[0m' + '|'
                        userReport += f"{'|':>27}"
                        userReport += f"\n{'-':->{barLength}}"
                        
                        print(userReport)

                        # makes a list of [0,0,0,...] where length is based on the number of questions in the topic
                        correctAnswerList = [0] * numOfQuestion   
                        totalAnswerList = [0] * numOfQuestion

                        # Looping through each attempt in the chosen quiz for the chosen topic
                        for s, attempt in enumerate(testStatistics[chosenOption]):
                            userAnswerList = []
                            l = 0 # For indexing 
                            for key in questionDict: 
                                if questionDict[key][7] == chosenTopic:
                                    keyList = []
                                    for dictKey in attempt:
                                        keyList.append(dictKey)
                                        if questionDict[key][0] == attempt[dictKey]:        # if question is found within attempt[key]
                                            userAnswerIndex = keyList.index(dictKey) + 2    # the index of the user's answer is found key +2        
                                            correctAnswerIndex = keyList.index(dictKey) + 1 # Index of the correct answer of the question        \

                                    # Assigning of user answers and checking for correct / wrong
                                    userAnswer = attempt[keyList[userAnswerIndex]]
                                    correctAnswer = attempt[keyList[correctAnswerIndex]] # Assigning correct answer
                                    
                                    # Checking for correct answer
                                    if correctAnswer == userAnswer:
                                        correctAnswerList[l] = correctAnswerList[l] + 1 # Adding for num of correct

                                    # Assigning user answers for printing to be either a) to d) or --- or N/A based on their input in quiz
                                    if userAnswer not in ['a)','b)','c)','d)']:
                                        if userAnswer == 'Unanswered':
                                            userAnswer = '---'
                                            totalAnswerList[l] = totalAnswerList[l] + 1

                                        else: 
                                            userAnswer = 'N/A'

                                    else: 
                                        userAnswer = ' ' + userAnswer
                                        totalAnswerList[l] = totalAnswerList[l] + 1

                                    userAnswerList.append(userAnswer)      # Store user answer
                                    l += 1
                            
                            userReport = f'{s+1}. ' + f"{attempt['UserID']:<20}" + '|'
                            
                            # Printing of user answer for each question
                            for i in userAnswerList:
                                if numOfQuestion >= 4:
                                    userReport += f'  {i}  |'
                                else: 
                                    userReport += f'{i:^{columnSpacing}} |'

                            # Makes printing nicer when grade is 0.00
                            if attempt['Grade (%)'] == '0.00':
                                grade = ' ' + '\33[31m' + attempt['Grade (%)'] + '\33[0m'
                            
                            # Makes priting of menu nicer when grade is 100
                            elif attempt['Grade (%)'] == '100.00':
                                grade = '\33[32m' + '100.0' +'\33[0m'
                            
                            else: 
                                grade = '\33[93m' + attempt['Grade (%)'] + '\33[0m'

                            userReport += '   ' + grade + ' %  | ' + attempt['Time Submitted'] + ' |'
                            userReport += f"\n{'-':->{barLength}}"

                            print(userReport)
                        

                        userReport = '|' + f"{' ':>22}"  + '|'  '\33[42m' +'\33[30m' + f"{'Summary (Total Users: '+ f'{s+1})':^{questionTextLength}} " + '\33[0m' +'|' + f"{' ':>12}" + '|' + f"{'|':>27}"
                        userReport += f"\n|{'Total Correct:':^22}|"
                        for i, totalCorrect in enumerate(correctAnswerList):
                            if numOfQuestion >= 4:
                                userReport += '\33[42m' +'\33[30m' + f" {totalCorrect} / {totalAnswerList[i]} " + '\33[0m' + '|' 
                            else: 
                                tmpStr = f"{totalCorrect} / {totalAnswerList[i]}"
                                userReport += '\33[42m' +'\33[30m' + f"{tmpStr:^{columnSpacing}} " + '\33[0m' + '|' 
                        
                        userReport += f"{' ':>12}" + '|'
                        userReport += f"{'|':>27}"
                        userReport += f"\n{'=':=>{barLength}}"
                        print(userReport)

                        userReport = f"\n{'=':=>24}"
                        userReport += '\n|' + '\33[42m' +'\33[30m' +  f"{'Legend':^22}" + '\33[0m' + '|'
                        userReport += '\n|' + '\33[41m' + f"{'--- = Unanswered':^22}" + '\33[0m' + '|'
                        userReport += '\n|' + '\33[41m' + f"{'N/A = Not Tested':^22}" + '\33[0m' + '|'
                        userReport += f"\n{'=':=>24}"
                        print(userReport)

                        # press enter to continue for more stats
                        input('\n' + '\33[42m' + 'Press enter for more statistics...' + '\33[0m' + '\n')

                        questionReport = '\n' + '\33[32m' + 'Statistics for all user inputs (options)' + '\33[0m'
                        questionReport += '\n========================================================================================================================'
                        questionReport += '\nQuestion\t\t\t\t\t|  Correct Option  |  Option A  |  Option B  |  Option C  |  Option D  |'
                        questionReport += '\n========================================================================================================================'

                        print(questionReport)

                        # for Numbering
                        i = 0
                        # for each question in question Pool, print the number of inputs for a) to d) based on all user inputs
                        # To give a statistics on how many people choose which options
                        for key in questionDict:
                            if questionDict[key][7] == chosenTopic:
                                countA = 0
                                countB = 0
                                countC = 0
                                countD = 0
                                # checks through each attempt 
                                for attempt in testStatistics[chosenOption]:
                                    keyList = []        # keylist to contain all keys of attempts
                                    for dictKey in attempt:
                                        keyList.append(dictKey)                             # append the key onto keyList
                                        if questionDict[key][0] == attempt[dictKey]:        # if question is found within attempt[key]
                                            userAnswerIndex = keyList.index(dictKey) + 2    # the index of the user's answer is found key +2        
                                    try:
                                        userAnswer = attempt[keyList[userAnswerIndex]]      # Store user answer
                                    except UnboundLocalError:   # when question is in question list but was not tested in attempt
                                        userAnswer = False
                                        break    
                                    # adds respective count for user inputs a to d
                                    if userAnswer == 'a)':
                                        countA += 1
                                    
                                    elif userAnswer == 'b)':
                                        countB += 1
                                    
                                    elif userAnswer == 'c)':
                                        countC += 1
                                    
                                    elif userAnswer == 'd)':
                                        countD += 1 

                                if userAnswer != False:
                                    questionLength = len(questionDict[key][0])
                                    i += 1
                                    questionTitle = questionDict[key][0]
                                    # for string formatting for if the question is length is too long, add and format new lines
                                    if questionLength >= 45 and questionLength < 80:
                                        questionTitle = questionTitle[:45] + f'|                  |            |            |            |            |'
                                        questionTitle += f'\n   {questionDict[key][0][45:]:<45}' 
                                    
                                    elif questionLength >= 80:
                                        questionTitle = questionTitle[:45] + f'|                  |            |            |            |            |'
                                        questionTitle += f'\n   {questionDict[key][0][45:80]:<45}' +'|                  |            |            |            |            |'
                                        questionTitle +=  f'\n   {questionDict[key][0][80:]:<45}'

                                    # Prints question, correct answer, and how many users input as options a to d
                                    print(f'{i}. {questionTitle:<45}|        {questionDict[key][5]}        '+ f'|     {countA}      |     {countB}      |     {countC}      |     {countD}      |')
                                    print('------------------------------------------------------------------------------------------------------------------------')
                
                        # press enter to continue for more stats
                        input('\33[42m' + 'Press enter for more statistics...' + '\33[0m' + '\n')

                        timeTakenList = []
                        gradeList = []
                        numOfQuestionAnswered = []
                        numOfCorrectAnswer = []
                        numUserAttempts = len(testStatistics[chosenOption])

                        # Appends data to appropriate list to be used for calculation later
                        # Since we need it to be used for calculations, we will have to change the datatype to int / float
                        for attempt in testStatistics[chosenOption]:    
                            # Append to timeTaken list
                            timeTakenList.append(int(attempt['Time Used (min)']))

                            # Append to gradeList
                            gradeList.append(float(attempt['Grade (%)']))

                            # Append to numOfQuestionAnswered list
                            numOfQuestionAnswered.append(int(attempt['Number of Question Answered']))

                            # Append to numOfCorrectAnswer list
                            numOfCorrectAnswer.append(int(attempt['Number of Correct Answer']))

                        # Formatting of statistic report printing
                        statisticReport =  '\n' + '\33[32m' + 'Statistics Report' + '\33[0m' +'\n==============================================' 
                        statisticReport += f'\nTotal Amount of Attempts: {numUserAttempts}'
                        statisticReport += '\n\nAverage Grade : ' + '\33[32m' + f'{statistics.mean(gradeList):.2f} %' + '\33[0m' 
                        statisticReport += '\nHighest Grade: \t' + '\33[32m' + f'{max(gradeList):.2f} %' + '\33[0m'
                        statisticReport += '\nLowest Grade: \t' + '\33[32m' + f'{min(gradeList):.2f} %' + '\33[0m' 
                        statisticReport += '\nMedian Grade : \t' + '\33[32m' + f'{statistics.median(gradeList):.2f} %' + '\33[0m' 
                        statisticReport += '\nMode Grade : \t' + '\33[32m' + f'{statistics.median(gradeList):.2f} %' + '\33[0m' 
                        
                        # Error occurs when there is only 1 attempt / 1 data in the dataset
                        # This is because standard deviation requires at least 2 sets of data
                        try:
                            statisticReport += '\nStandard Deviation : ' + '\33[32m' + f'{statistics.stdev(gradeList):.2f}' + '\33[0m' 
                            
                        # for when error occurs, add no string to it
                        except statistics.StatisticsError:
                            statisticReport += ''
                        finally:
                            statisticReport += f'\n\nAverage Number of Questions Answered: {statistics.mean(numOfQuestionAnswered):.2f} / {chosenOption}'
                            statisticReport += f'\nAverage Number of Correct Answers: {statistics.mean(numOfCorrectAnswer):.2f} / {chosenOption}'
                            statisticReport += f'\nAverage Time Taken: {statistics.mean(timeTakenList)} min'
                            statisticReport += '\n\n==============================================\n' 

                        print(statisticReport)

                        input('\33[42m' + 'Press enter to continue...' + '\33[0m' + '\n')


# This function helps the user go into the selected function given what they want to do in the admin menu
def mainMenu():
    
    # Formatting of main menu prompt
    mainMenu = '\n==============================================\n' + '\33[32m' + '\t\t' + '\33[4m'+ '\ Admin Menu /' + '\33[0m'
    mainMenu += '\n\n[1] User Settings\n[2] Setup Question Pool\n[3] Quiz Settings\n[4] Edit modules\n[5] Edit Courses\n[6] Generate Quiz Report\n[0] Logout'
    mainMenu += '\n\n==============================================\n>>> '

    while True:    
        try: 
            chosenOption = validationRange(start=0,end=6,question=mainMenu)
            
            # Quit
            if chosenOption == 0:
                print('\33[91m' + 'Logging out...' + '\33[0m')
                print('\33[32m' + 'Logged out successfully!' + '\33[0m' + '\n')
                break

            # User Settings
            elif chosenOption == 1:
                userSetting()
            
            # Setup Question Pool
            elif chosenOption == 2:
                setupQuestion()

            # Quiz Settings
            elif chosenOption == 3:
                quizSetting()

            elif chosenOption == 4:
                # Creats a dict of quiz settings by reading file quiz_setting.txt
                settingsDict = readFile(quizSettingTxt)

                if settingsDict == {}:   # If dictionary is empty,
                    settingsDict['1'] = ['Time for quiz: ','empty']
                    settingsDict['2'] = ['Number of Question for each Topic: ','empty']
                    settingsDict['3'] = ['Maximum number of attempts for each quiz: ','empty']
                    settingsDict['4'] = ['Randomize Options for quiz: ','empty']
                    settingsDict['5'] = ['Quiz tested for each Module: ','empty']
                    fn = open(quizSettingTxt,'w') # Write mode
                    for key in settingsDict:                                  # for each key in dict
                        fn.write(settingsDict[key][0] + '|' + settingsDict[key][1])   # Write settings onto txt file
                        fn.write('\n')                                # Add line feed for new line
                    fn.close()
                
                moduleSetting(dict=settingsDict)

            elif chosenOption == 5:
                courseSetting()

            # Generate Quiz Report
            else: 
                # list that contains all previous attempts stored in csv file
                dataList = []
                # Reading of previously stored data in csv file and store in a list
                with open(resultsCsv,'r') as file: # Read mode
                    writer = csv.DictReader(file)
                    for line in writer:
                        # Appends each attempt into list as a dictionary
                        dataList.append(dict(line))
                
                if dataList != []: # if dataList is not empty, go to generate report
                    generateReport(results = dataList)
                else:              # Error for when csv file is empty
                    print('\n'  + '\33[41m' + 'Error! No Attempt has been made for quiz!' + '\33[0m' + '\n')

        except EOFError:            # error for when user enters ctrl + z
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
        except KeyboardInterrupt:   # Error for when user enters ctrl + c
            print('\n'  + '\33[41m' + 'Error! Illegal character entered' + '\33[0m' + '\n')
            

# This function prompts the user to enter the correct password for the admin user stored in the userid_pswd.txt
# This will be the first function and the start of the programme entirely.
def adminLogin():

    # use time module to get seconds since 1970 and convert into Local time with .ctime
    currentTime = time.ctime(time.time())
    # Creates a temp dictionary that stores userID and passwords from the userid_pswd.txt
    tempDict = readFile(userID_pwdTxt)
    
    loginMenu = '\n==============================================\n' + '\33[32m' + '\t     ' + '\33[4m'+ '\ Welcome To Admin /' + '\33[0m'
    loginMenu += '\n\n\n' +'\33[41m'+ '\33[4m' +'Please Enter Password For Login' + '\33[0m' + f'\n[0] Quit Programme\n\n{currentTime}'
    loginMenu += '\n==============================================\n>>> '

    # login for admin
    while True:
        # Prompts the user the question. User input will be not shown on the terminal
        checkPwd = getpass.getpass(prompt=loginMenu)

        # Quitting of programme if user enters 0 
        if checkPwd == '0':
            print('\33[91m' + 'Terminating Programme...' + '\33[0m')
            print('\33[32m' + 'Programme Terminated' + '\33[0m' + '\n')
            break
        
        # Checking of valid password and subsequent login / error message 
        else: 
            checkPwd = ' pwd: wla' + checkPwd[::-1] 
            # Checks if password matchs accordingly to the admin user in the userid_pswd.txt
            if checkPwd == tempDict['1'][1]:
                input('\33[42m' + 'Login Successfully! Press enter to continue...' + '\33[0m' + '\n')
                mainMenu()
            else:
                print('\n'  + '\33[41m' + 'Error! Password is incorrect! Please Enter again.' + '\33[0m' + '\n')

adminLogin()