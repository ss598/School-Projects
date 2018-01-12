## Shelly Smith
## CS 3378
## Mini project
##
## This was a regex project for Theory of Automata. The assignment was to create a
##   script that would parse through the Texas State Computer Science website and create 
##   a folder of text files with the names and information of all the Computer Science 
##   professors. One challenge was that one of the professors had an accent on her name, 
##   which had to be accounted for.

import urllib.request
import re
import os
import ast

sourceUrl = "https://cs.txstate.edu/accounts/faculty/"
baseUrl = 'https://cs.txstate.edu'

directory = "results/"
if not os.path.exists(directory):
    os.makedirs(directory)

request = urllib.request.Request(sourceUrl)
response = urllib.request.urlopen(request)
responseData = response.read()

facultyArray = re.findall(r'<h3 class="title"><a href="(.*?)">', str(responseData))
for facultyMember in facultyArray:

    request = urllib.request.Request(baseUrl + facultyMember)
    response = urllib.request.urlopen(request)
    responseData = response.read()

    nameArray = re.findall(r'<h3 class="heading-title pull-left">(.*?)</h3>',str(responseData))
    h3Array = re.findall(r'<h3 class="panel-title">(.*?)</h3>.*?<p>(.*?)</p>', str(responseData))
    emailArray = re.findall(r'user=(.*?)&domain=(.*?)&font', str(responseData))
    linksArray = re.findall(r'href="(.*?)">(.*?)</a>', str(responseData))


    nameFormatted = ""
    education = ""
    researchInterests = ""
    webpage = "No webpage for this professor"

    for name in nameArray:
        nameFormatted = re.sub(r"(\\n+ +)+", " ", name)
        nameFormatted = nameFormatted.strip()

    if '\\x' in nameFormatted:
        nameAsBytes = bytes(nameFormatted, 'latin1')
        nameAsBytes = ast.literal_eval(str(nameAsBytes).replace('\\\\', '\\'))
        nameFormatted = nameAsBytes.decode('utf8')

    for section in h3Array:
        if section[0] == "Education":
            education = section[1]
        if section[0] == "Research Interests":
            researchInterests = section[1]

    for link in linksArray:
        if link[1] == "Homepage":
            webpage = link[0]

        filename = directory + re.sub(r"[\.+ +]+", "", nameFormatted) + ".txt"
        file = open(filename, 'w')
        file.write ("Name: " + nameFormatted + "\n")    
        file.write ("Education: " + education + "\n")
        file.write ("Research Interests: " + researchInterests + "\n")
        file.write ("Email: " + emailArray[0][0] + "@" + emailArray[0][1] + "\n")
        file.write ("Webpage: " + webpage)

        file.close()


