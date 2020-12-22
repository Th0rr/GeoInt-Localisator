import folium
from folium.plugins import MarkerCluster
	

def create_map(data):
	m = folium.Map(location=list(data[0][3]), zoom_start=12)
	marker_cluster = MarkerCluster().add_to(m)
	colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred','lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
	for pair in data:
		create_markers_pairs(marker_cluster,pair,colors,m)
	return m


def create_markers_pairs(marker_cluster,pair,colors,m):
	folium.Marker(
	    list(pair[3]),
	    popup=pair[1],
	    icon=folium.Icon(color=colors[0])
	).add_to(marker_cluster)

	folium.Marker(
	    list(pair[4]),
	    popup=pair[2],
	    icon=folium.Icon(color=colors[0])
	).add_to(marker_cluster)

	folium.PolyLine([pair[3],pair[4]], 
		color=colors[0], 
		weight=7, 
		opacity=0.7,
		smooth_factor=0.7,
		tooltip="N°"+str(pair[0])+"  "+str(pair[-1])+"km").add_to(m)
	colors.pop(0)
