from PyPDF2 import PdfReader
import docx
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi


def extract_text(file):

    text = ""

    if file.type == "application/pdf":

        reader = PdfReader(file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

        doc = docx.Document(file)

        for para in doc.paragraphs:
            text += para.text + " "

    return text


def extract_from_url(url):

    text = ""

    try:

        if "youtube.com" in url or "youtu.be" in url:

            if "v=" in url:
                video_id = url.split("v=")[1].split("&")[0]
            else:
                video_id = url.split("/")[-1]

            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            for t in transcript:
                text += t["text"] + " "

        else:

            response = requests.get(url, timeout=10)

            soup = BeautifulSoup(response.text, "html.parser")

            for p in soup.find_all("p"):
                text += p.get_text() + " "

    except Exception as e:

        text = ""

    return text
