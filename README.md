# Github Follow Compare — Compare GitHub followers and following (CLI)

A small, focused command-line tool that fetches a GitHub user's **followers** and **following** pages, extracts usernames and display names, compares the two lists, and reports differences. The project is lightweight, easy to read, and intended for personal or educational use.

---

### ⚠️ Responsible use and legal notice

**This tool scrapes public GitHub profile pages.** Use it responsibly and avoid automated scraping at scale. Respect GitHub’s Terms of Service and applicable laws. If you plan to run many requests or run this tool frequently, prefer the official GitHub API with proper authentication and rate-limit handling.

**Recommendations**
- Use a personal access token (`--token`) to reduce the chance of being rate-limited.
- Add delays between requests (the script already includes a small pause).
- Do not use the tool for abusive or large-scale automated scraping.

---

### Key features

* **CLI tool** that compares followers vs following for a GitHub username.
* Extracts **username**, **display name**, and a short **bio** snippet from profile list pages.
* **CSV export** option (`--csv`) to save results.
* **GUI popup** (Tkinter) to display results by default; can be disabled with `--no-gui`.
* **Pagination support** to handle profiles spanning multiple pages.
* Simple, modular code split into `config.py`, `functions.py`, and `github_follow_compare.py`.

---

### Project provenance

This repository and its code were produced with the assistance of an AI. The repository owner provided the design and instructions; the AI generated the implementation and documentation. The owner reviewed and tested the code before publishing.

---

## Quick start

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd github-follow-compare
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # macOS / Linux
   source .venv/bin/activate
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   # Windows (Command Prompt)
   .venv\Scripts\activate.bat
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   If you don't have a `requirements.txt`, install:
   ```bash
   pip install requests beautifulsoup4
   ```

4. **Run the script**
   ```bash
   python github_follow_compare.py <githubUsername>
   ```

---

## Usage examples

- **Default (GUI + console)**
  ```bash
  python github_follow_compare.py AppInHand-Dev
  ```

- **Console only (no GUI)**
  ```bash
  python github_follow_compare.py AppInHand-Dev --no-gui
  ```

- **Save results to CSV**
  ```bash
  python github_follow_compare.py AppInHand-Dev --csv results.csv
  ```

- **Use a GitHub token to reduce rate limits**
  ```bash
  python github_follow_compare.py AppInHand-Dev --token ghp_xxx
  ```

---

## Command-line options

* **`githubUsername`** — GitHub username to analyze (positional).
* **`--no-gui`** — Do not open the Tkinter popup; print results to console only.
* **`--csv FILE`** — Save followers and following rows to `FILE` (columns: `list_type`, `username`, `display_name`, `bio`).
* **`--token GITHUB_TOKEN`** — Optional GitHub personal access token for authenticated requests.

---

## Output format

- **Console / GUI**: human-readable comparison showing:
  - users you follow who do not follow you back,
  - users who follow you but you do not follow back,
  - detailed lists of followers and following (username | display_name).

- **CSV**: rows with `list_type` (`followers` or `following`), `username`, `display_name`, `bio`.

---

## Implementation notes and limitations

* The scraper relies on the current GitHub HTML structure and CSS classes (e.g., `a.d-inline-block.no-underline.mb-1`, `span.f4.Link--primary`). If GitHub changes its markup, selectors may need updating.
* For robust, production-grade usage prefer the **GitHub API** (requires authentication and handles pagination and rate limits explicitly).
* The script includes a small delay between page requests to reduce load; adjust `SLEEP_BETWEEN_PAGES` in `config.py` if needed.
* The tool reads only public profile pages; private data is not accessible.

---

## Files in this repository

- **`github_follow_compare.py`** — CLI entry point.
- **`functions.py`** — Scraping, CSV export, formatting, and GUI helper functions.
- **`config.py`** — Configuration constants (headers, timeouts, delays).
- **`requirements.txt`** — Python dependencies (recommended).
- **`LICENSE`** — Project license (MIT).

---

## Contributing

Contributions are welcome. Suggested improvements:
- Add an API-based mode using the GitHub REST API.
- Add unit tests for parsing and formatting functions.
- Add an option to export separate CSV files for followers and following.
- Improve error handling and retry logic for transient network errors.

When contributing, please update the README to reflect any changes that affect usage or legal/ethical considerations.

---

## Reproducibility and provenance

This project is a small orchestration of standard Python libraries (`requests`, `beautifulsoup4`, `tkinter`). It is reproducible by installing the listed dependencies and running the script. The implementation was generated with AI assistance; the repository owner provided the instructions and validated the code.

---

## License

This project is released under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Final notes

* Keep dependencies up to date.
* If you plan to run this tool frequently or at scale, switch to the GitHub API and implement proper rate-limit handling.
* Use the tool responsibly and respect the terms of service of the platforms you interact with.