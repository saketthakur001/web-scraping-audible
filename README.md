# Web Scraping Audible

A Python project that scrapes audiobook listings from [Audible](https://www.audible.com)'s search pages, stores the results in a local SQLite database, and serves them through a small Flask web app with search/filter/sort functionality.

## What it does

1. **Scraping** (`audible scrape.py`): builds Audible search URLs (by genre, sort order, language, etc.), fetches each result page with `requests`, and parses out per-title details with `BeautifulSoup` — title, subtitle, author, narrator, series, runtime, release date, language, rating, vote count, cover image, and product link.
2. **Storage**: parsed results are cleaned (e.g. converting `"12 hr and 30 min"` to minutes, splitting `"4.5 out of 5 stars 1,234 ratings"` into rating/vote count) and inserted into a SQLite database (`audiobooks` table, keyed by product link so re-running skips duplicates).
3. **Web app** (`webapp/webapp.py`): a Flask app that loads the scraped data into a pandas DataFrame and exposes a homepage (`webapp/templates/index.html`, styled with `webapp/static/style.css`) supporting search, filtering (author, narrator, series, language, min length/rating/votes), sorting, and pagination.

## Key files

| File | Purpose |
|---|---|
| `audible scrape.py` | Scraper + `AudibleDB` class (create/insert/read/close) that builds the SQLite database from Audible search results. |
| `webapp/webapp.py` | Flask app that reads from the database and renders the searchable/filterable listing page. |
| `webapp/templates/index.html` | Homepage template. |
| `webapp/static/style.css` | Page styling. |
| `test.ipynb`, `gpt_prompts.ipynb`, `webapp/test.ipynb` | Scratch notebooks used while developing the scraping/parsing logic and experimenting with prompts. |
| `soup.html`, `test.html` | Saved HTML snapshots of Audible pages, used as local fixtures for developing the parser without hitting the live site every time. |

## Running it

### 1. Scrape data
```bash
pip install requests beautifulsoup4
python "audible scrape.py"
```
This scrapes a hardcoded page range (see `start_page`/`end_page` in the `__main__` block) using the `full_cast_paid_inclueded` link generator, and writes results into `audible_paid.db` in the current directory. Genre/sort options can be changed by calling `generate_link(...)` or `Romance(...)` instead.

### 2. Run the web app
```bash
pip install flask pandas
python webapp/webapp.py
```
Then open `http://127.0.0.1:5000/`.

## Limitations / known issues

- **Hardcoded local path**: `webapp/webapp.py` points `database_location` at a Windows path (`C:\Users\saket\...`) instead of a relative path — this needs to be changed to point at wherever the scraper's `.db` file actually lives before the app will run for anyone else.
- **Two separate databases**: the scraper writes to `audible_paid.db`, but the web app reads from a differently-named/located database — they aren't currently wired together automatically.
- **Fragile scraping**: relies on specific Audible CSS class names and URL query parameters that can change or break at any time; there's no error handling for network failures or rate limiting beyond a fixed `time.sleep(3)` between pages.
- **No requirements file**: dependencies (`requests`, `beautifulsoup4`, `flask`, `pandas`) are not pinned or listed anywhere.
- **No tests**: correctness of the scraping/parsing logic (e.g. `hour_min_to_min`, `extract_rating`) is unverified.
