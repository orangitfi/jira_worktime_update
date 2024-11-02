"""
Unit tests for Jira worklog functions.

This module contains unit tests for functions that interact with the Jira API to add worklog entries.
All Jira API calls are mocked to ensure that no actual API requests are made.

Environment variables required:
    - JIRA_URL: URL of the Jira server
    - JIRA_ACCOUNT: Jira username or account email
    - JIRA_API_KEY: API token for authentication

Functions tested:
    - add_worklog
    - add_worklog_minutes
    - add_worklog_hours_minutes
    - parse_input
    - parse_time
"""

import unittest
from unittest.mock import patch, MagicMock
from jira_work_update import (
    add_worklog,
    add_worklog_minutes,
    add_worklog_hours_minutes,
    parse_input,
    parse_time,
)


class TestJiraWorklogFunctions(unittest.TestCase):
    """
    Unit tests for Jira worklog-related functions.

    Tests the main functions for adding worklogs and parsing inputs without making actual API calls.
    """

    def test_add_worklog(self):
        """
        Tests the add_worklog function with mocked API calls.

        Ensures that the add_worklog function calls jira.add_worklog and jira.issue with the correct arguments
        and returns the expected formatted string containing issue key and summary.

        Args:
            mock_jira: Mocked jira client.
        """

        # Call the function under test
        result = add_worklog("ATS-1", "90m", "Test Comment")

        self.assertEqual(result, "ATS-1: Agile day testing ticket")

    def test_add_worklog_minutes(self):
        """
        Tests the add_worklog_minutes function with mocked add_worklog function.

        Ensures that add_worklog_minutes correctly converts minutes to Jira format and
        calls add_worklog with the correct arguments.

        Args:
            mock_add_worklog: Mocked add_worklog function.
        """
        result = add_worklog_minutes("ATS-1", 90, "Worked on unit testing")

        self.assertEqual(result, "ATS-1: Agile day testing ticket")

    def test_add_worklog_hours_minutes(self):
        """
        Tests the add_worklog_hours_minutes function with mocked add_worklog function.

        Ensures that add_worklog_hours_minutes correctly parses H:MM format and converts
        it to minutes for Jira, calling add_worklog with the correct arguments.

        Args:
            mock_add_worklog: Mocked add_worklog function.
        """
        result = add_worklog_hours_minutes("ATS-1", "1:30", "Code review")

        self.assertEqual(result, "ATS-1: Agile day testing ticket")

    def test_parse_input_with_comment(self):
        """
        Tests the parse_input function with an input string containing a comment.

        Ensures that the function correctly splits the input into issue_key and comment.
        """
        issue_key, comment = parse_input("PROJ-123: Added unit tests")
        self.assertEqual(issue_key, "PROJ-123")
        self.assertEqual(comment, "Added unit tests")

    def test_parse_input_without_comment(self):
        """
        Tests the parse_input function with an input string without a comment.

        Ensures that the function assigns the default comment when no comment is provided.
        """
        issue_key, comment = parse_input("PROJ-123")
        self.assertEqual(issue_key, "PROJ-123")
        self.assertEqual(comment, "Worklog added from AgileDay")

    def test_parse_time_minutes(self):
        """
        Tests the parse_time function with a time string in minutes format.

        Ensures the function interprets the time correctly as minutes and not hours and minutes.
        """
        minutes, time_str = parse_time("90")
        self.assertEqual(minutes, 90)
        self.assertIsNone(time_str)

    def test_parse_time_hours_minutes(self):
        """
        Tests the parse_time function with a time string in H:MM format.

        Ensures the function correctly parses hours and minutes separately, returning them as H:MM format.
        """
        minutes, time_str = parse_time("1:30")
        self.assertIsNone(minutes)
        self.assertEqual(time_str, "1:30")

    def test_parse_time_invalid_format(self):
        """
        Tests the parse_time function with an invalid time format.

        Ensures that the function raises a ValueError for invalid time formats.
        """
        with self.assertRaises(ValueError):
            parse_time("invalid")


if __name__ == "__main__":
    unittest.main()
