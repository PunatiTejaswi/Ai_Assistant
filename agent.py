
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent as lc_create_agent

from tools import search_tool, pdf_tool

load_dotenv()


def create_agent():

    llm = ChatGoogleGenerativeAI(
        # model="gemini-3-flash-preview",
        model="gemini-3-flash-preview",
        temperature=0.3
    )

    tools = [search_tool, pdf_tool]

    system_prompt = """
You are a professional AI Research Assistant.

Follow this workflow carefully:

1. Use the search tool to collect the latest information.
2. Analyze and summarize the results.
3. Generate a structured research report with:
   - Title
   - Executive Summary
   - Key Findings
   - References
   - Conclusion
4. After completing the report, use the PDF tool to generate a PDF document.

Always think step-by-step before answering.
"""

    agent = lc_create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    return agent

    




   


