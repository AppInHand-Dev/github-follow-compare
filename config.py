"""
# v1.0.0 16/04/2026
# Author: AppInHand-Dev
"""

# config.py
"""
Configuration constants for github_follow_compare project.
"""

DEFAULT_HEADERS = {
    "User-Agent": "github-follow-compare-script/1.0"
}

# HTTP request timeout in seconds
REQUEST_TIMEOUT = 10

# Pause between page requests to avoid overloading the server (seconds)
SLEEP_BETWEEN_PAGES = 0.5

# Recommended virtual environment directory name (convention only)
VENV_DIR_NAME = ".venv"
