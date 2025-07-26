from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files (index.html, form.html, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route for terms of use page (index.html)
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

# Route for form page (form.html)
@app.get("/form", response_class=HTMLResponse)
async def form():
    with open("static/form.html", "r") as f:
        return HTMLResponse(content=f.read())

# Endpoint for logging location data
@app.post("/log")
async def log_location(request: Request):
    data = await request.json()
    print("Received location:", data)  # Later you can write to a file or DB
    return {"status": "ok"}
