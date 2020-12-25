import folium
from folium.plugins import MarkerCluster
from const import *
	

def create_map(data):
	m = folium.Map(location=list(data[0][3]), 
		zoom_start=12,
		control_scale=True,
		zoom_control = True)

	marker_cluster = MarkerCluster().add_to(m)
	colors = ['green', 'darkgreen', 'red', 'blue', 'purple', 'orange', 'darkred','lightred', 'darkblue',
	 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue','lightgreen', 'gray', 'black', 'lightgray']
	for pair in data:
		create_markers_pairs(marker_cluster,pair,colors,m)
	return m


def create_markers_pairs(marker_cluster,pair,colors,m) -> None:

	link1 = create_html_link(pair[1])
	link2 = create_html_link(pair[2])

	folium.Marker(
	    list(pair[3]),
	    popup=link1,
	    icon=folium.Icon(color=colors[0],icon=LOCATION_ICON,prefix="fa")
	).add_to(marker_cluster)

	folium.Marker(
	    list(pair[4]),
	    popup=link2,
	    icon=folium.Icon(color=colors[0],icon=LOCATION_ICON,prefix="fa")
	).add_to(marker_cluster)

	folium.PolyLine([pair[3],pair[4]], 
		color=colors[0], 
		weight=LINE_WIDTH, 
		opacity=0.7,
		smooth_factor=0.7,
		tooltip="N°"+str(pair[0])+"  "+str(pair[-1])+"km").add_to(m)
	colors.pop(0)

def create_html_link(address: str):
	html = folium.Html("""<a href ="""+STREET_VIEW_URL+address.replace(" ","+")+""">
	Street View</a><br><p>"""+address+"""</p>""",script=True)
	link = folium.Popup(html, max_width=2650)
	return link
