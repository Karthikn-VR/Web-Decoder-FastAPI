from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scrape/")
async def scrape_url(url: str = Form(...)):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

    
        title = soup.title.text if soup.title else "No title found"
        num_images = len(soup.find_all("img"))
        links = [a["href"] for a in soup.find_all("a", href=True)]  
        paragraphs = len(soup.find_all("p"))
        buttons = len(soup.find_all("button"))
        footers = soup.find("footer").text.strip() if soup.find("footer") else "No footer found"
        functions = len(soup.find_all("script")) 

        return {
            "Title": title,
            "Number of Images": num_images,
            "Total Links": len(links),
            "Links": links,  
            "Paragraphs": paragraphs,
            "Buttons": buttons,
            "Footer Information": footers,
            "Available Functions (Scripts)": functions
        }

    except Exception as e:
        return {"error": str(e)}
