"""BigQuery Agent definition using Google ADK."""

import os

from google.adk.agents import LlmAgent
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.oauth2.credentials import Credentials


def create_bigquery_agent(
    access_token: str,
    project_id: str,
    default_dataset: str | None = None,
    model: str = "gemini-3-pro-preview",
) -> LlmAgent:
    """Create a BigQuery agent using an OAuth access token.

    Args:
        access_token: Google OAuth2 access token from the browser.
        project_id: Google Cloud project ID chosen by the user.
        default_dataset: Default BigQuery dataset. If None, agent will discover.
        model: The Gemini model to use.

    Returns:
        Configured LlmAgent with BigQuery tools.
    """
    # Build credentials from the user's OAuth token
    credentials = Credentials(token=access_token)

    credentials_config = BigQueryCredentialsConfig(
        credentials=credentials,
    )

    tool_config = BigQueryToolConfig(
        compute_project_id=project_id,
    )

    bigquery_toolset = BigQueryToolset(
        credentials_config=credentials_config,
        bigquery_tool_config=tool_config,
    )

    dataset_clause = ""
    if default_dataset:
        dataset_clause = f"""
- Default Dataset: {default_dataset}
When writing SQL queries, prefer the fully qualified table name: `{project_id}.{default_dataset}.table_name`
"""

    agent = LlmAgent(
        model=model,
        name="BigQueryAgent",
        description="An AI agent that can query and analyze data in Google BigQuery.",
        instruction=f"""You are a helpful data analyst agent with access to Google BigQuery.

IMPORTANT CONFIGURATION:
- Project ID: {project_id}
{dataset_clause}

Your capabilities include:
- Listing available datasets and tables
- Getting schema information for tables
- Executing SQL queries to answer questions about the data

When a user asks a question:
1. Start by discovering available datasets if you haven't already
2. Get table schemas to understand the structure before writing queries
3. Write and execute SQL queries to answer the user's questions
4. Present results in a clear, readable format

Always use the project "{project_id}" for all queries unless the user explicitly specifies otherwise.
Always explain what you're doing and provide context for your answers.
If a query fails, explain the error and try to fix it.
Be concise but thorough in your responses.""",
        tools=[bigquery_toolset],
    )

    return agent
