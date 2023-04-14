#Author: Jonathan Ramirez
#Course Number: COSC 499
#Date Completed:4/7/2023
#Description: This program essentially creates the website and local Url so that we are able to put the wanted info onto our site
#Input:N/A
#output: Makes the website exist through http://127.0.0.1:8000 when ran all together with the other files
#things that need attention: being able to change the given Url

from views import views
import math
from destiny import champions,weapons,c,d,e
from flask import Flask, redirect, render_template, request


#registers and records operations to executed( activates website)
app = Flask(__name__)
app.register_blueprint(views, url_prefix="")

@app.route("/", methods=["POST","GET", "DELETE"])
def index():
    count = 1
    champ = 0
    oc = 0

    #Author: Andrew Alcala
    #-----------------------------------------------------------------------------
    loadout = [int(request.form['Plevel']), request.form['SubEle'], request.form['Primwep'], request.form['Secwep'], request.form['Hevwep']]            #grabs data from user input from website

    #makes a list of the active weekly overcharged weapon
    overcharged = [e[3]]  
    #print("This weeks overcharged weapon is ", overcharged)                      #['Machine']  as of (4/7 - 4/11)

    #adds the weapons list using indexing to the overcharged list
    for i in range(len(weapons)):
        overcharged.append(weapons[i])

    #holds the weekly (changes on a weekly basis) and seasonal (unchanging til 5/23) surge 
    elements = [c[4], d[4]]                     #['Void', 'Strand'] as of (4/7 - 4/11)
    mod = [1820, champions, overcharged, elements]


    for j in range(2,4):                                 #checks if champ weapons are in the loadout
        r = loadout[j].split()                                                             #['strand', 'Glaive']
        for i in range(len(weapons)):                           
            if r[1] == weapons[i]:
                champ = champ + .25

    sub = loadout[1]
    if sub in elements:                                     #checks the subclass for 2 different scenarios
        oc = oc +.15
    elif sub == elements[1] and loadout[2].split()[0] == 'Kinetic':
        oc = oc + .15

    #checks if the elements or the weapon but not both from player's weapons from loadout synergize
    #if so add to a counter 
    for element in loadout[2:]:
        x = element.split()
        if x[0] in elements or x[1] in overcharged:
            oc = oc +.15

    #print(elements)                                    #prints the weekly surge (changes every Tuesday) with the seasonal; seasonal won't change until 5/23

    if oc < 0.45:
        oc = 1 - oc

    if champ <=.35:
        champ = 2*champ
    if champ > .5:
        champ = champ/2

    #takes player level and compares it to level cap to determine multiplier
    if loadout[0] >= mod[0]:                                                   #if power is at or above 1815 it will only be 100%  
        loadout[0] = mod[0]
        pow = 1+(1-oc)+(1-champ)
    if mod[0]-5 < loadout[0] <= mod[0]:
        pow = .9
    if mod[0]-10 < loadout[0] <= mod[0]-5:
        pow = .8
    if mod[0]-15 < loadout[0] <= mod[0]-10:
        pow = .7
    if 0 < loadout[0] <= mod[0]-15:                                         #0 < 1802 <= 1805
        pow = (1-(.6**2 *(loadout[0]/mod[0])))                                    #.6^2 * (1805/1820) = .356...


    #print(champ)
    #gives a probability of success based on your loadout and the API given active modifiers
    input = float(1 - (oc*pow*champ))
    rate = 1.1 *math.log((input)**.5) + .9                                           
    #print(rate*100)
    return render_template("index.html", name = 100*rate) #returns the value of success 


#  this provides the Url and runs the website
if __name__ == '__main__':
    app.run(debug=True, port=8000)
