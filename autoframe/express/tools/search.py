import os

import chainlit as cl
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


search_doc = {
    "name": "search",
    "description": """
検索クエリを指定して、検索結果を応答するアシスタントです。
""",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": """検索クエリを指定します。(ex: "Should I invest in Apple in 2024?")""",
            },
        },
        "required": ["query"],
    },
}


def search(query: str):
    cl.run_sync(
        cl.Message(
            content=f"@programmer\n{query}",
            author="user_proxy",
        ).send()
    )
    response = tavily.search(query=query)
    if "results" in response:  # type: ignore
        urls = [result["url"] for result in response["results"]]  # type: ignore
        cl.run_sync(
            cl.Message(
                content=f"@programmer\n{urls}",
                author="user_proxy",
            ).send()
        )
    return response
