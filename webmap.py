#!/usr/bin/env python
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
#import requests

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


#===============================================================================
# url='https://api.ellipsis-drive.com/v3/path/4dcef727-21d2-4bb4-b672-44fdef18c03d/file/data?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZTQ4NTM5M2EtNzI2Mi00YTg4LTkzNzUtODI4OTg3MzJkMzczIiwiaWF0IjoxNjcxMDQ0MDI0LCJleHAiOjE2NzM3MjI0MjR9.UCuwowNeUnd8TdiIABiE6rGy4QyDyQhJXkZgnz81e3M'
# download=requests.get(url)
# print(download)
# quit()
#===============================================================================

def popup_html(z):
    tile_id=f'Tile: {int(z["properties"]["id"])}'
    utm=f'UTM zone: {str(int(z["properties"]["UTM"]))}'
    link=f'https://raw.githubusercontent.com/eccc-Antoine/DEM_GLAM_app/main/1m_DTM_overview2/{int(z["properties"]["id"])}_1m_DEM_idw_filtered_hillshade.png'
    #link2=f'https://raw.githubusercontent.com/eccc-Antoine/DEM_GLAM_app/main/plotly_html/{int(z["properties"]["id"])}_100m.html'
    #link2='http://htmlpreview.github.io/?https://github.com/eccc-Antoine/DEM_GLAM_app/blob/main/plotly_html/170_100m.html'
    #link2=f'https://raw.githack.com/eccc-Antoine/DEM_GLAM_app/main/plotly_100m_3D/{int(z["properties"]["id"])}_100m.html'
   
    html = """
<!DOCTYPE html>
<html>
<center><p> """ + tile_id + """ </p></center>
<center><p> """ + utm + """ </p></center>
<center><a href=\"""" + link + """\" target="_blank">Tile overview (1m res)</a></center>

</html>
"""
    return html
    
for z in js_data['features']:
    #link=f'https://007gc-my.sharepoint.com/personal/antoine_maranda_ec_gc_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m%2F{int(z["properties"]["id"])}%5F10m%5FDEM%5Fidw%2Ezip&parent=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m&ga=1'
    b = f.GeoJson(z['geometry'], tooltip=f'Tile: {int(z["properties"]["id"])}', name='Tiles')
    #b.add_child(f.Popup(f'Tile: {str(int(z["properties"]["id"]))} \n UTM_ZONE: {str(int(z["properties"]["UTM"]))} \n <a href={link} target="_blank">download (ECCC members only)</a>' ))
    html = popup_html(z)
    #b.add_child(f.Popup(f'Tile: {str(int(z["properties"]["id"]))} \n UTM_ZONE: {str(int(z["properties"]["UTM"]))}'))
    b.add_child(f.Popup(f.Html(html, script=True), min_width=300, max_width=300))
    b.add_to(folium_map)

##hillshade_4326
## dont seem to ba available anymore from ellipsis (copy XYZ path link and adapt to fit this pattern)
#xyz_hillshade='https://api.ellipsis-drive.com/v3/path/58365cdd-cf3d-4601-909d-f58feead0c94/raster/timestamp/d076f5ea-b93c-49e3-b809-a452895ffb4d/tile/{z}/{x}/{y}?style=ffc495e8-9dc1-44fd-9ca4-cc813f7970bc&token=epat_cyWz6w9UyHVTqmBplpDYT7x4pIsF1ucCIkfrXTjUUG1FJsyU3otkGqKYpX2S1dfo'
#xyz_hillshade='https://api.ellipsis-drive.com/v3/path/4a0dc72e-613c-40d3-bd16-10fa6b02f76b/raster/timestamp/078210ff-b941-4482-bc53-cd9915f45b78/tile/{z}/{x}/{y}?style=76fe80c8%2d5596%2d4481%2d9159%2ded16d50689bb&token=epat_7ET8ZDhEl0cRU4cEyHYei8STvCkAIGhj9pIIr4IvdwdNOUqmocDxJBJDvycLzUBM'
xyz_hillshade='https://api.ellipsis-drive.com/v3/path/6c500157-ddc3-4ee6-ba56-995b7fce7c3a/raster/timestamp/477207fd-39f0-4b87-acfd-48142c0a0b4f/tile/{z}/{x}/{y}?style=dc490889-3eaa-41df-b37a-96006b95d780&token=epat_j2PrTLqXDwJW9EiKZbaGzr9chhCrUACOWsZ0ZBOzvU2p6oo5CqliKOBw4io0SOeZ'

##DEM_4326
## dont seem to ba available anymore from ellipsis (copy XYZ path link and adapt to fit this pattern)
#xyz_DEM='https://api.ellipsis-drive.com/v3/path/cb6ae9bb-ddf7-4e5a-a77e-e7aae2776ad8/raster/timestamp/b19b2f73-3bc3-46bb-a043-09c01c77d506/tile/{z}/{x}/{y}?style=801c69ff-2364-46d8-804b-2a79d65fb3f2&token=epat_93TjyBAf6LLAFP7DPHeIDgnUW0BRqVjOMWqpRK4X7n5TZGHddK8hkn6tOYd8U958'
#xyz_DEM='https://api.ellipsis-drive.com/v3/path/3853ae6f-5c70-43c0-81d2-d1df4558510b/raster/timestamp/088a7ed4-d0b7-4aea-a7cb-868e398fc866/tile/{z}/{x}/{y}?style=4eac556d%2dada4%2d4995%2d9a2a%2d83d76e594236&token=epat_yAzrz2vUde9NBFt4N71HRTOsePLqmBmKGfxCd9Dfv4BfrUJhN5V0JUxDLGU4ESB1'
xyz_DEM='https://api.ellipsis-drive.com/v3/path/03cf5d98-4bfd-430a-88d2-17a197413993/raster/timestamp/ad2301e1-2409-405a-abce-dc53d47467c2/tile/{z}/{x}/{y}?style=c83a840d-d2c9-4257-b676-ea17065a3314&token=epat_7wS4MJ5XqrwjRBn2B8xcfy8HPM29jDLbhSetvKq1VWDj04sQ3Dlc9ImGRSYeAOx0'

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

