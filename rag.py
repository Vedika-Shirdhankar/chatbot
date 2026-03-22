from ollama_client import get_ollama_response

pdf_text = ""

def set_pdf_text(text):
    global pdf_text
    pdf_text = text


def generate_response(user_input):
    try:
        if not pdf_text.strip():
            prompt = f"""
You are a helpful AI assistant.

User: {user_input}
"""
        else:
            prompt = f"""
Use this document to answer:

{pdf_text[:3000]}

Question: {user_input}
"""

        return get_ollama_response(prompt)

    except Exception as e:
        return f"Error: {str(e)}"