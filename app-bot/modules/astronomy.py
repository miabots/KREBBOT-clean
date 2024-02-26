# astro.py
# astronomy code for trying to plot astrology stuff

import discord
from discord.ext import commands
from cns import *

from datetime import datetime, timedelta

import pandas as pd

from typing import Dict, Any, Optional, List, Callable, Awaitable, Generic

from pydap.client import open_url
from pydap.cas.urs import setup_session

import itertools
import pandas as pd
import numpy as np
import plotly.express as px
import requests
print(requests.certs.where())
import nasapy
import os
from datetime import datetime
import urllib.request
from IPython.display import Image
from dotenv import load_dotenv

path = "./"
load_dotenv()

pw = os.getenv("ASTRO_PW")

class Astronomy(commands.Cog):
    """
    Various Space Utilities and Tools
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Basic test command to confirm that the module is loaded and responding.\nIt is only usable by Power Users.", brief="Power User Command", hidden=True)
    async def testast(self, ctx):
        if ctx.guild.id in cns.PROD_GUILDS:
            # print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        print('Test Command Works from astronomy.')
        pass

    @commands.command(help="Gets the NASA image of the day, pass YYYY-MM-DD for a date or nothing for today!")
    async def spacepic(self, ctx, arg: str):

        if ctx.guild.id in cns.PROD_GUILDS:
            # print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        # if str(responseuser) not in cns.POWER_USERS:
        #    return

        k = "523p5hPYHGzafYGLCkqa54kKMTV2vbP0XcPxkcLm"
        nasa = nasapy.Nasa(key=k)

        if arg:
            d = arg  # .strftime('%Y-%m-%d')
        else:
            d = datetime.today().strftime('%Y-%m-%d')

        apod = nasa.picture_of_the_day(date=d, hd=True)

        # POINT A:
        # Check the media type available:
        if(apod["media_type"] == "image"):

            # POINT B:
            # Displaying hd images only:
            if("hdurl" in apod.keys()):

                # POINT C:
                # Saving name for image:
                title = d + "_" + apod["title"].replace(" ", "_").replace(":", "_") + ".jpg"

                # POINT D:
                # Path of the directory:
                image_dir = "./Astro_Images"

                # Checking if the directory already exists?
                dir_res = os.path.exists(image_dir)

                # If it doesn't exist then make a new directory:
                if (dir_res == False):
                    os.makedirs(image_dir)

                # If it exist then print a statement:
                else:
                    print("Directory already exists!\n")

                # POINT E:
                # Retrieving the image:
                print("URL for this image: ", str(apod["hdurl"]))
                urllib.request.urlretrieve(url=apod["hdurl"], filename=os.path.join(image_dir, title))

                # POINT F:s
                # Displaying information related to image:

                # if("date" in apod.keys()):
                #    print("Date image released: ", apod["date"])
                #    print("\n")
                # if("copyright" in apod.keys()):
                #    print("This image is owned by: ", apod["copyright"])
                #    print("\n")
                # if("title" in apod.keys()):
                #    print("Title of the image: ", apod["title"])
                #    print("\n")
                # if("explanation" in apod.keys()):
                #    print("Description for the image: ", apod["explanation"])
                #    print("\n")
                # if("hdurl" in apod.keys()):
                print("URL for this image: ", apod["hdurl"])
                #    print("\n")

                # POINT G:
                # Displaying main image:
                # display(Image(os.path.join(image_dir, title)))

                img = Image(os.path.join(image_dir, title))

                embed = discord.Embed(title="Astronomy Image for " + apod.get('date') + ": ", description=apod.get('title'))
                # embed.set_author(name="TEST AUTHOR")
                # embed.add_field(name="Explanation", value=apod.get('explanation'), inline=True)
                # embed.add_field(name="Major/Minor Arcana:", value=cd[1], inline=True)
                # embed.add_field(name="Associated Planet", value=cd[8], inline=True)
                # embed.add_field(name="Associated Sign", value=cd[9], inline=True)
                # embed.add_field(name="Associated Element", value=cd[10], inline=True)
                # for key in apod:
                #    print(key)
                # print(apod)
                embed.set_image(url=apod.get('hdurl'))
                # embed.set_thumbnail(url=thumburl)
                embed.set_footer(text="Delivered by KREBBOT with love <3")

                await ctx.channel.send(embed=embed)

                # Point H:
                # Text to Speech Conversion:
                # Take input from user:
                # print("\n")
                # choice = input("Press * to hear the audio explanation : ")

                # if(choice == "*"):
                # Text to be converted:
                #    mytext = apod["explanation"]
                # mytext="Good Evening Pratik."

                # Creating an object:
                #    myobj = gTTS(text=mytext, lang="en", slow=False)

                # Generating audio file name:
                #    audio_title = d + "_" + apod["title"] + ".mp3"

                # Save the converted file:
                #    myobj.save(os.path.join(image_dir, audio_title))

                # Name of sound file:
                #    sound_file = os.path.join(image_dir, audio_title)

                # Playing the converted file
                #    display(Audio(sound_file, autoplay=True))

        # POINT I:
        # If media type is not image:
        else:
            print("Sorry, Image not available!")

    @commands.command(hidden=True)
    async def astro(self, ctx):

        if ctx.guild.id in cns.PROD_GUILDS:
            # print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return
        print("astro")

        # testp = { "event": "YYYYMMDDhhmmss", "planets": ["Sun", "Moon"], "topo": [ longitude, latitude, geoalt], "zodiac": "sidereal mode name" }

    @ commands.command(hidden=True)
    async def astdatatest(self, ctx):
        if ctx.guild.id in cns.PROD_GUILDS:
            # print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return

        url = 'https://gpm1.gesdisc.eosdis.nasa.gov/dods/GPM_3IMERGHHL_06'

        session = setup_session(username='notte_a_problem', password=pw, check_url=url)
        dataset = open_url(url, session=session)

        lat_range = [24.7, 25.2]  # Latitude extents of Karachi
        lon_range = [66.8, 67.3]  # Longitude extents of Karachi
        lat_vals = dataset['lat'][:].data
        lon_vals = dataset['lon'][:].data
        lat_indices = np.where(
            (lat_vals >= lat_range[0]) &
            (lat_vals <= lat_range[1])
        )[0]
        lon_indices = np.where(
            (lon_vals >= lon_range[0]) &
            (lon_vals <= lon_range[1])
        )[0]

        min_time = datetime(year=2000, month=6, day=1, hour=0, minute=0)
        event_start_time = datetime(year=2020, month=8, day=25, hour=0, minute=0)
        start_time_index = int((event_start_time - min_time).total_seconds()/(60*30))

        # For start time check
        start_time_days = dataset['time'][start_time_index].data[0]
        start_time_date = datetime(year=1, month=1, day=1) + timedelta(days=start_time_days-2)
        print(start_time_date)

        var_name = 'precipcal'
        var_dataset = dataset[var_name][
            start_time_index:start_time_index + 48*4,
            min(lat_indices): max(lat_indices)+1,
            min(lon_indices): max(lon_indices)+1


        ]

        time = var_dataset['time'].data

        lat_column = var_dataset['lat'].data
        lon_column = var_dataset['lon'].data
        var_data = var_dataset[var_name].data

        time_column = [event_start_time + timedelta(minutes=30*n) for n in range(len(time))]

        # Transform pydap model data to dataframe
        map_data = [list(time_column), list(lat_column), list(lon_column)]
        map_tuple_list = list(itertools.product(*map_data))
        base_data = pd.DataFrame(map_tuple_list, columns=['Time', 'Lat', 'Long'])
        base_data[var_name] = var_data.flatten()

        base_data.to_csv('karachi_rains_august_2020.csv')

        my_data = pd.read_csv('karachi_rains_august_2020.csv')

        karachi_cantt_data = my_data[
            (my_data['Lat'] == 24.85) &
            (my_data['Long'] == 67.05)
        ]

        fig = px.line(karachi_cantt_data, x="Time", y=var_name, title='August 2020 Rains in Karachi (mm / hour)', height=400, width=900)
        fig.show()

    @ commands.command(hidden=True)
    async def astdatatest2(self, ctx):
        if ctx.guild.id in cns.PROD_GUILDS:
            # print('Returning due to Production Guild.')
            return
        responseuser = ctx.message.author
        if str(responseuser) not in cns.POWER_USERS:
            return

        AUTH_HOST = 'urs.earthdata.nasa.gov'

    #def __init__(self, username, password):

        #super().__init__()

    #    self.auth = (username, password)

    # Overrides from the library to keep headers when redirected to or from the NASA auth host.

    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url

        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and redirect_parsed.hostname != self.AUTH_HOST and original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return

        # create session with the user credentials that will be used to authenticate access to the data
        username = "notte_a_problem"
        password = pw

        # the url of the file we wish to retrieve
        url = "http://e4ftl01.cr.usgs.gov/MOLA/MYD17A3H.006/2009.01.01/MYD17A3H.A2009001.h12v05.006.2015198130546.hdf.xml"
        # session = SessionWithHeaderRedirection(username, password)
        session = setup_session(username='notte_a_problem', password='pw', check_url=url)

        # extract the filename from the url to be used when saving the file
        filename = url[url.rfind('/')+1:]

        try:
            # submit the request using the session
            response = session.get(url, stream=True)
            print(response.status_code)

            # raise an exception in case of http errors
            response.raise_for_status()

            # save the file
            with open(filename, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    fd.write(chunk)

        except requests.exceptions.HTTPError as e:
            # handle any errors here
            print(e)


async def setup(bot):
    await bot.add_cog(Astronomy(bot))