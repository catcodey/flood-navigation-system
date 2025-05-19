def generate_google_earth_image(place):
    """Return pre-saved Google Earth image path for the given place."""
    
    # Dictionary to map place names to respective image paths
    place_to_path = {
        "nungambakkam": "/Users/bbhavna/Desktop/final project code/backend/gearthimgs/ngmbkm gearth.jpg",
        "mahalingapuram": "/Users/bbhavna/Desktop/final project code/backend/gearthimgs/maha.jpg"
    }

    # Check if place is available
    if place in place_to_path:
        im_path = place_to_path[place]
        print(f"✅ Returning Google Earth image for {place}: {im_path}")
        return im_path
    else:
        print(f"❌ No Google Earth image available for: {place}")
        return None
