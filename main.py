from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Serve static files like index.html and form.html
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root route: NDA / Terms screen
@app.get("/", response_class=HTMLResponse)
async def nda():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

# Form route: Opens the map and input form after agreeing to NDA
@app.get("/form", response_class=HTMLResponse)
async def form():
    with open("static/form.html", "r") as f:
        return HTMLResponse(content=f.read())

# Schema for full survey form
class SurveySubmission(BaseModel):
    name: str
    property: str
    notes: str
    lat: float
    lng: float
    timestamp: str
    ua: str
    geojson: str

# Survey form submission handler
@app.post("/log")
async def log_location(data: SurveySubmission):
    print("=== NEW SURVEY SUBMISSION ===")
    print("Timestamp:", data.timestamp)
    print("Name:", data.name)
    print("Property:", data.property)
    print("Lat/Lng:", data.lat, data.lng)
    print("Notes:", data.notes)
    print("User Agent:", data.ua)
    print("GeoJSON:", data.geojson)

    with open("location_log.csv", "a") as f:
        f.write(f"{data.timestamp},{data.name},{data.property},{data.lat},{data.lng},{data.notes},{data.ua},{data.geojson}\n")

    return {"status": "ok"}


# -------------------------------
# ✅ NEW: Immediate location logger
# -------------------------------
class LocationData(BaseModel):
    lat: float
    lng: float

@app.post("/log-location")
async def log_location_only(data: LocationData):
    timestamp = datetime.utcnow().isoformat()
    print(f"Immediate location received: {data.lat}, {data.lng} at {timestamp}")

    with open("locations.txt", "a") as f:
        f.write(f"{data.lat},{data.lng} @ {timestamp}\n")

    return {"status": "logged"}
