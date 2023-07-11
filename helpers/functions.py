import requests

base_url = "https://v3.openstates.org"
api_key = "4349fe58-8a5c-4668-a799-d1dc7629890e"  # Replace with your OpenStates API key
geocoding_api_key = "1c698a0cd2594755b43caaa27ed53b82"  # Replace with your OpenCage Geocoding API key

def get_coordinates(zip_code):
    geocoding_url = f"https://api.opencagedata.com/geocode/v1/json?q={zip_code}&key={geocoding_api_key}"
    response = requests.get(geocoding_url)
    data = response.json()

    if data and "results" in data and data["results"]:
        for result in data["results"]:
            country = result["components"].get("country")
            if country == "United States":
                latitude = result["geometry"]["lat"]
                longitude = result["geometry"]["lng"]
                return latitude, longitude

    return None, None

def get_district_by_zip(zip_code):
    latitude, longitude = get_coordinates(zip_code)

    if latitude and longitude:
        url = f"{base_url}/people.geo?lat={latitude}&lng={longitude}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        if data and "results" in data and data["results"]:
            for result in data["results"]:
                district = result["current_role"]["district"]
                imgurl = result["image"]

                if "-" in district:
                    return district

    print("No district found for the provided ZIP code.")

def get_image_by_zip(zip_code):
    latitude, longitude = get_coordinates(zip_code)

    if latitude and longitude:
        url = f"{base_url}/people.geo?lat={latitude}&lng={longitude}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        if data and "results" in data and data["results"]:
            for result in data["results"]:

                district = result["current_role"]["district"]
                imgurl = result["image"]

                if "-" in district:
                    imgurl = result["image"]
                    return imgurl, district
                
def get_all_information(zip_code):
    latitude, longitude = get_coordinates(zip_code)

    if latitude and longitude:
        url = f"{base_url}/people.geo?lat={latitude}&lng={longitude}&apikey={api_key}"
        response = requests.get(url)
        return response.text

    print("No representative image found for the provided ZIP code.")
