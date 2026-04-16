"""
# v1.0.0 16/04/2026
# Author: AppInHand-Dev
"""

# functions.py
"""
Utility functions for github_follow_compare project.
"""

import time
import csv
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from typing import List, Dict
import config


def fetch_tab_profiles(username: str, tab: str, token: str = "") -> List[Dict[str, str]]:
    """
    Download all profiles from the specified tab ('followers' or 'following').
    Returns a list of dicts: {'username': ..., 'display_name': ..., 'bio': ...}
    """
    headers = config.DEFAULT_HEADERS.copy()
    if token:
        headers["Authorization"] = f"token {token}"

    page = 1
    results: List[Dict[str, str]] = []
    seen = set()

    while True:
        url = f"https://github.com/{username}?page={page}&tab={tab}"
        try:
            resp = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        except requests.RequestException as e:
            print(f"Network error while fetching {url}: {e}")
            break

        if resp.status_code == 404:
            print(f"Profile not found: {username}")
            break
        if resp.status_code != 200:
            print(f"Unexpected response {resp.status_code} for {url}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        # Select the anchor that contains username and display name
        anchors = soup.select("a.d-inline-block.no-underline.mb-1")
        if not anchors:
            # likely end of pagination
            break

        page_profiles: List[Dict[str, str]] = []
        for a in anchors:
            href = a.get("href", "").strip()
            if not href.startswith("/"):
                continue
            uname = href.lstrip("/").split("/")[0]
            display_span = a.select_one("span.f4.Link--primary")
            display_name = display_span.get_text(strip=True) if display_span else ""
            parent = a.find_parent("div", class_="d-table-cell")
            bio_text = ""
            if parent:
                bio_div = parent.select_one("div.color-fg-muted.text-small.mb-2")
                if bio_div:
                    bio_text = bio_div.get_text(" ", strip=True)
            if uname and uname not in seen:
                page_profiles.append({"username": uname, "display_name": display_name, "bio": bio_text})
                seen.add(uname)

        if not page_profiles:
            break

        results.extend(page_profiles)
        page += 1
        time.sleep(config.SLEEP_BETWEEN_PAGES)

    return results


def save_csv(filename: str, followers: List[Dict[str, str]], following: List[Dict[str, str]]):
    """
    Save results to a CSV file with columns: list_type, username, display_name, bio
    """
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["list_type", "username", "display_name", "bio"])
        for p in followers:
            writer.writerow(["followers", p["username"], p["display_name"], p["bio"]])
        for p in following:
            writer.writerow(["following", p["username"], p["display_name"], p["bio"]])
    print(f"Results saved to {filename}")


def format_results(username: str, followers: List[Dict[str, str]], following: List[Dict[str, str]]) -> str:
    """
    Return a formatted string with the comparison and details.
    """
    set_followers = {p["username"] for p in followers}
    set_following = {p["username"] for p in following}

    not_following_back = sorted(set_following - set_followers)
    not_followed_by_you = sorted(set_followers - set_following)

    lines: List[str] = []
    lines.append(f"Profile: {username}")
    lines.append(f"Followers: {len(followers)}")
    lines.append(f"Following: {len(following)}")
    lines.append("")
    lines.append("Users you follow who do NOT follow you back (following - followers):")
    if not_following_back:
        for u in not_following_back:
            dn = next((p["display_name"] for p in following if p["username"] == u), "")
            lines.append(f"- {u}  {('('+dn+')') if dn else ''}")
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("Users who follow you but you do NOT follow back (followers - following):")
    if not_followed_by_you:
        for u in not_followed_by_you:
            dn = next((p["display_name"] for p in followers if p["username"] == u), "")
            lines.append(f"- {u}  {('('+dn+')') if dn else ''}")
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("Followers detail (username | display_name):")
    for p in followers:
        lines.append(f"- {p['username']} | {p['display_name']}")
    lines.append("")
    lines.append("Following detail (username | display_name):")
    for p in following:
        lines.append(f"- {p['username']} | {p['display_name']}")

    return "\n".join(lines)


def show_popup(title: str, text: str):
    """
    Show a Tkinter window with a scrollable text widget.
    """
    root = tk.Tk()
    root.title(title)
    root.geometry("800x600")
    st = ScrolledText(root, wrap=tk.WORD)
    st.pack(fill=tk.BOTH, expand=True)
    st.insert(tk.END, text)
    st.configure(state=tk.DISABLED)
    root.mainloop()
