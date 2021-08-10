from collections import defaultdict
import CYKParse
import Tree
import re
import os
import time
import math
import numpy as np

def get_words(text):
    words = text.lower()
    words = words.split()   
    return words

def words(text, regex):   
    words = set()	
    for word in re.findall(regex, text):
        words.add(word.lower())
	
    return words

#a boolean variable for the initation status
haveGreeted = False
compared = False
lookingForLocation = False
lookingForAvailablity = False
lookingForHours = False
lookingForName = False
gotPhoneNum = False
cancelled = False
#a dictionary to hold name, time and location
requestInfo = {
    'customer': '',
    'time': '',
    'date': '',
    'phone': '',
    'service':'',
    'howMany': '',
    'type': ''
} ##  KNOWLEDGE-BASE 
f = open("customerFile.txt","a+")

def printV(*args):
    print(*args)

# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    sentenceTrees = {k: v for k,v in T.items()}
    # for k, v in T.items():
        # print(k, ' corresponding to ', v)
    # print(T)
    completeSentenceTree = max(sentenceTrees.keys())
    # print('getSentenceParse', completeSentenceTree)
    return T[completeSentenceTree]

def getName(sentence):
    global lookingForName
    global requestInfo   
    if (len(sentence) > 1):
        for i in range(len(sentence)):
            if sentence[i] == 'my' and sentence[i+1] == 'name':
                requestInfo['customer'] = sentence[i+3]
                lookingForName = True
                return
            elif sentence[i] == "it's" or sentence[i] == "i'm" :
                requestInfo['customer'] = sentence[i+1]
                lookingForName = True
                return
            elif sentence[i] == 'it' and sentence[i+1] == 'is': 
                requestInfo['customer'] = sentence[i+2]
                lookingForName = True
                return
            elif sentence[i] == 'this' and sentence[i+1] == 'is': 
                requestInfo['customer'] = sentence[i+2]
                lookingForName = True
                return
            elif sentence[i] == 'I' and sentence[i+1] == 'am': 
                requestInfo['customer'] = sentence[i+2]
                lookingForName = True
                return
    else:
        requestInfo['customer'] = sentence[0]
        lookingForName = True
        return


# Processes the leaves of the parse tree to pull out the user's request.
# def TELL(user's query)
def updateRequestInfo(Tr, tokens):
    global requestInfo
    global haveGreeted
    global compared
    global lookingForAvailablity
    global lookingForHours
    global lookingForLocation
    global lookingForName
    global cancelled
    WHQuestion = False  # a predicate to indicate if the query is one of the Wquestions or Hquestion
    #access key k, and value v in each item of the Tr dictionary
    for k, v in Tr.items():
        #if the key is an adverb, store a key 'time' with value v in the requestnfo dictionary 
        if k == 'Adverb':
            requestInfo['date'] = v
        if k == 'Verb' and v == 'cancel':
            cancelled = True
            print("BookIt:")
            print("We are sorry to hear that you are canceling your appointment.")
            print("Is there anything else I can do for you today?")
            tokens = get_words(input())
            if tokens[0] == 'yes':
                return 1
            elif tokens[0] == 'no':
                return 0
            else:
                print("Sorry I didn't get that.")
                return 1
        if k == 'Hour':
            requestInfo['time'] = v

        if k == 'Date':
            requestInfo['date'] = v

        if k == 'WQuestion' or k == 'HQuestion':
            WHQuestion = True

        if k == 'Noun':
            if v == 'appointment' or v == 'arrangement' or v == 'appointments' or v == 'arrangements':
                for k, v in Tr.items():
                    if k == 'Digit':
                        requestInfo['howMany'] = v
            elif v == 'pedicure' or v == 'manicure' or v == 'mani' or v == 'pedi' or v == 'pedicures' or v == 'manicures' or v == 'manis' or v == 'pedis':
                requestInfo['service'] = v
                for k, v in Tr.items():
                    if k == 'Digit':
                        requestInfo['howMany'] = v
                    if k == 'Type':
                        requestInfo['type'] = v
                    if k == 'Article':
                        if v == 'a':
                            requestInfo['howMany'] = 1
                        elif v == 'couple':
                            requestInfo['howMany'] = 2   
            elif v == 'phone':
                getPhone()               
            

    if WHQuestion == True:
        ASK(Tr, tokens)    #if it's a question, call ASK function
        return -1
    else:
        return 2



