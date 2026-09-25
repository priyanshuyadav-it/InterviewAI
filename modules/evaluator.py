import os
import json
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

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
        temperature=0.2,
        google_api_key=api_key,
    )


# ============================================================
# HELPER — EXTRACT JSON
# ============================================================

def _extract_json(text):
    """
    Extract a JSON object from the AI response.

    Gemini may return response.content as either
    a string or a list of content blocks.
    """

    # --------------------------------------------------------
    # Handle Gemini list-based content
    # --------------------------------------------------------

    if isinstance(text, list):

        parts = []

        for item in text:

            if isinstance(item, dict):

                if item.get("type") == "text":
                    parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):
                parts.append(item)

        text = "\n".join(parts)

    # --------------------------------------------------------
    # Convert to string
    # --------------------------------------------------------

    text = str(text).strip()

    # --------------------------------------------------------
    # Remove markdown code fences
    # --------------------------------------------------------

    text = re.sub(
        r"```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```\s*",
        "",
        text
    )

    # --------------------------------------------------------
    # Find JSON object
    # --------------------------------------------------------

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:
        raise ValueError(
            "AI did not return a valid JSON object."
        )

    json_text = match.group(0)

    return json.loads(json_text)


# ============================================================
# EVALUATE ONE ANSWER
# ============================================================

def evaluate_answer(
    question,
    answer,
    target_role,
    resume_text=""
):
    """
    Evaluate one interview answer using
    LangChain + Google Gemini.

    Returns:
        Dictionary containing scores and feedback.
    """

    llm = get_llm()

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer for a mock interview.

TARGET ROLE:

{target_role}

INTERVIEW QUESTION:

{question}

CANDIDATE ANSWER:

{answer}

Use the candidate's answer only to determine the scores.

Do not give credit for information that the candidate did not provide.

Evaluate these five dimensions:

1. technical_knowledge
2. relevance
3. communication
4. completeness
5. confidence

Each score must be an integer from 0 to 100.

Scoring guidance:

Technical Knowledge:
How accurately and correctly does the candidate demonstrate
knowledge related to the question?

Relevance:
How directly does the answer address the question?

Communication:
How clearly and logically is the answer explained?

Completeness:
Does the answer sufficiently cover the important parts
of the question?

Confidence:
Does the answer appear structured, decisive and professional?

Do not infer personal or medical traits.

Also provide:

strengths:
A short list of 2 or 3 specific strengths.

improvements:
A short list of 2 or 3 specific improvements.

feedback:
A concise overall feedback paragraph.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "technical_knowledge": 0,
    "relevance": 0,
    "communication": 0,
    "completeness": 0,
    "confidence": 0,
    "strengths": [
        "strength 1",
        "strength 2"
    ],
    "improvements": [
        "improvement 1",
        "improvement 2"
    ],
    "feedback": "Overall feedback"
}}
"""

    # --------------------------------------------------------
    # Generate evaluation
    # --------------------------------------------------------

    response = llm.invoke(prompt)

    # ChatGoogleGenerativeAI returns an AIMessage
    if hasattr(response, "content"):
        response_text = response.content
    else:
        response_text = str(response)

    result = _extract_json(response_text)

    # --------------------------------------------------------
    # Validate scores
    # --------------------------------------------------------

    score_fields = [
        "technical_knowledge",
        "relevance",
        "communication",
        "completeness",
        "confidence"
    ]

    for field in score_fields:

        value = result.get(field, 0)

        try:
            value = int(value)
        except (TypeError, ValueError):
            value = 0

        value = max(0, min(100, value))

        result[field] = value

    # --------------------------------------------------------
    # Validate lists
    # --------------------------------------------------------

    if not isinstance(
        result.get("strengths"),
        list
    ):
        result["strengths"] = []

    if not isinstance(
        result.get("improvements"),
        list
    ):
        result["improvements"] = []

    # --------------------------------------------------------
    # Calculate average
    # --------------------------------------------------------

    result["overall_score"] = round(
        (
            result["technical_knowledge"]
            + result["relevance"]
            + result["communication"]
            + result["completeness"]
            + result["confidence"]
        ) / 5
    )

    return result


# ============================================================
# EVALUATE COMPLETE INTERVIEW
# ============================================================

def evaluate_interview(
    answers,
    target_role,
    resume_text=""
):
    """
    Evaluate all interview answers.

    answers format:

    [
        {
            "question": "...",
            "answer": "..."
        }
    ]

    Returns a list of evaluation dictionaries.
    """

    evaluations = []

    for item in answers:

        question = item.get(
            "question",
            ""
        )

        answer = item.get(
            "answer",
            ""
        )

        evaluation = evaluate_answer(
            question=question,
            answer=answer,
            target_role=target_role,
            resume_text=resume_text
        )

        evaluation["question"] = question
        evaluation["answer"] = answer

        evaluations.append(evaluation)

    return evaluations


# ============================================================
# OVERALL INTERVIEW SCORE
# ============================================================

def calculate_overall_scores(evaluations):
    """
    Calculate average scores across the complete interview.
    """

    if not evaluations:
        return {
            "technical_knowledge": 0,
            "relevance": 0,
            "communication": 0,
            "completeness": 0,
            "confidence": 0,
            "overall_score": 0
        }

    fields = [
        "technical_knowledge",
        "relevance",
        "communication",
        "completeness",
        "confidence"
    ]

    scores = {}

    for field in fields:

        values = [
            evaluation.get(field, 0)
            for evaluation in evaluations
        ]

        scores[field] = round(
            sum(values) / len(values)
        )

    scores["overall_score"] = round(
        sum(
            scores[field]
            for field in fields
        ) / len(fields)
    )

    return scores