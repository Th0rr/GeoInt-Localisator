from datetime import datetime
from gmapplot import create_map
import webbrowser
import sys
import os
from geoloc import get_address_by_geopy
from progress.bar import Bar
from web import progress


def select_element(final_results,selection):
	'''return elements selected from final_results by indice '''
	if not selection:
		ch = input("Select the pairs to act on\nPress \"q\" to quit\n")
	else:
		ch = "0-"+str(selection)

	try:
		if "-" in ch: #"1-4"
			ch = ch.split("-")
			return final_results[int(ch[0])::int(ch[1])]

		elif "," in ch: #"1,3,2"
			ch = ch.split(",")
			return [final_results[int(i)] for i in ch]

		elif ch == "q" or ch == "Q":
			sys.exit()

		elif ch.isdigit():
			return [final_results[int(ch)]]

	except ValueError:
		print("Enter a number please, use - to select a range of continuous elements "
		 "and , to select several elements")

def get_full_addresses(selection):
	try :
		for i,el in enumerate(selection):	
			progress(i,len(selection),status='Reverse geocoding...')
			sys.stdout.write('\r')
			a1 = get_address_by_geopy(el[3])
			a2 = get_address_by_geopy(el[4])
			if a1: el[1] = a1
			if a2: el[2] = a2
	except ValueError :
		print("Error in element value")

def mapping(selection,command_line):
	now = datetime.now()
	current_time = now.strftime("%H:%M")
	m = create_map(selection)
	name = 'map_'+str(command_line[0])+'_'+str(command_line[1])+'_'+str(current_time)+'.html'
	name = name.replace(" ","_")
	name = name.replace(":",",")
	m.save(name)
	move_file_by_ext("Maps",".html")
	os.startfile(name)


def write_to_text(final_results,filename):
	with open(filename, 'w') as f:
		for item in final_results:
			for el in item:
				if type(el) == int: 
					f.write("{0}!\n".format(el))
				else: 
					f.write("{0}\n".format(el))

def move_file_by_ext(out_dir,ext):
    for file in os.listdir(os.getcwd()):
        if file.endswith(ext):
            if file and os.path.isdir(out_dir):
                os.replace(file,os.path.join(out_dir,file))