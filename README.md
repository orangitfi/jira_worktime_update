# jira_work_update

`jira_work_update` is a proof-of-concept how you can you to log work time to Jira issues easily. This tool interacts with the Jira API to add worklog entries to specified issues, allowing you to specify the time in either minutes or `H:MM` format.

The jira-id is provided as input. If input is just `jira-id` the default comment is inserted into the entry for time tracking. If the input is in `jira-id: comment` format then the comment is placed on the worktime entry.format then the comment is placed on the worktime entry.

## Requirements

- [uv](https://github.com/astral-sh/uv
- A Jira account with API access permissions
- Jira API token (for authentication)

## Installation

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/yourusername/jira_work_update.git
cd jira_work_updat
```

This installs the package and makes the jira_work_update CLI command available.

## Setting Up Environment Variables

The tool requires the following environment variables for connecting to your Jira instance:

`JIRA_URL`: The base URL of your Jira instance (e.g., https://your-jira-instance.atlassian.net)
`JIRA_ACCOUNT`: Your Jira account email or username
`JIRA_API_KEY`: Your Jira API token
Setting Environment Variables in bash/zsh
To set these variables temporarily for the current session in bash or zsh, use:

```bash
export JIRA_URL="https://your-jira-instance.atlassian.net"
export JIRA_ACCOUNT="your-email@example.com"
export JIRA_API_KEY="your-api-token"
```

To make these variables persist across sessions, add the above lines to your ~/.bashrc (for bash) or ~/.zshrc (for zsh) file, then restart your terminal or source the file:

```bash

source ~/.bashrc   # For bash
source ~/.zshrc    # For zsh
```

In a fish shell, you can set these variables for the session:

```fish

set -x JIRA_URL "https://your-jira-instance.atlassian.net"
set -x JIRA_ACCOUNT "your-email@example.com"
set -x JIRA_API_KEY "your-api-token"
```

To make them persistent in fish, add the following lines to ~/.config/fish/config.fish:

```fish

set -x JIRA_URL "https://your-jira-instance.atlassian.net"
set -x JIRA_ACCOUNT "your-email@example.com"
set -x JIRA_API_KEY "your-api-token"
```

To make them persistent in fish, add the following lines to ~/.config/fish/config.fish:

```fish
set -x JIRA_URL "https://your-jira-instance.atlassian.net"
set -x JIRA_ACCOUNT "your-email@example.com"
set -x JIRA_API_KEY "your-api-token"
```

## Usage

To log work time to a Jira issue, use the following command:

```bash
uv run python -m jira_work_update -i "ISSUE-123: Optional comment" -t "1:30"
```

## Command-Line Options

-i or --input: Jira issue ID or "JiraID: Comment" format (e.g., "PROJ-123: Added unittesting"). If only the ID is provided, the comment defaults to "Worklog added from AgileDay".

-t or --time: Time spent on the issue, specified in either minutes (e.g., 90) or H:MM format (e.g., 1:30).

## Jira API Calls

This tool makes use of the following Jira API endpoints:

1. Add Worklog Entry
   Adds a worklog entry to a specified Jira issue.

Endpoint: `POST /rest/api/3/issue/{issueIdOrKey}/worklog`
Description: Adds time spent on a given Jira issue with an optional comment.
Example JSON Payload:

```json
{
  "timeSpent": "1h 30m",
  "comment": "Worklog added from AgileDay"
}
```

Example cURL Command
Here’s how to add a worklog to a Jira issue using cURL:

```bash

curl -X POST -u your-email@example.com:your-api-token \
  -H "Content-Type: application/json" \
  -d '{
        "timeSpent": "1h 30m",
        "comment": "Worked on code review"
      }' \
  "https://your-jira-instance.atlassian.net/rest/api/3/issue/ISSUE-123/worklog"
```

[More in jira rest api documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-worklogs/#api-rest-api-3-issue-issueidorkey-worklog-post)

2. Get Issue Details

Fetches details of a specific issue to retrieve metadata, like the issue summary.

Endpoint: `GET /rest/api/3/issue/{issueIdOrKey}`
Description: Retrieves detailed information about a specific issue, including the summary field.
Example cURL Command
This retrieves the details of an issue by its ID or key:

```bash

curl -X GET -u your-email@example.com:your-api-token \
  -H "Content-Type: application/json" \
  "https://your-jira-instance.atlassian.net/rest/api/3/issue/ISSUE-123"
```

[More in Jira API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-get)

## Example Usage

Add Worklog in Minutes
To add 90 minutes to issue PROJ-123 with a custom comment:

```bash

su run python -m jira_work_update -i "PROJ-123: Working on code updates" -t "90"
```

Add Worklog in Hours and Minutes
To add 1 hour and 30 minutes to issue PROJ-123 with the default comment:

```bash

su run python -m jira_work_update -i "PROJ-123" -t "1:30"
```

## Development and Testing

Run tests using pytest:

````bash
```bash
pytest
````
