from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


def generate_interview_questions(
    resume_text,
    target_role,
    experience_level,
    interview_type,
    number_of_questions=10
):
    """
    Generate personalized interview questions using
    LangChain + Ollama + Qwen.
    """

    if not resume_text:
        raise ValueError("Resume text is empty.")

    # Local AI model
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0.7
    )

    # Interview question prompt
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

    # Create LangChain chain
    chain = prompt | llm

    # Generate questions
    response = chain.invoke(
        {
            "resume_text": resume_text,
            "target_role": target_role,
            "experience_level": experience_level,
            "interview_type": interview_type,
            "number_of_questions": number_of_questions
        }
    )

    return response.content