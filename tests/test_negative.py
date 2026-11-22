import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.negative
def test_unknown_page_returns_404(page: Page, base_url):
    response = page.goto(f"{base_url}/this-page-does-not-exist")

    assert response is not None
    assert response.status == 404
    # A friendly not-found page should still render something, not a blank screen
    expect(page.locator("body")).not_to_be_empty()


@pytest.mark.negative
def test_nonexistent_race_page_fails_gracefully(page: Page, base_url):
    response = page.goto(f"{base_url}/races/zzz-not-a-real-race-000")

    assert response is not None
    assert response.status in (404, 410), f"Expected not-found, got {response.status}"
    expect(page.locator("body")).not_to_be_empty()
    # Should not leak a server error to the user
    expect(page.get_by_text(re.compile("500|internal server error|traceback", re.IGNORECASE))).to_have_count(0)


@pytest.mark.negative
def test_search_valid_city_updates_results(ready_page: Page, search_box):
    """Control test: proves the search mechanism works, so the failures below mean something."""
    search_box.fill("Irvine")
    search_box.press("Enter")

    expect(ready_page.get_by_text(re.compile(r"\d+ races in view"))).to_be_visible()


@pytest.mark.negative
@pytest.mark.xfail(
    strict=True,
    reason="Known bug: searching an invalid city silently does nothing, with no empty/error message",
)
def test_search_with_no_matches_shows_empty_state(ready_page: Page, search_box):
    search_box.fill("zzzzqqqq-no-such-city")
    search_box.press("Enter")

    feedback = ready_page.get_by_text(
        re.compile(r"no (races|results)|not found|couldn.t find|invalid|try another", re.IGNORECASE)
    ).first
    expect(feedback).to_be_visible(timeout=5000)


@pytest.mark.negative
def test_search_with_special_characters_does_not_break_page(ready_page: Page, search_box):
    dialogs = []
    # Register BEFORE interacting so an alert fired by the search can't slip past
    ready_page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))

    search_box.fill("<script>alert(1)</script>' OR 1=1 --")
    search_box.press("Enter")
    ready_page.wait_for_timeout(2000)

    assert not dialogs, f"Unexpected JS dialog fired from search input: {dialogs}"
    expect(ready_page.get_by_role("link", name="About")).to_be_visible()
    expect(ready_page.get_by_text(re.compile(r"\d+ races"))).to_be_visible()

@pytest.mark.negative
def test_submit_race_rejects_invalid_email(ready_page: Page):
    ready_page.get_by_role("link", name="Submit a Race").click()
    expect(ready_page).to_have_url(re.compile(r"/submit", re.IGNORECASE))

    email = ready_page.locator("form input[type='email']").first
    email.fill("not-an-email")
    ready_page.get_by_role("button", name=re.compile("Submit", re.IGNORECASE)).click()

    # Native validation blocks the submit, so nothing is written to production
    expect(ready_page).to_have_url(re.compile(r"/submit", re.IGNORECASE))
    assert email.evaluate("el => !el.validity.valid")