require('dotenv').config();
const { OpenAI } = require('openai');
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function smartTrade() {
  try {
    // نطلب من OpenAI تحليل السوق وقرارات البيع/الشراء
    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "You are an NFT trading assistant." },
        { role: "user", content: "Analyze my Enjin wallet and suggest smart trades to reach 100 ENJ." }
      ],
    });

    const advice = response.choices[0].message.content;
    console.log("🤖 AI advice:", advice);

    // هنا تضع كود تنفيذ البيع/الشراء عبر API Enjin
    // مثال: axios.post(...) لإرسال أوامر البيع والشراء

  } catch (error) {
    console.error("❌ AI Error:", error.message);
  }
}

// نفذ التداول الذكي كل 10 دقائق (600000 مللي ثانية)
setInterval(smartTrade, 600000);

// تشغيل أول مرة عند بدء التشغيل
smartTrade();