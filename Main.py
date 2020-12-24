import argparse
from geoloc import broad_search,print_results
from const import *
from menu_interactions import *


parser = argparse.ArgumentParser(description='group close locations')
parser.add_argument(
	'-q', '--queries', required=True, type=str, 
	help="""Google map queries ex: -q town store1!town store2 additional_query_info\n
	""",nargs='*')

parser.add_argument(
	'-o', '--output',required=False, type=str, 
	help="export to text file\nEx: -o address.txt")

parser.add_argument(
	'-s', '--scope', required=False, type=float,default=0.75, 
	help='filter results above specified distance in a locations pair (km) Ex: -s 0.5')

parser.add_argument(
	'-M','--map',action='store_true',
	help='Show on a map location of targets by pair')

parser.add_argument(
	'-A','--AInfos',type=str,default="selection",choices=["full","selection"],
	help="""Gives you the whole addresses with reverse-geocoding (slower), use \"full\"
	for all addresses, and \"selection\" to get only the addresses you will selected\n
	We don\'t recommend using the full option if you expect a lot of results""")

args = parser.parse_args()

if args.queries :
	command_line = (" ".join(args.queries)).split("!")
	final_results = broad_search(command_line[0],command_line[1],args)
	print_results(final_results,command_line[0],command_line[1])

	if args.AInfos == "full":
		get_full_addresses(final_results)
	if args.output:
		write_to_text(final_results,args.output)

	while 1:
		selection = select_element(final_results)
		if args.AInfos == "selection":
			get_full_addresses(selection)
			if args.output:
				write_to_text(final_results,args.output+"_selection")
		if selection:
			break;
	if args.map:
		m = mapping(selection,command_line)

else:
	print("Enter valid options")
