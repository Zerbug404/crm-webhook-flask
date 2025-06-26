from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return "🟢 Webhook server is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        # Optional: log incoming data for debugging
        print("Received data:", data)

        # Example: extract user input
        user_message = data.get("message", "")

        # Use OpenAI to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content.strip()

        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
