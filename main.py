from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static HTML (index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/log")
async def log_location(request: Request):
    data = await request.json()
    print("Received location:", data)  # You could log to a file/db later
    return {"status": "ok"}
