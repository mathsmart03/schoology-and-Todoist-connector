from csv import writer
from ics import Calendar
import requests
import todoist
import webbrowser

readKey = open("variableStorage.txt", "r")
readInputs = readKey.read()

iCalLink = readInputs.split("-")[0]
todoistAPItoken = readInputs.split("-")[1]
subjectsList = readInputs.split("-")[2].split("|")[:-1]
subjectsNumberList = readInputs.split("-")[3].split("|")[:-1]
todoistProjectID = readInputs.split("-")[4]

print(iCalLink)
print(todoistAPItoken)
print(subjectsList)
print(subjectsNumberList)


#
# dbUrl = []
# dbSub = []
# for events in schoologyCalender:
#     deadlineUF = events._end_time
#     deadlineF = str(deadlineUF)[:10].split("-")
#
#     urlUF = events.url[30:]
#     urlF = events.url[30:].split("/")[0:2]
#
#     if urlF[1] not in dbUrl:
#         dbUrl.append(urlF[1])
#
#     if urlF[0] not in dbSub:
#         dbSub.append(urlF[0])
#     print(f"{deadlineF} {events.url}")
#
# print(dbSub)
# print(dbUrl)
# print(deadlineF)
# for events in schoologyCalender:
#     events.

readCsv = open("completedTasksStorage.csv", "r")
ignoreLinks = readCsv.read().split("\n")[:-1]

schoologyCalender = Calendar(requests.get(iCalLink).text)
schoologyCalender = list(schoologyCalender.events)


schoologyCalenderProcessed = []
for events in schoologyCalender:
    if events.url not in ignoreLinks:
        schoologyCalenderProcessed.append(events)

myTodoist = todoist.api.TodoistAPI(token='{}'.format(todoistAPItoken), api_endpoint='https://todoist.com', session=None, cache='~/.todoist-sync/')
projectsData = myTodoist.projects.get_data(todoistProjectID)
sectionData = projectsData['sections']

schoologyCalenderLoop = 0
eventName = ""
courseUrl = ""
eventSubject = ""

def callback(urlLink):
    webbrowser.open_new(urlLink)

def courseEvent(Name):
    global schoologyCalenderLoop
    global currentEvent
    global eventName
    global eventUrl
    global  eventSubject

    eventSubject = Name
    subject["text"] = "Subject: " + eventSubject

def ignorePress():
    global schoologyCalenderLoop
    global currentEvent
    global eventName
    global eventUrl
    global  eventSubject

    storageCsv = open("completedTasksStorage.csv", "a+")
    storageCsvWriter = writer(storageCsv)
    storageCsvWriter.writerow([schoologyCalenderProcessed[schoologyCalenderLoop].url])
    storageCsv.close()

    schoologyCalenderLoop += 1
    currentEvent = schoologyCalenderProcessed[schoologyCalenderLoop]
    eventName = currentEvent.name
    eventUrl = currentEvent.url
    eventSubject = ""

    name["text"] = "Name: " + eventName
    subject["text"] = "Subject: " + eventSubject
    link["text"] = "Link: " + eventUrl
    link.bind("<Button-1>", lambda e: callback(eventUrl))
    progress["text"] = "{}/{}".format(schoologyCalenderLoop, len(schoologyCalenderProcessed))
    link.bind("<Button-1>", lambda e: callback(eventUrl))

def submitPress():
    global schoologyCalenderLoop
    global currentEvent
    global eventName
    global eventUrl
    global  eventSubject
    if eventSubject != "":
        storageCsv = open("completedTasksStorage.csv", "a+")
        storageCsvWriter = writer(storageCsv)
        storageCsvWriter.writerow([schoologyCalenderProcessed[schoologyCalenderLoop].url])
        storageCsv.close()

        newItem = myTodoist.add_item("[{}]({})".format(eventName, eventUrl), date_string="{}".format(str(schoologyCalenderProcessed[schoologyCalenderLoop]._end_time)[:10]))
        link.bind("<Button-1>", lambda e: callback(eventUrl))
        myTodoist.commit()
        for x in sectionData:
            if x['name'] == eventSubject:
                myTodoist.items.get_by_id(newItem['id']).move(section_id = int(x['id']))
                myTodoist.commit()
        schoologyCalenderLoop += 1
        currentEvent = schoologyCalenderProcessed[schoologyCalenderLoop]
        eventName = currentEvent.name
        eventUrl = currentEvent.url
        eventSubject = ""


        name["text"] = "Name: " + eventName
        subject["text"] = "Subject: " + eventSubject
        link["text"] = "Link: " + eventUrl
        link.bind("<Button-1>", lambda e: callback(eventUrl))
        progress["text"] = "{}/{}".format(schoologyCalenderLoop, len(schoologyCalenderProcessed))

        link.bind("<Button-1>", lambda e: callback(eventUrl))




import tkinter as tk

window = tk.Tk()
top = tk.Frame(window)
center = tk.Frame(window)
bottom = tk.Frame(window)
footer = tk.Frame(window)


window.configure(bg='#a3c6ff')
top.configure(bg='#a3c6ff')
center.configure(bg='#a3c6ff')
bottom.configure(bg='#a3c6ff')

name = tk.Label(text = "Name: This is the name", relief = "solid", borderwidth = 1, width = 70,font = ("Arial", 20))
name.pack(in_=top)

subject = tk.Label(text = "Subject: This is the subject.", relief = "solid", borderwidth = 1, width = 70, font = ("Arial", 20))
subject.pack(in_=top, pady = 10)

link = tk.Label(text = "Link: This is the link", relief = "solid", borderwidth = 1, width = 50, font = ("Arial", 20))
link.pack(in_=top)

progress = tk.Label(text = "0/0", font = ("Arial", 15))
progress.place(in_=footer)

for x in subjectsList:
    vars()[x] = tk.Button(text = "{}".format(x), highlightbackground='#a3c6ff', height = 5, width = 10, pady = 5, padx = 5, font = ("Arial", 15), command = lambda m = "{}".format(x): courseEvent(m))
    vars()[x].pack(in_= center, side=tk.LEFT, anchor=tk.CENTER, pady = 10)



ignore = tk.Button(text = "Ignore", command = ignorePress)
submit = tk.Button(text = "Submit", command = submitPress)

ignore.pack(in_=bottom, anchor=tk.CENTER)
submit.pack(in_=bottom, anchor=tk.CENTER)

top.pack()
center.pack()
bottom.pack()
footer.pack()


schoologyCalenderLoop = 0
currentEvent = schoologyCalenderProcessed[schoologyCalenderLoop]
eventName = currentEvent.name
eventUrl = currentEvent.url

name["text"] = "Name: " + eventName
subject["text"] = "Subject: " + eventSubject
link["text"] = "Link: " + eventUrl
link.bind("<Button-1>", lambda e: callback(eventUrl))
progress["text"] = "{}/{}".format(schoologyCalenderLoop, len(schoologyCalenderProcessed))

window.mainloop()
