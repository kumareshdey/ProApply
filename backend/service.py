import os
from adapter import (
    generate_embeddings,
    store_embedding,
    genai_model,
    query_similar_texts,
)
from fastapi import UploadFile
import PyPDF2
import io
from assets import resume_template_default_filling
from jinja2 import Environment, FileSystemLoader, Template
import subprocess
from pylatex import Document

current_dir = os.path.dirname(__file__)

def store_informations(text):
    embedding = generate_embeddings(text)
    id = store_embedding(text, embedding)
    return id


def read_and_parse_pdf(file: UploadFile):
    pdf_bytes = file.file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

    text = ""
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"

    text = text.strip()
    prompt = (
        """Based on the text below which is a resume, give me a list of informations seperated by double new line \n
                For example:
                experience: (company_name) (designation) (mention all the points in experience as it is),
                education: (degree) (institute) (year of completion),
                skills: (mention all the skills) 
                add anything else if there in the pdf, which can include but not restricted to name, phone number, email, any social profile 
                for every point you find write a double new line. for example there can be 5 expereinces with different company and designations
                write in this manner. experience: (details for experience 1) \n\n, experience: (details of experience2) ... similarly skill:  skill1, skill: skill2
                Do not miss any point from the text. extract all the documents and format it.
                The text is:
            """
        + text
    )
    response = genai_model(prompt)
    print(response[0])
    texts = response[0].split("\n\n\n")
    return texts


def generate_resume(jd):
    default_prompt = """Based on the job description below, write the latex snippet for the resume Keep the styling as per the sample snippet.
        provide only the working latext snippet and nothing else. Remember, the snippet text will not contain any information which are not part of "related texts to generate the text content of the snippet" section.
        Job description: {jd}
        part of the resume to write: {part}
        sample snippet: {sample}
        related texts to generate the text content of the snippet: {documents}
        The text should perform better in the ATS scanning. Try to keep the text length similar.
        """
    print("Generating experience")
    experience_documents = "\n".join(
        query_similar_texts("what all work experiences do I have?")
    )
    experience = genai_model(
        default_prompt.format(
            jd=jd,
            part="experience",
            sample=resume_template_default_filling.experience,
            documents=experience_documents,
        )
    )

    print("Generating education")
    education_documents = "\n".join(
        query_similar_texts("what all education qualifications do I have?")
    )
    education = genai_model(
        default_prompt.format(
            jd="It can be anything. Put all the educations.",
            part="education",
            sample=resume_template_default_filling.education,
            documents=education_documents,
        )
    )

    print("Generating profile")
    profile_documents = "\n".join(
        query_similar_texts(
            "what all personal informations like phone number, email and other social profile do I have?"
        )
    )
    profile = genai_model(
        default_prompt.format(
            jd="Jd is nor required. Maintain the sample format. Only add contact details and social media links if available. Do not add anything else like skillset or other information.",
            part="profile",
            sample=resume_template_default_filling.profile,
            documents=profile_documents,
        )
    )

    print("Generating publication")
    publication_documents = "\n".join(
        query_similar_texts("what all research papers and publications do I have?")
    )
    publication = genai_model(
        default_prompt.format(
            jd=jd,
            part="publication",
            sample=resume_template_default_filling.publication,
            documents=publication_documents,
        )
    )

    print("Generating skills")
    skills_documents = "\n".join(query_similar_texts("what all skills do I have?"))
    skills = genai_model(
        default_prompt.format(
            jd=jd,
            part="skills",
            sample=resume_template_default_filling.skills,
            documents=skills_documents,
        )
    )

    current_dir = os.path.dirname(__file__)

    env = Environment(
        loader=FileSystemLoader(current_dir),
        block_start_string="{%",
        block_end_string="%}",
        variable_start_string="[[",
        variable_end_string="]]",
        comment_start_string="/*",
        comment_end_string="*/",
    )

    with open(os.path.join(current_dir, "assets/resume_template.tex")) as file_:
        template = env.from_string(file_.read())

    rendered_resume = template.render(
        experience=experience[0],
        education=education[0],
        profile=profile[0],
        publication=publication[0],
        skills=skills[0],
    )
    print("Giving some finishing touch ... ")
    final_correction_prompt = (
        "Correct the below latex page for any mistakes in syntax or any compilation error and provide the final latex code. DO not change anything else not even usepackage, only correct the errors. Return only the complete corrected code and nothing else. The text is: \n"
        + rendered_resume
    )
    rendered_resume = genai_model(final_correction_prompt)[0]
    rendered_resume = rendered_resume.replace("latex", "").replace("```", "").replace(r"\usepackage{sym}", r"\usepackage{latexsym}")
    tex_output_path = os.path.join(current_dir, "assets/generated_resume.tex")
    with open(tex_output_path, "w") as tex_file:
        tex_file.write(rendered_resume)
    return rendered_resume


def modification_resume(text, additional_prompt):
    prompt = f"""only return the corrected version of the resume in latex format and no additional changes and writings. 
        prompt = {additional_prompt}, 
        previous version of the resume = {text}"""

    rendered_resume = genai_model(prompt)[0]
    rendered_resume = rendered_resume.replace("latex", "").replace("```", "").replace(r"\usepackage{sym}", r"\usepackage{latexsym}")
    return rendered_resume


def generate_cover_letter(prompt, jd):
    prompt = """Based on the job description below, generate a response.
        Job description: {jd}
        what i need? {prompt}
        my information : {documents}.
        The writing should professional but should look like a smart human has written it. Keep it simple and short.
        """
    documents = "\n".join(
        query_similar_texts(
            "Give me all my details, name, phone number, email, experiences, skill, education, publications",
            n_results=50,
        )
    )
    response = genai_model(prompt.format(jd=jd, prompt=prompt, documents=documents))
    cover_letter_path = os.path.join(current_dir, "assets/cover_letter.txt")
    with open(cover_letter_path, "w") as file:
        file.write(response[0])
    return response[0]


def modification_cover_letter(text, additional_prompt):
    prompt = f"""only return the corrected version of the cover letter and no additional changes and writings. 
        prompt = {additional_prompt}, 
        previous version of the cover letter = {text}"""
    return genai_model(prompt)[0]


def latex_to_pdf(latex_code, output_filename="output.pdf"):
    """
    Converts LaTeX code to a PDF using pylatex (No pdflatex needed).

    Args:
        latex_code (str): The LaTeX document as a string.
        output_filename (str): The desired output PDF filename.

    Returns:
        str: Path to the generated PDF file.
    """
    doc = Document()
    doc.preamble.append(r"\usepackage{lmodern}")

    doc.append(latex_code)
    pdf_path = doc.generate_pdf(output_filename.replace(".pdf", ""), clean_tex=False)
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    return pdf_bytes
