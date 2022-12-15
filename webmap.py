
#import ellipsis as el
import folium as f
import streamlit as st
import os
import streamlit.components.v1 as components
from folium import plugins
import geopandas as gpd
import json
from datetime import date

#===============================================================================
# def _max_width_():
#     max_width_str = f"max-width: 5000px;"
#     st.markdown(f""" 
#                 <style> 
#                 .reportview-container .main .block-container{{{max_width_str}}}
#                 </style>    
#                 """, 
#                 unsafe_allow_html=True,
#     )
#===============================================================================

def folium_static(fig, width, height):
    if isinstance(fig, f.Map):
        fig = f.Figure().add_child(fig)
        return components.html(
            fig.render(), height=(fig.height or height) + 10, width=width
            )

    # if DualMap, get HTML representation
    elif isinstance(fig, plugins.DualMap):
        return components.html(
            fig._repr_html_(), height=height + 10, width=width
        )
        

folium_map = f.Map(location=[43.9, -77.3], zoom_start=8, tiles='openstreetmap')
#===============================================================================
#grille="F:\DEM_GLAMM\AOI\grille_Charles\Tuile_final.shp"
##grille='https://github.com/eccc-Antoine/DEM_GLAM_app/blob/main/tiles.zip'

#file = open(grille, "rb")
#gdf_grille=gpd.read_file(grille)
#gjson = gdf_grille.to_crs(epsg='4326').to_json()
gjson='https://github.com/eccc-Antoine/DEM_GLAM_app/blob/main/tuile_final3.geojson'
js_data = json.loads(gjson)
for z in js_data['features']:
    link=f'https://007gc-my.sharepoint.com/personal/antoine_maranda_ec_gc_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m%2F{int(z["properties"]["id"])}%5F10m%5FDEM%5Fidw%2Ezip&parent=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m&ga=1'
    b = f.GeoJson(z['geometry'])
    b.add_child(f.Popup(f'Tile: {str(int(z["properties"]["id"]))} \n UTM_ZONE: {str(int(z["properties"]["UTM"]))} \n <a href={link} target="_blank">download (ECCC members only)</a>' ))
    #fg.add_child(b)
    b.add_to(folium_map)
# gdf_grille=gdf_grille.to_crs(4326)
# pop=str(int(gdf_grille['id'].iloc[0]))
# centre=gdf_grille['geometry'].centroid
# 
# geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in centre]
# count=-1
# for g in geo_df_list:
#     count+=1
#     mk = f.Marker(location=g, popup=f.Popup(f'tile: {str(int(gdf_grille["id"].iloc[count]))}'), icon=f.Icon(color="blue", icon="info-sign", size=1) )
#     mk.add_to(folium_map)
#===============================================================================


#===============================================================================
# i = f.features.CustomIcon(icon_image,
#                                icon_size=(38, 95),
#                                icon_anchor=(22, 94),
#                                shadow_image=shadow_image,
#                                shadow_size=(50, 64),
#                                shadow_anchor=(4, 62),
#                                popup_anchor=(-3, -76),)
# mk = f.Marker([43.88, -78.77], popup=f.Popup('Hello'))
#===============================================================================



#grille="F:\DEM_GLAMM\AOI\grille_Charles\grille.geojson"

##hillshade_4326
#xyz_hillshade='https://api.ellipsis-drive.com/v3/path/b07b0572-e7a1-4df2-b673-50e10d453bf5/raster/timestamp/7ec941be-28fa-4e14-af08-75785a7de252/tile/{z}/{x}/{y}?style=aeb6cc57-7d84-4555-bff8-e29278b16516&token=epat_l4Q8VPgD01Fud7VksfwB7zkhuyQpJyYa77ayDC29cA1jHhFuIrb1ooHXc8P2MAGD'
xyz_hillshade='https://api.ellipsis-drive.com/v3/path/58365cdd-cf3d-4601-909d-f58feead0c94/raster/timestamp/d076f5ea-b93c-49e3-b809-a452895ffb4d/tile/{z}/{x}/{y}?style=ffc495e8-9dc1-44fd-9ca4-cc813f7970bc&token=epat_cyWz6w9UyHVTqmBplpDYT7x4pIsF1ucCIkfrXTjUUG1FJsyU3otkGqKYpX2S1dfo'
#xyz_hillshade='https://api.ellipsis-drive.com/v3/path/58365cdd-cf3d-4601-909d-f58feead0c94/styleSheet?timestampId=d076f5ea-b93c-49e3-b809-a452895ffb4d&style=ffc495e8-9dc1-44fd-9ca4-cc813f7970bc&token=epat_cyWz6w9UyHVTqmBplpDYT7x4pIsF1ucCIkfrXTjUUG1FJsyU3otkGqKYpX2S1dfo'


