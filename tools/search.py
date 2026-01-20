from langchain_community.tools.tavily_search import TavilySearchResults

def get_search_tool():
    """Returns the Tavily search tool."""
    return TavilySearchResults(max_results=3)
