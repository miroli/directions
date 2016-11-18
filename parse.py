# -*- coding: utf-8 -*-

import requests
import json
import click


@click.command()
@click.option('--olat', help='latitude of origin')
@click.option('--olng', help='longitude of origin')
@click.option('--dlat', help='latitude of destination')
@click.option('--dlng', help='longitude of destination')
@click.option('--filename', help='save geojson linestring to file')
def main(olat, olng, dlat, dlng, filename=None):
    origin = [olat, olng]
    dest = [dlat, dlng]
    URL = 'http://maps.googleapis.com/maps/api/directions/json'
    origin = '?origin=%s,%s' % (str(origin[0]), str(origin[1]))
    dest = '&destination=%s,%s' % (str(dest[0]), str(dest[1]))
    URL = URL + origin + dest

    r = requests.get(URL)
    response = json.loads(r.content)

    steps = response['routes'][0]['legs'][0]['steps']
    distance = response['routes'][0]['legs'][0]['distance']['text']

    coordinates = []
    for step in steps:
        start = step['start_location']
        coordinates.append([start['lng'], start['lat']])

    coordinates.append([step['end_location']['lng'], step['end_location']['lat']])

    if filename:
        to_geojson(coordinates, distance, filename)
    else:
        click.echo(to_geojson(coordinates))


def to_geojson(steps, distance, filename):
    linestring = """\
    { "type": "FeatureCollection",
    "features": [
      { "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": %s
          },
        "properties": {
          "distance": "%s"
          }
         }
       ]
     }
     """ % (steps, distance)

    with open(filename, 'w') as f:
        f.write(linestring)
