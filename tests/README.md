# race-app-tests

Automated smoke and negative tests for [nextrace.live](https://nextrace.live), a public
race-directory site, built with Playwright + pytest and run in GitHub Actions.

This started as a personal learning project: I do manual QA on this app already and wanted
to move from manual test cases into a real automated suite. Everything here is read-only:
no login, no completed form submissions, so it's safe to run against the live production site.

## Why these design choices

- **Playwright over Selenium**: built-in auto-waiting (`expect()` retries until an assertion
  passes or times out) removes a large class of flaky-test bugs that Selenium suites often
  need extra explicit-wait code to handle.
- **`get_by_role` / `get_by_text` / `get_by_placeholder` locators over CSS selectors**: more
  resistant to breaking when the frontend is restyled, since they target accessible semantics,
  not markup structure.
- **Visible-only locators for duplicated elements**: the page renders two identical search
  inputs (one hidden), so Playwright's strict mode rejects a bare locator and `.first` can
  silently pick the hidden one. The `search_box` fixture filters to the visible input so
  every test types into the real field.
- **No hardcoded data that changes**: e.g. the "Upcoming races" stat is checked for
  *visibility*, not an exact number, since the real count changes daily. Asserting on
  volatile data is a classic self-inflicted flakiness cause.
- **Control tests next to negative tests**: a negative test is only meaningful if the happy
  path works, so `test_search_valid_city_updates_results` proves the search mechanism
  works before the invalid-input tests rely on it.
- **`base_url` centralized in `conftest.py`**: one place to point tests at a staging
  environment later, instead of hardcoding the domain in every test file.
- **CI runs on push, PR, a daily schedule, and manual trigger**: push/PR catches regressions
  in this repo's own test code; the daily scheduled run (08:00 UTC) acts as synthetic
  monitoring, catching production issues (e.g. a site outage or a broken page) even when
  nothing in this repo changed.

## Setup

```bash
pip install -r tests/requirements.txt
playwright install
```

## Run

Run pytest against the `tests` folder. Running a bare `pytest` from the repo root can also
collect unrelated scripts elsewhere in the repo and slow collection down.

```bash
# everything in tests/, headless
pytest tests

# watch it run in an actual browser window
pytest tests --headed --browser chromium

# just the smoke tests
pytest tests -m smoke

# just the negative tests
pytest tests -m negative -v

# see print output / more detail
pytest tests -v -s
```

## Files

- `conftest.py`: shared fixtures.
  - `base_url`: defined once, so pointing tests at a staging URL later means changing it
    in one place.
  - `ready_page`: loads the homepage and dismisses the email signup popup so every test
    starts from the same state.
  - `search_box`: the visible "Search by city or zip code..." input (see design choices above).
- `tests/test_smoke.py` — read-only checks: homepage title, hero heading, stats bar,
  nav links, featured race click-through, About/Support pages, footer legal pages
  (Privacy, Terms, Affiliate Disclosure), the Submit a Race form's validation, and
  a city search that checks the URL, heading, and result cards update.
- `test_negative.py`: 6 negative and error-handling tests covering:
  - unknown URL returns a 404 and still renders a page
  - nonexistent race URL fails gracefully (404/410, no server error text leaked)
  - valid city search updates results (control test)
  - invalid city search shows an empty/error state (**expected failure**, see Known bugs)
  - special characters / script injection in the search box don't fire dialogs or break the page
  - Submit a Race form rejects an invalid email via native validation (nothing is submitted)
- `pytest.ini`: registers the `smoke` and `negative` markers so pytest doesn't warn about them.
- `requirements.txt`: Python dependencies (pytest, pytest-playwright, playwright).

## CI

`.github/workflows/smoke-tests.yml` (workflow name: "Daily tests") runs this suite automatically:
- on every push and pull request (catches regressions in the test code itself)
- daily at 08:00 UTC on a schedule (synthetic monitoring of production, which catches site
  problems even when nothing in this repo changed)
- on demand via the "Run workflow" button in the Actions tab

Smoke and negative tests run as separate steps, so a smoke failure doesn't skip the negative
tests and each result is easy to find in the log. Failed runs upload Playwright traces
(split into `test-results/smoke` and `test-results/negative`) as an artifact so failures can
be diagnosed without re-running locally. Scheduled and manual runs also post a pass/fail
summary to Slack.

## Known bugs

Bugs the suite has found in the app are tracked as `xfail(strict=True)` tests. The suite
stays green today, and the test fails loudly (XPASS) once the app is fixed, which is the cue
to remove the marker.

- **Invalid city searches fail silently.** Searching for an unrecognized city (e.g.
  `zzzzqqqq-no-such-city`) shows no empty-state or error message and leaves the previous
  results in place. Tracked by `test_search_with_no_matches_shows_empty_state`.

## Notes / known limitations

- These locators were built from the live page structure as of Aug 2026. If the
  team redesigns the homepage, some `get_by_role`/`get_by_text` calls may need updating.
  That's normal, ongoing test maintenance rather than a bug in the suite.
- This suite is fast, shallow, and no-auth. It intentionally does not cover login or
  completed race submissions, since those need a dedicated test account and either a staging
  environment or a data-cleanup strategy (they write real data). The submit-race tests only
  check that the form renders and that empty or invalid input is blocked by validation;
  nothing is ever sent.
- Search is covered by Enter-key submission only. The icon-only search button has no stable
  locator yet (an `aria-label` would fix that).
- This is a smoke suite: fast, shallow, no-auth checks that the app is "alive." It
  intentionally does not cover login or race submission. Those need a dedicated test
  account and either a staging environment or a data-cleanup strategy, since they
  write real data. Search is covered because it's read-only.

## Roadmap

- [ ] Negative search tests for an invalid zip code (e.g. `00000`) and an empty search submit
- [ ] Click-based search test once the search button has a stable locator
- [ ] `tests/test_filters.py`: read-only filter checks (distance, entry fee)
- [ ] `tests/test_signup.py`: once a dedicated test email is available
- [ ] `tests/test_submit_race.py`: once staging or a test-data cleanup strategy exists
- [ ] API-level tests (if/when the app exposes a documented API)
- [ ] Parallel test execution + HTML/Allure reporting