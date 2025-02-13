import streamlit as st
from rasterio.io import MemoryFile
import geopandas as gpd
from rasterio.mask import mask
import cv2
import numpy as np
from utils import color_map
from utils import value_to_class
import folium
from streamlit_folium import st_folium
from folium.raster_layers import ImageOverlay

st.sidebar.title('Menu')

raster_file = st.sidebar.file_uploader('Selecione o raster (Mapbiomas) para análise',type=["tif","tiff"])
polygon_file = st.sidebar.file_uploader('Selecione o polígono a ser analisado')

if raster_file and polygon_file:
    with MemoryFile(raster_file.getvalue()) as memfile:
        with memfile.open() as src:
            polygon = gpd.read_file(polygon_file)

            if polygon.crs != src.crs:
                polygon = polygon.to_crs(src.crs)

            geometries = polygon.geometry
            out_image, out_transform = mask(src, geometries, crop=True)
            out_image = out_image[0]

            height, width = out_image.shape
            min_x, min_y = out_transform * (0,0)
            max_x, max_y = out_transform * (width,height)

            centroid_x, centroid_y = (min_x + max_x) / 2, (min_y + max_y) / 2

            rgb_image = np.zeros((height,width,4), dtype=np.uint8)

            for value, color in color_map.items():
                rgb_image[out_image == value] = color

            resized_image = cv2.resize(rgb_image,(width,height),interpolation=cv2.INTER_NEAREST)

            m = folium.Map(location=[centroid_y,centroid_x],zoom_start=8,tiles='Esri World Imagery')

            bounds = [[min_y,min_x],[max_y,max_x]]

            ImageOverlay(
                image=resized_image,
                bounds=bounds,
                opacity=0.7,
                interactive=True,
                cross_origin=False,
                zindex = 1
            ).add_to(m)

            folium.LayerControl().add_to(m)
            m.fit_bounds(bounds)
            st_folium(m,width="100%")

            unique_values, count = np.unique(out_image, return_counts=True)

            for value, count in zip(unique_values,count):
                class_name = value_to_class.get(value,"Unknown")
                area_ha = (count * 900)/10000
                st.write(f"{class_name}: {area_ha},ha")