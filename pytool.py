import os
from unidecode import unidecode
from PIL import Image
import re

calendarFilesPages = os.listdir("dist/themes")

outputFile = open('dist/index.html', 'w')
map = str.maketrans("", "", "+?'")
map2 = str.maketrans("_", " ", ".jpg")

for i in calendarFilesPages:
    os.rename("dist/themes/" + i, "dist/themes/" + unidecode(i).translate(map))

calendarFilesPages = os.listdir("dist/themes")

def klasa(i):
    obraz = Image.open("dist/themes/" + i)
    x, y = obraz.size
    return "portrait" if y == 360 else "landscape"


calendarPages = [(unidecode(i).translate(map), klasa(i)) for i in calendarFilesPages]

prevTitle = ""
wrapper = ""
themeContainer = ""
a = []

# Loop through files
for i, css in calendarPages:
    themeTitle = "\n<h1 class='title'>" + i.translate(map2) + "</h1>\n"
    themeImg = "<img class='b-lazy {}' data-src='themes/{}' src='1px.gif'/>".format(css, i)
    themeImg += "<noscript><img src='" + i + "' /></noscript>"
    title = re.sub(r"\W|jpg|\d|_", '', i)

    # Close container
    if title != prevTitle and prevTitle != "":
        themeContainer += "".join(list(reversed(a)))
        themeContainer += "</div>\n"
        wrapper += themeContainer
        themeContainer = ""
        a = []

    # New container
    if title != prevTitle:
        themeContainer += themeTitle
        themeContainer += "<div class='container'>\n"

    a.append("  <div class='frame'>" + themeImg + "</div>\n")
    prevTitle = title

# Append last theme
themeContainer += "".join(list(reversed(a)))
themeContainer += "</div>\n"
wrapper += themeContainer

templateFile = open('template.html', 'r')
template = templateFile.read()

if template.find("{placeholder}") != -1:
    html = template.replace("{placeholder}", wrapper)

outputFile.writelines(html)

templateFile.close()
outputFile.close()
