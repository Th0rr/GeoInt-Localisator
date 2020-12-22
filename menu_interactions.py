from datetime import datetime
from gmapplot import create_map
import webbrowser
import sys
import os
from geoloc import get_address_by_geopy
from progress.bar import Bar
from web import progress


def select_element(final_results):
	'''return elements selected from final_results by indice '''
	ch = input("Select the pair to examinate\nPress \"q\" to quit\n")
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
	os.startfile(name)


def write_to_text(final_results,filename):
	with open(filename, 'w') as f:
		for item in final_results:
			for el in item:
				if type(el) == int: 
					f.write("{0}!\n".format(el))
				else: 
					f.write("{0}\n".format(el))

kk = [[0, "Bistrot d'Eustache, Rue Berger, Quartier Les Halles, Paris 1er Arrondissement, Les Halles, Paris, Île-de-France, France métropolitaine, 75001, France", 'Nintendo European Research & Development, 128, Rue de Rivoli, Quartier de la Madeleine, Paris 8e Arrondissement, Paris, Île-de-France, France métropolitaine, 75001, France', (48.862, 2.3435), (48.8598, 2.3447), 0.2545], [1, "Bistrot d'Eustache, Rue Berger, Quartier Les Halles, Paris 1er Arrondissement, Les Halles, Paris, Île-de-France, France métropolitaine, 75001, France", 'MAC Cosmetics, Rue Rambuteau, Quartier Les Halles, Paris 1er Arrondissement, Les Halles, Paris, Île-de-France, France métropolitaine, 75001, France', (48.862, 2.3435), (48.8624, 2.3484), 0.3598], [2, 'H&M, Rue de Rivoli, Beaubourg, Quartier Saint-Merri, Paris 4e Arrondissement, Paris, Île-de-France, France métropolitaine, 75004, France', 'Nintendo European Research & Development, 128, Rue de Rivoli, Quartier de la Madeleine, Paris 8e Arrondissement, Paris, Île-de-France, France métropolitaine, 75001, France', (48.8582, 2.3494), (48.8598, 2.3447), 0.3859], [3, 'H&M, Rue de Rivoli, Beaubourg, Quartier Saint-Merri, Paris 4e Arrondissement, Paris, Île-de-France, France métropolitaine, 75004, France', 'MAC Cosmetics, Rue Rambuteau, Quartier Les Halles, Paris 1er Arrondissement, Les Halles, Paris, Île-de-France, France métropolitaine, 75001, France', (48.8582, 2.3494), (48.8624, 2.3484), 0.4648], [4, '14, Avenue du Général Leclerc, Alésia, Quartier du Petit-Montrouge, Paris 14e Arrondissement, Paris, Île-de-France, France métropolitaine, 75014, France', 'Promod, Place Victor et Hélène Basch, Alésia, Quartier du Petit-Montrouge, Paris 14e Arrondissement, Paris, Île-de-France, France métropolitaine, 75014, France', (48.8328, 2.3309), (48.8275, 2.327), 0.6576], [5, 'H&M, Rue de Rivoli, Beaubourg, Quartier Saint-Merri, Paris 4e Arrondissement, Paris, Île-de-France, France métropolitaine, 75004, France', 'Le Bistrot 30, Rue Saint-Séverin, Quartier de la Sorbonne, Paris 5e Arrondissement, Paris, Île-de-France, France métropolitaine, 75005, France', (48.8582, 2.3494), (48.8525, 2.3449), 0.7151]]
mapping(kk,["tt 1", "jj 2"])  