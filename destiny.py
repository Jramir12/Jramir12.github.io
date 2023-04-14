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
from flask import Flask

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

#Andrew Alcala
#if the champion foe's is one of these add the specified weapons to a list
if b[4] == 'Barrier':
    champions.append(b[4])
if b[7] == 'Unstoppable':
    champions.append(b[7])

for i in range(len(champions)):                                             #adds the weapons needed for each champion to then check later
    if champions[i] == 'Unstoppable':
        weapons += ['Scout', 'Glaive']
    elif champions[i] == 'Barrier':
        weapons +=['Pulse', 'Sidearm']
    elif champions[i] == 'Overload':
            weapons +=['Auto', 'Submachine', 'Bow', 'Sword']

count = 1
champ = 0
oc = 0

#Author: Andrew Alcala
#-----------------------------------------------------------------------------
loadout = [1802, 'Solar', 'Kinetic Scout', 'Void Glaive', 'Arc Rocket']

#makes a list of the active weekly overcharged weapon
overcharged = [e[3]]  
print("This weeks overcharged weapon is ", overcharged)                      #['Machine']

#adds the weapons list using indexing to the overcharged list
for i in range(len(weapons)):
    overcharged.append(weapons[i])

#holds the weekly (changes on a weekly basis) and seasonal (unchanging until 5/23) surge 
elements = [c[4], d[4]]                     #['Void', 'Strand'] as of (4/7)
mod = [1820, champions, overcharged, elements]


for j in range(2,4):                                 #checks if champ weapons are in the loadout
    r = loadout[j].split()                                                             #['strand', 'Glaive']
    for i in range(len(weapons)):                           
        if r[1] == weapons[i]:
            champ = champ + .25

sub = loadout[1]
if sub in elements:
    oc = oc +.15

#checks if the elements or the weapon but not both from player's weapons from loadout synergize
#if so add to a counter 
for element in loadout[2:]:
    x = element.split()
    if x[0] in elements or x[1] in overcharged:
        oc = oc +.15

print(elements)                                    #prints the weekly surge (changes every Tuesday) with the seasonal; seasonal won't change until 5/23


#takes player level and compares it to level cap to determine multiplier
if loadout[0] >= mod[0]:                                                   #if power is at or above 1815 it will only be 100%  
	loadout[0] = mod[0]
	pow = 1
if mod[0]-5 < loadout[0] <= mod[0]:
	pow = .9
if mod[0]-10 < loadout[0] <= mod[0]-5:
	pow = .8
if mod[0]-15 < loadout[0] <= mod[0]-10:
	pow = .7
if 0 < loadout[0] <= mod[0]-15:                                         #0 < 1802 <= 1805
	pow = (1-(.6**2 *(loadout[0]/mod[0])))                                    #.6^2 * (1805/1820) = .356...


if oc < 0.5:
    oc = 1 - oc

if champ < .5:
    champ = 1 - champ

#gives a probability of success based on your loadout and the API given active modifiers
input = float(.9 - (oc*pow*champ))                                              
rate = 1.1 *math.log((input)**.5) + .7                                           
print(rate*100)
