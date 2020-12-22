import itertools
import haversine as hs
import math
import numpy as np
from scipy.spatial.distance import cdist
from operator import itemgetter
from const import *

def return_matches(coords,ppairs): # ppairs {dist:((float,float),(float,float))}
	final_res = []
	temp = []
	for pair in ppairs:
		for gps in ppairs[pair]:
			address = get_value_from_coord(coords, (gps[0],gps[1]))
			data = [address[0], address[1][0], address[1][1],pair] # remove letter
			final_res.extend(data)

	for i in range (0,len(ppairs)*2,2): 
		el = create_element(final_res[0::4],final_res[1::4],final_res[2::4],final_res[3::4],i)
		temp.append(el)
	temp = sorted(temp,key=itemgetter(4),reverse=False)

	# add columun indices
	for i in range(len(temp)):
		temp[i].insert(0,i)
	return temp


def create_element(add,gpsLon,gpsLat,distance,i)->[str,str,(float,float),(float,float),float]:
	el = []
	dec_nb = 4
	el.append(add[i])
	el.append(add[i+1])
	el.append((round(gpsLon[i],dec_nb),round(gpsLat[i],dec_nb)))
	el.append((round(gpsLon[i+1],dec_nb),round(gpsLat[i+1],dec_nb)))
	el.append(round(distance[i],dec_nb))
	return el


def get_distances(coords,scope: float):
	tab = []
	if len(coords) < 2:
		return None

	for i in range(len(coords)):
		tab.append([])
	coordDic_to_coordList(coords, tab)
	ppairs = calculate_distances(tab[0],tab[1],scope)
	return ppairs


def calculate_distances(add_list1,add_list2,scope):
	distance = {}
	points = [tup for tup in itertools.product(add_list1, add_list2)]
	for p in points:
		d = hs.haversine(p[0],p[1])
		if d < scope:
			distance[d] = (p[0],p[1])
	return distance # {dist:((float,float),(float,float))}

def get_value_from_coord(lis,coord):
	for dic in lis:
		for key,value in dic.items():
			if (value[0],value[1]) == coord:
				return key,value


def get_distance_from_coord(dic,coord):
	for key,value in dic.items():
		if value[0] == coord or coord ==value[1]:
			return key

def coordDic_to_coordList(coord,tab):
	try:
		for dic in coord:
			for key,value in dic.items():
				for i,el in enumerate(tab):
					if value[2] == chr(ord("a")+i):
						tab[i].append((value[0],value[1]))
	except ValueError :
		print("Error in order_coord_data")
