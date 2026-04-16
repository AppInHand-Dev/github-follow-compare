"""
# v1.0.0 16/04/2026
# Author: AppInHand-Dev
"""

#!/usr/bin/env python3
# github_follow_compare.py
import argparse
import functions
import sys

def main():
    parser = argparse.ArgumentParser(description="Compare followers and following lists for a GitHub profile")
    parser.add_argument("githubUsername", help="GitHub username to analyze")
    parser.add_argument("--no-gui", action="store_true", help="Do not open the GUI window; print results to console only")
    parser.add_argument("--csv", metavar="FILE", help="Save results to FILE in CSV format")
    parser.add_argument("--token", metavar="GITHUB_TOKEN", help="GitHub token for authenticated requests", default="")
    args = parser.parse_args()

    username = args.githubUsername.strip()
    token = args.token.strip()

    print(f"Fetching followers for {username} ...")
    followers = functions.fetch_tab_profiles(username, "followers", token=token)
    print(f"Found {len(followers)} followers.")

    print(f"Fetching following for {username} ...")
    following = functions.fetch_tab_profiles(username, "following", token=token)
    print(f"Found {len(following)} following.")

    if args.csv:
        try:
            functions.save_csv(args.csv, followers, following)
        except Exception as e:
            print(f"Error saving CSV: {e}")

    text_output = functions.format_results(username, followers, following)
    print("\n" + text_output)

    if not args.no_gui:
        try:
            functions.show_popup(f"Followers vs Following for {username}", text_output)
        except Exception as e:
            print(f"Unable to open GUI: {e}")

if __name__ == "__main__":
    main()
