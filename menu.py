#Import required libraries
import starbuilder
import datetime
import time
import os

#Clear the console
os.system("cls")

#Loop until there is a valid latitude input
while True:
    #Input must be converted to a float value
    lat = float(input("Enter latitude: "))
    #Latitudes min/max values are -90 and 90 respectively
    if lat == False or lat < -90 or lat > 90:
        #If invalid input is given then notify user and clear the console
        print("Invalid input")
        time.sleep(0.45)
        os.system("cls")
        continue
    #If input is valid then clear the console and break out of the loop
    else:
        os.system("cls")
        break

#Loop until there is a valid longitude input
while True:
    #Input must be converted to a float value
    lng = float(input("Enter longitude: "))
    #Longitudes min/max values are -180 and 180 respectively
    if lng == False or lng < -180 or lng > 180:
        #If invalid input is given then notify user and clear the console
        print("Invalid input")
        time.sleep(0.45)
        os.system("cls")
        continue
    #If input is valid then clear the console and break out of the loop
    else:
        os.system("cls")
        break

#Loop until there is a valid date input
while True:
    try:
        date_input = input("Enter date (DD/MM/YYYY): ")
        #Get the day, month, and year values
        dd, mm, yyyy = map(int, date_input.split("/"))
        #The ephemeris segment used only covers dates between 1899 and 2053
        if yyyy > 2052 or yyyy < 1900:
            print("Year must be between 1900 and 2052")
            time.sleep(0.75)
            os.system("cls")
            continue
        #Attempt to map day, month, year values to a datetime, if this fails it will trigger the exception
        date = datetime.date(yyyy, mm, dd)
    except:
        #If invalid input is given then notify user and clear the console
        print("Invalid input")
        time.sleep(0.45)
        os.system("cls")
        continue
    #If input is valid then clear the console and break out of the loop
    else:
        os.system("cls")
        break

#Loop until there is a valid hour input
while True:
    #Input must be converted to an int value
    hour = int(input("Enter hour (0-23): "))
    #Must be between 0 and 23, with 0 being midnight
    if hour == False or hour < 0 or hour > 23:
        #If invalid input is given then notify user and clear the console
        print("Invalid input")
        time.sleep(0.45)
        os.system("cls")
        continue
    #If input is valid then clear the console and break out of the loop
    else:
        os.system("cls")
        break

print("Building the image...")

#Build the image using the starbuilder code
starbuilder.create_stars_image(lat, lng, yyyy, mm, dd, hour)




