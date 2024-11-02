"""
CLI tool to add worklog entries to Jira issues.

This script allows users to log work time to Jira issues from the command line, with support for time formats
in minutes or H:MM. It requires Jira credentials and server URL to be set as environment variables:

Environment variables:
    - JIRA_URL: The base URL of your Jira server.
    - JIRA_ACCOUNT: Your Jira username or account email.
    - JIRA_API_KEY: Your Jira API token for authentication.

Command-line arguments:
    - -i / --input: Jira issue ID or "JiraID: Comment" format (e.g., "PROJ-123: Added unittesting").
    - -t / --time: Time spent on the issue, in minutes (e.g., "90") or H:MM format (e.g., "1:30").

Example usage:
    python jira_worklog.py -i "PROJ-123: Code review" -t "1:30"
"""

import os
import re
import argparse
from jira import JIRA

# Retrieve Jira credentials and server from environment variables
JIRA_SERVER = os.getenv("JIRA_URL")
JIRA_USERNAME = os.getenv("JIRA_ACCOUNT")
JIRA_API_TOKEN = os.getenv("JIRA_API_KEY")

# Validate environment variables
if not JIRA_SERVER or not JIRA_USERNAME or not JIRA_API_TOKEN:
    raise EnvironmentError(
        "Please set JIRA_URL, JIRA_ACCOUNT, and JIRA_API_KEY environment variables."
    )

# Initialize JIRA client
jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))


def add_worklog(issue_key, time_spent, comment="Worklog added from AgileDay"):
    """
    Adds a worklog entry to a Jira issue.

    Args:
        issue_key (str): The key of the Jira issue (e.g., "PROJ-123").
        time_spent (str): Time spent in Jira format (e.g., "1h" or "30m").
        comment (str): A comment for the worklog entry.

    Returns:
        str: Formatted string containing the issue key and summary.

    Raises:
        Exception: If adding the worklog fails or the issue cannot be retrieved.
    """
    try:
        # Add worklog to the specified issue
        jira.add_worklog(issue=issue_key, timeSpent=time_spent, comment=comment)

        # Retrieve the issue to get the summary
        issue = jira.issue(issue_key)
        summary = issue.fields.summary

        result = f"{issue_key}: {summary}"
        print(result)
        return result

    except Exception as e:
        print(f"Failed to add worklog: {e}")
        return None


def add_worklog_minutes(issue_key, minutes, comment="Worklog added from AgileDay"):
    """
    Adds a worklog entry to a Jira issue with time specified in minutes.

    Args:
        issue_key (str): The key of the Jira issue (e.g., "PROJ-123").
        minutes (int): Time spent in minutes.
        comment (str): A comment for the worklog entry.

    Returns:
        str: Result from add_worklog with the formatted issue key and summary.
    """
    time_spent = f"{minutes}m"
    return add_worklog(issue_key, time_spent, comment)


def add_worklog_hours_minutes(
    issue_key, time_str, comment="Worklog added from AgileDay"
):
    """
    Adds a worklog entry to a Jira issue with time specified in H:MM format.

    Args:
        issue_key (str): The key of the Jira issue (e.g., "PROJ-123").
        time_str (str): Time spent in H:MM format (e.g., "1:30" for 1 hour and 30 minutes).
        comment (str): A comment for the worklog entry.

    Returns:
        str: Result from add_worklog with the formatted issue key and summary.
    """
    hours, minutes = map(int, time_str.split(":"))
    total_minutes = hours * 60 + minutes
    time_spent = f"{total_minutes}m"
    return add_worklog(issue_key, time_spent, comment)


def parse_input(input_value):
    """
    Parses the input to separate Jira issue key and comment.

    Args:
        input_value (str): Jira issue key or "JiraID: Comment" format.

    Returns:
        tuple: A tuple containing the issue key and comment. If no comment is provided,
               defaults to "Worklog added from AgileDay".
    """
    if ":" in input_value:
        issue_key, comment = input_value.split(":", 1)
        issue_key = issue_key.strip()
        comment = comment.strip()
    else:
        issue_key = input_value.strip()
        comment = "Worklog added from AgileDay"
    return issue_key, comment


def parse_time(time_value):
    """
    Parses the time argument to determine if it's in minutes or H:MM format.

    Args:
        time_value (str): Time in minutes (e.g., "90") or H:MM format (e.g., "1:30").

    Returns:
        tuple: A tuple (minutes, time_str) where one of the values is None.
               - If time is in minutes, returns (minutes, None).
               - If time is in H:MM format, returns (None, time_str).

    Raises:
        ValueError: If the time format is invalid.
    """
    if re.match(r"^\d+$", time_value):  # Only digits, assume minutes
        return int(time_value), None
    elif re.match(r"^\d+:\d{2}$", time_value):  # H:MM format
        return None, time_value
    else:
        raise ValueError(
            "Time must be in minutes (e.g., 90) or H:MM format (e.g., 1:30)"
        )


def main():
    """
    Main function to parse command-line arguments and add a worklog entry to a Jira issue.

    Retrieves issue key and comment from the input, parses time format, and calls the appropriate
    function to add worklog in minutes or H:MM format.
    """
    parser = argparse.ArgumentParser(description="Add worklog to a Jira issue.")
    parser.add_argument(
        "-i", "--input", required=True, help="Jira issue ID or 'JiraID: Comment'"
    )
    parser.add_argument(
        "-t",
        "--time",
        required=True,
        help="Time in minutes (e.g., 90) or H:MM format (e.g., 1:30)",
    )

    args = parser.parse_args()

    issue_key, comment = parse_input(args.input)
    minutes, time_str = parse_time(args.time)

    if minutes is not None:
        add_worklog_minutes(issue_key, minutes, comment)
    elif time_str is not None:
        add_worklog_hours_minutes(issue_key, time_str, comment)


if __name__ == "__main__":
    main()
