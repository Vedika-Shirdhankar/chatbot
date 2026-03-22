from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

from rag import generate_response, set_pdf_text
from file_handler import extract_text_from_pdf

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# HOME ROUTE
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# CHAT API
@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()

        if not data or "message" not in data:
            return JSONResponse(content={"response": "No message received"})

        user_input = data["message"]

        print("\n--- USER QUESTION ---")
        print(user_input)

        response = generate_response(user_input)

        print("\n--- AI RESPONSE ---")
        print(response)

        return JSONResponse(content={"response": response})

    except Exception as e:
        print("CHAT ERROR:", e)
        return JSONResponse(content={"response": f"Error: {str(e)}"})


# FILE UPLOAD API
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".pdf"):
            return JSONResponse(content={"message": "❌ Only PDF files allowed"})

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(filepath, "wb") as f:
            f.write(await file.read())

        print("\n=== FILE UPLOADED ===")
        print("Path:", filepath)

        # Extract text
        text = extract_text_from_pdf(filepath)

        print("\n=== EXTRACTED TEXT PREVIEW ===")
        print(text[:500])
        print("=== END PREVIEW ===\n")

        if not text or text.strip() == "" or "No text found" in text:
            return JSONResponse(content={
                "message": "⚠️ Could not extract text from this PDF. Try another file."
            })

        set_pdf_text(text)

        return JSONResponse(content={
            "message": "✅ PDF uploaded & processed successfully! Ask questions now."
        })

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return JSONResponse(content={"message": f"Error: {str(e)}"})