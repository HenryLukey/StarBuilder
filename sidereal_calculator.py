import math

#Calculates the Julian Day for a given UTC date and hour value
def julian_day(yyyy, mm, dd, hour):
    #Calculate Julian day using formula found here: https://quasar.as.utexas.edu/BillInfo/JulianDatesG.html (0 hours)
    a = math.floor(yyyy/100)
    b = math.floor(a/4)
    c = 2-a+b
    e = math.floor(365.25 * (yyyy + 4716))
    f = math.floor(30.6001 * (mm + 1))
    jd = c + dd + e + f - 1524.5
    
    #Incorporate the given hour value (1 hour = 1/24 in Julian time)
    jd = jd + (hour * (1/24))
    
    return jd

#Returns just the value after the decimal point of a given value
def frac(x):
    #Takes just the decimal part of x
    x = x - math.floor(x)
    #If x becomes negative add 1.0 to ensure it remains between 0 and 1
    if (x<0):
        x = x + 1.0

    return x;

#Calculates Local Mean Sidereal Time for a given Julian day and longitude value
def lm_sidereal_time(jd, lng):
    #Get the GMST value
    gmst = gm_sidereal_time(jd);
    #Calculate lmst value by adding longitude to gmst, convert this from degrees into hours by dividing by 15, divide by 24 to convert
    #into days, use frac method to get time (in terms of days), finally multiply by 24 to convert from days to hours
    lmst = 24.0 * frac(((gmst + lng) / 15) / 24.0)

    return lmst

#Calculates Greenwich Mean Sidereal Time for a given Julian day (GMST is used in LMST calculation)
def gm_sidereal_time(jd):
    #Calculate time in Julian Centuries
    t = (jd - 2451545.0) / 36525
    #Calculate gmst (in degrees) using formula from Astronomical Algorithms by Jean Meeus
    gmst = 280.46061837 + (360.98564736629 * (jd - 2451545.0)) + (0.000387933 * (t**2)) - ((t**3) / 38710000.0)

    return gmst

#Returns Local Sidereal Time from a longitude, year, month, day, and hour value
def calc_lst(lng, yyyy, mm, dd, hour):
    #Get Julian day
    jd = julian_day(yyyy, mm, dd, hour)
    #Get local sidereal time
    lst = lm_sidereal_time(jd, lng)

    return lst
