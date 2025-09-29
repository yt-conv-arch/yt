from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
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
            #status { margin-top: 20px; font-weight: bold; color: #333; white-space: pre-line; }
        </style>
        <script>
            function updateStatus(message) {
                document.getElementById("status").innerText = message;
            }

            function handleSubmit(event) {
                event.preventDefault();
                const url = document.getElementById("url").value;
                updateStatus("🔗 URL reçue...");
                fetch(`/download?url=${encodeURIComponent(url)}`)
                    .then(response => response.json())
                    .then(data => {
                        let steps = data.etapes.join("\\n");
                        updateStatus("✅ Étapes:\\n" + steps);
                        if (data.fichier) {
                            const link = document.createElement("a");
                            link.href = `/video.mp4`;
                            link.download = data.fichier;
                            link.innerText = "📥 Télécharger la vidéo";
                            document.getElementById("status").appendChild(document.createElement("br"));
                            document.getElementById("status").appendChild(link);
                        }
                    })
                    .catch(error => {
                        updateStatus("❌ Erreur : " + error);
                    });
            }
        </script>
    </head>
    <body>
        <h1>Convertisseur YouTube → MP4</h1>
        <form onsubmit="handleSubmit(event)">
            <input type="text" id="url" placeholder="Colle l'URL YouTube ici" required>
            <br><br>
            <button type="submit">Télécharger</button>
        </form>
        <pre id="status"></pre>
    </body>
    </html>
    """

@app.get("/download")
async def download_video(url: str):
    etapes = []
    etapes.append("🔗 URL reçue")

    try:
        yt = YouTube(url)
        etapes.append(f"🎬 Vidéo trouvée : {yt.title}")
        stream = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
        etapes.append("📥 Téléchargement en cours...")
        filename = "video.mp4"
        stream.download(filename=filename)
        etapes.append("✅ Téléchargement terminé")
        return JSONResponse(content={"etapes": etapes, "fichier": yt.title + ".mp4"})
    except Exception as e:
        etapes.append(f"❌ Erreur : {str(e)}")
        return JSONResponse(content={"etapes": etapes, "fichier": None})