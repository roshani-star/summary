from dis import Instruction
from groq import Groq
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from newspaper import Article
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_summary(text, length, language):

    if length == "Short":
        instruction = "Summarize in 3-4 lines."
    elif length == "Medium":
        instruction = "Summarize in medium detail."
    else:
        instruction = "Summarize in bullet points."

    if language == "Hindi":
        lang_instruction = "Write ONLY in Hindi."
    else:
        lang_instruction = "Write ONLY in English."

    prompt = f"""
You are a helpful AI assistant.

Language Rule:
{lang_instruction}

Task:
{instruction}

Content:
{text[:4000]}
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-8b-instant"
    )

    return chat_completion.choices[0].message.content

    chat_completion = client.chat.completions.create(

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        model="llama-3.1-8b-instant"
    )

    summary = chat_completion.choices[0].message.content

    return summary

# ---------- PDF ----------

def extract_text_from_pdf(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

# ---------- WEBSITE ----------

def extract_text_from_url(url):

    article = Article(url)

    article.download()

    article.parse()

    return article.text
# ---------- VIVA QUESTIONS ----------
def generate_viva_questions(text, language):

    if language == "Hindi":
        language_instruction = "Generate all viva questions in Hindi."
    else:
        language_instruction = "Generate all viva questions in English."

    prompt = f"""
    {language_instruction}

    Read the following content and generate 10 viva questions.

    Rules:
    - Questions should be suitable for diploma students.
    - Number each question.
    - Only return questions.
    - No answers.

    Content:

    {text[:4000]}
    """

    chat_completion = client.chat.completions.create(

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        model="llama-3.1-8b-instant"
    )

    return chat_completion.choices[0].message.content
# ---------- STUDY NOTES ----------
def generate_study_notes(text, language):

    if language == "Hindi":
        language_instruction = "Create study notes in Hindi."
    else:
        language_instruction = "Create study notes in English."

    prompt = f"""
    {language_instruction}

    Create well-structured study notes from the following content.

    Format:

    Topic:

    Key Concepts:
    - Point 1
    - Point 2

    Important Notes:
    - Point 1
    - Point 2

    Quick Revision:
    - Point 1
    - Point 2

    Content:

    {text[:4000]}
    """

    chat_completion = client.chat.completions.create(

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        model="llama-3.1-8b-instant"
    )

    return chat_completion.choices[0].message.content

