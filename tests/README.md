# race-app-tests

Automated smoke tests for [nextrace.live](https://nextrace.live), a public race-directory
site, built with Playwright + pytest and run in GitHub Actions.

This started as a personal learning project: I do manual QA on this app already and wanted
to move from manual test cases into a real automated suite. Everything here is read-only —
no login, no form submissions — so it's safe to run against the live production site.

## Why these design choices

- **Playwright over Selenium** — built-in auto-waiting (`expect()` retries until an assertion
  passes or times out) removes a large class of flaky-test bugs that Selenium suites often
  need extra explicit-wait code to handle.
- **`get_by_role` / `get_by_text` locators over CSS selectors** — more resistant to breaking when the frontend is restyled, since they target accessible semantics, not markup structure.
- **No hardcoded data that changes** — e.g. the "Upcoming races" stat is checked for
  *visibility*, not an exact number, since the real count changes daily. Asserting on volatile data is a classic self-inflicted flakiness cause.
- **`base_url` centralized in `conftest.py`** — one place to point tests at a staging
  environment later, instead of hardcoding the domain in every test file.
- **CI runs on push, PR, a daily schedule, and manual trigger** — push/PR catches regressions
  in this repo's own test code; the daily scheduled run (08:00 UTC) acts as synthetic monitoring, catching production issues (e.g. a site outage or a broken page) even when nothing in this repo changed.

## Setup

```bash
pip install -r requirements.txt
playwright install
```

## Run

```bash
# all tests, headless
pytest

# watch it run in an actual browser window
pytest --headed --browser chromium

# just the smoke-marked tests
pytest -m smoke

# see print output / more detail
pytest -v
```

## Files

- `conftest.py`: shared fixtures. `base_url` is defined here once, so pointing tests at a
  staging URL later means changing it in one place. The `ready_page` fixture loads the
  homepage and dismisses the email signup popup so every test starts from the same state.
- `test_smoke.py`: 12 smoke tests covering:
  - homepage title, hero heading, and "Upcoming races" stat
  - top navigation links (Submit a Race, About)
  - featured race click-through to a detail page
  - About, Privacy Policy, Terms of Service, Affiliate Disclosure, and Support pages
  - Submit a Race form rendering and empty-form validation (no data is submitted)
- `pytest.ini`: registers the `smoke` marker so pytest doesn't warn about it.
- `requirements.txt`: Python dependencies (pytest, pytest-playwright, playwright).

## CI

`.github/workflows/smoke-tests.yml` runs this suite automatically:
- on every push and pull request (catches regressions in the test code itself)
- daily at 08:00 UTC on a schedule (synthetic monitoring of production, which catches site problems even when nothing in this repo changed)
- on demand via the "Run workflow" button in the Actions tab

Failed runs upload Playwright traces as an artifact so failures can be diagnosed without re-running locally. Scheduled and manual runs also post a pass/fail summary to Slack.

## Notes / known limitations

- These locators were built from the live page structure as of Aug 2026 — if the
  team redesigns the homepage, some `get_by_role`/`get_by_text` calls may need updating.
  That's normal, ongoing test maintenance rather than a bug in the suite.
- This is a smoke suite: fast, shallow, no-auth checks that the app is "alive." It
  intentionally does not cover login or completed race submissions, since those need a
  dedicated test account and either a staging environment or a data-cleanup strategy
  (they write real data). The submit-race test only checks that the form renders and
  that an empty submission is blocked by validation; nothing is ever sent.
- Search and filtering are read-only and are planned as the next functional tests
  (see Roadmap).

## Roadmap

- [ ] `tests/test_search.py`: read-only search and filter checks
- [ ] `tests/test_signup.py` — once a dedicated test email is available
- [ ] `tests/test_submit_race.py` — once staging or a test-data cleanup strategy exists
- [ ] API-level tests (if/when the app exposes a documented API)
- [ ] Parallel test execution + HTML/Allure reporting

