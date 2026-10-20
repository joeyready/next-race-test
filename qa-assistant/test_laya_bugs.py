from laya import load

agent_root = load("convaiinnovations/laya")
agent_td = load("convaiinnovations/laya", subfolder="typed-decisions")

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
        "report": """I enter a search query and click the Search button, but the search is not executed and the results do not update."""
    },
    {
        "name": "Wrong registration link",
        "expected": "navigation",
        "report": """
        from the race deatil page, when clicking on a race registration link, I am taken to the wrong race's registration page.
        """
    },
    {
        "name": "Incorrect race date",
        "expected": "content",
        "report": """
        I have found multiple instances where the race detail page displays the incorrect date.
        """
    },
    {
        "name": "Slow search",
        "expected": "performance",
        "report": """
        When searching for a specific race from the search bar, the results page takes approximately 8 seconds to load. Load time should be much shorter
        """
    },
    {
        "name": "Wrong race location",
        "expected": "content",
        "report": """
        The Irvine 5k race page displays 'Fullerton' as the race location. City displayed should be 'Irvine'.
        """
    },
    {
        "name": "Broken race page",
        "expected": "functional",
        "report": """
        When clicking on a link to a race page, the site loads a blank page instead of loading the correct race page.
        """
    },
    {
        "name": "Registration link unavailable",
        "expected": "navigation",
        "report": """
        When clicking the registration link on a race page, I am taken to a 404 page and nothing loads. This could be a problem with our link, or the race registration page URL has changed.
        """
    },
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
    {
        "name": "Wrong race distance",
        "expected": "content",
        "report": """
        The Fish Fry 5k race displays 10k on our race deatail page for that race
        """
    },
    {
        "name": "Filter doesn't work",
        "expected": "functional",
        "report": """
        I select the 10k filter, but the results include races that are not 10k. The filter is not applying correctly.        """
    },
    {
        "name": "Broken external registration",
        "expected": "navigation",
        "report": """
        When clicking the 'register' button on a race listing, I am sent to the correct ragistration site, but to a page for a different race sign-up
        """
    },
    {
        "name": "Text too small",
        "expected": "ui_ux",
        "report": """
        On mobile version of the site, when viewing the race detail pages, the text is extremely small, and very difficult to read.
        """
    },
    {
        "name": "Slow race details",
        "expected": "performance",
        "report": """
        Search results load quickly, but the individual race pages take over 10 seconds to load.
        """
    },
]

questions = {
    "issue_type": {
        "type": "choice",
        "instructions": "What kind of software issue does this report describe?",
        "criteria": {
            "functional": (
                "A feature fails to execute or produces no result, even though the "
                "correct destination loads and the data involved would otherwise be "
                "correct. Examples: a button click does nothing, a filter returns "
                "unfiltered results, a page loads blank. This does NOT include cases "
                "where the destination itself is wrong (see navigation), where the "
                "content shown is wrong (see content), where the layout is broken but "
                "the action still works (see ui_ux), or where it eventually works but "
                "is slow (see performance)."
            ),
            "navigation": (
                "A link, button, or redirect takes the user to the wrong destination, "
                "an unavailable page, or fails to route to the intended target at all. "
                "This is specifically about WHERE the user ends up, not whether the "
                "destination page itself works or what it displays."
            ),
            "content": (
                "The destination and functionality are correct, but a specific piece "
                "of displayed information is factually wrong: a date, location, "
                "distance, name, or other event detail. This does NOT include broken "
                "actions (see functional) or wrong destinations (see navigation)."
            ),
            "ui_ux": (
                "The information is correct and the feature works, but the visual "
                "presentation itself is broken: something is cut off, overlapping, "
                "misaligned, or too small to read. This does NOT include wrong data "
                "(see content), wrong destinations (see navigation), or a feature that "
                "fails to execute (see functional)."
            ),
            "performance": (
                "The feature works and eventually produces the correct result, but "
                "takes noticeably longer than expected or times out. If it ultimately "
                "fails or loads blank rather than just being slow, classify as "
                "functional instead."
            ),
        }
    }
}

# same bug_reports list as before

for bug in bug_reports:
    state = f"""
    You are a QA team lead reviewing software issue reports from a team of
    website testers. Your job is to determine what type of software issue
    the tester is describing.

    Tester report:
    {bug["report"]}
    """

    print(f"\n=== {bug['name']} (expected: {bug['expected']}) ===")
    for label, agent in [("root", agent_root), ("typed-decisions", agent_td)]:
        result = agent.predict(state, questions)
        answer = result["answers"]["issue_type"]
        print(f"  [{label:15s}] choice={answer['choice']:12s} "
              f"conf={answer['confidence']:.4f} probs={answer['probabilities']}")