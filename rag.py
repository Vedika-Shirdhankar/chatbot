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
            # 🔥 better slicing (not just first 3000 chars)
            chunks = [pdf_text[i:i+1000] for i in range(0, len(pdf_text), 1000)]

            # simple keyword match
            relevant_chunks = [c for c in chunks if user_input.lower() in c.lower()]

            context = "\n".join(relevant_chunks[:3]) if relevant_chunks else pdf_text[:2000]

            prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question: {user_input}

If answer not found, say: Not found in document.
"""

        return get_ollama_response(prompt)

    except Exception as e:
        return f"Error: {str(e)}"