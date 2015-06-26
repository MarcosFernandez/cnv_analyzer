#!/usr/bin/env python

import os
import json
import argparse
import sys
import re

def buildStyleSheet():
        ''' Add HTML header to a given vector '''
        cssContents = []
        cssContents.append(" #title\n")
        cssContents.append(" {\n")
        cssContents.append("   font-family: \"Sans-Serif\";\n")
        cssContents.append("   font-size: 20px;\n")
        cssContents.append("   text-align: center;\n")
        cssContents.append("   color: #039;\n")
        cssContents.append("   border-collapse: collapse;\n")
        cssContents.append(" }\n")
        cssContents.append(" #section\n")
        cssContents.append(" {\n")
        cssContents.append("   font-family: \"Sans-Serif\";\n")
        cssContents.append("   font-size: 18px;\n")
        cssContents.append("   text-align: center;\n")
        cssContents.append("   color: #039;\n")
        cssContents.append("   border-collapse: collapse;\n")
        cssContents.append(" }\n")
        #LINKS TABLE
        cssContents.append("#linksTable-b\n")
        cssContents.append("{\n")
        cssContents.append("   font-family: \"Sans-Serif\";\n")
        cssContents.append("	font-size: 12px;\n")
        cssContents.append("	background: #fff;\n")
        cssContents.append("	margin: 5px;\n")
        cssContents.append("	width: 200px;\n")
        cssContents.append("	border-collapse: collapse;\n")
        cssContents.append("	text-align: left;\n")
        cssContents.append("}\n")
        cssContents.append("#linksTable-b th\n")
        cssContents.append("{\n")
        cssContents.append("	font-size: 14px;\n")
        cssContents.append("	font-weight: normal;\n")
        cssContents.append("	color: #039;\n")
        cssContents.append("	padding: 10px 8px;\n")
        cssContents.append("	border-bottom: 2px solid #6678b1;\n")
        cssContents.append("}\n")
        cssContents.append("#linksTable-b td\n")
        cssContents.append("{\n")
        cssContents.append("	border-bottom: 1px solid #ccc;\n")
        cssContents.append("	color: #669;\n")
        cssContents.append("	padding: 6px 8px;\n")
        cssContents.append("}\n")
        cssContents.append("linksTable-b tbody tr:hover td\n")
        cssContents.append("{\n")
        cssContents.append("	color: #009;\n")
        cssContents.append("}\n")
        #BLUE TABLE
        cssContents.append(" #hor-zebra\n")
        cssContents.append(" {\n")
        cssContents.append("   font-family: \"Sans-Serif\";\n")
        cssContents.append("   font-size: 12px;\n")
        cssContents.append("   margin: 0px;\n")
        cssContents.append("   width: 100%;\n")
        cssContents.append("   text-align: left;\n")
        cssContents.append("   border-collapse: collapse;\n")
        cssContents.append(" }\n")
        cssContents.append(" #hor-zebra th\n")
        cssContents.append(" {\n")
        cssContents.append("   font-size: 14px;\n")
        cssContents.append("   font-weight: normal;\n")
        cssContents.append("   padding: 10px 8px;\n")
        cssContents.append("   color: #039;\n")
        cssContents.append("   border-bottom: 2px solid #6678b1;\n")
        cssContents.append("   border-right: 1px solid #6678b1; \n")
        cssContents.append("	border-left: 1px solid #6678b1;\n")
        cssContents.append(" }\n")
        cssContents.append(" #hor-zebra td\n")
        cssContents.append(" {\n")
        cssContents.append("   padding: 8px;\n")
        cssContents.append("   color: #669;\n")
        cssContents.append("   border-right: 1px solid #6678b1; \n")
        cssContents.append("	border-left: 1px solid #6678b1;\n")
        cssContents.append(" }\n")
        cssContents.append(" #hor-zebra .odd\n")
        cssContents.append(" {\n")
        cssContents.append("   background: #e8edff;\n")
        cssContents.append("   border-right: 1px solid #6678b1; \n")
        cssContents.append("	border-left: 1px solid #6678b1;\n")
        cssContents.append(" }\n")
        #GREEN TABLE
        cssContents.append(" #green \n")
        cssContents.append(" {\n")
        cssContents.append("   font-family: \"Sans-Serif\";\n")
        cssContents.append("   font-size: 12px;\n")
        cssContents.append("   margin: 0px;\n")
        cssContents.append("   width: 100%;\n")
        cssContents.append("   text-align: left;\n")
        cssContents.append("   border-collapse: collapse;\n")
        cssContents.append(" }\n")
        cssContents.append(" #green th\n")
        cssContents.append(" {\n")
        cssContents.append("   font-size: 14px;\n")
        cssContents.append("   font-weight: normal;\n")
        cssContents.append("   padding: 10px 8px;\n")
        cssContents.append("   color: #2b9900;\n")
        cssContents.append("   border-bottom: 2px solid #66b16f;\n")
        cssContents.append("   border-right: 1px solid #66b16f; \n")
        cssContents.append("	border-left: 1px solid #66b16f;\n")
        cssContents.append(" }\n")
        cssContents.append(" #green td\n")
        cssContents.append(" {\n")
        cssContents.append("   padding: 8px;\n")
        cssContents.append("   color: #578055;\n")
        cssContents.append("   border-right: 1px solid #66b16f; \n")
        cssContents.append("	border-left: 1px solid #66b16f;\n")
        cssContents.append(" }\n")
        cssContents.append(" #green .odd\n")
        cssContents.append(" {\n")
        cssContents.append("   background: #eaffe8;\n")
        cssContents.append("   border-right: 1px solid #66b16f; \n")
        cssContents.append("	border-left: 1px solid #66b16f;\n")
        cssContents.append(" }\n")
        #LINKS
        cssContents.append("a.link:link {font-family: \"Sans-Serif\";font-size: 12px;color: #039;text-decoration:none;}")
        cssContents.append("a.link:visited {font-family: \"Sans-Serif\";font-size: 12px;color: #039;text-decoration:none;}")
        cssContents.append("a.link:hover {font-family: \"Sans-Serif\";font-size: 12px;color: #039;text-decoration:underline;}")
        #P BLUE
        cssContents.append(" #descriptionBlue \n")
        cssContents.append(" {\n")
        cssContents.append("   font-family: \"Sans-Serif\";\n")
        cssContents.append("   font-size: 14px;\n")
        cssContents.append("   text-align: left;\n")
        cssContents.append("   color: #039;\n")
        cssContents.append("   border-collapse: collapse;\n")
        cssContents.append(" }\n")
        #P GREEN
        cssContents.append(" #descriptionGreen \n")
        cssContents.append(" {\n")
        cssContents.append("   font-family: \"Sans-Serif\";\n")
        cssContents.append("   font-size: 14px;\n")
        cssContents.append("   text-align: left;\n")
        cssContents.append("   color: #009900;\n")
        cssContents.append("   border-collapse: collapse;\n")
        cssContents.append(" }\n")
        #P SUBTITLE BLUE
        cssContents.append(" #subtitleBlue \n")
        cssContents.append(" {\n")
        cssContents.append("   font-family: \"Sans-Serif\";\n")
        cssContents.append("   font-size: 16px;\n")
        cssContents.append("   font-weight: bold;\n")
        cssContents.append("   text-decoration:underline;\n")
        cssContents.append("   text-align: left;\n")
        cssContents.append("   color: #039;\n")
        cssContents.append("   border-collapse: collapse;\n")
        cssContents.append(" }\n")
        #P SUBTITLE GREEN
        cssContents.append(" #subtitleGreen \n")
        cssContents.append(" {\n")
        cssContents.append("   font-family: \"Sans-Serif\";\n")
        cssContents.append("   font-size: 16px;\n")
        cssContents.append("   font-weight: bold;\n")
        cssContents.append("   text-decoration:underline;\n")
        cssContents.append("   text-align: left;\n")
        cssContents.append("   color: #009900;\n")
        cssContents.append("   border-collapse: collapse;\n")
        cssContents.append(" }\n")

        return cssContents

