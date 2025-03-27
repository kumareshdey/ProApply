from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from service import (
    generate_cover_letter,
    generate_resume,
    latex_to_pdf,
    modification_cover_letter,
    modification_resume,
    store_informations,
    read_and_parse_pdf,
)
import uvicorn
from pylatex import Document
import os

app = FastAPI()


@app.post("/store_informations/")
async def process(text: str = Form(None), file: UploadFile = File(None)):
    if file:
        parsed_texts = read_and_parse_pdf(file)
        ids = [store_informations(t) for t in parsed_texts]
        return JSONResponse(content={"ids": ids})
    elif text:
        id = store_informations(text)
        return JSONResponse(content={"ids": [id]})
    else:
        return JSONResponse(
            content={"error": "No text or file provided"}, status_code=400
        )


@app.post("/generate_resume/")
async def generate_resume_endpoint(jd: str = Form(...)):
    resume = generate_resume(jd)
    return JSONResponse(content={"resume": resume})


@app.post("/modification_resume/")
async def modification_resume_endpoint(
    text: str = Form(...), additional_prompt: str = Form(...)
):
    modified_resume = modification_resume(text, additional_prompt)
    return JSONResponse(content={"modified_resume": modified_resume})


@app.post("/generate_application_message/")
async def generate_cover_letter_endpoint(prompt: str = Form(...), jd: str = Form(...)):
    cover_letter = generate_cover_letter(prompt, jd)
    return JSONResponse(content={"response": cover_letter})


@app.post("/modification_cover_letter/")
async def modification_cover_letter_endpoint(
    text: str = Form(...), additional_prompt: str = Form(...)
):
    modified_cover_letter = modification_cover_letter(text, additional_prompt)
    return JSONResponse(content={"modified_cover_letter": modified_cover_letter})


@app.post("/download_resume_in_pdf/")
async def latex_to_pdf_endpoint(latex_code: str = Form(...)):
    pdf_bytes = latex_to_pdf(latex_code)
    return JSONResponse(content={"pdf": pdf_bytes.hex()})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
