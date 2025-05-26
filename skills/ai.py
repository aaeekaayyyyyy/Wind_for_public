import openai

# Initialize the OpenAI client
openai.api_key = "your-api-key-here"

def aiProcess(command):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Wind skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
                {"role": "user", "content": command}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("OpenAI API error:", e)
        return "Sorry, something went wrong with the AI service."