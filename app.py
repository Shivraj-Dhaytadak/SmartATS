import base64
import io
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import PyPDF2
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # make sure create .env file with variable GOOGLE_API_KEY and get the Gemini key from AI-studio google site


def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-pro') # Latest Model at the time other models gemini-1.5-flash 
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in range(len(reader.pages)):
            page = reader.pages[page]
            text += str(page.extract_text())
        return text
    else:
        raise FileNotFoundError("No File")
    
st.set_page_config(page_title="ATS resume reviewer")
st.header("ATS grader")
input_text= st.text_area("Job description " , key="input")
uploaded_file = st.file_uploader("Upload Your Resume ( PDF only )" , type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Sucessfully")
    
submit3 = st.button("What are the Keywords that are missing")

submit4 = st.button("Percentage match")

# Review the Prompt as per the position your would apply too 
input_prompt = """
You are a experienced Technical Human Resource Manager in Tech experience in Hiring Python Developer,Full stack , Big Data Engineer , Data analyst , Your task is to review the provided resume agaist the Job Description.
Please Share Your Professional evaluation on whether the candidate's profile align with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
and give a score only.
Resume:{pdf_contents}
Job:{input_text}
"""
# Review the Prompt as per the position your would apply too  
input_prompt_next = """
You are an expert ATS (Applicant Tracking System) scanner with a deep understanding of roles such as Python Developer, Full Stack Engineer, Big Data Engineer, and Data Analyst, along with comprehensive ATS functionality.

**Task:** Assess the provided resume against the job description for the position of [Insert Job Title].

**Output Format:**

1. **Percentage Match:** Calculate the percentage of alignment between the resume and the job description, focusing on how well the resume matches the required skills, experience, and qualifications.
2. **Missing Keywords:** Identify any important keywords, skills, or qualifications from the job description that are not present in the resume.
3. **All the Keywords:** Extract all relevant keywords from the job description, categorizing them as:
    - **Technical Skills**: Tools, programming languages, platforms, certifications, etc.
    - **Soft Skills**: Communication, teamwork, problem-solving, leadership, etc.
4. **Final Thoughts:** Provide an insightful evaluation of the resume, highlighting strengths and weaknesses. Comment on the overall suitability of the candidate for the role, based on the job description and the resume's content.

Resume: {pdf_contents}
Job Description: {input_text}
"""



if submit3 or submit4:
    if uploaded_file is not None:
        pdf_contents = input_pdf_setup(uploaded_file)
        if submit3:
            formatted_prompt = input_prompt_next.format(pdf_contents=pdf_contents, input_text=input_text)
        else:
            formatted_prompt = input_prompt.format(pdf_contents=pdf_contents, input_text=input_text)

        response = get_gemini_response(input=input_text, pdf_content=pdf_contents, prompt=formatted_prompt)
        
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")