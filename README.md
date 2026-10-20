# MapBiomas raster classroom dashboard

Streamlit study project for clipping an uploaded classified GeoTIFF to an
uploaded polygon, rendering the classes on a Folium map and estimating the area
of each class.

## Expected inputs

- one GeoTIFF with MapBiomas-style integer class values;
- one polygon dataset readable by GeoPandas and carrying a CRS.

The application reprojects the polygon to the raster CRS when necessary. The
area calculation assumes every pixel represents exactly 900 m², so its hectare
results are valid only for a 30 m × 30 m raster. No resolution check enforces
that assumption.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run home.py
```

## Status and limitations

This is an untested teaching prototype. It has no sample input, automated test,
NoData handling or validation of the class legend. A compiled Python cache is
unnecessarily tracked. An existing license file is present, but input-data
rights remain the operator's responsibility.
