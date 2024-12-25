from fastapi import FastAPI, Query
from models.text import load_text_model, generate_text

app = FastAPI()


@app.get("/generate/text")
def serve_language_model_controller(prompt=Query(...)):
    pipe = load_text_model()
    output = generate_text(pipe, prompt)
    return output
