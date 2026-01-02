"""
CECS 451 - Artificial Intelligence
Assignment 0 - One paragraph summarizer
Name: Aalind Kale
Student ID: 030892041
Due Date: 09/10/2025

"""


import argparse
import os
import sys
import google.generativeai as genai
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urlparse
import json
from dotenv import load_dotenv
import requests


class ContentSummarizer:
    def __init__(self, api_key = None):

        load_dotenv()
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("We Couldn't find the correct API key. Kindly try again.")
        genai.configure(api_key=self.api_key)
        self.model = "gemini-1.5-flash"

    def fetch_webpage(self, url, max_retries=3):
        ''' I am making it to handle timeouts and basically handle some errors such as 404s'''
        print(f"Fetching...: {url}")
        if not self.api_key:
            raise ValueError("The API key couldn't be located. Try providing it as an argument or adding it to the environment.")
        parsed_url = urlparse(url)
        if not (parsed_url.scheme and parsed_url.netloc):
            raise ValueError("The provided URL is invalid.")
        
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'}

        for total_attempts in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                print(f"{len(response.text)} characters fetched from {url}")
                return response.text
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    raise Exception("Error 404: URL not found.")
                else:
                    raise Exception(f"HTTP error occurred: {e}")
                
            except requests.exceptions.Timeout:
                print(f"Attempt {total_attempts + 1} timed out.")
                if total_attempts == 2:
                    raise Exception("We reached maximum retries but were unable to fetch the URl.")
                

            
            except requests.exceptions.RequestException as e:
                print(f"Attempt {total_attempts + 1} failed: {e}")
                if total_attempts == 2:
                    raise Exception("We reached maximum retries but were unabe to fetch the URl.")
    

    def extraction(self, html_content):
        print("Extracting content...")
        try: 
            content = trafilatura.extract(html_content, include_comments=False, include_tables=False, include_formatting=False)

            if content and len(content) > 100:
                print("Trafilatura extraction successful!")
                return content
            else:
                print("Trafilatura extraction failed or content too short, trying BeautifulSoup...") 
     
        except Exception as e:
            raise ValueError(f"We ran into an error during content extraction: {e}")
        
        try:
            print("Using BeautifulSoup for extraction...")
            soup = BeautifulSoup(html_content, 'html.parser')
            for i in soup(['script', 'style', 'header', 'footer', 'nav']):
                i.decompose()

            desired_content = None
            for j in ['main', 'article', 'body']:
                desired_content = soup.select_one(j)
                if desired_content:
                    break

            if not desired_content:
                desired_content = soup

            text = desired_content.get_text(separator='\n', strip=True)
            lines = (line.strip() for line in text.splitlines())
            paragraph = " ".join(lines)

            if len(paragraph) < 100:
                print("The content that was extracted seems to be way too short.")
                return None
            else:
                print("BeautifulSoup extraction successful!")
                return paragraph
        
        except Exception as e:
            raise Exception(f"We faced an error during BeautifulSoup extraction: {e}")


    def summarize_text(self, text, url):
        print("Summarizing content...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        try:
            prompt = f"""Summarize the following text in precisely 3 sentences and 5 Keywords.\n\n{text}",
                Format your response exactly as:
                Summary: [your 3-sentence paragraph here]
                Keywords: [comma-separated keywords here]

                Text to summarize:
                {text}"""
            response = model.generate_content(
                prompt,
                generation_config={
                    'max_output_tokens': 512,
                    'temperature': 0.2,
                    'top_p': 0.9,
                    'top_k': 40
                }
            )

            if not response or not response.text:
                raise Exception("No response from the API.")
            print("Summarization successful.")
            return self.parse_response(response.text, url)
        except Exception as e:
            raise Exception(f"An errror seems to have occured while summarizing: {e}")
        
    def parse_response(self, response, url):
        summary_para = ""
        keywords = ""

        all_lines = response.split('\n')
        for line in all_lines:
            if line.startswith("Summary:"):
                summary_para = line[8:].strip()
            elif line.startswith("Keywords:"):
                keywords = line[9:].strip()
            elif line.startswith("**Summary**"):
                summary_para = line[12:].strip()
            elif line.startswith("**Keywords**"):
                keywords = line[13:].strip()

        if not summary_para or not keywords:
            parts = response.split('\n\n')

            for k in parts:
                k = k.strip()
                if 'summary' in k.lower()[:20] or (not summary_para and len(k) > 50):
                    summary_para = k
                elif 'keyword' in k.lower()[:20] or (not keywords and ',' in k and len(k) < 200):
                    keywords = k


        if summary_para.lower().startswith("summary:"):
            summary_para = summary_para[8:].strip()

        if keywords.lower().startswith("keywords:"):
            keywords = keywords[9:].strip()

        if not summary_para:
            summary_para = response.strip[:300]
        
        if not keywords:
            keywords = "content, web, article, data, summary"
        return {
            "url": url,
            "summary": summary_para,
            "keywords": keywords,
            "reference": url
        }

def main():
    parser = argparse.ArgumentParser(description="Summarize web content from a URL.")
    parser.add_argument('--url', type=str, required=True, help="The URL of the web page to summarize.")
    args = parser.parse_args()

    try:
        summarizer = ContentSummarizer()
        html = summarizer.fetch_webpage(args.url)
        content = summarizer.extraction(html)
        if not content:
            raise Exception("Failure occured while extracting the content from the webpage.")
        res = summarizer.summarize_text(content, args.url)

        print(f"From URL: {args.url}")
        print(f"Summary: {res['summary']}")
        print(f"Keywords: {res['keywords']}")
        print(f"Reference: {res['reference']}")
        print()

        json_output = {
            "url": res['url'],
            "summary": res['summary'],
            "keywords": res['keywords'],
            "reference": res['reference']
        }

        print(json.dumps(json_output, indent=2))

        if os.path.exists('output.json'):
            with open('output.json', 'r') as f:
                try: 
                    l = json.load(f)
                    if not isinstance(l, list):
                        l = [l]
                except json.JSONDecodeError:
                    l = []
        else:
            l = []

        l.append(json_output)


        with open('output.json', 'w') as f:
            json.dump(l, f, indent=2)


    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
        sys.exit(1)

if __name__ == "__main__":
    main()