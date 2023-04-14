#Authors: Andrew Alcala and Jonathan Ramirez
#Course Number: COSC 499
#Date Completed: 4/7/23
#Purpose: Takes info from Destiny 2 API to then  calculate success rate of an in-game mode
#Input: Player's Loadout
#Output: A percentage on the probability of success
#Issues: Integrating into our website so this file and the html file can send info back and forth when requested



import math 
import requests
import jinja2
#from app import x

#Jonathan Ramirez
reqUrl = "https://www.bungie.net/Platform/Destiny2/Manifest/DestinyActivityDefinition/2103025314/"

headersList0 = {
 "Accept": "*/*",
 "x-api-key": "411922366414449c9f73045e743776a1" 
}

payload0 = ""

#sends a request to the Bungie API using a specific hash code from reqUrl
response0 = requests.request("GET", reqUrl, data=payload0,  headers=headersList0)

#allows the data to be accessed 
d=response0.json()

#adds needed hash codes from d to a list 

print(d.get('Response')['modifiers'][0])
print((d.get('Response')['modifiers'][0].get('activityModifierHash')))
modifier=[str(d.get('Response')['modifiers'][0].get('activityModifierHash')),str(d.get('Response')['modifiers'][4].get('activityModifierHash')), str(d.get('Response')['modifiers'][19].get('activityModifierHash')), str(d.get('Response')['modifiers'][20].get('activityModifierHash')), str(d.get('Response')['modifiers'][21].get('activityModifierHash'))] #in order to get the data we have to go through 2 dictionaries to get the data using a multiple keys
j=[]


#Jonathan Ramirez and Andrew Alcala
#requests data using the hash codes
for i in range(len(modifier)):
    reqUrl = "https://www.bungie.net/Platform/Destiny2/Manifest/DestinyActivityModifierDefinition/"+modifier[i]+"/"

    headersList = {
    "Accept": "*/*",
    "x-api-key": "411922366414449c9f73045e743776a1" 
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

    #appends the retrieved data into an empty list
    j.append(str(response.json().get('Response')['displayProperties'].get('description')))
print(j)                                                #makes a list of all the modifiers; each element is a string

#Andrew Alcala
#breaks apart the info into a string list
a= j[0].split()
b=j[1].split()                                          #takes the 2nd string of words and splits into a list
c = j[2].split()
d = j[3].split()
e = j[4].split()

print(d)                                                 #prints the weekly surge

champions = []
weapons =[]

#if the champion foe's is one of these add the specified weapons to a list
if 'Barrier' in b:
    champions.append(b[4])
if 'Unstoppable' in b:
    champions.append(b[7])
if 'Overload' in b:
    champions.append(b[7])

for i in range(len(champions)):                                             #adds the weapons needed for each champion to then check later
    if champions[i] == 'Unstoppable':
        weapons += ['Scout', 'Glaive']
    elif champions[i] == 'Barrier':
        weapons +=['Pulse', 'Sidearm']
    elif champions[i] == 'Overload':
            weapons +=['Auto', 'Submachine', 'Bow', 'Sword']