def ASK(question, tokens):
    global requestInfo

    for k, v in question.items():
        if k == 'WQuestion' and v == 'what':
            print("BookIt:")

            for k, v in question.items():
                if v == 'services' or v == 'service':
                    print("We offer gel, regular, paraffin, or deluxe pedicure/manicure. What service would you like?")
                    return
                elif v == 'staff':
                    staffAvailibility('staff')
                    return
                elif v == 'gel':
                    print("We use UV light that is used to help cure the gel or nail paint after each coating. This prevents chipping and helps the results last longer.")
                    return
                elif v == 'regular':
                    print("After a scrub that takes away all the dead cells, the manicurist then clips the nails to your desired size, shaping them according to your preference, the pushing of the cuticles, and the polishing of the nails.")
                    return 
        elif k == 'WQuestion' and v == 'where':
            for k, v in question.items():
                if k == 'Verb' and v == 'park':
                    print("BookIt:")

                    print("There are plenty 2 hour limit street parkings")
                    return
                elif k == 'Verb' and v == 'located':
                    reply(10)
        elif k == 'HQuestion':
            print("BookIt:")
            for k, v in question.items():
                if v == 'much':
                    # print("ASKING A QUESTION")
                    if (requestInfo['service'] == 'pedicure' or requestInfo['service'] == 'pedicures' or requestInfo['service'] == 'pedi' or requestInfo['service'] == 'pedis'):                    
                        if (requestInfo['type'] == 'gel'):
                            print(str(requestInfo['howMany']) + " " + requestInfo['type'] + " " + requestInfo['service'] + " would be $" + str(getPrice(requestInfo['howMany'],requestInfo['type'],1)))
                            return
                        elif (requestInfo['type'] == 'regular'):
                            print(str(requestInfo['howMany']) + " " + requestInfo['type'] + " " + requestInfo['service'] + " would be $" + str(getPrice(requestInfo['howMany'],requestInfo['type'],1)))
                            return
                        elif (requestInfo['type'] == 'paraffin'):
                            print(str(requestInfo['howMany']) + " " + requestInfo['type'] + " " + requestInfo['service'] + " would be $" + str(getPrice(requestInfo['howMany'],requestInfo['type'],1)))
                            return
                    else:
                        if (requestInfo['type'] == 'gel'):
                            print(str(requestInfo['howMany']) + " " + requestInfo['type'] + " " + requestInfo['service'] + " would be $" + str(getPrice(requestInfo['howMany'],requestInfo['type'],2)))
                            return
                        elif (requestInfo['type'] == 'regular'):
                            print(str(requestInfo['howMany']) + " " + requestInfo['type'] + " " + requestInfo['service'] + " would be $" + str(getPrice(requestInfo['howMany'],requestInfo['type'],2)))
                            return
                        elif (requestInfo['type'] == 'paraffin'):
                            price = getPrice(requestInfo['howMany'],requestInfo['type'],2)
                            print(str(requestInfo['howMany']) + " " + requestInfo['type'] + " " + requestInfo['service'] + " would be $" + str(price))
                            return
    answer = ''
    return answer

def getPrice(howMany,type,service):
    # print("CALCULATING THE PRICE")
    howMany = int(howMany)
    if (service == 1):  #pedicure
        if (type == "gel"):
            return 40*howMany
        elif (type == 'regular' or type == ''):
            return 25*howMany
        elif (type == 'paraffin'):
            return 30*howMany
    else:
        if (type == 'gel'):
            return 25*howMany
        elif (type == 'regular' or type == ''):
            return 15*howMany
        elif (type == 'paraffin'):
            return 20*howMany
    return 0
        
# This function contains the data known by our simple chatbot
def staffAvailibility(name):
    staff = ['Bebe', 'Tammy', 'Bao']
    for who in staff:
        if who == name:
            return 1 ## returns true
    if name == 'staff':
        print("Bebe, Tammy and Bao are available.")
    return 0
    #return staff

def services():
    services = ['manicure', 'pedicure']
    # A basic manicure is your standard manicure. 
    # "The nail tech will start off by soaking your hands in warm soapy water to soothe and soften dead skin cells," 
    # Higuchi says. "Then, the nail tech will file and buff, clean the cuticle, and massage your hands with a hand cream.

    return 0

def isSatisfiable(word):
    return 0 #returns false when customer is not happy 



def isComplete(knowledge_base, Tr):
    global requestInfo
    global gotPhoneNum
    done = False
    if (requestInfo['customer'] != '' and requestInfo['time'] != ' ' and requestInfo['date'] != '' and requestInfo['phone'] != ' ' and requestInfo['service'] != '' and requestInfo['howMany'] != ' ' and requestInfo['type'] != '' ):
        print("BookIt:")
        if requestInfo['phone'] == '':
            print("One last thing. What is your phone number?")
            requestInfo['phone'] = input()    
            gotPhoneNum = True
            print(requestInfo['customer'] + ", you are all set.\nIs there anything else that we can help you with today?")
            return 1        
            # isComplete(knowledge_base, Tr)
        else:
            print(requestInfo['customer'] + ", you are all set.\nIs there anything else that we can help you with today?")
            tokens = get_words(input())
            if tokens[0] == 'yes':
                done = False
            elif tokens[0] == 'no':
                done = True
            else:
                print("Sorry I didn't get that.")
                done = False
    if done == False:
        return 1 #returns true when all info has been obtained
    else:
        return 0


