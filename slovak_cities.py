import folium
import pandas

data = pandas.read_csv("slovak_cities.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
pop = list(data["POP2019"])
name = list(data["NAME"])

def color_producer(population):
    if population < 20000:
        return "green"
    elif 20000 <= population < 40000:
        return "yellow"
    elif 40000 <= population < 60000:
        return "orange"
    elif 60000 <= population < 100000:
        return "blue"
    else:
        return "red"


html = """
City name: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Population: %s
"""

# Add Category Legend
legend_html = """
<div style="position:fixed;
     top: 780px;
     right: 20px;
     width: 280px;
     height: 170px;
     border:3px solid grey;
     z-index: 9999;
     color: black;
     background: #d9e0d1;
     font-size:16px;">
     &nbsp;<b>Cities and towns in Slovakia and their population as of 31. 12. 2019:</b><br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:green"></i>&nbsp;Under 20.000<br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:yellow"></i>&nbsp;Over 20.000<br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:orange"></i>&nbsp;Over 40.000<br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:blue"></i>&nbsp;Over 60.000<br>
     &nbsp;<i class="fa fa-circle fa-1x" style="color:red"></i>&nbsp;Over 100.000
</div>"""

map = folium.Map(location=[48.803889, 19.643611], zoom_start=9, tiles="OpenStreetMap")

fg = folium.FeatureGroup(name="Cities and towns")

for lt, ln, pp, nm in zip(lat, lon, pop, name):
    iFrame = folium.IFrame(html=html % (nm, nm, pp), width=180, height=100)
    fg.add_child(folium.CircleMarker(location=[lt, ln], radius=10, popup=folium.Popup(iFrame), fill_color=color_producer(pp), color="gray", fill_opacity=0.7))

fgc = folium.FeatureGroup(name="Capital city")

fgc.add_child(folium.Marker(location=[48.143889, 17.109722], popup="Capital city", icon="red"))

# Add Legend
map.get_root().html.add_child(folium.Element(legend_html))

map.add_child(fg)
map.add_child(fgc)
map.add_child(folium.LayerControl())

map.save("slovak_cities.html")
