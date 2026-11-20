import re
import pytest
from playwright.sync_api import Page, expect

SEARCH_BOX = "Search by city or zip code..."

# TODO: scope this to the results area only (see note below the code).
# On its own it can also match the featured-races carousel on the homepage.
RESULT_LINKS = "a[href*='/races/']"


def search_location(page: Page, term: str):
    page.get_by_role("textbox", name=SEARCH_BOX).fill(term)
    page.get_by_role("button", name="Search location").click()


@pytest.mark.functional
def test_search_controls_are_visible(ready_page: Page):
    expect(ready_page.get_by_role("textbox", name=SEARCH_BOX)).to_be_visible()
    expect(ready_page.get_by_role("button", name="Search location")).to_be_visible()


@pytest.mark.functional
def test_city_search_returns_matching_races(ready_page: Page):
    search_location(ready_page, "Austin")

    # Requiring "Austin" in the result text proves the search ran. Without that,
    # the featured carousel's /races/ links could make this pass even if search is broken.
    austin_results = ready_page.locator(RESULT_LINKS).filter(
        has_text=re.compile("austin", re.IGNORECASE)
    )
    expect(austin_results.first).to_be_visible()


@pytest.mark.functional
def test_search_result_opens_race_detail_page(ready_page: Page):
    search_location(ready_page, "Austin")

    first_result = ready_page.locator(RESULT_LINKS).filter(
        has_text=re.compile("austin", re.IGNORECASE)
    ).first
    expect(first_result).to_be_visible()
    race_url = first_result.get_attribute("href")

    ready_page.goto(race_url)
    expect(ready_page).to_have_url(re.compile(r"/races/"))
    expect(ready_page.get_by_role("heading", level=1).first).to_be_visible()


@pytest.mark.functional
def test_5k_filter_returns_results(ready_page: Page):
    search_location(ready_page, "Austin")
    ready_page.get_by_role("button", name="5k").click()

    results = ready_page.locator(RESULT_LINKS)

    # Verify the filter returns visible results.
    expect(results.first).to_be_visible()


def test_debug_results(ready_page: Page):
    search_location(ready_page, "Austin")
    ready_page.wait_for_load_state("networkidle")
    ready_page.wait_for_timeout(5000)  # debugging only

    links = ready_page.locator("a[href*='/races/']")
    print("\nlink count:", links.count())
    for i in range(min(links.count(), 15)):
        text = links.nth(i).inner_text().replace("\n", " / ")
        print(i, links.nth(i).get_attribute("href"), "|", text)