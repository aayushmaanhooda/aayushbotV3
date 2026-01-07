from langchain.tools import tool
from datetime import datetime
from langchain_tavily import TavilySearch
from zoneinfo import ZoneInfo


@tool
def now_tool(tz: str = "Australia/Sydney") -> str:
    """
    Use this tool to return current dat eand time to the user
    Return the current local date/time.
    """
    return datetime.now(ZoneInfo(tz)).strftime("%Y-%m-%d %H:%M:%S %Z")


@tool
def age_calculator() -> str:
    """
    Use when age is asked
    Calculate age from a hardcoded date of birth (30 August 1999).
    Returns the current age as an integer of aayushmaan.
    """
    dob = datetime(1999, 8, 30)
    today = datetime.now()
    age = today.year - dob.year

    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return f"Current age: {age} years old (DOB: 30 August 1999)"


@tool("web_search_tool", return_direct=False)
def web_search_tool(query: str) -> str:
    """
    Use this tool to search the web when the user asks about current events,
    news, or things not in the local knowledge.
    Input: query (str) - the search term.
    Output: short text with titles and urls of results.
    """
    web_search = TavilySearch(max_results=3)
    res = web_search.invoke({"query": query})
    return res["results"]


tools = [now_tool, age_calculator, web_search_tool]
