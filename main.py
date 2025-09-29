from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from pytube import YouTube
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Convertisseur YouTube → MP4</title>
        <style>
            body { font-family: sans-serif; text-align: center; margin-top: 50px; }
            input, button { padding: 10px; font-size: 16px; width: 400px; }
        </style>
    </head>
    <body>
        <h1>Convertisseur YouTube → MP4</h1>
        /download
            <input type="text" name="url" placeholder="Colle l'URL YouTube ici" required>
            <br><br>
            <button type="submit">Télécharger</button>
        </form>
    </body>
    </html>
    """

@app.get("/download")
async def download_video(url: str):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
    filename = "video.mp4"
    stream.download(filename=filename)
    return FileResponse(filename, media_type='video/mp4', filename=yt.title + ".mp4")