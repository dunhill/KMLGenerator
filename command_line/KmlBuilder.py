#!/usr/bin/python

from pykml.factory import KML_ElementMaker as KML
from lxml import etree
from lxml import html
import random

import urllib, json, time


def geocode_location(address,api="",delay=0.1):
  print("-----------------------------------")
  stop_address = u'Transit stop, ' + unicode(address)
  print(stop_address, type(stop_address))
  stop_address = unicode(urllib.quote_plus(stop_address.encode('utf-8')), 'utf-8')
  print(stop_address, type(stop_address))

  base = "https://maps.googleapis.com/maps/api/geocode/json?"
  GeoUrl = base + "address=" + stop_address + "&key=" + api 
  GeoUrl = str(GeoUrl)
  response = urllib.urlopen(GeoUrl)
  jsonRaw = response.read()
  jsonData = json.loads(jsonRaw)
  if jsonData['status'] == 'OK':
    print('num results: ', len(jsonData['results']))
    if len(jsonData['results']) > 1:
      print jsonData['results']
    resu = jsonData['results'][0]
    location = [resu['geometry']['location']['lng'],resu['geometry']['location']['lat']]
    print('types: ', resu['types'])
    print('location_type: ', resu['geometry']['location_type'])
    print('formatted_address: ', resu['formatted_address'])
  else:
    location = [None,None]
  time.sleep(delay) #in seconds
  return location[0], location[1]


def save_to_klm(fileName, folderObject):
  f = open(fileName, 'w')
  f.write(etree.tostring(folderObject, pretty_print=True))


def build_test_folder():
  pm1 = KML.Placemark(KML.name("Hello World!"), KML.Point(KML.coordinates("-64.5253,18.4607")))
  print(pm1.__dict__)
  print(etree.tostring(pm1, pretty_print=True))
  pm2 = KML.Placemark(KML.name("A second placemark!"),KML.Point(KML.coordinates("-64.5358,18.4486")))
  fld = KML.Folder(pm1,pm2)
  
  print()
  print(etree.tostring(fld, pretty_print=True))

  save_to_klm('test.kml', fld)

  return fld


def store_transit_line_as_kml(transitRouteHtmlFile, transitName, transitOutputKmlFile):
  page = open(transitRouteHtmlFile, 'r')
  tree = html.fromstring(page.read())
  # stations = tree.xpath('//*[@id="ivu_trainroute_table"]/tbody/tr/td[3]/text()')
  stations = tree.xpath('//*[@id="HFSResult"]/div[2]/div/table/tbody/tr/td[2]/a/text()')

  folder = KML.Folder()
  coords = ""
  for station in stations:
    lng, lat = geocode_location(station)
    coord = "{}, {} ".format(lng, lat);
    place = KML.Placemark(KML.name(station), KML.Point(KML.coordinates(coord)))
    coords += coord
    folder.append(place)

  line = KML.Placemark(KML.name(transitName), KML.LineString(KML.coordinates(coords)))
  folder.append(line)

  #print(etree.tostring(folder, pretty_print=True))

  save_to_klm(transitOutputKmlFile, folder)


# -------------------------------------------

#store_transit_line_as_kml('res/M10-route.html', 'M10', 'res/M10_test.kml')
store_transit_line_as_kml('res/bus_142.html', '142', 'res/out_bus_142_test.kml')


