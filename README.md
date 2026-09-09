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
- **`get_by_role` / `get_by_text` locators over CSS selectors** — more resistant to breaking
  when the frontend is restyled, since they target accessible semantics, not markup structure.
- **No hardcoded data that changes** — e.g. the "Upcoming races" stat is checked for
  *visibility*, not an exact number, since the real count changes daily. Asserting on
  volatile data is a classic self-inflicted flakiness cause.
- **`base_url` centralized in `conftest.py`** — one place to point tests at a staging
  environment later, instead of hardcoding the domain in every test file.
- **CI runs on push, PR, schedule, and manual trigger** — push/PR catches regressions
  in this repo's own test code; the scheduled run acts as synthetic monitoring, catching
  production issues (e.g. a broken OAuth integration) even when nothing in this repo changed.

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

- `conftest.py` — shared fixtures. `base_url` is defined here once, so if you ever
  point tests at a staging URL instead of production, you only change it in one place.
- `tests/test_smoke.py` — homepage checks: title, hero heading, stats bar, nav links,
  a featured race link click-through, footer legal links.
- `pytest.ini` — registers the `smoke` marker so pytest doesn't warn about it.

## CI

`.github/workflows/smoke-tests.yml` runs this suite automatically:
- on every push and pull request to this repo
- every 4 hours on a schedule (production monitoring)
- on demand via the "Run workflow" button in the Actions tab

Failed runs upload a report artifact so failures can be diagnosed without re-running locally.

## Notes / known limitations

- These locators were built from the live page structure as of Aug 2026 — if the
  team redesigns the homepage, some `get_by_role`/`get_by_text` calls may need updating.
  That's normal, ongoing test maintenance rather than a bug in the suite.
- This is a smoke suite: fast, shallow, no-auth checks that the app is "alive." It
  intentionally does not cover login, race submission, or search — those need a
  dedicated test account and either a staging environment or a data-cleanup strategy,
  since they write real data.

## Roadmap

- [ ] `tests/test_signup.py` — once a dedicated test email is available
- [ ] `tests/test_submit_race.py` — once staging or a test-data cleanup strategy exists
- [ ] API-level tests (if/when the app exposes a documented API)
- [ ] Parallel test execution + HTML/Allure reporting

