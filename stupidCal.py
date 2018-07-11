#make some very specific calendar application
import math
import datetime as dt
import os
import sys

#Starters
print('hi, this will help you automatically generate your work-calendar and try to do the thinking for you. First I will need to know all about what you are trying to do (and your blood group).')


################################Get all the inputs ##############################
task=raw_input('Enter task name: ')
#today's date:
#now = dt.date.today()
#print(str(now))

#deadline date
def ObtainDeadline():
    isValid=False
    while not isValid:
        userIn = raw_input('When is the deadline? dd/mm/yy: ')
        try: # strptime throws an exception if the input doesn't match the pattern
            deadline = dt.datetime.strptime(userIn, '%d/%m/%y')
            isValid=True
        except:
            print "Boo, try again!\n"
    return deadline
#test the function
deadline = ObtainDeadline()
#print(deadline)

#starting date
def ObtainStartDate():
    isValid=False
    while not isValid:
        userIn = raw_input('When do you want to start? dd/mm/yy: ')
        try: # strptime throws an exception if the input doesn't match the pattern
            startdate = dt.datetime.strptime(userIn, '%d/%m/%y')
            isValid=True
        except:
            print "Boo, try again!\n"
    return startdate

StartDate = ObtainStartDate()
#print(StartDate)

# Defining the starting date
#start = dt.datetime.now()
start = StartDate


totalHours=float(input('What is the total time required for the task (in h)?'+' '))
timeBuffer=int(raw_input('How many days would you like as a buffer before the deadline? '))
#maxHours=raw_input('Maximum hours working on this per day: ')

def ObtainMaxHours() :
    while True :
        maxHours = float(raw_input('Maximum hours working on this per day: '))
        if workHours <= maxHours:
            return maxHours
        else :
            print('You will need to work more than that every day...')

startWork=int(input('Earliest start for work each day? (hh in 24-hour format) '))
#starting work every day: fancy way of doing this, not working yet
# def ObtainStartWork():
#     isValid=False
#     while not isValid:
#         userIn = raw_input('Earliest start for work? (hh:mm): ')
#         try: # strptime throws an exception if the input doesn't match the pattern
#             startwork = dt.datetime.strptime(userIn, '%H:%M')
#             #startwork = dt.time.strftime('%H %M', startwork_in)
#             isValid=True
#         except:
#             print "Boo, try again!\n"
#     return startwork
# #test the function
# startWork = ObtainStartWork()
#print(str(startWork))
##################################Do the calculations ###############################
#days to deadline
delta=deadline-start
deltaDays =int(delta.days)
#print(deltaDays)

#Calculate the number of days including buffer and distribute equally among remaining days
actualDelta=deltaDays-timeBuffer
t_perDay=totalHours/actualDelta

#hours of work every day
workHours=t_perDay
#only the front of the decimal point
workHoursOnly=int(workHours*100/100.)
#print(workHoursOnly)

#end of work
endWork_hour=workHoursOnly+startWork
endWork_minute=round((workHours-workHoursOnly)*60,2)
#print(endWork_hour+endWork_minute)

#get the maximal working hours and check if they don't conflict with the calculated hours, pretty useless still...
max_Hours = ObtainMaxHours()
#print(max_Hours)

###################### Make sure those are the inputs and print results ###################
print('Planning task:'+' ' +str(task)+' '+'for a total of '+str(totalHours)+' hours with '+str(timeBuffer)+' days as a buffer. Your deadline is: '+str(deadline))
check=raw_input('Is this correct? y/n ')
if check=='n':
	print('Great, you made a mistake.')
elif check=='y':
	print('yay! You will need to work ' +str(round(t_perDay,2))+' h every day for '+str(actualDelta)+' days starting on '+str(StartDate)+'.')

###################### Make calendar files ###################
#get the dates and times that are missing in usable format
# Start=str(startWork)
# startHour=Start[0:2]
# print(startHour)
EndWork=str(endWork_hour)+str(endWork_minute)

#I will need the date in the format yyyymmdd

#make a directory
script_dir = os.path.dirname(__file__)
cal_dir = os.path.join(script_dir, 'Calendarfiles/'+str(task))

if not os.path.isdir(cal_dir):
	os.makedirs(cal_dir)


for n in range(actualDelta):
	date_n=start+dt.timedelta(days=n)
	#make the date the appropriate format
	date_str=str(date_n)
	CalendarDate_n=date_str[0:4]+date_str[5:7]+date_str[8:10]
	outfile = open("Calendarfiles/"+ str(task)+'/day'+str(n+1)+'.ics','w')
	#outfile.write(str(date_n)+'\n')
	outfile.write('BEGIN:VCALENDAR \n')
	outfile.write('VERSION:2.0 \n')
	outfile.write('CALSCALE:GREGORIAN \n')
	outfile.write('BEGIN:VEVENT \n')
	outfile.write('SUMMARY:'+str(task)+'/day'+str(n) + '\n')
	outfile.write('DTSTART;TZID=America/New_York:'+CalendarDate_n+'T'+str(startWork)+'00 \n')
	outfile.write('DTEND;TZID=America/New_York:'+CalendarDate_n+'T'+str(EndWork)+'00 \n')
	outfile.write('LOCATION: \n')
	outfile.write('DESCRIPTION: automatically generated calendar task for '+str(task)+'.\n')
	outfile.write('STATUS: CONFIRMED \n')
	outfile.write('BEGIN:VALARM \n')
	outfile.write('TRIGGER:-PT10M \n')
	outfile.write('DESCRIPTION: you need to do '+str(task)+' now. \n')
	outfile.write('ACTION:DISPLAY \n')
	outfile.write('END:VALARM \n')
	outfile.write('END:VEVENT \n')
	outfile.write('END:VCALENDAR \n')
	outfile.write('BEGIN:VCALENDAR \n')
	outfile.close