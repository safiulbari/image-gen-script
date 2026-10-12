// server.js
// Simple Express server for the dashboard and delete endpoint

const express = require('express');
const path = require('path');
const fs = require('fs');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// Workspace root
const workspaceRoot = path.resolve(__dirname, '/Users/safiulbari/Documents/Office projects/othe.app images');
app.use(express.static(workspaceRoot));
app.use(bodyParser.json());

function safePath(...segments) {
  return path.join(workspaceRoot, ...segments);
}

app.post('/delete_image', (req, res) => {
  const { key } = req.body;
  if (!key) return res.status(400).json({ error: 'Missing key' });

  const [industry, profession] = key.split('::');
  if (!industry || !profession) return res.status(400).json({ error: 'Invalid key format' });

  const sanitize = name => name.replace(/[\\/\\:*?"<>|]/g, '-').trim() || 'untitled';
  const imgPath = safePath('images', sanitize(industry), `${sanitize(profession)}.png`);
  const progressPath = safePath('images', 'batch_progress.json');

  // Delete image file
  try {
    if (fs.existsSync(imgPath)) fs.unlinkSync(imgPath);
  } catch (e) {
    console.error('Error deleting image:', e);
    return res.status(500).json({ error: 'Failed to delete image' });
  }

  // Update progress log
  try {
    const data = JSON.parse(fs.readFileSync(progressPath, 'utf-8'));
    delete data[key];
    fs.writeFileSync(progressPath, JSON.stringify(data, null, 2), 'utf-8');
  } catch (e) {
    console.error('Error updating progress log:', e);
    return res.status(500).json({ error: 'Failed to update log' });
  }

  res.json({ ok: true });
});

// Fallback middleware to serve view.html for any unknown route
app.use((req, res) => {
  res.sendFile(path.join(workspaceRoot, 'view.html'));
});

app.listen(PORT, () => {
  console.log(`Dashboard running at http://localhost:${PORT}`);
});
