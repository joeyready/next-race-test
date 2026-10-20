from laya import load

agent = load(
    "convaiinnovations/laya",
    subfolder="typed-decisions"
)

report = """
On Next Race, I entered a city into the race search field and clicked Search.
Nothing happens and the results do not update.
"""

# Same questions every time.
# Only the order will change.

score_question = {
    "severity": {
        "type": "score",
        "instructions": "How severe is this software issue?",
        "criteria": {
            "0": "Minor issue with little impact.",
            "1": "Moderate issue that affects the user.",
            "2": "Major issue that significantly affects the user.",
            "3": "Critical issue that prevents the user from completing an important task."
        }
    }
}

choice_question = {
    "issue_type": {
        "type": "choice",
        "instructions": "Classify the primary type of software issue described in the report.",
        "criteria": {
            "functional": (
                "The feature does not work as intended. "
                "An action produces no result, the wrong result, "
                "or unexpected behavior."
            ),
            "ui_ux": (
                "The feature works correctly, but there is a problem "
                "with its visual appearance, layout, readability, "
                "spacing, or presentation."
            ),
            "navigation": (
                "A link, route, redirect, or navigation action "
                "takes the user to the wrong destination."
            ),
            "content": (
                "Information displayed by the application is "
                "incorrect, inaccurate, or outdated."
            ),
            "performance": (
                "The application is unusually slow, laggy, "
                "or takes too long to respond."
            )
        }
    }
}

noul_question = {
    "functional_failure": {
        "type": "noul",
        "instructions": (
            "Determine whether the report describes a failure "
            "of a software feature or user action."
        ),
        "criteria": {
            "yes": (
                "YES: A software feature or user action fails to "
                "work correctly. Examples include a button that "
                "does nothing, a filter that produces incorrect "
                "results, or a feature that produces an incorrect result."
            ),
            "no": (
                "NO: The software feature works, and the problem "
                "is instead visual, content-related, navigation-related, "
                "or performance-related."
            )
        }
    }
}


def run_test(name, questions):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    result = agent.predict(report, questions)

    for question_id, answer in result["answers"].items():
        print(f"\n{question_id}")
        print(f"  Answer:       {answer.get('choice')}")
        print(f"  Confidence:   {answer.get('confidence')}")
        print(f"  Probabilities: {answer.get('probabilities')}")


# ---------------------------------------------------------
# ORDER A: score → choice → noul
# ---------------------------------------------------------

questions_a = {}

questions_a.update(score_question)
questions_a.update(choice_question)
questions_a.update(noul_question)

run_test("ORDER A: score → choice → noul", questions_a)


# ---------------------------------------------------------
# ORDER B: noul → choice → score
# ---------------------------------------------------------

questions_b = {}

questions_b.update(noul_question)
questions_b.update(choice_question)
questions_b.update(score_question)

run_test("ORDER B: noul → choice → score", questions_b)


# ---------------------------------------------------------
# ORDER C: choice → noul → score
# ---------------------------------------------------------

questions_c = {}

questions_c.update(choice_question)
questions_c.update(noul_question)
questions_c.update(score_question)

run_test("ORDER C: choice → noul → score", questions_c)


# ---------------------------------------------------------
# ORDER D: noul → choice
# ---------------------------------------------------------

questions_d = {}

questions_d.update(noul_question)
questions_d.update(choice_question)

run_test("ORDER D: noul → choice", questions_d)


# ---------------------------------------------------------
# ORDER E: choice → noul
# ---------------------------------------------------------

questions_e = {}

questions_e.update(choice_question)
questions_e.update(noul_question)

run_test("ORDER E: choice → noul", questions_e)