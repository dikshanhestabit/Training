const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://mongodb:27017/capstone';

app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'UP', timestamp: new Date() });
});

// Simple Data Model
const ItemSchema = new mongoose.Schema({
  name: String,
  createdAt: { type: Date, default: Date.now }
});
const Item = mongoose.model('Item', ItemSchema);

// API Endpoints
app.get('/api/data', async (req, res) => {
  try {
    const items = await Item.find().limit(10);
    res.json(items);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/data', async (req, res) => {
  try {
    const newItem = new Item({ name: req.body.name || 'New Item' });
    await newItem.save();
    res.status(201).json(newItem);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

mongoose.connect(MONGODB_URI)
  .then(() => {
    console.log('Connected to MongoDB');
    app.listen(PORT, () => console.log(`Backend running on port ${PORT}`));
  })
  .catch(err => console.error('Could not connect to MongoDB', err));
