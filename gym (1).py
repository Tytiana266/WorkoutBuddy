from flask import Flask, request, jsonify, Response, render_template
import openai
import config
import requests  # Make sure to import requests


openai.api_key = config.API_KEY

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("workout.html")

@app.route("/goalText", methods=["POST"])
def get_text():
    #app.logger.debug("Received request: %s", request.json)  # Log the incoming request data
    data = request.json
    context = data.get("goalText")
    question = data.get("workoutText")
    userText = f"Create me a workout plan based on content:\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"

    try:
        response = openai.chat.completions.create(

            model="gpt-4",
      messages=[
          {
              "role": "system",
              "content": context,
          },
          {
              "role": "user",
              "content": userText,
          },
      ],
        
      )
        
        workout_plan = response.choices[0].message.content
        #app.logger.debug("Generated answer: %s", answer)
    except Exception as e:
        #app.logger.error("Error: %s", str(e))
        return jsonify({"error": str(e)}), 500

    return jsonify({"workoutPlan": workout_plan})

'''image'''
@app.route("/generate-image", methods=["POST"])
def generate_image():
    description = request.json['description']
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        # Getting the image content from the URL
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            return Response(image_response.content, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'Failed to fetch the generated image.'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/readmyworkout", methods=["POST"])
def speak_workout():
    workout_text = request.json['workoutText']
    engine = pyttsx3.init()
    engine.say(workout_text)
    engine.runAndWait()
    return jsonify({'message': 'Workout plan spoken.'})

@app.route("/responseText", methods=["POST"])
def gett_text():
    #app.logger.debug("Received request: %s", request.json)  # Log the incoming request data
    data = request.json
    context = data.get("responseText")
    question = data.get("workoutText")
    userText = f"Create me a workout plan based on content:\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"

    try:
        response = openai.chat.completions.create(

            model="gpt-4",
      messages=[
          {
              "role": "system",
              "content": context,
          },
          {
              "role": "user",
              "content": userText,
          },
      ],
        
      )
        
        workout_plan = response.choices[0].message.content
        #app.logger.debug("Generated answer: %s", answer)
    except Exception as e:
        #app.logger.error("Error: %s", str(e))
        return jsonify({"error": str(e)}), 500

    return jsonify({"workoutPlan": workout_plan})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

# flask --app gym run --debug --host=0.0.0.0
# Go to Project -> Box Info -> Dynamic Content
# https://caravanjupiter-fishvitamin-5000.codio.io


