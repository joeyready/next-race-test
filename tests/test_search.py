import re
import pytest
from playwright.sync_api import Page, expect

SEARCH_BOX = "Search by city or zip code..."

# TODO: scope this to the results area only (see note below the code).
# On its own it can also match the featured-races carousel on the homepage.
RESULT_LINKS = "a[href*='/races/']"

# Matches "5K", "5KM", "3.1 MILES", "3.11 MILES". Card text arrives without spaces
# between chips ("running_race5katx..."), so no \b word boundaries; the lookbehind
# only stops "15K", "2.5K" and "13.1 MILES" from matching.
FIVE_K = re.compile(r"(?<![\d.])(5\s?k|3\.1\d?\s*mi)", re.IGNORECASE)

# Only links that carry the search parameters belong to the search results.
SEARCH_RESULT_LINKS = "a[href*='/races/'][href*='lat=']"

def search_location(page: Page, term: str):
    page.get_by_role("textbox", name=SEARCH_BOX).fill(term)
    page.get_by_role("button", name="Search location").click()

    # The page shows a default list first, then swaps in the real results.
    # Wait until a result for the searched city actually appears.
    expect(
        page.locator(RESULT_LINKS).filter(has_text=re.compile(term, re.IGNORECASE)).first
    ).to_be_visible(timeout=15000)


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
def test_5k_filter_only_shows_5k_races(ready_page: Page):
    search_location(ready_page, "Austin")
    ready_page.get_by_role("button", name="5k").click()

    expect(ready_page).to_have_url(re.compile(r"distance=5k"))

    results = ready_page.locator(SEARCH_RESULT_LINKS)

    # Wait for an Austin 5K result to show up, so we know the filtered list loaded.
    expect(
        results.filter(has_text=re.compile("austin", re.IGNORECASE)).filter(has_text=FIVE_K).first
    ).to_be_visible(timeout=15000)

    others = results.filter(has_not_text=FIVE_K)
    try:
        expect(others).to_have_count(0, timeout=15000)
    except AssertionError:
        details = [
            f"{others.nth(i).get_attribute('href')} | "
            f"{others.nth(i).inner_text().replace(chr(10), ' / ')[:100]}"
            for i in range(others.count())
        ]
        raise AssertionError("Non-5K results:\n" + "\n".join(details))

def test_debug_results(ready_page: Page):
    search_location(ready_page, "Austin")
    ready_page.wait_for_load_state("networkidle")
    ready_page.wait_for_timeout(5000)  # debugging only

    links = ready_page.locator("a[href*='/races/']")
    print("\nlink count:", links.count())
    for i in range(min(links.count(), 15)):
        text = links.nth(i).inner_text().replace("\n", " / ")
        print(i, links.nth(i).get_attribute("href"), "|", text)