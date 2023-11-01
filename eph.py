# eph.py
# lets try some charting

# AI-Generated Code
import ephem
from svgwrite import Drawing

# Create an instance of the solar system
solar_system = ephem.SolarSystem()

# Define the date and time for which you want to calculate the planetary positions
date_time = ephem.now()

# Calculate the positions of all the planets
planets = [ephem.Mercury(), ephem.Venus(), ephem.Mars(), ephem.Jupiter(), ephem.Saturn(), ephem.Uranus(), ephem.Neptune(), ephem.Pluto()]
for planet in planets:
    planet.compute(date_time)

# Create an SVG drawing
dwg = Drawing(size=("200px", "200px"))

# Plot the positions of the planets on the SVG image
for planet in planets:
    # Calculate the x and y coordinates for the planet
    x, y = planet.x, planet.y
    dwg.circle(center=(x, y), r=5, stroke='black', fill='red')

# Determine the aspects between the planets
for i in range(len(planets)):
    for j in range(i+1, len(planets)):
        angle = ephem.separation(planets[i], planets[j])
        dwg.line((planets[i].x, planets[i].y), (planets[j].x, planets[j].y), stroke='black')

# Save the SVG image
dwg.save()
