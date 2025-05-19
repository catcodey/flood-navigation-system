import rasterio
import matplotlib.pyplot as plt
import numpy as np
import geopy.geocoders
import os
import requests

# DEM Save Path
DEM_PATH = "/Users/bbhavna/Desktop/final project code/backend/outputs/dem_map.png"
DEM_TIF_PATH = "/Users/bbhavna/Desktop/final project code/backend/outputs/place_dem.tif"

# Get Coordinates Using Nominatim
def get_coordinates(place):
    geolocator = geopy.geocoders.Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(place)
    if location:
        return round(location.latitude, 6), round(location.longitude, 6)
    else:
        return None, None

# Generate Bounding Box
def get_bounding_box(lat, lon):
    offset = 0.0045
    return (lat - offset, lat + offset, lon - offset, lon + offset)

# Download DEM Using OpenTopography
def download_dem(place, api_key="2b849f869a6fde8f92daf278f98fecf9"):
    global center_coords
    lat, lon = get_coordinates(place)
    lat=lat-0.000663
    lon=lon+0.002813
    if not lat or not lon:
        return False
    
    south, north, west, east = get_bounding_box(lat, lon)
    dem_url = (f"https://portal.opentopography.org/API/globaldem?demtype=SRTMGL1"
               f"&south={south}&north={north}&west={west}&east={east}"
               f"&outputFormat=GTiff&API_Key={api_key}")
    
    center_coords=(lat,lon)
    response = requests.get(dem_url)
    if response.status_code == 200:
        with open(DEM_TIF_PATH, "wb") as f:
            f.write(response.content)
        return True
    return False

def gearth_img_save():
    import folium
    
    import io
    from PIL import Image


    lat = center_coords[0]
    lon= center_coords[1]

    # Create a folium map centered at Mahalingapuram with satellite tiles
    m = folium.Map(location=[lat,lon], zoom_start=15, tiles=None)

    # Add Satellite Layer (Esri)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Satellite"
    ).add_to(m)

    # Display the map directly in Colab
  
    import io
    from PIL import Image
    import selenium

    img_data = m._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    # Convert RGBA to RGB before saving
    if img.mode == "RGBA":
        img = img.convert("RGB")
    img.save('/Users/bbhavna/Desktop/final project code/backend/outputs/gearth_image.jpg')

# Generate DEM Map and Save as PNG
def generate_dem(place):
    if not download_dem(place):
        return False
    
    with rasterio.open(DEM_TIF_PATH) as dem:
        dem_data = dem.read(1).astype(float)
        dem_data[dem_data == dem.nodata] = np.nan
        dem_data = np.nan_to_num(dem_data, nan=np.nanmin(dem_data))
    
    plt.figure(figsize=(10, 8))
    plt.imshow(dem_data, cmap="terrain", origin="upper", interpolation="bilinear")
    plt.axis("off")
    plt.savefig(DEM_PATH, dpi=300, bbox_inches="tight", pad_inches=0)
    plt.close()
    return True
    #gearth_img_save()

 


