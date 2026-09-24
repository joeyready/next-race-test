from laya import load

agent = load("convaiinnovations/laya", subfolder="typed-decisions")

bug_report = """
The profile menu is broken. It doesn't display correctly.
"""

questions = {
    "issue_type": {
        "type": "choice",
        "instructions": "Classify the type of software issue described in the report.",
        "criteria": {
            "ui_ux": "The issue affects the user interface, visual layout, or user experience.",
            "functional": "The software does not perform a function correctly.",
            "performance": "The issue involves slow response, lag, or excessive resource usage.",
            "other": "The issue does not clearly fit the other categories."
        }
    },

    "severity": {
        "type": "choice",
        "instructions": "Classify how severe the reported issue appears to be.",
        "criteria": {
            "low": "Minor issue with little impact on the user's ability to use the software.",
            "medium": "Noticeable issue that affects the user experience but has a workaround.",
            "high": "Significant issue that prevents or seriously interferes with an important function.",
            "critical": "Issue that makes the software unusable or creates a serious safety or security problem."
        }
    },

    "reproducibility": {
        "type": "choice",
        "instructions": "Determine how reproducible the issue is based only on the information provided.",
        "criteria": {
            "confirmed": "The report explicitly states that the issue was reproduced.",
            "possible": "The report suggests the issue may be reproducible but does not clearly confirm it.",
            "unknown": "There is not enough information to determine reproducibility."
        }
    }
}

result = agent.predict(bug_report, questions)

print(result)