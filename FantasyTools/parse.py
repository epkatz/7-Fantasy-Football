#Parses the XML File teams.xml and creates the fixture.
#######################################################
########################WARNING########################
##This function leaves a comma after the last fixture##
#so... don't leave it there or your shit will explode!#
######################(probably?)######################
#######################################################

import re
import random

xml = open("teams.xml")
players = open("players.txt", "r+")
teams = open("teams.txt", "r+")
data = open("initial_data.json", "w")
playersList = []
teamList = []
spotsList = ['QB', 'WR', 'RB', 'TE', 'PK', 'ST']

for line in xml:
    m = re.split("\"", line)
    if len(m) > 7:
        n = re.split(",", m[3]) 
        if (spotsList.count(m[5]) == 1) and (m[7][0:2] != 'FA'):
            players.write((n[1] + " " + n[0] + "," + m[7] + "," + m[5]).strip() + "\n")
            playersList.append([n[1], n[0], m[7], m[5]])
        elif (m[5] == 'TMDL'):            
            teams.write((n[1] + " " + n[0] + "," + m[7]).strip() + "\n")
            teamList.append([n[1], n[0], m[7]])
            
print "Parsing Complete"
print teamList
print playersList
print spotsList

data.write("[\n");
i = 1;
for player in playersList:
    data.write("\t{\n")
    data.write("\t\t\"model\": \"football.Player\",\n")
    data.write("\t\t\"pk\": " + str(i) + ",\n")
    data.write("\t\t\"fields\": {\n")
    data.write("\t\t\t\"full_name\": \""+player[0]+" "+player[1]+"\",\n")
    data.write("\t\t\t\"position\": \""+player[3]+"\",\n")
    data.write("\t\t\t\"salary\": "+str(random.randint(1,15))+"\n")
    data.write("\t\t}\n")
    data.write("\t},\n")
    i = i + 1
data.write("]")
