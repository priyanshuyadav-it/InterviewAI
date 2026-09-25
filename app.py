import streamlit as st
import textwrap
import pandas as pd
import plotly.graph_objects as go

from modules.question_generator import generate_interview_questions
from modules.evaluator import evaluate_interview
from modules.fuzzy_engine import calculate_readiness


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    st.html(textwrap.dedent(content))


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="InterviewAI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: #080B12;
}

/* MAIN */

.main .block-container {
    max-width: 1450px;
    padding-top: 35px;
    padding-left: 40px;
    padding-right: 40px;
    padding-bottom: 60px;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: #F5F7FB;
    border-right: 1px solid #D9E0EA;
}

section[data-testid="stSidebar"] * {
    color: #172033;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
}

.sidebar-subtitle {
    font-size: 14px;
    color: #64748B !important;
    margin-top: 4px;
}

.sidebar-heading {
    font-size: 15px;
    font-weight: 800;
    margin-top: 25px;
}

.sidebar-about {
    color: #64748B !important;
    font-size: 13px;
    line-height: 1.7;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;

    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(99, 102, 241, 0.35),
            transparent 35%
        ),
        radial-gradient(
            circle at 20% 100%,
            rgba(37, 99, 235, 0.25),
            transparent 40%
        ),
        linear-gradient(
            135deg,
            #172E59,
            #10182F 55%,
            #24145F
        );

    border: 1px solid #3A527C;
    border-radius: 24px;
    padding: 50px;
    min-height: 330px;
    overflow: hidden;

    box-shadow:
        0 25px 70px rgba(0, 0, 0, 0.35);
}

.hero::after {
    content: "";

    position: absolute;

    width: 280px;
    height: 280px;

    right: -110px;
    top: -120px;

    border-radius: 50%;

    background: rgba(96, 165, 250, 0.08);

    border: 1px solid rgba(147, 197, 253, 0.15);
}

.hero-label {
    color: #63B3FF;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 14px;
}

.hero-title {
    color: #FFFFFF;
    font-size: 58px;
    font-weight: 850;
    line-height: 1.05;
    margin-bottom: 14px;
}

.hero-subtitle {
    color: #C8DDF8;
    font-size: 21px;
    font-weight: 600;
    margin-bottom: 20px;
    max-width: 850px;
}

.hero-description {
    color: #D9E7F8;
    font-size: 16px;
    line-height: 1.75;
    max-width: 800px;
}


/* ============================================================
   ROBOT
   ============================================================ */

.robot-area {
    position: absolute;
    right: 65px;
    top: 55px;
    width: 260px;
    height: 230px;
}

.robot-antenna {
    position: absolute;
    width: 4px;
    height: 30px;
    background: #CBD5E1;
    right: 115px;
    top: 10px;
}

.robot-dot {
    position: absolute;
    width: 13px;
    height: 13px;
    background: #60A5FA;
    border-radius: 50%;
    right: 110px;
    top: 0;

    box-shadow:
        0 0 18px #60A5FA;
}

.robot {
    position: absolute;

    width: 135px;
    height: 105px;

    right: 50px;
    top: 38px;

    background: linear-gradient(
        145deg,
        #F8FAFF,
        #AABCF5
    );

    border-radius: 42px;
    border: 5px solid #DCE7FF;

    box-shadow:
        0 0 40px rgba(96, 165, 250, 0.45);
}

.robot-face {
    position: absolute;

    left: 20px;
    right: 20px;
    top: 20px;
    bottom: 20px;

    background: #172554;
    border-radius: 28px;
}

.robot-eye {
    position: absolute;

    width: 12px;
    height: 12px;

    border-radius: 50%;

    background: #60A5FA;

    top: 28px;

    box-shadow:
        0 0 12px #60A5FA;
}

.robot-eye.left {
    left: 27px;
}

.robot-eye.right {
    right: 27px;
}

.robot-body {
    position: absolute;

    width: 82px;
    height: 55px;

    right: 77px;
    top: 150px;

    background: linear-gradient(
        145deg,
        #F1F5FF,
        #9CAFEF
    );

    border-radius: 25px;
    border: 4px solid #DCE7FF;
}


/* ============================================================
   TITLES
   ============================================================ */

.section-title {
    color: #FFFFFF;
    font-size: 31px;
    font-weight: 800;
    margin-top: 42px;
    margin-bottom: 22px;
}


/* ============================================================
   CARDS
   ============================================================ */

.feature-card {
    background:
        linear-gradient(
            145deg,
            #131B28,
            #0D131D
        );

    border: 1px solid #2A3B55;
    border-radius: 18px;

    padding: 28px;
    min-height: 235px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.15);
}

.feature-icon {
    width: 56px;
    height: 56px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 16px;

    font-size: 27px;

    margin-bottom: 18px;
}

.icon-blue {
    background: rgba(37, 99, 235, 0.22);
}

.icon-pink {
    background: rgba(236, 72, 153, 0.22);
}

.icon-green {
    background: rgba(16, 185, 129, 0.22);
}

.feature-title {
    color: #FFFFFF;
    font-size: 21px;
    font-weight: 800;
    margin-bottom: 12px;
}

