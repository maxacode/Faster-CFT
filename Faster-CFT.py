#Boto3 Program that acts like CDK Deploy but for Cloudformation Directly. 

#Name of the input Cloudformation File. YAML or JSON. 
cftName = "demo.yaml"

#How often to check for template update. 
checkForFinishTime = 2 #Seconds


import boto3
import os, random, time
from datetime import datetime
from colorama import Fore, Back, Style

#Colors in the output
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))


#Vars for looping
key = "ResourceStatusReason"
word = "StackId"

#Session creation and region declaration.
session = boto3.Session(region_name='us-east-1')

#Boto3 Cloudformation client.
client = boto3.client('cloudformation')

#INTRO:
#This function creates the Cloudformation stack based on AWS CLI
def createStack():
    print()
    prGreen("--------------------------------")
    prGreen(f"Starting the Stack Deployment!\n StackName = {stackName} \n Template File: {cftName}")
    prGreen("--------------------------------")

    #Opening CF template and saving it to file. 
    with open(cftName) as template_fileobj:
        template_data = template_fileobj.read()
    client.validate_template(TemplateBody=template_data)
    
    #Deploying stack
    response = client.create_stack(
        StackName=stackName,
        TemplateBody= template_data,
        Capabilities= [
            'CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND',
            ])

  
   # os.system(command)
    print()
    print()
    constantUpdateEvents()


#Function that describes the stack events, so gets all events for that stack just created. 
def getStackInfo():
    #print("Line 36")
    global response
    #Getting all info for this stack. 
    response = client.describe_stack_events(
        StackName=stackName,
    )
    #print(response)

#Function that gets teh stack outputs.
def outputsOfCF(stackName):
    stackNameNew = stackName
    rep2 = client.describe_stacks(
        StackName=stackNameNew,
    )
     
    try:
        prCyan("\nStack Outputs:\n")
        outputs = rep2["Stacks"][0]["Outputs"]
        for x in outputs:
            prGreen(x)
    except:
        prRed("No Outputs\n\n")

    print()
    
    delete = input("1) Delete stack now or 2) New Stack: ")
    if delete == "1":
        deleteStack(stackName)
    elif delete == "2":
        actions()
 
#Gets all the Stack events and shows if it failed or the notes for that event. 
def getStatusAndReason():
    previousResponse = '1'
    previousResponse2 = '1'
    numsPrinted = []
    signature = signature2 = ''
    resourcesId = []
    while True:
        getStackInfo()
        #Getting the number of events in a stack
        stacksIDnum = str(list(response["StackEvents"]))
        stacksIDnum = stacksIDnum.count(word)
        #Looping through all events and printing out Status and Status Reason. Some wont have a status reason so it wont print. 
        for num in range(0,stacksIDnum):
            counter =+ 1
            tempString = response["StackEvents"][num]

            #If this event has a description for the event it will print both. 
            try:
                signature = response["StackEvents"][num]["LogicalResourceId"] + " : " +  response["StackEvents"][num]["ResourceStatus"] +"---" +response["StackEvents"][num]["ResourceStatusReason"]
            except:
                signature2 = response["StackEvents"][num]["LogicalResourceId"] + " : " + response["StackEvents"][num]["ResourceStatus"]

            #Checking to see if status updates are not printed on the screen twice. 
            if signature not in numsPrinted or signature2 not in numsPrinted:
                try:
                    timestamp = response["StackEvents"][num]["Timestamp"] 
                    currentResponse = str(timestamp) +  " : " + response["StackEvents"][num]["LogicalResourceId"] + " : " +  response["StackEvents"][num]["ResourceStatus"] +"---" +response["StackEvents"][num]["ResourceStatusReason"] #+ "---" + response["StackEvents"][num]["PhysicalResourceId"] 
                    signature = response["StackEvents"][num]["LogicalResourceId"] + " : " +  response["StackEvents"][num]["ResourceStatus"] +"---" +response["StackEvents"][num]["ResourceStatusReason"]
                    resourceId2 = response["StackEvents"][num]["PhysicalResourceId"] 
                    if resourceId2 not in resourcesId:
                        resourcesId.append(resourceId2)

                    prGreen(currentResponse)
                    previousResponse = currentResponse
                    numsPrinted.append(signature)
                    print()

                except:
                    #Printing just the event status since no description is available. 
                    timestamp = str(response["StackEvents"][num]["Timestamp"])
                    currentResponse2 = str(timestamp) + " : " + response["StackEvents"][num]["LogicalResourceId"] + " : " + response["StackEvents"][num]["ResourceStatus"]#+ "---" + response["StackEvents"][num]["PhysicalResourceId"] 
                    signature2 = response["StackEvents"][num]["LogicalResourceId"] + " : " + response["StackEvents"][num]["ResourceStatus"]
                    prPurple(currentResponse2)
                    resourceId2 = response["StackEvents"][num]["PhysicalResourceId"] 
                    if resourceId2 not in resourcesId:
                        resourcesId.append(resourceId2)
                    currentResponse2 = previousResponse2
                    numsPrinted.append(signature2)
                    print()
                   # print(numsPrinted)

            #If Respponse says its compltete then we will call function to get output of the Stack.
            if f"{stackName} : CREATE_COMPLETE" in signature2 or f"{stackName} : CREATE_COMPLETE" in signature:
              
                prGreen("Getting Resources: \n ")
                for ind in resourcesId:
                    prCyan(ind)
              
                prLightPurple("\nCompleted! Getting outputs\n")
                outputsOfCF(stackName)
                
            #Stack failed so will exit. 
            if "DELETE_COMPLETE" in signature2 or "ROLLBACK_COMPLETE" in signature:
                print("Failed: Exiting")
                exit()

        time.sleep(checkForFinishTime)

#Function to get updates on that Stack.
def constantUpdateEvents():

    prYellow("--------------------------------")
    prYellow(f"{stackName} Update! ")
    prYellow("--------------------------------")

    print()

    prCyan("--------------------------------------------------------------------------------------------------------------------------------")
    prCyan("-------------Timestamp-----------Logical ID -------Status------Status Reason----------------Physical Resource ID----------------")
    prCyan("--------------------------------------------------------------------------------------------------------------------------------")

    #while True:
    getStatusAndReason()

#Funciton to delete stack. 
def deleteStack(stackName):
    prGreen(f"\nDeleting Stack: {stackName} \n Response: \n")

    response = client.delete_stack(
    StackName=stackName,
    )
    prYellow(response)
    prGreen(f"\n\n\n Thank you for using this script!! \n \n")
    exit()

#Inital actions prompted to user. 
def actions():
    print()
    prRed("-------------------------------------------------------------------------------------------")
    prRed("To Create a New Stack - Just hit Enter/Return. or Enter '1' Delete Stack or '2' Stack Outputs:" )
    prRed("-------------------------------------------------------------------------------------------")

    action = input()
    if action == '':
        global stackName
        #Creating a stack name with a random number after. 
        stackName = "CFTStack" + str(random.randint(0,100000))
        createStack()
    elif action == "1":
        stackName = input("Enter Stack Name: ")
        deleteStack()
    elif action == "2":
        outputStackName = input("Enter Stack Name: ")
        outputsOfCF(outputStackName)

#Starting program with Actions function
actions()