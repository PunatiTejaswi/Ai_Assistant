import os
import requests
import datetime
from dotenv import load_dotenv
from langchain_core.tools import Tool
from fpdf import FPDF

# LOAD ENV VARIABLES
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


# GOOGLE SEARCH FUNCTION
def google_search(query: str) -> str:
    
    if not SERPAPI_KEY:
        return "Error: SERPAPI_KEY not found in environment variables."

    serp_url = "https://serpapi.com/search.json"

    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5
    }

    try:
        response = requests.get(serp_url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Error while fetching search results: {str(e)}"

    results = ""

    organic_results = data.get("organic_results", [])

    if not organic_results:
        return "No results found."

    for i, result in enumerate(organic_results, 1):
        title = result.get("title", "No title")
        snippet = result.get("snippet", "No description")
        link = result.get("link", "No link")

        results += f"{i}. {title}\n"
        results += f"{snippet}\n"
        results += f"URL: {link}\n\n"

    return results

# # def generate_pdf(content: str) -> str:
    
# #     filename = f"research_output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

# #     pdf = FPDF()
# #     pdf.set_auto_page_break(auto=True, margin=10)
# #     pdf.add_page()
# #     pdf.set_font("Arial", size=12)

# #     for line in content.split("\n"):
# #         # Avoid encoding errors
# #         clean_line = line.encode("latin-1", "replace").decode("latin-1")
# #         pdf.multi_cell(0, 8, clean_line)

# #     pdf.output(filename)

# #     return f"PDF generated successfully: {filename}"
# def generate_pdf(content: str) -> str:

#     # If content is a list, convert it to string
#     if isinstance(content, list):
#         content = " ".join(str(item) for item in content)

#     filename = f"research_output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=10)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     for line in content.split("\n"):
#         # Avoid encoding errors
#         clean_line = line.encode("latin-1", "replace").decode("latin-1")
#         pdf.multi_cell(0, 8, clean_line)

#     pdf.output(filename)

#     return f"PDF generated successfully: {filename}"
def generate_pdf(content) -> str:

    if isinstance(content, list):
        content = content[0]["text"]

    filename = f"research_output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    lines = content.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            pdf.ln(4)
            continue

        # TITLE
        if line.startswith("# "):
            pdf.set_font("Arial", "B", 16)
            pdf.multi_cell(0, 10, line.replace("# ", ""))
            pdf.ln(3)

        #  MAIN HEADINGS
        elif line.startswith("## "):
            pdf.set_font("Arial", "B", 14)
            pdf.multi_cell(0, 8, line.replace("## ", ""))
            pdf.ln(2)

        # SUB HEADINGS
        elif line.startswith("### "):
            pdf.set_font("Arial", "B", 12)
            pdf.multi_cell(0, 7, line.replace("### ", ""))
            pdf.ln(1)

        #  BULLET POINTS
        elif line.startswith("*"):
            pdf.set_font("Arial", "", 11)
            clean_line = "• " + line.replace("*", "").strip()
            pdf.multi_cell(0, 6, clean_line)

        #  NORMAL TEXT
        else:
            pdf.set_font("Arial", "", 11)
            clean_line = line.encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 6, clean_line)

    pdf.output(filename)

    return f"PDF generated successfully: {filename}"


# TOOL OBJECTS (For Agent)
search_tool = Tool(
    name="google_search",
    func=google_search,
    description="Search Google for latest information."
)

pdf_tool = Tool(
    name="pdf_generator",
    func=generate_pdf,
    description="Generate a PDF document from text."
)