import base64
import io
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # make sure create .env file with variable GOOGLE_API_KEY and get the Gemini key from AI-studio google site


def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-pro') # Latest Model at the time other models gemini-1.5-flash 
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]
        
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File")
    
st.set_page_config(page_title="ATS resume reviewer")
st.header("ATS grader")
input_text= st.text_area("Job description " , key="input")
uploaded_file = st.file_uploader("Upload Your Resume ( PDF only )" , type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Sucessfully")
    
submit1 = st.button("Tell me about the resume")

submit3 = st.button("What are the Keywords that are missing")

submit4 = st.button("Percentage match")

# Review the Prompt as per the position your would apply too 
input_prompt = """
You are a experienced Technical Human Resource Manager in Tech experience in Hiring Python Developer,Full stack , Big Data Engineer , Data analyst , Your task is to review the provided resume agaist the Job Description.
Please Share Your Professional evaluation on whether the candidate's profile align with the role.
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""
# Review the Prompt as per the position your would apply too  
input_prompt_next = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Python Developer,Full stack , Big Data Engineer , Data analyst and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""
if submit1:
    if uploaded_file is not None:
        pdf_contents = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input=input_text, pdf_content=pdf_contents , prompt= input_prompt)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt_next,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")