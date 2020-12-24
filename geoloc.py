from geopy.distance import geodesic
import requests
import time
from tabulate import tabulate
from progress.bar import Bar
from geopy.geocoders import Nominatim
import itertools
from web import *
from geo_recon import get_distances,return_matches
from const import *


def get_coord_by_geopy(address: str,query: str) -> (float,float):
	#time.sleep(WAIT_TIME) # avoid getting blacklisted by geopy
	if "," in address:
		address = address.split(",")[1] # fix some error where address is not detected correctly
	try :
		geolocator = Nominatim(user_agent="geo")
		location = geolocator.geocode(address+" "+query.split(" ")[0])

		if location: return(str(location.latitude),str(location.longitude))
		else :
			time.sleep(WAIT_TIME)
			location = geolocator.geocode(address)
			if location: return (str(location.latitude),str(location.longitude))
			print("\nNOT FOUND "+address)

	except :
		print("\nerror in getting geolocation of address: "+address)


def get_address_by_geopy(coords: (float,float)) -> str:
	"""take GPS coords as Input and return full address """
	#time.sleep(WAIT_TIME)
	geolocator = Nominatim(user_agent="georev")
	location = geolocator.reverse(coords)
	if location :
		return location.address # str
	else :
		print("Coords "+query+" not found")
		return None


def selenium_search(query: str) -> [str]: # => address or name + global location (town)
	driver = webdriver.Firefox() 
	for i in range(2): # try again if an error occurred
		add_list = scrape_addresses(driver,query)
		if add_list:
			print(len(add_list)+" has been found")
			return add_list

def find_addresses_GPS(add_list, query: str) ->{str:(float,float,str)}:
	coord_dict = {}
	letter = chr(ord("a")+selenium_search.counter)
	if add_list:
		add_list = list(set(add_list))
		for i,address in enumerate(add_list):
			progress(i,len(add_list),status='Geocoding addresses')
			sys.stdout.write('\r')
			tup = get_coord_by_geopy(address,query) # (float,float)
			if tup and address:
				sys.stdout.write('\r')
				print(address,tup)
				coord_dict[address] = (float(tup[0]),float(tup[1]),letter)
			else:
				pass;
		selenium_search.counter +=1
		return coord_dict # {address:(lat,lon,letter)}


def broad_search(q1: str,q2: str,args) -> list():
	address_list = []
	selenium_search.counter = 0
	final_result = []
	#----------------- SCRAPING ADDRESSES -----------------------
	try :
		add1 = selenium_search(q1) # [add1,add2]
		add2 = selenium_search(q2) # [add1,add2]

	#----------------- GEOCODING COORDINATES ---------------------
		if add1 and add2:
			# write r1 and r2 for 1st save
			r1 = find_addresses_GPS(add1,q1) # {address:(lat,lon,letter)}
			r2 = find_addresses_GPS(add2,q2)
			address_list.extend([r1,r2])
			change_equal_GPS(address_list) # fix geolocation errors

	#----------------- CALCULATE SHORTEST DISTANCES --------------
			distance_list = get_distances(address_list,args.scope)
			final_result = return_matches(address_list,distance_list)

	except ValueError as e :
		print("ValueError occured",e)
	return final_result

	

#
def detect_double(a: {str:(float,float)},b: {str:(float,float)}) -> None:
	'''Spot different addresses with same GPS and slightly increment one GPS to allow future differenciation '''
	if a and b:
		el = []
		for k1,v1 in a.items():
			for k2,v2 in b.items():
				if (v1[0],v1[1]) == (v2[0],v2[1]):
					el = [k1,v1[0],v1[1]+0.0001,v1[2]]
		if el:
			del a[el[0]]
			a[el[0]] = (el[1],el[2],el[3])


def change_equal_GPS(llist):
	comb = list(itertools.combinations_with_replacement([0,1],2))
	for i in comb:
		detect_double(llist[i[0]],llist[i[1]])


def print_results(final_result,q1,q2):
	q1 = q1.split(" ")[1]
	q2 = q2.split(" ")[1]
	print(tabulate(final_result, headers=["Col",q1,q2,"GPS N°1",
	"GPS N°2","distance (km)"],tablefmt=DISPLAY_STYLE))
