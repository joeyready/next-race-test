import re
import pytest


@pytest.fixture(scope="session")
def base_url():
    """
    Central place to set the site under test.
    Change this once if the domain or a staging URL ever changes.
    """
    return "https://nextrace.live"


@pytest.fixture
def ready_page(page, base_url):
    """
    Navigates to the homepage and dismisses the email signup popup if it
    appears, so every test starts from the same clean, unblocked state
    instead of each test repeating this setup itself.
    """
    page.goto(base_url)
    close_button = page.get_by_role("button", name=re.compile("close|dismiss|×", re.IGNORECASE))
    if close_button.is_visible():
        close_button.click()
    return page