#repo_link='https://007gc-my.sharepoint.com/personal/antoine_maranda_ec_gc_ca/_layouts/15/onedrive.aspx?login_hint=antoine%2Emaranda%40ec%2Egc%2Eca&id=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m'
#st.title(f"Version 4.2 of Topographic and bathymetric Digital Terrain Model\n Lake Ontario and Upper St. Lawrence River [Download Repository (ECCC members only)]({repo_link})")
#repo_link='https://007gc-my.sharepoint.com/:f:/r/personal/antoine_maranda_ec_gc_ca/Documents/DEM_GLAM/DTM_LKO_USL_CAN_v4?csf=1&web=1&e=4tdin7'
#repo_link='https://007gc-my.sharepoint.com/personal/antoine_maranda_ec_gc_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDTM%5FLKO%5FUSL%5Fv4&view=0'
repo_link='https://ijccmi.sharepoint.com/sites/GLAM/ILOSLRB%20Technical%20Teams/Forms/AllItems.aspx?csf=1&web=1&e=QzZsej&CID=c6846815%2Dc9d1%2D4d59%2Da204%2D63366a96e9a9&FolderCTID=0x012000290495FEB2027644A86E4691A6154C95&id=%2Fsites%2FGLAM%2FILOSLRB%20Technical%20Teams%2FExternal%20Data%20Sharing%2FDEM%5FLKO%5FUSL%5FSLR%5FV4%5F2&viewid=3f981477%2D2845%2D4f20%2Db31c%2Dceae155d20b2'
#repo_link='https://007gc-my.sharepoint.com/:f:/g/personal/antoine_maranda_ec_gc_ca/Er5RUAKOWQROpjumUgyyPg4Bv10ZLSsNg-mUpcsBviUlOg?e=57q7Y3'
plotly_link='https://007gc-my.sharepoint.com/:f:/g/personal/antoine_maranda_ec_gc_ca/EmYSvAyqCv9MnqSQw2Ic9BEB0AYRx9XJYZkeWZMUzLdiXg?e=0WdUCJ'
st.title(f"PRELIMINARY VERSION of Topobathymetric Digital Elevation Model (Lake Ontario and Upper St. Lawrence River)")
members='(GLAM members only)'
st.header(f'[Full resolution DTM Download Repository {members}]({repo_link})')
st.subheader('Or click on a tile for a 1m resolution overview')
#link_mosaic='https://007gc-my.sharepoint.com/personal/antoine_maranda_ec_gc_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m%2Fmosaic%5F100m%5F4326%2Ezip&parent=%2Fpersonal%2Fantoine%5Fmaranda%5Fec%5Fgc%5Fca%2FDocuments%2FDEM%5FGLAM%2FDEM%5F10m'
#link_mosaic='https://007gc-my.sharepoint.com/:u:/g/personal/antoine_maranda_ec_gc_ca/ERUhVqRdYQtNnaks3JKOkgMBydx9qBcmaAZNfMg19Be9yw?e=sdwrMt'
link_mosaic='https://ijccmi.sharepoint.com/:i:/r/sites/GLAM/ILOSLRB%20Technical%20Teams/External%20Data%20Sharing/DEM_LKO_USL_SLR_V4_2/mosaic_100m_32618.tif?csf=1&web=1&e=soxgJX'

with st.sidebar:
    #clicked = st.button('More info...')
    #if clicked:
    st.write('Version 4.2 of Topobathymetric Digital Elevation Model created from various topographic and bathymetric data sources')
    st.write('This is product is in conitnuous imporovement and should be used and shared with caution')
    st.write('DTMs are available at 1 and 10 meter resolution')
    st.write('Elevation values are in IGLD85 (m) and each tiles are projected in EPSG: 32617, 32618 and 32619 according to the UTM zone they belong to')
    st.write('Attached log files provide information on DEM creation process and dataset prioritization')
    st.write(f"This overview is a 100m resolution mosaic of the DEM in EPSG:4326 [Download (ECCC members only)]({link_mosaic})")
    st.write('Complete methodology and metadata will be available in the next few months')
    st.write('St.Lawrence River portion up to Trois-Rivières should be added in a few months')
    st.write('For any comments or enquiries send an email to  antoine.maranda@ec.gc.ca')
    st.write('Author: Antoine Maranda')
    st.write('Contributors: Dominic Theriault, Patrice Fortin and Charles Marcotte')
    st.write('©Environment and Climate Change Canada, National Hydrologic Services, Hydrodynamic and Ecohydraulic Section, 2023')
    st.write(f'Last update: {date.today()}')
folium_static(folium_map, 1200, 700)


#===============================================================================
# cmd=fr'streamlit run "C:\Users\MarandaA\eclipse-workspace\py_antoine\geo_env\DEM\webmap.py"'
# 
# os.system(cmd)
# 
# quit()
#===============================================================================



