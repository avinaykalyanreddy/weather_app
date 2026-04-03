from sys import exception

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
                language = form.cleaned_data["language_field"]
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
                
                give content in {language} with html tags make each section with table with more accurate data mention header Name | Duration | Shelf Life | Reason for each section vegetable 
                Fruits Crops pick top 6 where people use daily for each section 
                """


                models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-flash-latest", "gemini-2.5-flash-lite",
                          "gemini-pro-latest", "gemini-2.0-flash",
                          "gemini-2.0-flash-001", "gemini-2.0-flash-lite", "gemini-2.0-flash-lite-001",
                          "gemini-3-flash-preview", "gemini-3-pro-preview",
                          "gemini-3-pro-preview", "gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview",
                          "gemma-3-27b-it", "gemma-3-12b-it", "gemma-3-12b-it",
                          "gemma-3-4b-it", "gemma-3-1b-it"]

                for m in models:

                    model = genai.GenerativeModel(m)

                    try:
                        ai_response = model.generate_content(prompt)
                        ai_text = ai_response.text
                        break


                    except Exception as e:
                        print(f"Model {m} failed:", e)
                        continue
                else:
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