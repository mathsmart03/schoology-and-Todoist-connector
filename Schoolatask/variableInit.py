iCalLink = ""
subjectsList = ["Math","ELA","Science","Social Studies","Band","Info Tech","PE","Study Skills","Guidance","Media Center","German", "Art"]
subjectsNumberList = ["2638213180", "2638201246", "2638213814", "2638207207", "2638224582", "2638219518", "2638190561", "2638238557", "2638192015", "2638195737", "2638218654", "2638224091"]
todoistAPItoken = ""
todoistProjectID = ""
ignoreDate = ""
import time

try:
    from csv import writer
    from ics import Calendar
    import requests
    import todoist
    import os
    import tkinter as tk
except ModuleNotFoundError:
    print("Hey, you didn't import the modules properly. Redo that step to make sure you are on the right track.")


if iCalLink == "" or todoistAPItoken == "" or len(subjectsList) == 0:
    print("Properly fill out all of the inputs.")
else:
    openKey = open('variableStorage.txt', "w")
    openKey.truncate(0)
    openKey.write("{}-{}-".format(iCalLink, todoistAPItoken))

    for loop in subjectsList:
        openKey.write("{}|".format(loop)).bit_length()

    openKey.write("-")

    for loop in subjectsNumberList:
        openKey.write("{}|".format(loop))

    openKey.write("-{}".format(todoistProjectID))

    openKey.close()

os.remove("completedTasksStorage.csv")

schoologyCalender = Calendar(requests.get(iCalLink).text)
schoologyCalender = list(schoologyCalender.events)

ignoreYear = int(ignoreDate.split("-")[0])
ignoreMonth = int(ignoreDate.split("-")[1])
ignoreDay = int(ignoreDate.split("-")[2])
print(ignoreYear)

openCsv = open("completedTasksStorage.csv", "w")
openCsvWriter = writer(openCsv)

for events in schoologyCalender:
    deadlineUF = events._end_time
    deadlineYear = int(str(deadlineUF)[:10].split("-")[0])
    deadlineMonth = int(str(deadlineUF)[:10].split("-")[1])
    deadlineDay = int(str(deadlineUF)[:10].split("-")[2])

    if deadlineYear < ignoreYear:
        openCsvWriter.writerow(["{}".format(events.url)])
        print(deadlineYear, " ", deadlineMonth, " ", deadlineDay)
    elif deadlineMonth < ignoreMonth:
        openCsvWriter.writerow(["{}".format(events.url)])
        print(deadlineYear, " ", deadlineMonth, " ", deadlineDay)
    elif deadlineDay < ignoreDay:
        openCsvWriter.writerow(["{}".format(events.url)])
        print(deadlineYear, " ", deadlineMonth, " ", deadlineDay)




openCsv.close()

myTodoist = todoist.api.TodoistAPI(token='{}'.format(todoistAPItoken), api_endpoint='https://todoist.com', session=None, cache='~/.todoist-sync/')
projectsData = myTodoist.projects.get_data(todoistProjectID)
sectionData = projectsData['sections']

sectionNames = []
for x in sectionData:
    sectionNames.append(x['name'])

notCreated = []
for x in subjectsList:
    if x not in sectionNames:
        notCreated.append(x)

for x in notCreated:
    myTodoist.sections.add('{}'.format(x), project_id=todoistProjectID)

print(notCreated)
myTodoist.commit()