##DEM_4326
#xyz_DEM='https://api.ellipsis-drive.com/v3/path/947a5370-d3c8-4a38-a865-5d40ffe68c17/raster/timestamp/5204cc5b-e6bd-49cf-89ec-cce80fb11e48/tile/{z}/{x}/{y}?style=8d7cbf2c-e090-4460-be57-caf1f9116ad4&token=epat_EDVTAZoCwZkdXyiqdN6maeeb1d6m3yD3ZP5S6OXaEz5iPE1Ht0vSYqbqUeQmir7C'
xyz_DEM='https://api.ellipsis-drive.com/v3/path/cb6ae9bb-ddf7-4e5a-a77e-e7aae2776ad8/raster/timestamp/b19b2f73-3bc3-46bb-a043-09c01c77d506/tile/{z}/{x}/{y}?style=801c69ff-2364-46d8-804b-2a79d65fb3f2&token=epat_93TjyBAf6LLAFP7DPHeIDgnUW0BRqVjOMWqpRK4X7n5TZGHddK8hkn6tOYd8U958'
#xyz_DEM='https://api.ellipsis-drive.com/v3/path/cb6ae9bb-ddf7-4e5a-a77e-e7aae2776ad8/styleSheet?timestampId=b19b2f73-3bc3-46bb-a043-09c01c77d506&style=801c69ff-2364-46d8-804b-2a79d65fb3f2&token=epat_93TjyBAf6LLAFP7DPHeIDgnUW0BRqVjOMWqpRK4X7n5TZGHddK8hkn6tOYd8U958'
#xyz_DEM='https://api.ellipsis-drive.com/v3/ogc/wms/58365cdd-cf3d-4601-909d-f58feead0c94?request=getCapabilities&token=epat_kWzCbaNxMyqIcBXfMiZrBkfzLNqQ3HtucrG9qFPHFQEXIPvAD6b1kURnPWkvWhjx'
#58365cdd-cf3d-4601-909d-f58feead0c94
#xyz_url='https://api.ellipsis-drive.com/v3/path/b7e05dc1-89d9-4d1a-962c-7eefd64a26c0/raster/timestamp/97f84ffd-df2d-4118-9a9b-56732eb22781/tile/{z}/{x}/{y}?style=570eeada-f46f-4bcc-bc45-500a2bb48069&token=epat_a2M7uKJi2geaRaQFGamaqLCeae4l1StrazI0mn27bNJbPwMitzKJgRF14Rxi0poK'
hillshade_layer=f.raster_layers.TileLayer(tiles=xyz_hillshade, attr = 'ED', max_native_zoom=17)
hillshade_layer.add_to(folium_map)


dem_layer=f.raster_layers.TileLayer(tiles=xyz_DEM, attr = 'ED', max_native_zoom=17)
dem_layer.add_to(folium_map)

#mk.add_to(folium_map)
#st.markdown(folium_map._repr_html_(), unsafe_allow_html =True)
st.set_page_config(page_title=None, layout="wide")
streamlit_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo&display=swap');

            html, body, [class*="css"]  {
            font-family: 'Nanum Myeongjo', serif;
            }
            </style>
            """
st.markdown(streamlit_style, unsafe_allow_html=True)

#===============================================================================
# [theme]
# base="dark"
# primaryColor="#358343"
# textColor="#57e043"
#===============================================================================




st.title("Topographic and bathymetric Digital Terrain Model\n Lake Ontario and Upper St. Lawrence River")

#===============================================================================
# def my_widget(key):
#     st.subheader('Info')
#     return st.button("Click me " + key)
#===============================================================================

with st.sidebar:
    #clicked = st.button('More info...')
    #if clicked:
    st.write('Seamless Digital Terrain Model created from various topographic and bathymetric data sources')
    st.write('Elevation values are in IGLD85 (m) and each tiles are projected in EPSG: 32617, 32618 and 32619 according to the UTM zone they belong to.')
    st.write('This overview is a 100m resolution mosaic of the DTM in EPSG:4326') 
    st.write('Click on a tile to download a 10m resolution DTM (ECCC members only), Note that 1m resolution DTM are also available on demand by email')
    st.write('Complete methodology and metadata will be available soon')
    st.write('The complete St.Lawrence River and United States portions should be added in a few months')
    st.write('For any comments or enquiries send an email to  antoine.maranda@ec.gc.ca')
    st.write('Author: Antoine Maranda')
    st.write('Contributors: Dominic Thériault, Charles Marcotte and Patrice Fortin')
    st.write('©Environment and Climate Change Canada, National Hydrologic Services, Hydrodynamic and Ecohydraulic Section, 2022')
    st.write(f'Last update: {date.today()}')
folium_static(folium_map, 1200, 700)
#html_map = folium_map._repr_html_()

#html_map = folium_static(folium_map, width=1000, height=500)
#maps=components.html(folium_map.render(), height=500, width=1000)

#st.markdown(html_map, unsafe_allow_html =True)
#_max_width_()

#===============================================================================
# cmd=fr'streamlit run "C:\Users\MarandaA\eclipse-workspace\py_antoine\geo_env\DEM\webmap.py"'
# 
# os.system(cmd)
# 
# quit()
#===============================================================================



