require('dotenv').config();
const express = require('express');
const ngrok = require('ngrok');
const { OpenAI } = require('openai');
const axios = require('axios');

const app = express();
const port = 3000;

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const ENJIN_API_KEY = process.env.ENJIN_API_KEY;
const ENJIN_WALLET_ADDRESS = process.env.ENJIN_WALLET_ADDRESS;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('NFT Bot API is running');
});

// مثال استعلام بيانات من Enjin (تبدل حسب API الحقيقي)
app.get('/enjin/balance', async (req, res) => {
  try {
    // هنا استدعاء API حقيقي لـ Enjin
    const response = await axios.post('https://graphql.enjin.io', {
      query: `
      {
        wallet(address: "${ENJIN_WALLET_ADDRESS}") {
          balances {
            value
            assetId
          }
        }
      }
      `
    }, {
      headers: { Authorization: `Bearer ${ENJIN_API_KEY}` }
    });
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

(async () => {
  const url = await ngrok.connect(port);
  console.log(`🌐 ngrok tunnel open at: ${url}`);

  app.listen(port, () => {
    console.log(`✅ Server running at http://localhost:${port}`);
  });
})();