import os
import json
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

class WikipediaSearch:
    def __init__(self):
        """
        Initialize the Wikipedia search
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('RILEY_MODEL', 'gpt-4o')
    
    def search(self, query):
        """
        Search Wikipedia for information and summarize the results
        """
        try:
            # Search Wikipedia
            search_results = self._search_wikipedia(query)
            
            if not search_results or 'error' in search_results:
                return {
                    "error": "No Wikipedia results found",
                    "query": query
                }
            
            # Get the page content for the first result
            page_content = self._get_wikipedia_content(search_results[0]['title'])
            
            if not page_content or 'error' in page_content:
                return {
                    "error": "Failed to retrieve Wikipedia content",
                    "query": query,
                    "search_results": search_results
                }
            
            # Summarize the content
            summary = self._summarize_content(page_content, query)
            
            return {
                "query": query,
                "title": search_results[0]['title'],
                "summary": summary,
                "source": "Wikipedia",
                "search_results": search_results
            }
        except Exception as e:
            print(f"Error in Wikipedia search: {e}")
            return {
                "error": "Failed to search Wikipedia",
                "details": str(e)
            }
    
    def _search_wikipedia(self, query):
        """
        Search Wikipedia API for articles related to the query
        """
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "utf8": 1,
                "srlimit": 5
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'query' in data and 'search' in data['query']:
                results = []
                for item in data['query']['search']:
                    results.append({
                        "title": item['title'],
                        "snippet": BeautifulSoup(item['snippet'], 'html.parser').get_text(),
                        "pageid": item['pageid']
                    })
                return results
            else:
                return []
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return {"error": str(e)}
    
    def _get_wikipedia_content(self, title):
        """
        Get the content of a Wikipedia page by title
        """
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "titles": title,
                "prop": "extracts",
                "exintro": 1,
                "explaintext": 1
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            
            if 'extract' in pages[page_id]:
                return pages[page_id]['extract']
            else:
                return ""
        except Exception as e:
            print(f"Error getting Wikipedia content: {e}")
            return {"error": str(e)}
    
    def _summarize_content(self, content, query):
        """
        Summarize content using OpenAI
        """
        try:
            # Create a system prompt for summarization
            system_prompt = f"""
            You are Riley, an advanced AI specialized in research and summarization.
            Summarize the following Wikipedia content related to the query: "{query}"
            
            Focus on:
            1. Key facts and information
            2. Relevance to the original query
            3. Important context and background
            
            Provide a concise but comprehensive summary.
            """
            
            # Use OpenAI to summarize content
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ]
            )
            
            # Extract the summary
            summary = response.choices[0].message.content
            
            return summary
        except Exception as e:
            print(f"Error in content summarization: {e}")
            return f"Error summarizing content: {str(e)}"
