import flask
from flask import Flask, render_template, request, jsonify
import mysql.connector
import pickle
import base64
import requests
from training import prediction

app = flask.Flask(__name__)

# Predefined cities and months
cities = [{'name': 'Delhi', "sel": "selected"}, {'name': 'Mumbai', "sel": ""}, 
          {'name': 'Kolkata', "sel": ""}, {'name': 'Bangalore', "sel": ""}, 
          {'name': 'Chennai', "sel": ""}, {'name': 'New York', "sel": ""}, 
          {'name': 'Los Angeles', "sel": ""}, {'name': 'London', "sel": ""}, 
          {'name': 'Paris', "sel": ""}, {'name': 'Sydney', "sel": ""}, 
          {'name': 'Beijing', "sel": ""}]

months = [{"name": "May", "sel": ""}, {"name": "June", "sel": ""}, {"name": "July", "sel": "selected"}]

# Load ML Model
try:
    with open("training/model.pickle", 'rb') as model_file:
        model_data = pickle.load(model_file)
        model = model_data["model"]
        print(f"✅ Model loaded successfully. Expected Features: {model.n_features_in_}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# MySQL Connection
# mysql = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Prakhar@2004",
#     database="flood"
# )
# cursor = mysql.cursor()

# Home Page
@app.route("/")
# @app.route('/index.html')
# def index():
#     return render_template("index.html")

# Register Volunteer Route
# @app.route('/register', methods=['POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         subject = request.form.get('subject')

#         if not name or not email or not subject:
#             return "Error: Missing form fields!", 400

#         query = "INSERT INTO volunteer (name, email, subject) VALUES (%s, %s, %s)"
#         cursor.execute(query, (name, email, subject))
#         mysql.commit()

#         return render_template("index.html", registration_success=True)

#Different Web Pages
@app.route('/plots.html')
def plots():
    return render_template('plots.html')

# @app.route('/heatmaps.html')
# # def heatmaps():
# #     return render_template('heatmaps.html')

# @app.route('/satellite.html')
# def satellite():
#     direc = "processed_satellite_images/Delhi_July.png"
#     with open(direc, "rb") as image_file:
#         image = base64.b64encode(image_file.read()).decode('utf-8')
    
#     return render_template('satellite.html', data=cities, image_file=image, months=months, text="Delhi in January 2020")

# Flood Prediction Route
@app.route('/predicts.html', methods=["GET", "POST"])
def get_predicts():
    cityname = request.form.get("city")

    if not cityname:
        return render_template('predicts.html', error="City name is missing!", cities=cities)

    print(f"✅ Received City: {cityname}")

    # API Request to Fetch Latitude & Longitude
    URL = "https://geocode.search.hereapi.com/v1/geocode"
    API_KEY = 'WwoKB74UsD0vvwIwbs-pLuLX2Mimm0yi0ThBD2H1FAA'  # ⚠️ Replace with your actual API key
    PARAMS = {'apikey': API_KEY, 'q': cityname}
    
    try:
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        print(f"📍 Geolocation API Response: {data}")
    except Exception as e:
        print(f"❌ API Request Error: {e}")
        return render_template('predicts.html', error="Failed to fetch location data!", cities=cities)

    if 'items' not in data or not data['items']:
        print(f"❌ Error: No location found for {cityname}")
        return render_template('predicts.html', error="Could not fetch location data!", cities=cities)

    latitude = data['items'][0]['position']['lat']
    longitude = data['items'][0]['position']['lng']
    print(f"🌍 Latitude: {latitude}, Longitude: {longitude}")

    # Fetch Weather Data for Prediction
    try:
        final = prediction.get_data(latitude, longitude)
        prediction_result = model.predict([final])[0]
        pred = "Safe" if str(prediction_result) == "0" else "Unsafe"

        return render_template(
            'predicts.html',
            cityname=f"Information about {cityname}",
            cities=cities,
            latitude=latitude,  # ✅ Passing coordinates to the template
            longitude=longitude,
            temp=round(final[0], 2),
            maxt=round(final[1], 2),
            wspd=round(final[2], 2),
            cloudcover=round(final[3], 2),
            percip=round(final[4], 2),
            humidity=round(final[5], 2),
            pred=pred
        )
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return render_template('predicts.html', error=f"Prediction failed: {e}", cities=cities)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
