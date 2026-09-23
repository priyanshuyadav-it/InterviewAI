# ============================================================
# INTERVIEWAI - FUZZY LOGIC READINESS ENGINE
# ============================================================

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ============================================================
# FUZZY READINESS CALCULATOR
# ============================================================

def calculate_readiness(
    technical_knowledge,
    relevance,
    communication,
    completeness,
    confidence
):
    """
    Calculate interview readiness using
    a Fuzzy Logic inference system.

    Inputs:
        technical_knowledge : 0-100
        relevance          : 0-100
        communication      : 0-100
        completeness       : 0-100
        confidence         : 0-100

    Returns:
        Dictionary containing readiness score,
        readiness level and explanation.
    """

    # ========================================================
    # INPUT VARIABLES
    # ========================================================

    technical = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "technical"
    )

    relevance_input = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "relevance"
    )

    communication_input = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "communication"
    )

    completeness_input = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "completeness"
    )

    confidence_input = ctrl.Antecedent(
        np.arange(0, 101, 1),
        "confidence"
    )


    # ========================================================
    # OUTPUT VARIABLE
    # ========================================================

    readiness = ctrl.Consequent(
        np.arange(0, 101, 1),
        "readiness"
    )


    # ========================================================
    # MEMBERSHIP FUNCTIONS
    # ========================================================

    # ---------------- TECHNICAL ----------------

    technical["low"] = fuzz.trimf(
        technical.universe,
        [0, 0, 50]
    )

    technical["medium"] = fuzz.trimf(
        technical.universe,
        [30, 55, 80]
    )

    technical["high"] = fuzz.trimf(
        technical.universe,
        [60, 100, 100]
    )


    # ---------------- RELEVANCE ----------------

    relevance_input["low"] = fuzz.trimf(
        relevance_input.universe,
        [0, 0, 50]
    )

    relevance_input["medium"] = fuzz.trimf(
        relevance_input.universe,
        [30, 55, 80]
    )

    relevance_input["high"] = fuzz.trimf(
        relevance_input.universe,
        [60, 100, 100]
    )


    # ---------------- COMMUNICATION ----------------

    communication_input["low"] = fuzz.trimf(
        communication_input.universe,
        [0, 0, 50]
    )

    communication_input["medium"] = fuzz.trimf(
        communication_input.universe,
        [30, 55, 80]
    )

    communication_input["high"] = fuzz.trimf(
        communication_input.universe,
        [60, 100, 100]
    )


    # ---------------- COMPLETENESS ----------------

    completeness_input["low"] = fuzz.trimf(
        completeness_input.universe,
        [0, 0, 50]
    )

    completeness_input["medium"] = fuzz.trimf(
        completeness_input.universe,
        [30, 55, 80]
    )

    completeness_input["high"] = fuzz.trimf(
        completeness_input.universe,
        [60, 100, 100]
    )


    # ---------------- CONFIDENCE ----------------

    confidence_input["low"] = fuzz.trimf(
        confidence_input.universe,
        [0, 0, 50]
    )

    confidence_input["medium"] = fuzz.trimf(
        confidence_input.universe,
        [30, 55, 80]
    )

    confidence_input["high"] = fuzz.trimf(
        confidence_input.universe,
        [60, 100, 100]
    )


    # ========================================================
    # READINESS MEMBERSHIP FUNCTIONS
    # ========================================================

    readiness["low"] = fuzz.trimf(
        readiness.universe,
        [0, 0, 45]
    )

    readiness["medium"] = fuzz.trimf(
        readiness.universe,
        [30, 55, 75]
    )

    readiness["high"] = fuzz.trimf(
        readiness.universe,
        [60, 100, 100]
    )


    # ========================================================
    # FUZZY RULES
    # ========================================================

    # Rule 1
    rule1 = ctrl.Rule(
        technical["high"]
        & relevance_input["high"]
        & communication_input["high"],
        readiness["high"]
    )


    # Rule 2
    rule2 = ctrl.Rule(
        technical["high"]
        & relevance_input["high"]
        & completeness_input["high"],
        readiness["high"]
    )


    # Rule 3
    rule3 = ctrl.Rule(
        communication_input["high"]
        & confidence_input["high"]
        & completeness_input["high"],
        readiness["high"]
    )


    # Rule 4
    rule4 = ctrl.Rule(
        technical["medium"]
        & relevance_input["medium"]
        & communication_input["medium"],
        readiness["medium"]
    )


    # Rule 5
    rule5 = ctrl.Rule(
        completeness_input["medium"]
        & confidence_input["medium"],
        readiness["medium"]
    )


    # Rule 6
    rule6 = ctrl.Rule(
        technical["low"]
        & relevance_input["low"],
        readiness["low"]
    )


    # Rule 7
    rule7 = ctrl.Rule(
        communication_input["low"]
        & confidence_input["low"],
        readiness["low"]
    )


    # Rule 8
    rule8 = ctrl.Rule(
        technical["high"]
        & communication_input["low"],
        readiness["medium"]
    )


    # Rule 9
    rule9 = ctrl.Rule(
        technical["low"]
        & communication_input["high"],
        readiness["medium"]
    )


    # Rule 10
    rule10 = ctrl.Rule(
        confidence_input["low"]
        & completeness_input["low"],
        readiness["low"]
    )


    # ========================================================
    # CONTROL SYSTEM
    # ========================================================

    readiness_control = ctrl.ControlSystem(
        [
            rule1,
            rule2,
            rule3,
            rule4,
            rule5,
            rule6,
            rule7,
            rule8,
            rule9,
            rule10
        ]
    )


    # ========================================================
    # SIMULATION
    # ========================================================

    simulation = ctrl.ControlSystemSimulation(
        readiness_control
    )


    # ========================================================
    # SET INPUT VALUES
    # ========================================================

    simulation.input["technical"] = float(
        technical_knowledge
    )

    simulation.input["relevance"] = float(
        relevance
    )

    simulation.input["communication"] = float(
        communication
    )

    simulation.input["completeness"] = float(
        completeness
    )

    simulation.input["confidence"] = float(
        confidence
    )


    # ========================================================
    # COMPUTE
    # ========================================================

    simulation.compute()


    # ========================================================
    # GET OUTPUT
    # ========================================================

    readiness_score = simulation.output[
        "readiness"
    ]


    readiness_score = round(
        float(readiness_score),
        2
    )


    # ========================================================
    # READINESS LEVEL
    # ========================================================

    if readiness_score < 40:

        readiness_level = "Low"

        recommendation = (
            "More interview practice is recommended. "
            "Focus on strengthening technical knowledge, "
            "answer relevance and confidence."
        )


    elif readiness_score < 70:

        readiness_level = "Moderate"

        recommendation = (
            "You have a developing interview skill set. "
            "Continue practicing technical questions and "
            "work on communication, completeness and confidence."
        )


    else:

        readiness_level = "High"

        recommendation = (
            "You demonstrate strong interview readiness. "
            "Continue practicing realistic interview scenarios "
            "and refine communication and confidence."
        )


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {
        "readiness_score": readiness_score,
        "readiness_level": readiness_level,
        "recommendation": recommendation
    }