#1. ARGUMENT PARSING
parser = argparse.ArgumentParser(prog="createHtml",description="Create HTML from JSON file.", formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=350))

general_group = parser.add_argument_group('Input')
general_group.add_argument('--json_file', dest="json_file",help='JSON file to create a HTML file')

output_group = parser.add_argument_group('Output')
output_group.add_argument('--output', dest="output", help='HTML output file')

args = parser.parse_args()

if args.json_file == "":
     raise Exception("Sorry!! Json File was not defined!!")

if args.output == "":
     raise Exception("Sorry!! Output File was not defined!!")


#2. CREATE DICTIONARY FROM JSON FILE
jsonDirectory = {}
with open(args.json_file) as json_file:
    jsonDirectory = json.load(json_file)

#3. PARSE JSON DICTIONARY

#3.1 HTML CONTENT
htmlContent = []
htmlContent.append("<HTML>\n")

htmlContent.append(" <HEAD>\n")
htmlContent.append(" <STYLE TYPE=\"text/css\">\n")

htmlContent.append("  <!--\n")
htmlContent.append("   @import url(\"style.css\"); \n")
htmlContent.append("  -->\n")

htmlContent.append(" </STYLE>\n")
htmlContent.append(" </HEAD>\n")

htmlContent.append(" <BODY>\n")

htmlContent.append("  <H1 id=\"title\"> <U> GENE COPY NUMBER </U> </H1>\n")

htmlContent.append("  <TABLE id=\"hor-zebra\">\n")

isOdd = False

for title in sorted(jsonDirectory):
     conceptValue = jsonDirectory[title]

     rowSetup = ""
     if isOdd == True: 
         rowSetup = "   <TR class=\"odd\">\n"
         htmlContent.append(rowSetup)
         isOdd = False
     else:
         rowSetup = "   <TR>\n"
         htmlContent.append(rowSetup)
         isOdd = True

     htmlContent.append("      <TH scope=\"col\"> " + title + " </TH> <TH> Concept </TH> <TH> Value </TH>\n")
     htmlContent.append("   </TR>\n")

     
     #3.1 Parse concept value
     for fields in sorted(conceptValue):
         name = fields
         value = conceptValue[fields]
         htmlContent.append(rowSetup)
         htmlContent.append("      <TD> </TD> <TD> " + name + " </TD> <TD> " + str(value) + " </TD>\n")
         #3.2 Close row
         htmlContent.append("   </TR>\n")

htmlContent.append("  </TABLE> \n")
htmlContent.append(" </BODY> \n")
htmlContent.append("</HTML>\n")

#4 PRINT HTML DOCUMENT
with open(args.output, 'w') as htmlDocument:
    for line in htmlContent:
        htmlDocument.write(line+ '\n')

#5 RECOVER HTML VECTOR
cssContent = buildStyleSheet()
with open(os.path.dirname(args.output) + "style.css", 'w') as cssDocument:
    for line in cssContent:
        cssDocument.write(line+ '\n')







