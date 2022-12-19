#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#import ellipsis as el
#allo
import folium as f
import streamlit as st
import os
import streamlit.components.v1 as components
from folium import plugins
import geopandas as gpd
import json
from datetime import date

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
tuiles='https://raw.githubusercontent.com/eccc-Antoine/DEM_GLAM_app/main/tuile_final3.geojson'
gdf_grille=gpd.read_file(tuiles)
gjson = gdf_grille.to_crs(epsg='4326').to_json()
js_data = json.loads(gjson)
for z in js_data['features']:
    link=f'https://007gc-my.sharepoint.com/personal/antoine_maranda_ec_gc_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m%2F{int(z["properties"]["id"])}%5F10m%5FDEM%5Fidw%2Ezip&parent=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m&ga=1'
    b = f.GeoJson(z['geometry'])
    b.add_child(f.Popup(f'Tile: {str(int(z["properties"]["id"]))} \n UTM_ZONE: {str(int(z["properties"]["UTM"]))} \n <a href={link} target="_blank">download (ECCC members only)</a>' ))
    b.add_to(folium_map)

##hillshade_4326
## dont seem to ba available anymore from ellipsis (copy XYZ path link and adapt to fit this pattern)
xyz_hillshade='https://api.ellipsis-drive.com/v3/path/58365cdd-cf3d-4601-909d-f58feead0c94/raster/timestamp/d076f5ea-b93c-49e3-b809-a452895ffb4d/tile/{z}/{x}/{y}?style=ffc495e8-9dc1-44fd-9ca4-cc813f7970bc&token=epat_cyWz6w9UyHVTqmBplpDYT7x4pIsF1ucCIkfrXTjUUG1FJsyU3otkGqKYpX2S1dfo'


##DEM_4326
## dont seem to ba available anymore from ellipsis (copy XYZ path link and adapt to fit this pattern)
xyz_DEM='https://api.ellipsis-drive.com/v3/path/cb6ae9bb-ddf7-4e5a-a77e-e7aae2776ad8/raster/timestamp/b19b2f73-3bc3-46bb-a043-09c01c77d506/tile/{z}/{x}/{y}?style=801c69ff-2364-46d8-804b-2a79d65fb3f2&token=epat_93TjyBAf6LLAFP7DPHeIDgnUW0BRqVjOMWqpRK4X7n5TZGHddK8hkn6tOYd8U958'
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

st.title("Topographic and bathymetric Digital Terrain Model\n Lake Ontario and Upper St. Lawrence River")

link_mosaic='https://007gc-my.sharepoint.com/personal/antoine_maranda_ec_gc_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m%2Fmosaic%5F100m%5F4326%2Ezip&parent=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m'

with st.sidebar:
    #clicked = st.button('More info...')
    #if clicked:
    st.write('Seamless Digital Terrain Model created from various topographic and bathymetric data sources')
    st.write('Elevation values are in IGLD85 (m) and each tiles are projected in EPSG: 32617, 32618 and 32619 according to the UTM zone they belong to.')
    st.write(f"This overview is a 100m resolution mosaic of the DTM in EPSG:4326 [link] (https://007gc-my.sharepoint.com/personal/antoine_maranda_ec_gc_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m%2Fmosaic%5F100m%5F4326%2Ezip&parent=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m)") 
    st.write('Click on a tile to download a 10m resolution DTM (ECCC members only), Note that 1m resolution DTM are also available on demand by email')
    st.write('Complete methodology and metadata will be available soon')
    st.write('The complete St.Lawrence River and United States portions should be added in a few months')
    st.write('For any comments or enquiries send an email to  antoine.maranda@ec.gc.ca')
    st.write('Author: Antoine Maranda')
    st.write('Contributors: Dominic Thériault, Charles Marcotte and Patrice Fortin')
    st.write('©Environment and Climate Change Canada, National Hydrologic Services, Hydrodynamic and Ecohydraulic Section, 2022')
    st.write(f'Last update: {date.today()}')
folium_static(folium_map, 1200, 700)


#===============================================================================
# cmd=fr'streamlit run "C:\Users\MarandaA\eclipse-workspace\py_antoine\geo_env\DEM\webmap.py"'
# 
# os.system(cmd)
# 
# quit()
#===============================================================================



