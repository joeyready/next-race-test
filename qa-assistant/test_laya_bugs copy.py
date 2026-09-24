from laya import load

agent = load("convaiinnovations/laya", subfolder="typed-decisions")


bug_reports = [
    {
        "name": "Cut off menu",
        "expected": "ui_ux",
        "report": """
        On the race detail page/card/ the bottom portion of the menu is cut off and not visible on screen.
        """
    },
    {
        "name": "Search button does nothing",
        "expected": "functional",
        "report": """
        on the home page, when entering a query and clicking the 'search' button there is no response.
        """
    },
    # {
    #     "name": "Wrong registration link",
    #     "expected": "navigation",
    #     "report": """
    #     from the race deatil page, when clicking on a race registration link, I am taken to the wrong race's registration page.
    #     """
    # },
    # {
    #     "name": "Incorrect race date",
    #     "expected": "content",
    #     "report": """
    #     I have found multiple instances where the race detail page displays the incorrect date.
    #     """
    # },
    # {
    #     "name": "Slow search",
    #     "expected": "performance",
    #     "report": """
    #     When searching for a specific race from the search bar, the results page takes approximately 8 seconds to load. Load time should be much shorter
    #     """
    # },
    # {
    #     "name": "Wrong race location",
    #     "expected": "content",
    #     "report": """
    #     The Irvine 5k race page displays 'Fullerton' as the race location. City displayed should be 'Irvine'.
    #     """
    # },
    {
        "name": "Broken race page",
        "expected": "functional",
        "report": """
        When clicking on a link to a race page, the site loads a blank page instead of loading the correct race page.
        """
    },
    # {
    #     "name": "Registration link unavailable",
    #     "expected": "navigation",
    #     "report": """
    #     When clicking the registration link on a race page, I am taken to a 404 page and nothing loads. This could be a problem with our link, or the race registration page URL has changed.
    #     """
    # },
    {
        "name": "Mobile layout overlap",
        "expected": "ui_ux",
        "report": """
        when accessing the race detail page the menu items overlap the race details making the lising hard to read and the menu difficult to access.
        """
    },
    {
        "name": "Search timeout",
        "expected": "performance",
        "report": """
        When clicking the search it takes about 30 seconds to get to the new page, and ultimatly only loads a blank page.
        """
    },
    # {
    #     "name": "Wrong race distance",
    #     "expected": "content",
    #     "report": """
    #     The Fish Fry 5k race displays 10k on our race deatail page for that race
    #     """
    # },
    {
        "name": "Filter doesn't work",
        "expected": "functional",
        "report": """
        WHen selecting the '10k' option from the race filter menu, the website is still showing results that are not 10k races
        """
    },
    # {
    #     "name": "Broken external registration",
    #     "expected": "navigation",
    #     "report": """
    #     When clicking the 'register' button on a race listing, I am sent to the correct ragistration site, but to a page for a different race sign-up
    #     """
    # },
    # {
    #     "name": "Text too small",
    #     "expected": "ui_ux",
    #     "report": """
    #     On mobile version of the site, when viewing the race detail pages, the text is extremely small, and very difficult to read.
    #     """
    # },
    # {
    #     "name": "Slow race details",
    #     "expected": "performance",
    #     "report": """
    #     Search results load quickly, but the individual race pages take over 10 seconds to load.
    #     """
    # },
]

questions = {
    "functional_failure": {
        "type": "choice",
        "instructions": "Determine whether the report describes a failure of a software feature or action.",
        "criteria": {
            "yes": (
                "YES: A software feature or user action fails to work correctly. "
                "Examples: a button does nothing, a filter produces the wrong results, "
                "a page fails to load, or an action produces an incorrect result."
            ),
            "no": (
                "NO: The software feature works, and the problem is instead visual, "
                "content-related, navigation-related, or performance-related."
            )
        }
    }
}


# questions = {
#     "issue_type": {
#         "type": "choice",
#         "instructions": "Classify the primary type of software issue described in the report.",
#         "criteria": {
#             "functional": (
#                 "The feature itself is not working correctly. The user performs an action, "
#                 "but the application does nothing, produces the wrong result, or behaves "
#                 "differently from what the action is supposed to do."
#             ),
#             "ui_ux": (
#                 "The feature works correctly, but there is a problem with its "
#                 "visual appearance, layout, readability, spacing, or presentation."
#             ),
#             "navigation": (
#                 "A link, route, redirect, or navigation action takes the user "
#                 "to the wrong destination."
#             ),
#             "content": (
#                 "Information displayed by the application is incorrect, "
#                 "inaccurate, or outdated."
#             ),
#             "performance": (
#                 "The application is unusually slow, laggy, or takes too long "
#                 "to respond."
#             ),
#         }
#     }
# }


for bug in bug_reports:
    result = agent.predict(bug["report"], questions)
    answer = result["answers"]["functional_failure"]

    print(f"Laya:    {answer['choice']}")
    print(f"Confidence: {answer['confidence']}")
    print(f"Probabilities: {answer['probabilities']}")