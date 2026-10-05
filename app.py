from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

model = joblib.load("crop_model.pkl")


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    recommendations = []
    error = None

    if request.method == "POST":
        N = float(request.form["N"])
        P = float(request.form["P"])
        K = float(request.form["K"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        ph = float(request.form["ph"])
        rainfall = float(request.form["rainfall"])

        if N < 0 or P < 0 or K < 0:
            error = "N, P and K values cannot be negative."

        elif temperature < -50 or temperature > 60:
            error = "Please enter a realistic temperature between -50°C and 60°C."

        elif humidity < 0 or humidity > 100:
            error = "Humidity must be between 0% and 100%."

        elif ph < 0 or ph > 14:
            error = "Soil pH must be between 0 and 14."

        elif rainfall < 0:
            error = "Rainfall cannot be negative."

        else:
            data = [[N, P, K, temperature, humidity, ph, rainfall]]

            prediction = model.predict(data)[0]

            probabilities = model.predict_proba(data)[0]
            top_3 = probabilities.argsort()[-3:][::-1]

            for i in top_3:
                recommendations.append({
                    "crop": model.classes_[i],
                    "probability": round(probabilities[i] * 100, 2)
                })

    return render_template(
        "index.html",
        prediction=prediction,
        recommendations=recommendations,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)