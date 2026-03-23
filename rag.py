from ollama_client import get_ollama_response

# Global storage
pdf_text = ""


def set_pdf_text(text):
    global pdf_text
    pdf_text = text


def clear_pdf_text():
    global pdf_text
    pdf_text = ""


def generate_response(user_input):
    try:
        # ✅ CASE 1: No PDF uploaded → normal chat
        if not pdf_text.strip():
            prompt = f"""
You are a helpful AI assistant.

Answer the question clearly and simply.

User: {user_input}
"""

        # ✅ CASE 2: PDF uploaded → smart behavior
        else:
            prompt = f"""
You are an intelligent AI assistant.

You have access to a document.

Follow these rules:
1. First check if the answer exists in the document.
2. If YES → answer using the document.
3. If NO → say "Not found in document." and then answer using your general knowledge.

Keep answers clear and structured.

Document:
{pdf_text[:4000]}

Question: {user_input}
"""

        return get_ollama_response(prompt)

    except Exception as e:
        return f"Error: {str(e)}"