def getServices():
    return 0
def getPhone():
    return 0

def getDate():
    return 0

def getTime():
    return 0



# Format a reply to the user, based on what the user wrote.
def reply(num):
    salutation = ''
    time = 'now' # the default
    global f 
    global requestInfo
    global haveGreeted
    global compared
    global lookingForAvailablity
    global lookingForHours
    global lookingForLocation
    global lookingForName
    # if num == -1: #do nothing
    #     return 
    print("BookIt:")

    if num == 0:
        print("We are sorry to hear that you're canceling your appointment with us.\nIs there anything else I can help you with today "+requestInfo['customer'] + " ?")
        print("Customer: ")
        tokens = get_words(input()) 
        if (tokens[0] == 'no'):
            print("We hope to see you another time. Enjoy your day!")
        else:
            return     

    if not haveGreeted and requestInfo['customer'] != '' and num == -1:
        f = open("customerFile.txt", "r")
        f_read = f.readlines()
        flag = False    ## set to true if the current customer has previously called
        for each in f_read:
            words = each.split()
            if len(words) >= 1:
                if words[0] == requestInfo['customer']:
                    print("Welcome back, " + requestInfo['customer'])
                    flag = True
                    break
        if flag == False:
            f = open("customerFile.txt", "a+")
            print("Hello", requestInfo['customer'] + '.')
            f.write(requestInfo['customer'])
            f.write("\n")
        lookingForName = True
        haveGreeted = True
        print("What can I help you?")
        return
 
    # print(requestInfo)
    if num == 10:
        print("The store is located at 235 F street, Davis, California.")
        return
    if num == 1:
        print("Absolutely.")
        if (requestInfo['howMany']  != ''):
            print("What services would you like for a party of " + requestInfo['howMany'])
        else:
            print("What service would you like?")
        return
    elif num == 2:
        if (requestInfo['type'] != ''):
            if (requestInfo['time'] == '' and requestInfo['date'] == ''):
                print(str(requestInfo['howMany']) + " " + requestInfo['type'] + " " + requestInfo['service'] + " it is.")
                print("When would you like to come over?")
            else:
                print("Awesome! " + str(requestInfo['howMany']) + " " + requestInfo['type'] + " " + requestInfo['service'] + " at " +requestInfo['time'] + " " + requestInfo['date'] + " it is.")
        else:
            if requestInfo['service'] == '':
                print("What can I help you?")
            else:
                print("What type of " + requestInfo['service'] + " would you like?")
                print("We have gel, regular or paraffin.")
    
        return
    elif num == -1:
        return
    else:
        print("Sorry, I didn't get that.")
        return

def greeting():
    print("BookIt:")
    print("This is BookIt from Natural Nails & Spa. Who am I speaking with?")

def entropy(prob):
    if prob == 0:
        return 0
    return -(prob)*(np.log2(prob)) #- (1-prob)*(np.log2(1-prob))
# A simple hard-coded proof of concept.
def main():
    global f
    global requestInfo
    global lookingForName
    global gotPhoneNum
    global cancelled
    greeting()
    done  = False   #sets true when all information has been obtained and confirmed.
    staffAvailibility('Bebe')
    knowledge_base = defaultdict()
    tokens = ''
    skip = False
    num = -11
    ##open a file that stores previous customers' info
    while (isComplete(knowledge_base,tokens)):  
        if gotPhoneNum == True:
            skip == True     
        # print(T)
        # print(requestInfo)
        if skip == False:
            print("Customer: ")
            tokens = get_words(input())     
            if lookingForName == False:
                # print(tokens) 
                getName(tokens)
                if (len(tokens) < 2):
                    skip == True    
                reply(-1) 
            else:
                T, P = CYKParse.CYKParse(tokens, CYKParse.getGrammar())       
                num = updateRequestInfo(T, tokens)
        if (num == 1):
            reply(1)
        elif (num == 2):
            reply(2)
        elif (num == 10):
            reply(10)
        elif (num == -1):
            reply(-1)
        elif (num == 0):
            break
    
    print("BookIt:")
    if cancelled == False:
        print("Thank you for trusting in BookIt from Natural Nails & Spa.\nWe are looking forward to meeting you.\nHave a great day!")
    else:
        print("We hope to see you another time soon, " + requestInfo['customer']+" .\nEnjoy the day." )
    f.close()


main()