.feature-text {
    color: #AFC0D5;
    font-size: 15px;
    line-height: 1.7;
}


/* ============================================================
   SCORE CARD
   ============================================================ */

.score-card {
    background:
        linear-gradient(
            135deg,
            #13213F,
            #172A5A
        );

    border: 1px solid #3A679D;

    border-radius: 22px;

    padding: 35px;

    text-align: center;

    margin: 25px 0;
}

.score-label {
    color: #AFC8E8;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 1px;
}

.score-value {
    color: #60A5FA;
    font-size: 58px;
    font-weight: 900;
    margin-top: 10px;
}


/* ============================================================
   QUESTION CARD
   ============================================================ */

.question-card {
    background:
        linear-gradient(
            145deg,
            #111B2A,
            #0E1623
        );

    border: 1px solid #345277;

    border-radius: 20px;

    padding: 35px;

    margin: 20px 0;
}

.question-number {
    color: #63B3FF;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 20px;
}

.question-text {
    color: #FFFFFF;
    font-size: 21px;
    line-height: 1.8;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton {
    margin-top: 20px;
}

.stButton > button {
    width: 100% !important;

    min-height: 60px !important;

    border-radius: 14px !important;

    border: 1px solid #4A9BFF !important;

    background:
        linear-gradient(
            90deg,
            #3B9BFF,
            #2563EB
        ) !important;

    color: white !important;

    font-size: 17px !important;

    font-weight: 800 !important;

    box-shadow:
        0 10px 30px rgba(37,99,235,0.25);
}

.stButton > button p {
    color: white !important;
}

.stButton > button:hover {
    border-color: #93C5FD !important;

    background:
        linear-gradient(
            90deg,
            #60A5FA,
            #3B82F6
        ) !important;
}


/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stFileUploader label,
.stSlider label {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

.stTextInput input,
.stTextArea textarea {
    background: #F8FAFC !important;
    color: #111827 !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] {
    background: #F8FAFC !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] * {
    color: #111827 !important;
}

[data-testid="stFileUploader"] {
    background: #F8FAFC !important;
    border-radius: 12px !important;
}


/* ============================================================
   STAT CARDS
   ============================================================ */

.stat-card {
    background: #111824;

    border: 1px solid #293A53;

    border-radius: 17px;

    padding: 22px;

    min-height: 115px;
}

.stat-icon {
    font-size: 24px;
}

.stat-label {
    color: #9FB0C7;
    font-size: 14px;
    margin-top: 7px;
}

.stat-value {
    color: #FFFFFF;
    font-size: 27px;
    font-weight: 800;
    margin-top: 3px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    background: #101722;

    border: 1px solid #26374F;

    border-radius: 18px;

    padding: 28px;

    margin-top: 35px;

    text-align: center;

    color: #9FB0C7;

    line-height: 1.8;
}

.footer-title {
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 800;
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {
    border-color: #26374F !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 900px) {

    .hero {
        padding: 30px;
    }

    .hero-title {
        font-size: 40px;
    }

    .robot-area {
        display: none;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

defaults = {
    "page": "Dashboard",

    "candidate_name": "",
    "experience": "Fresher",
    "role": "Python Developer",
    "interview_type": "Technical",

    "number_of_questions": 5,

    "resume_text": "",

    "questions": [],
    "questions_text": "",

    "current_question": 0,

    "answers": [],
    "evaluations": [],

    "overall_scores": {},

    "readiness_score": 0,
    "readiness_level": "",
    "readiness_recommendation": "",

    "interview_started": False,
    "interview_completed": False,

    "interview_count": 0,
    "question_count": 0,
    "best_score": 0
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    html(
        """
        <div class="sidebar-title">
            🎯 InterviewAI
        </div>

        <div class="sidebar-subtitle">
            AI-Powered Interview Preparation
        </div>
        """
    )

    st.divider()

    html(
        """
        <div class="sidebar-heading">
            Navigation
        </div>
        """
    )

    # Navigation state
    if "_navigation_target" in st.session_state:
        st.session_state["navigation"] = st.session_state.pop(
            "_navigation_target"
        )

    if "navigation" not in st.session_state:
        st.session_state["navigation"] = "🏠 Dashboard"

    def sync_navigation():
        navigation_map = {
            "🏠 Dashboard": "Dashboard",
            "🎤 Mock Interview": "Mock Interview",
            "📊 Performance": "Performance",
            "📄 Interview Report": "Interview Report"
        }

        st.session_state.page = navigation_map[
            st.session_state.navigation
        ]

    page_choice = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎤 Mock Interview",
            "📊 Performance",
            "📄 Interview Report"
        ],
        key="navigation",
        label_visibility="collapsed",
        on_change=sync_navigation
    )

    # Keep the internal page state synchronized with the current
    # sidebar selection without overriding a button-triggered navigation.
    if not st.session_state.get("_navigation_target"):
        sync_navigation()

    st.divider()

    html(
        """
        <div class="sidebar-heading">
            About
        </div>

        <div class="sidebar-about">

            InterviewAI combines LangChain,
            AI-based answer evaluation and
            Fuzzy Logic to analyze interview
            performance and estimate candidate
            readiness.

        </div>
        """
    )


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    html(
        """
        <div class="hero">

            <div class="hero-label">
                AI CAREER PREPARATION PLATFORM
            </div>

            <div class="hero-title">
                🎯 InterviewAI
            </div>

            <div class="hero-subtitle">
                AI-Based Mock Interview Performance & Readiness Advisor
            </div>

            <div class="hero-description">

                Practice realistic interviews, receive intelligent
                AI-powered feedback, analyze your performance,
                and measure your interview readiness using a
                genuine Fuzzy Logic inference system.

            </div>

            <div class="robot-area">

                <div class="robot-antenna"></div>

                <div class="robot-dot"></div>

                <div class="robot">

                    <div class="robot-face">

                        <div class="robot-eye left"></div>
                        <div class="robot-eye right"></div>

                    </div>

                </div>

                <div class="robot-body"></div>

            </div>

        </div>
        """
    )


    if st.button(
        "🚀  START YOUR MOCK INTERVIEW  →",
        key="dashboard_start"
    ):

        st.session_state.page = "Mock Interview"
        st.session_state["_navigation_target"] = "🎤 Mock Interview"

        st.rerun()


    html(
        """
        <div class="section-title">
            Why InterviewAI?
        </div>
        """
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        html(
            """
            <div class="feature-card">

                <div class="feature-icon icon-blue">
                    🤖
                </div>

                <div class="feature-title">
                    AI Interviewer
                </div>

                <div class="feature-text">

                    Generate personalized interview
                    questions based on candidate
                    profile, resume, role and
                    interview type.

                </div>

            </div>
            """
        )


    with col2:

        html(
            """
            <div class="feature-card">

                <div class="feature-icon icon-pink">
                    🧠
                </div>

                <div class="feature-title">
                    Smart Evaluation
                </div>

                <div class="feature-text">

                    Evaluate technical knowledge,
                    relevance, communication,
                    completeness and confidence
                    using AI.

                </div>

            </div>
            """
        )


    with col3:

        html(
            """
            <div class="feature-card">

                <div class="feature-icon icon-green">
                    🌫️
                </div>

                <div class="feature-title">
                    Fuzzy Readiness
                </div>

                <div class="feature-text">

                    Combine multiple performance
                    factors using fuzzy membership
                    functions and inference rules.

                </div>

            </div>
            """
        )


    html(
        """
        <div class="section-title">
            Your Interview Journey
        </div>
        """
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    📄
                </div>

                <div class="stat-label">
                    Interviews
                </div>

                <div class="stat-value">
                    {st.session_state.interview_count}
                </div>

            </div>
            """
        )


    with c2:

        html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    💬
                </div>

                <div class="stat-label">
                    Questions
                </div>

                <div class="stat-value">
                    {st.session_state.question_count}
                </div>

            </div>
            """
        )


    with c3:

        best_score = st.session_state.best_score

        best_display = (
            f"{best_score}/100"
            if best_score
            else "—"
        )

        html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    🏆
                </div>

                <div class="stat-label">
                    Best Score
                </div>

                <div class="stat-value">
                    {best_display}
                </div>

            </div>
            """
        )


    with c4:

        readiness = st.session_state.readiness_score

        readiness_display = (
            f"{readiness:.1f}"
            if readiness
            else "—"
        )

        html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    🎯
                </div>

                <div class="stat-label">
                    Readiness
                </div>

                <div class="stat-value">
                    {readiness_display}
                </div>

            </div>
            """
        )


    html(
        """
        <div class="footer">

            <div class="footer-title">
                🎯 InterviewAI
            </div>

            AI-Based Mock Interview Performance &
            Readiness Advisor

            <br>

            T.Y. B.Sc. Information Technology

            <br><br>

            Practice • Improve • Succeed

        </div>
        """
    )


# ============================================================
# MOCK INTERVIEW
# ============================================================

elif st.session_state.page == "Mock Interview":

    html(
        """
        <div class="section-title">
            🎤 Mock Interview
        </div>

        <div style="
            color:#AFC0D5;
            font-size:16px;
            line-height:1.7;
        ">

            Configure your interview before we begin.

        </div>
        """
    )


    # ========================================================
    # INTERVIEW COMPLETED
    # ========================================================

    if st.session_state.interview_completed:

        html(
            """
            <div class="section-title">
                🎉 Interview Completed
            </div>

            <div style="
                color:#AFC0D5;
                font-size:17px;
                line-height:1.7;
            ">

                Great work! InterviewAI has completed
                the evaluation of your answers.

            </div>
            """
        )


        overall = st.session_state.overall_scores


        html(
            f"""
            <div class="score-card">

                <div class="score-label">
                    OVERALL INTERVIEW SCORE
                </div>

                <div class="score-value">
                    {overall.get("overall_score", 0)}/100
                </div>

            </div>
            """
        )


        # FIVE METRICS

        c1, c2, c3, c4, c5 = st.columns(5)


        c1.metric(
            "Technical",
            f"{overall.get('technical_knowledge', 0)}/100"
        )

        c2.metric(
            "Relevance",
            f"{overall.get('relevance', 0)}/100"
        )

        c3.metric(
            "Communication",
            f"{overall.get('communication', 0)}/100"
        )

        c4.metric(
            "Completeness",
            f"{overall.get('completeness', 0)}/100"
        )

        c5.metric(
            "Confidence",
            f"{overall.get('confidence', 0)}/100"
        )


        st.divider()


        # FUZZY READINESS

        html(
            """
            <div class="section-title">
                🌫️ Fuzzy Interview Readiness
            </div>
            """
        )


        readiness_score = st.session_state.readiness_score

        readiness_level = st.session_state.readiness_level

        readiness_recommendation = (
            st.session_state.readiness_recommendation
        )


        html(
            f"""
            <div class="score-card">

                <div class="score-label">
                    FUZZY READINESS SCORE
                </div>

                <div class="score-value">
                    {readiness_score:.2f}/100
                </div>

                <div style="
                    color:#D9E7F8;
                    font-size:19px;
                    margin-top:12px;
                ">

                    Readiness Level:
                    <strong>{readiness_level}</strong>

                </div>

            </div>
            """
        )


        st.progress(
            min(
                max(readiness_score / 100, 0),
                1
            )
        )


        st.info(
            f"💡 {readiness_recommendation}"
        )


        st.divider()


        # QUESTION-WISE EVALUATION

        html(
            """
            <div class="section-title">
                🧠 AI Answer Evaluation
            </div>

            <div style="
                color:#AFC0D5;
                font-size:16px;
                line-height:1.7;
                margin-bottom:20px;
            ">

                InterviewAI evaluated each answer using
                five performance dimensions.

            </div>
            """
        )


        if st.session_state.evaluations:

            for index, evaluation in enumerate(
                st.session_state.evaluations
            ):

                with st.expander(
                    (
                        f"Question {index + 1}  •  "
                        f"Score: "
                        f"{evaluation.get('overall_score', 0)}/100"
                    )
                ):

                    st.markdown("**Question**")

                    st.write(
                        evaluation.get(
                            "question",
                            ""
                        )
                    )

                    st.markdown("**Your Answer**")

                    st.write(
                        evaluation.get(
                            "answer",
                            ""
                        )
                    )

                    st.divider()


                    c1, c2, c3, c4, c5 = st.columns(5)


                    c1.metric(
                        "Technical",
                        evaluation.get(
                            "technical_knowledge",
                            0
                        )
                    )

                    c2.metric(
                        "Relevance",
                        evaluation.get(
                            "relevance",
                            0
                        )
                    )

                    c3.metric(
                        "Communication",
                        evaluation.get(
                            "communication",
                            0
                        )
                    )

                    c4.metric(
                        "Completeness",
                        evaluation.get(
                            "completeness",
                            0
                        )
                    )

                    c5.metric(
                        "Confidence",
                        evaluation.get(
                            "confidence",
                            0
                        )
                    )


                    st.markdown("### ✅ Strengths")

                    strengths = evaluation.get(
                        "strengths",
                        []
                    )

                    if strengths:

                        for strength in strengths:

                            st.markdown(
                                f"- {strength}"
                            )

                    else:

                        st.write(
                            "No strengths returned."
                        )


                    st.markdown(
                        "### 🔧 Areas for Improvement"
                    )

                    improvements = evaluation.get(
                        "improvements",
                        []
                    )

                    if improvements:

                        for improvement in improvements:

                            st.markdown(
                                f"- {improvement}"
                            )

                    else:

                        st.write(
                            "No improvements returned."
                        )


                    st.markdown(
                        "### 💬 AI Feedback"
                    )

                    st.info(
                        evaluation.get(
                            "feedback",
                            "No feedback available."
                        )
                    )


        st.divider()


        if st.button(
            "🔄  START NEW INTERVIEW",
            key="new_interview"
        ):

            st.session_state.questions = []

            st.session_state.questions_text = ""

            st.session_state.current_question = 0

            st.session_state.answers = []

            st.session_state.evaluations = []

            st.session_state.overall_scores = {}

            st.session_state.readiness_score = 0

            st.session_state.readiness_level = ""

            st.session_state.readiness_recommendation = ""

            st.session_state.interview_started = False

            st.session_state.interview_completed = False

            st.rerun()


    # ========================================================
    # ACTIVE INTERVIEW
    # ========================================================

    elif st.session_state.interview_started:

        questions = st.session_state.questions

        total_questions = len(questions)

        current_index = st.session_state.current_question


        if current_index < total_questions:

            # Progress

            progress_value = (
                current_index / total_questions
                if total_questions
                else 0
            )

            st.progress(progress_value)


            html(
                f"""
                <div style="
                    color:#AFC0D5;
                    font-size:16px;
                    margin-top:20px;
                ">

                    Question {current_index + 1}
                    of {total_questions}

                    &nbsp; • &nbsp;

                    Candidate:
                    {st.session_state.candidate_name}

                    &nbsp; • &nbsp;

                    Role:
                    {st.session_state.role}

                </div>
                """
            )


            # QUESTION CARD

            current_question = questions[current_index]


            html(
                f"""
                <div class="question-card">

                    <div class="question-number">
                        🎤 Question {current_index + 1}
                    </div>

                    <div class="question-text">
                        {current_question}
                    </div>

                </div>
                """
            )


            # ANSWER

            answer = st.text_area(
                "Your Answer",
                key=f"answer_box_{current_index}",
                height=260,
                placeholder=(
                    "Type your answer here...\n\n"
                    "Try to explain your answer clearly "
                    "and include examples where possible."
                )
            )


            # SUBMIT

            if current_index < total_questions - 1:

                button_text = "➡️ SUBMIT ANSWER & NEXT"

            else:

                button_text = "🏁 SUBMIT FINAL ANSWER"


            if st.button(
                button_text,
                key=f"submit_answer_{current_index}"
            ):

                if not answer.strip():

                    st.warning(
                        "Please enter an answer before continuing."
                    )

                else:

                    st.session_state.answers.append(
                        {
                            "question": current_question,
                            "answer": answer.strip()
                        }
                    )

                    st.session_state.current_question += 1

                    st.rerun()


        else:

            # =================================================
            # EVALUATE INTERVIEW
            # =================================================

            if not st.session_state.interview_completed:

                with st.spinner(
                    "🧠 InterviewAI is evaluating your answers..."
                ):

                    try:

                        evaluations = evaluate_interview(
                            answers=st.session_state.answers,
                            target_role=st.session_state.role,
                            resume_text=st.session_state.resume_text
                        )


                        # Ensure list

                        if not isinstance(
                            evaluations,
                            list
                        ):

                            evaluations = []


                        st.session_state.evaluations = (
                            evaluations
                        )


                        # =================================================
                        # CALCULATE OVERALL SCORES
                        # =================================================

                        if evaluations:

                            score_fields = [
                                "technical_knowledge",
                                "relevance",
                                "communication",
                                "completeness",
                                "confidence"
                            ]


                            overall_scores = {}


                            for field in score_fields:

                                values = []

                                for evaluation in evaluations:

                                    try:

                                        values.append(
                                            float(
                                                evaluation.get(
                                                    field,
                                                    0
                                                )
                                            )
                                        )

                                    except Exception:

                                        values.append(0)


                                overall_scores[field] = round(
                                    sum(values) / len(values)
                                    if values
                                    else 0
                                )


                            overall_values = []

                            for evaluation in evaluations:

                                try:

                                    overall_values.append(
                                        float(
                                            evaluation.get(
                                                "overall_score",
                                                0
                                            )
                                        )
                                    )

                                except Exception:

                                    overall_values.append(0)


                            overall_scores[
                                "overall_score"
                            ] = round(
                                sum(overall_values)
                                / len(overall_values)
                                if overall_values
                                else 0
                            )


                        else:

                            overall_scores = {
                                "technical_knowledge": 0,
                                "relevance": 0,
                                "communication": 0,
                                "completeness": 0,
                                "confidence": 0,
                                "overall_score": 0
                            }


                        st.session_state.overall_scores = (
                            overall_scores
                        )


                        # =================================================
                        # FUZZY LOGIC READINESS
                        # =================================================

                        fuzzy_result = calculate_readiness(

                            technical_knowledge=
                                overall_scores.get(
                                    "technical_knowledge",
                                    0
                                ),

                            relevance=
                                overall_scores.get(
                                    "relevance",
                                    0
                                ),

                            communication=
                                overall_scores.get(
                                    "communication",
                                    0
                                ),

                            completeness=
                                overall_scores.get(
                                    "completeness",
                                    0
                                ),

                            confidence=
                                overall_scores.get(
                                    "confidence",
                                    0
                                )
                        )


                        st.session_state.readiness_score = (
                            fuzzy_result.get(
                                "readiness_score",
                                0
                            )
                        )


                        st.session_state.readiness_level = (
                            fuzzy_result.get(
                                "readiness_level",
                                "Not Available"
                            )
                        )


                        st.session_state.readiness_recommendation = (
                            fuzzy_result.get(
                                "recommendation",
                                ""
                            )
                        )


                        # =================================================
                        # COMPLETE
                        # =================================================

                        st.session_state.interview_completed = True

                        st.session_state.interview_count += 1

                        st.session_state.question_count += (
                            len(
                                st.session_state.questions
                            )
                        )


                        current_best = (
                            overall_scores.get(
                                "overall_score",
                                0
                            )
                        )


                        if current_best > (
                            st.session_state.best_score
                        ):

                            st.session_state.best_score = (
                                current_best
                            )


                        st.rerun()


                    except Exception as e:

                        st.error(
                            f"Unable to evaluate interview: {e}"
                        )


    # ========================================================
    # INTERVIEW SETUP
    # ========================================================

    else:

        st.divider()


        col1, col2 = st.columns(2)


        with col1:

            candidate_name = st.text_input(
                "Candidate Name",
                value=(
                    st.session_state.candidate_name
                ),
                placeholder="Enter your name",
                key="candidate_name_input"
            )


        with col2:

            experience_options = [
                "Fresher",
                "Internship Candidate",
                "Entry Level"
            ]

            experience = st.selectbox(
                "Experience Level",
                experience_options,

                index=experience_options.index(
                    st.session_state.experience
                )
                if st.session_state.experience
                in experience_options
                else 0
            )


        col1, col2 = st.columns(2)


        with col1:

            role_options = [
                "Python Developer",
                "Data Analyst",
                "Web Developer",
                "Java Developer",
                "Software Developer",
                "Full Stack Developer"
            ]

            role = st.selectbox(
                "Target Role",
                role_options,

                index=role_options.index(
                    st.session_state.role
                )
                if st.session_state.role
                in role_options
                else 0
            )


        with col2:

            interview_options = [
                "Technical",
                "HR",
                "Behavioral",
                "Mixed"
            ]

            interview_type = st.selectbox(
                "Interview Type",
                interview_options,

                index=interview_options.index(
                    st.session_state.interview_type
                )
                if st.session_state.interview_type
                in interview_options
                else 0
            )


        st.divider()


        # ========================================================
        # RESUME
        # ========================================================

        html(
            """
            <div class="section-title">
                📄 Resume
            </div>

            <div style="
                color:#AFC0D5;
                margin-bottom:15px;
            ">

                Upload your resume so InterviewAI can
                personalize your interview questions.

            </div>
            """
        )


        resume = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx"],
            key="resume_upload"
        )


        if resume:

            st.success(
                f"Resume uploaded successfully: {resume.name}"
            )


        st.divider()


        html(
            """
            <div class="section-title">
                ⚙️ Interview Settings
            </div>
            """
        )


        number_of_questions = st.slider(
            "Number of Questions",
            5,
            15,
            st.session_state.number_of_questions
        )


        # ========================================================
        # BEGIN INTERVIEW
        # ========================================================

        if st.button(
            "🚀  BEGIN INTERVIEW",
            key="begin_interview"
        ):

            if not candidate_name.strip():

                st.error(
                    "Please enter your name before starting."
                )

            else:

                # Save candidate information

                st.session_state.candidate_name = (
                    candidate_name.strip()
                )

                st.session_state.role = role

                st.session_state.experience = experience

                st.session_state.interview_type = (
                    interview_type
                )

                st.session_state.number_of_questions = (
                    number_of_questions
                )


                # =================================================
                # RESUME TEXT
                # =================================================

                resume_text = ""

                if resume:

                    try:

                        file_bytes = resume.read()

                        if resume.name.lower().endswith(
                            ".pdf"
                        ):

                            import pymupdf

                            pdf = pymupdf.open(
                                stream=file_bytes,
                                filetype="pdf"
                            )

                            pages = []

                            for page in pdf:

                                pages.append(
                                    page.get_text()
                                )

                            resume_text = "\n".join(
                                pages
                            )

                            pdf.close()


                        elif resume.name.lower().endswith(
                            ".docx"
                        ):

                            from io import BytesIO

                            from docx import Document

                            document = Document(
                                BytesIO(file_bytes)
                            )

                            paragraphs = []

                            for paragraph in (
                                document.paragraphs
                            ):

                                if paragraph.text.strip():

                                    paragraphs.append(
                                        paragraph.text.strip()
                                    )

                            resume_text = "\n".join(
                                paragraphs
                            )


                    except Exception as e:

                        st.warning(
                            f"Resume could not be read: {e}"
                        )


                st.session_state.resume_text = (
                    resume_text
                )


                # =================================================
                # BUILD CANDIDATE CONTEXT
                # =================================================

                if resume_text.strip():

                    candidate_context = (
                        resume_text[:12000]
                    )

                else:

                    candidate_context = (
                        f"Candidate: {candidate_name}\n"
                        f"Experience: {experience}\n"
                        f"Target Role: {role}\n"
                        f"Interview Type: {interview_type}"
                    )


                # =================================================
                # GENERATE QUESTIONS
                # =================================================

                with st.spinner(
                    "🤖 InterviewAI is preparing your personalized interview..."
                ):

                    try:

                        questions_text = (
                            generate_interview_questions(
                                candidate_context,
                                role,
                                experience,
                                interview_type,
                                number_of_questions
                            )
                        )


                        st.session_state.questions_text = (
                            questions_text
                        )


                        # =================================================
                        # CONVERT AI OUTPUT INTO QUESTIONS
                        # =================================================

                        questions = []


                        for line in (
                            questions_text.splitlines()
                        ):

                            line = line.strip()


                            if not line:
                                continue


                            # Normal format:
                            # 1. Question

                            if (
                                line[0].isdigit()
                                and "." in line
                            ):

                                question = (
                                    line.split(
                                        ".",
                                        1
                                    )[1].strip()
                                )


                                if question.startswith(
                                    "Question:"
                                ):

                                    question = (
                                        question.replace(
                                            "Question:",
                                            "",
                                            1
                                        ).strip()
                                    )


                                if question:

                                    questions.append(
                                        question
                                    )


                        # =================================================
                        # FALLBACK PARSER
                        # =================================================

                        if not questions:

                            for line in (
                                questions_text.splitlines()
                            ):

                                line = line.strip()

                                if len(line) > 20:

                                    cleaned = line

                                    prefixes = [
                                        "Question:",
                                        "Q:",
                                        "-",
                                        "*"
                                    ]

                                    for prefix in prefixes:

                                        if cleaned.startswith(
                                            prefix
                                        ):

                                            cleaned = (
                                                cleaned[
                                                    len(prefix):
                                                ].strip()
                                            )

                                    if cleaned:

                                        questions.append(
                                            cleaned
                                        )


                        # Limit questions

                        questions = questions[
                            :number_of_questions
                        ]


                        if not questions:

                            st.error(
                                "AI did not generate readable questions. Please try again."
                            )

                        else:

                            st.session_state.questions = (
                                questions
                            )

                            st.session_state.current_question = 0

                            st.session_state.answers = []

                            st.session_state.evaluations = []

                            st.session_state.overall_scores = {}

                            st.session_state.readiness_score = 0

                            st.session_state.readiness_level = ""

                            st.session_state.readiness_recommendation = ""

                            st.session_state.interview_started = True

                            st.session_state.interview_completed = False

                            st.rerun()


                    except Exception as e:

                        st.error(
                            f"Unable to generate interview questions: {e}"
                        )


# ============================================================
# PERFORMANCE PAGE
# ============================================================

elif st.session_state.page == "Performance":

    html(
        """
        <div class="section-title">
            📊 Performance Analysis
        </div>

        <div style="
            color:#AFC0D5;
            font-size:16px;
            line-height:1.7;
        ">

            Review your AI-generated interview
            performance and Fuzzy Logic readiness.

        </div>
        """
    )


    if not st.session_state.overall_scores:

        st.info(
            "Complete a mock interview to see your performance analysis."
        )


    else:

        scores = st.session_state.overall_scores


        # ========================================================
        # OVERALL SCORE
        # ========================================================

        html(
            f"""
            <div class="score-card">

                <div class="score-label">
                    OVERALL INTERVIEW SCORE
                </div>

                <div class="score-value">
                    {scores.get('overall_score', 0)}/100
                </div>

            </div>
            """
        )


        # ========================================================
        # METRICS
        # ========================================================

        c1, c2, c3, c4, c5 = st.columns(5)


        c1.metric(
            "Technical Knowledge",
            f"{scores.get('technical_knowledge', 0)}/100"
        )


        c2.metric(
            "Relevance",
            f"{scores.get('relevance', 0)}/100"
        )


        c3.metric(
            "Communication",
            f"{scores.get('communication', 0)}/100"
        )


        c4.metric(
            "Completeness",
            f"{scores.get('completeness', 0)}/100"
        )


        c5.metric(
            "Confidence",
            f"{scores.get('confidence', 0)}/100"
        )


        st.divider()


        # ========================================================
        # PERFORMANCE CHART
        # ========================================================

        html(
            """
            <div class="section-title">
                📈 Performance Overview
            </div>
            """
        )


        categories = [
            "Technical Knowledge",
            "Relevance",
            "Communication",
            "Completeness",
            "Confidence"
        ]


        values = [
            scores.get(
                "technical_knowledge",
                0
            ),

            scores.get(
                "relevance",
                0
            ),

            scores.get(
                "communication",
                0
            ),

            scores.get(
                "completeness",
                0
            ),

            scores.get(
                "confidence",
                0
            )
        ]


        fig = go.Figure()


        fig.add_trace(
            go.Bar(
                x=categories,
                y=values,

                text=values,

                textposition="outside"
            )
        )


        fig.update_layout(
            height=450,

            paper_bgcolor="#080B12",

            plot_bgcolor="#080B12",

            font=dict(
                color="#AFC0D5"
            ),

            yaxis=dict(
                range=[0, 100],
                title="Score"
            ),

            xaxis=dict(
                title="Performance Area"
            ),

            margin=dict(
                l=40,
                r=40,
                t=40,
                b=80
            )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.divider()


        # ========================================================
        # QUESTION SUMMARY
        # ========================================================

        html(
            """
            <div class="section-title">
                📝 Answer Evaluation Summary
            </div>
            """
        )


        for index, evaluation in enumerate(
            st.session_state.evaluations
        ):

            score = evaluation.get(
                "overall_score",
                0
            )

            st.markdown(
                f"""
                **Question {index + 1}:**
                {score}/100
                """
            )


            st.progress(
                min(
                    max(score / 100, 0),
                    1
                )
            )


        st.divider()


        # ========================================================
        # FUZZY READINESS
        # ========================================================

        html(
            """
            <div class="section-title">
                🌫️ Fuzzy Interview Readiness
            </div>

            <div style="
                color:#AFC0D5;
                font-size:16px;
                line-height:1.7;
                margin-bottom:20px;
            ">

                The Fuzzy Logic inference system combines
                technical knowledge, relevance, communication,
                completeness and confidence to estimate
                overall interview readiness.

            </div>
            """
        )


        readiness_score = (
            st.session_state.readiness_score
        )

        readiness_level = (
            st.session_state.readiness_level
        )

        readiness_recommendation = (
            st.session_state.readiness_recommendation
        )


        html(
            f"""
            <div class="score-card">

                <div class="score-label">
                    FUZZY READINESS SCORE
                </div>

                <div class="score-value">
                    {readiness_score:.2f}/100
                </div>

                <div style="
                    color:#D9E7F8;
                    font-size:19px;
                    margin-top:12px;
                ">

                    Readiness Level:
                    <strong>{readiness_level}</strong>

                </div>

            </div>
            """
        )


        st.progress(
            min(
                max(readiness_score / 100, 0),
                1
            )
        )


        st.info(
            f"💡 {readiness_recommendation}"
        )


# ============================================================
# INTERVIEW REPORT
# ============================================================

elif st.session_state.page == "Interview Report":

    html(
        """
        <div class="section-title">
            📄 Interview Report
        </div>

        <div style="
            color:#AFC0D5;
            font-size:16px;
            line-height:1.7;
        ">

            Your detailed AI interview report is
            available after completing an interview.

        </div>
        """
    )


    if not st.session_state.overall_scores:

        st.info(
            "Complete a mock interview first to generate your report."
        )


    else:

        scores = st.session_state.overall_scores


        # ========================================================
        # RESULT
        # ========================================================

        html(
            f"""
            <div class="score-card">

                <div class="score-label">
                    INTERVIEW RESULT
                </div>

                <div class="score-value">
                    {scores.get('overall_score', 0)}/100
                </div>

            </div>
            """
        )


        # ========================================================
        # CANDIDATE INFORMATION
        # ========================================================

        html(
            f"""
            <div class="section-title">
                👤 Candidate
            </div>

            <div style="
                color:#AFC0D5;
                font-size:18px;
            ">

                {st.session_state.candidate_name}

            </div>
            """
        )


        html(
            f"""
            <div class="section-title">
                💼 Target Role
            </div>

            <div style="
                color:#AFC0D5;
                font-size:18px;
            ">

                {st.session_state.role}

            </div>
            """
        )


        html(
            f"""
            <div class="section-title">
                🎤 Interview Type
            </div>

            <div style="
                color:#AFC0D5;
                font-size:18px;
            ">

                {st.session_state.interview_type}

            </div>
            """
        )


        # ========================================================
        # PERFORMANCE
        # ========================================================

        html(
            """
            <div class="section-title">
                📊 Performance
            </div>
            """
        )


        performance_data = {
            "Technical Knowledge":
                scores.get(
                    "technical_knowledge",
                    0
                ),

            "Relevance":
                scores.get(
                    "relevance",
                    0
                ),

            "Communication":
                scores.get(
                    "communication",
                    0
                ),

            "Completeness":
                scores.get(
                    "completeness",
                    0
                ),

            "Confidence":
                scores.get(
                    "confidence",
                    0
                ),

            "Overall":
                scores.get(
                    "overall_score",
                    0
                )
        }


        for name, score in (
            performance_data.items()
        ):

            st.markdown(
                f"**{name}: {score}/100**"
            )

            st.progress(
                min(
                    max(score / 100, 0),
                    1
                )
            )


        st.divider()


        # ========================================================
        # FUZZY READINESS
        # ========================================================

        html(
            """
            <div class="section-title">
                🌫️ Fuzzy Readiness
            </div>
            """
        )


        html(
            f"""
            <div class="score-card">

                <div class="score-label">
                    READINESS SCORE
                </div>

                <div class="score-value">
                    {st.session_state.readiness_score:.2f}/100
                </div>

                <div style="
                    color:#D9E7F8;
                    font-size:19px;
                    margin-top:12px;
                ">

                    Level:
                    <strong>
                        {st.session_state.readiness_level}
                    </strong>

                </div>

            </div>
            """
        )


        st.info(
            "💡 "
            + st.session_state.readiness_recommendation
        )


        st.divider()


        # ========================================================
        # QUESTION DETAILS
        # ========================================================

        html(
            """
            <div class="section-title">
                🧠 Question-wise Evaluation
            </div>
            """
        )


        for index, evaluation in enumerate(
            st.session_state.evaluations
        ):

            with st.expander(
                f"Question {index + 1} • "
                f"{evaluation.get('overall_score', 0)}/100"
            ):

                st.markdown(
                    "**Question**"
                )

                st.write(
                    evaluation.get(
                        "question",
                        ""
                    )
                )


                st.markdown(
                    "**Your Answer**"
                )

                st.write(
                    evaluation.get(
                        "answer",
                        ""
                    )
                )


                st.divider()


                c1, c2, c3, c4, c5 = st.columns(5)


                c1.metric(
                    "Technical",
                    evaluation.get(
                        "technical_knowledge",
                        0
                    )
                )


                c2.metric(
                    "Relevance",
                    evaluation.get(
                        "relevance",
                        0
                    )
                )


                c3.metric(
                    "Communication",
                    evaluation.get(
                        "communication",
                        0
                    )
                )


                c4.metric(
                    "Completeness",
                    evaluation.get(
                        "completeness",
                        0
                    )
                )


                c5.metric(
                    "Confidence",
                    evaluation.get(
                        "confidence",
                        0
                    )
                )


                st.markdown(
                    "### ✅ Strengths"
                )


                strengths = evaluation.get(
                    "strengths",
                    []
                )


                for strength in strengths:

                    st.markdown(
                        f"- {strength}"
                    )


                st.markdown(
                    "### 🔧 Areas for Improvement"
                )


                improvements = evaluation.get(
                    "improvements",
                    []
                )


                for improvement in improvements:

                    st.markdown(
                        f"- {improvement}"
                    )


                st.markdown(
                    "### 💬 AI Feedback"
                )


                st.info(
                    evaluation.get(
                        "feedback",
                        "No feedback available."
                    )
                )


# ============================================================
# END
# ============================================================