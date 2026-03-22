from flask import Flask, render_template, request, jsonify
from rag import generate_response, set_pdf_text
from file_handler import extract_text_from_pdf
import os

app = Flask(__name__)

# create uploads folder if not exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"response": "No message received"})

        user_input = data["message"]

        print("User:", user_input)

        response = generate_response(user_input)

        print("AI:", response)

        return jsonify({"response": response})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"response": f"Error: {str(e)}"})


# ✅ NEW: File Upload Route
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"message": "No file uploaded"})

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        print("File saved:", filepath)

        # extract text
        text = extract_text_from_pdf(filepath)

        print("Extracted text length:", len(text))

        # store for RAG
        set_pdf_text(text)

        return jsonify({"message": "PDF uploaded and processed successfully"})

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({"message": f"Error: {str(e)}"})


# Run app
if __name__ == "__main__":
    app.run(debug=True)