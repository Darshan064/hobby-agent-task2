from flasgger import Swagger
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API Key
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq Client
client = Groq(api_key=api_key)

# Create Flask App
app = Flask(__name__)

# Swagger Initialization
Swagger(app)

# Fictional / Private Persons (Mock MCP Data)
fictional_people = {

    "Darshan": {
        "linkedin": "Darshan enjoys playing cricket and learning new technologies.",
        "instagram": "Watching movies, cricket highlights, and fun reels.",
        "facebook": "Sleeping, entertainment, and spending time with friends.",
        "resume": "Interested in cricket, movies, and relaxing activities."
    },

    "rahul sharma": {
        "linkedin": "Rahul enjoys photography and coding.",
        "instagram": "Traveling and gaming.",
        "facebook": "Music and cooking.",
        "resume": "Interested in cricket and cycling."
    }

}


# Home Route
@app.route("/")
def home():
    return jsonify({
        "message": "AI Hobby Extraction Agent Running"
    })


# Ask Route
@app.route('/ask', methods=['POST'])
def ask():
    """
    Ask celebrity hobbies
    ---
    tags:
      - Hobby API
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            name:
              type: string
              example: Virat Kohli
    responses:
      200:
        description: Returns hobbies
    """

    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({
            "status": "error",
            "message": "Please provide celebrity name"
        }), 400

    celebrity_name = data["name"].lower()

    prompt = f"""
    Give only hobbies/interests of {celebrity_name}.
    Return response as bullet points.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        raw_hobbies = response.choices[0].message.content

        hobbies = [
            hobby.replace("*", "").strip()
            for hobby in raw_hobbies.split("\n")
            if hobby.strip()
        ]

        return jsonify({
            "name": celebrity_name,
            "hobbies": hobbies,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Run Flask App
if __name__ == "__main__":
    app.run(debug=True, port=5000)