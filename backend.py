from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import yt_dlp

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

class VideoDownloadRequest(BaseModel):
    video_url: str

# Function to download the video
def download_video(video_url: str):
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # Limit to 1080p
        'outtmpl': '%(title)s.%(ext)s'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return {"status": "Video downloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# FastAPI route to trigger the download
@app.post("/download/")
async def download_endpoint(request: VideoDownloadRequest):
    if not request.video_url:
        raise HTTPException(status_code=400, detail="No video URL provided")
    return download_video(request.video_url)

# FastAPI route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def get_html():
    with open("index.html", encoding="utf-8") as f:
        return f.read()
