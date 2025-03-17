const options = {
  method: "GET",
  headers: {
    "X-RapidAPI-Key": "e63338f0d2mshd9d9c1cf8311cc4p1aae77jsn7031af475daa",
    "X-RapidAPI-Host": "weather-by-api-ninjas.p.rapidapi.com",
  },
};

const getWeather = (city) => {
  cityName.innerHTML = city;
  fetch("https://weather-by-api-ninjas.p.rapidapi.com/v1/weather?city=" + city, options)
    .then((response) => response.json())
    .then((response) => {
      console.log("Weather API Response:", response);
      cloud_pct.innerHTML = response.cloud_pct;
      temp.innerHTML = response.temp;
      feels_like.innerHTML = response.feels_like;
      feels_like2.innerHTML = response.feels_like;
      humidity2.innerHTML = response.humidity;
      humidity.innerHTML = response.humidity;
      min_temp.innerHTML = response.min_temp;
      max_temp.innerHTML = response.max_temp;
      wind_speed.innerHTML = response.wind_speed;
      wind_degrees.innerHTML = response.wind_degrees;
      sunrise.innerHTML = response.sunrise;
      sunset.innerHTML = response.sunset;

      // After fetching weather data, now fetch flood prediction
      getFloodPrediction(city);
    })
    .catch((err) => console.error("Weather API Error:", err));
};

// Function to get flood prediction from Flask backend
const getFloodPrediction = (city) => {
  fetch("/predicts.html", {  // Fix API endpoint
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ city: city }), // Send data in URL-encoded format
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Flood Prediction Response:", data);
      
      if (data.error) {
        document.getElementById("flood_prediction").innerHTML = "Error: " + data.error;
        return;
      }

      document.getElementById("flood_prediction").innerHTML =
        data.flood_risk === "Safe" ? "🟢 Safe" : "🔴 Unsafe";
    })
    .catch((err) => console.error("Flood Prediction Error:", err));
};

// Event listener for submit button
document.getElementById("submit").addEventListener("click", (e) => {
  e.preventDefault();
  getWeather(city.value);
});

// Default city when page loads
getWeather("Delhi");
