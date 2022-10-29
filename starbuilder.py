#Import required libraries
import numpy as np
import pandas as pd
import sidereal_calculator as sidereal_calc
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from skyfield.api import Star, load
from skyfield.data import hipparcos, stellarium
from skyfield.projections import build_stereographic_projection
from skyfield.api import wgs84


#This code was built upon the Neowise example found in the Skyfield docs here:
#https://rhodesmill.org/skyfield/example-plots.html



lat = 50.90704
lng = -1.41418
yyyy = 2021
mm = 4
dd = 16
hour = 15


def create_stars_image(lat, lng, yyyy, mm, dd, hour):
    # An ephemeris from the JPL provides Sun and Earth positions.
    eph = load('de421.bsp')

    #Set the field of view
    fov_degrees = 150.0

    #Set the limiting magnitude, this represents the brightness of the faintest
    #Star that can be seen, a larger number means more stars will be shown.
    #The limiting magnitude of the naked eye is around 6.5
    limiting_magnitude = 6.5

    #Get the location of Earth's position in space and the observers position on Earth
    earthLocation = wgs84.latlon(lat, lng)
    earth = eph['earth'] + earthLocation

    #Get the time
    ts = load.timescale()
    t = ts.utc(yyyy, mm, dd)

    #Open the Hipparcos star catalogue
    with load.open('hip_main.dat') as f:
        stars = hipparcos.load_dataframe(f)

    #The constellation information comes from Stellarium.
    with load.open("constellationship.fab") as f:
        #Creates a list of constellation outlines. Each outline is made of several edges.
        #Each edge is made of two stars representing the start and end of the line
        constellations = stellarium.parse_constellations(f)

    #A list of all the edges in all the constellations
    edges = [edge for name, edges in constellations for edge in edges]

    #A list of all the "start stars" of the edges. eg if the edges were: [(A,B),(C,D),(E,F)]
    #Then edges_star1 would be: [A,C,E]
    edges_star1 = [star1 for star1, star2 in edges]

    #A list of all the "end stars" of the edges
    edges_star2 = [star2 for star1, star2 in edges]

    # We will center the chart on the comet's middle position.
    #Calculate the local sidereal time of the observer
    lst = sidereal_calc.calc_lst(lng, yyyy, mm, dd, hour)

    #The zenith is the point directly above the observer. A star object is created to represent
    #this point because they can be observed using Skyfield. The declination of this point is
    #just the latitude of the observer. However, the right ascension is the local sidereal time
    #of the observer (rather than their longitude, this is because of the earths rotation)
    zenith = Star(ra_hours=lst, dec_degrees=lat)

    #Centre the chart on the observer's zenith
    centre = earth.at(t).observe(zenith)

    #Use Skyfield stereographic projection method to get X and Y coordinates
    projection = build_stereographic_projection(centre)

    #Use the projection variable to compute the x and y coordinates each star will have on the plot
    star_positions = earth.at(t).observe(Star.from_dataframe(stars))
    stars['x'], stars['y'] = projection(star_positions)

    #Create a True/False mask marking the stars bright enough to be included, based on the limiting magnitude
    bright_stars = (stars.magnitude <= limiting_magnitude)

    #Use the stars magnitudes to calculate the size of their markers on the plot
    magnitude = stars['magnitude'][bright_stars]
    marker_size = (0.2 + limiting_magnitude - magnitude) ** 2.0

    #Get the x and y coordinates (on the graph) of the "start" stars
    xy1 = stars[['x', 'y']].loc[edges_star1].values
    #Get the x and y coordinates (on the graph) of the "end" stars
    xy2 = stars[['x', 'y']].loc[edges_star2].values
    #Create a 3D numpy array from the 2 previously created arrays. This will have the following format:
    #[[[E1_start_x, E1_startY],[E2_start_x, E2_start_y],...], [[E1_end_x, E1_end_Y],[E2_end_x, E2_end_y],...]]
    edges_array = np.array([xy1, xy2])
    #Use numpy's rollaxis function to reshape the array into the format expected by matplotlib:
    #[[[E1_start_x, E1_start_y],[E1_end_x, E1_end_y]],[[E2_start_x, E2_start_Y],[E2_end_x, E2_end_y]]...]
    lines_xy = np.rollaxis(edges_array, 1)

    #Create the figure and axes objects (specifying the figures size)
    fig, ax = plt.subplots(figsize=[9, 9])

    #Draw the constellation lines onto the axes, specifying their thickness and colour
    ax.add_collection(LineCollection(lines_xy, linewidths=0.65, colors='White'))

    #Draw the stars that are bright enough, specifying their size and colour
    ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars], s=marker_size, color='White')

    #Set the view limits of the axes
    angle = np.pi - fov_degrees / 360.0 * np.pi
    limit = np.sin(angle) / (1.0 - np.cos(angle))
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)

    #Hide the axes
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    #Set X and Y aspect scaling to be equal
    ax.set_aspect(1)
    #Set the background colour to black
    ax.set_facecolor('Black')

    #Show the image
    plt.show()


