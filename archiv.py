import requests
import xml.etree.ElementTree as ET
from fastmcp import FastMCP



mcp=FastMCP(name="archive server")

@mcp.tool
def fetch_new_title(topic):
    '''Fetching newest research papers published on a given topic'''
    example_item = topic

    url = f"http://export.arxiv.org/api/query?search_query=all:{example_item}&start=0&max_results=5"

    headers = {
        "User-Agent": "MyBot/1.0"
    }

    response = requests.get(url, headers=headers)

    root = ET.fromstring(response.text)

    ns = {"atom": "http://www.w3.org/2005/Atom"}

    results = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text
        summary = entry.find("atom:summary", ns).text

        results.append({
            "title": title.strip(),
            "summary": summary.strip()[:200]
        })
    return results

if __name__=="__main__":
    mcp.run()
