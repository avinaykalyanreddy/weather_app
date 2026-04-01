from django.shortcuts import render
from .forms import InputForm
import requests
import google.generativeai as genai
from django.contrib import messages
import os



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def input_func(request):

    result = None

    if request.method == "POST":
        form = InputForm(request.POST)

        if form.is_valid():
            city = form.cleaned_data["city"]

            # Weather API
            url = f"http://api.weatherapi.com/v1/forecast.json?key=a15695c861f74c7cacb74541263003&q={city}&days=1"
            res = requests.get(url)
            data = res.json()

            if "error" not in data:
                current = data["current"]

                # Build AI prompt
                prompt = f"""
                You are an expert agriculture advisor.

                Weather:
                - Location: {city}
                - Temperature: {current['temp_c']}°C
                - Humidity: {current['humidity']}%
                - Condition: {current['condition']['text']}

                Give output in this EXACT format:

                🌱 Vegetables:
                - Name | Duration | Shelf Life | Reason

                🍎 Fruits:
                - Name | Duration | Shelf Life | Reason

                🌾 Crops:
                - Name | Duration | Shelf Life | Reason

                ⚙️ Tips:
                - Short bullet points

                Rules:
                - Use bullet points only
                - Keep each line short (max 1 line)
                - No paragraphs
                - Make it easy for farmers to read
                
                with more accurate data mention header Name | Duration | Shelf Life | Reason for each section vegetable 
                Fruits Crops pick top 6 where people use daily for each section 
                """

                model = genai.GenerativeModel("gemini-3-flash-preview")
                try:
                   ai_response = model.generate_content(prompt)
                   ai_text = ai_response.text


                except:

                    ai_text = "AI service temporarily unavailable"

                result = {
                    "city": city,
                    "temp": current["temp_c"],
                    "condition": current["condition"]["text"],
                    "ai": ai_text
                }

            else:

                messages.error(request, "No matching location found")




    else:
        form = InputForm()

    return render(request, "user_input.html", {
        "form": form,
        "result": result,

    })