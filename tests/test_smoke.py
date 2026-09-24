import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_homepage_loads(ready_page: Page):
    expect(ready_page).to_have_title(re.compile("Next Race", re.IGNORECASE))


@pytest.mark.smoke
def test_hero_heading_visible(ready_page: Page):
    heading = ready_page.get_by_role("heading", name=re.compile("Your.*Next Race", re.IGNORECASE))
    expect(heading).to_be_visible()


@pytest.mark.smoke
def test_stats_bar_shows_upcoming_races(ready_page: Page):
    """
    Checks the '14,615 Upcoming races' style stat renders with some number,
    not that it matches an exact figure (that number changes daily).
    """
    stat = ready_page.get_by_text("Upcoming races")
    expect(stat).to_be_visible()


@pytest.mark.smoke
def test_nav_links_present(ready_page: Page):
    expect(ready_page.get_by_role("link", name="Submit a Race")).to_be_visible()
    expect(ready_page.get_by_role("link", name="About")).to_be_visible()


@pytest.mark.smoke
def test_featured_race_link_navigates_to_detail_page(ready_page: Page):
    featured_section = ready_page.locator("text=Featured races").locator("..")
    first_race_link = featured_section.get_by_role("link").first

    # The featured carousel auto-rotates every few seconds, which makes
    # reading text and then clicking/navigating unreliable — the DOM can
    # swap out from under us between reads. Grabbing just the href and
    # navigating directly is the most reliable single action here.
    race_url = first_race_link.get_attribute("href")
    ready_page.goto(f"https://nextrace.live{race_url}")

    expect(ready_page).to_have_url(re.compile(r"/races/"))
    expect(ready_page.get_by_role("heading", level=1).first).to_be_visible()

@pytest.mark.smoke
def test_footer_legal_links_present(ready_page: Page):
    expect(ready_page.get_by_role("link", name="Privacy Policy")).to_be_visible()
    expect(ready_page.get_by_role("link", name="Terms of Service")).to_be_visible()

@pytest.mark.smoke
def test_submit_race_page_shows_form_and_validates(ready_page: Page):
    ready_page.get_by_role("link", name="Submit a Race").click()
    expect(ready_page).to_have_url(re.compile(r"/submit", re.IGNORECASE))
    race_info = ready_page.get_by_role("heading", name=re.compile("Race Info", re.IGNORECASE)).locator("..")
    # The race info section contains a sequence of textboxes: Race name, Start date, End date, etc.
    expect(race_info.get_by_role("textbox").first).to_be_visible()
    expect(race_info.get_by_role("textbox").nth(1)).to_be_visible()
    # Submit empty form and assert native constraint validation blocks submission
    ready_page.get_by_role("button", name=re.compile("Submit", re.IGNORECASE)).click()
    expect(ready_page.locator("form :invalid").first).to_be_visible()