// /api/log-location.js
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).send("Method not allowed");

  const { lat, lng } = req.body;
  if (!lat || !lng) return res.status(400).send("Missing lat/lng");

  const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
  const REPO = "dtreadwellstrategy/field-survey-kit";
  const FILE_PATH = "locations.txt";
  const API_URL = `https://api.github.com/repos/${REPO}/contents/${FILE_PATH}`;
  const message = `Location: ${lat}, ${lng} @ ${new Date().toISOString()}\n`;

  const headers = {
    Authorization: `Bearer ${GITHUB_TOKEN}`,
    Accept: "application/vnd.github+json"
  };

  // Step 1: Get existing content + sha
  const current = await fetch(API_URL, { headers });
  const currentData = await current.json();

  const existingContent = currentData.content
    ? Buffer.from(currentData.content, "base64").toString("utf-8")
    : "";

  const updatedContent = Buffer.from(existingContent + message).toString("base64");

  // Step 2: Push update
  const push = await fetch(API_URL, {
    method: "PUT",
    headers: {
      ...headers,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: "Log location",
      content: updatedContent,
      sha: currentData.sha
    })
  });

  if (push.ok) {
    res.status(200).json({ success: true });
  } else {
    const error = await push.json();
    res.status(500).json({ error: "GitHub update failed", details: error });
  }
}
