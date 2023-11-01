# chart.py
# lets try charting the planets, thats what I really want

from astropy.coordinates import SkyCoord
from sunpy.coordinates import get_body_heliographic_stonyhurst
from astropy.time import Time
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime
from pytz import timezone


class Chart():

    def __init__():
        print("Hello, Init Here")

    def chartit():

        #obstime = Time('2022-03-30T012:00:00')
        #obstime = datetime('2022-03-30 13:00:00')
        obstime = datetime(year=2022, month=3, day=30)
        planet_list = ['sun', 'moon', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        planet_coord = [get_body_heliographic_stonyhurst(this_planet, time=obstime) for this_planet in planet_list]

        #fig = plt.figure()
        #ax1 = plt.subplot(1, 1, 1, projection='polar')
        # for this_planet, this_coord in zip(planet_list, planet_coord):
        #    plt.plot(np.deg2rad(this_coord.lon), this_coord.radius, 'o', label=this_planet)
        #plt.legend(loc='lower left')
        # plt.show()

        fig, ax = plt.subplots(1)
        for planet, coord in zip(planet_list, planet_coord):
            x = np.cos(np.degrees(coord.lon))
            y = np.sin(np.degrees(coord.lon))
            plt.scatter(x, y, label=planet)

        # now let's do a circle
        theta = np.linspace(0, 2*np.pi, 100)
        r = np.sqrt(1.0)
        x1 = r*np.cos(theta)
        x2 = r*np.sin(theta)
        ax.plot(x1, x2)

        plt.legend()
        plt.show()

    if __name__ == '__main__':
        __init__()
        chartit()
