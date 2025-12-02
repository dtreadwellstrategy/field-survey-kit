// /api/log-location.js
// CoreConnect™ — Safe Passage™
// Logs lat/lng to the FastAPI backend instead of GitHub

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { lat, lng } = req.body;

    if (!lat || !lng) {
      return res.status(400).json({ error: "Missing lat/lng values" });
    }

    // 🔥 Send the location to your FastAPI backend
    const backendURL = process.env.BACKEND_URL || "http://localhost:8000/log-location";

    const response = await fetch(backendURL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lat, lng })
    });

    if (!response.ok) {
      const errBody = await response.text();
      console.error("FastAPI logging error:", errBody);
      return res.status(500).json({ error: "Backend logging failed" });
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error("Error in log-location.js:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}
