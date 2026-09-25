import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-3.5-flash-lite"


def get_llm():
    """
    Create the Gemini LLM using the API key
    stored in the environment.
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not configured."
        )

    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=0.7,
        google_api_key=api_key,
    )


# ============================================================
# GENERATE INTERVIEW QUESTIONS
# ============================================================

def generate_interview_questions(
    resume_text,
    target_role,
    experience_level,
    interview_type,
    number_of_questions=10
):
    """
    Generate personalized interview questions using
    LangChain + Google Gemini.
    """

    if not resume_text:
        raise ValueError("Resume text is empty.")

    # --------------------------------------------------------
    # Initialize Gemini
    # --------------------------------------------------------

    llm = get_llm()

    # --------------------------------------------------------
    # Interview prompt
    # --------------------------------------------------------

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are InterviewAI, an AI-powered professional interviewer.

Your task is to generate personalized interview questions
for a candidate based on their resume, target role,
experience level, and interview type.

Rules:

- Questions must be relevant to the candidate's resume.
- Questions must match the target role.
- Do not invent skills that are not present in the resume.
- Mix easy, medium, and challenging questions.
- Avoid duplicate questions.
- Make questions professional and realistic.
- Return ONLY the questions.
- Number each question clearly.
"""
            ),
            (
                "human",
                """
Candidate Resume:

{resume_text}

Target Role:

{target_role}

Experience Level:

{experience_level}

Interview Type:

{interview_type}

Number of Questions:

{number_of_questions}

Generate the interview questions now.
"""
            )
        ]
    )

    # --------------------------------------------------------
    # Create LangChain chain
    # --------------------------------------------------------

    chain = prompt | llm

    # --------------------------------------------------------
    # Generate questions
    # --------------------------------------------------------

    response = chain.invoke(
        {
            "resume_text": resume_text,
            "target_role": target_role,
            "experience_level": experience_level,
            "interview_type": interview_type,
            "number_of_questions": number_of_questions
        }
    )

    # --------------------------------------------------------
    # Handle Gemini response
    # --------------------------------------------------------

    if hasattr(response, "content"):

        content = response.content

        # Gemini may return content as a list of blocks
        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, dict):

                    if item.get("type") == "text":
                        text_parts.append(
                            item.get("text", "")
                        )

                elif isinstance(item, str):

                    text_parts.append(item)

            return "\n".join(text_parts).strip()

        # Normal string response
        return str(content).strip()

    return str(response).strip()