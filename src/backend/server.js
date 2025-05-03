require('dotenv').config();
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const AWS = require('aws-sdk');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// // AWS Configuration
// AWS.config.update({
//   region: process.env.AWS_REGION,
//   accessKeyId: process.env.AWS_ACCESS_KEY_ID,
//   secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
// });

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Nutritional Data Endpoints
app.post('/api/nutrition', async (req, res) => {
  try {
    // TODO: Implement nutritional data processing
    res.json({ message: 'Nutritional data processed' });
  } catch (error) {     
    res.status(500).json({ error: error.message });
  }
});

// User Preferences Endpoints
app.get('/api/preferences', async (req, res) => {
  try {
    // TODO: Implement user preferences retrieval
    res.json({ message: 'User preferences retrieved' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
