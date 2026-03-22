import requests

def get_ollama_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        return data.get("response", "No response from AI")

    except Exception as e:
        return f"Ollama Error: {str(e)}"