---

# 🛒 Day 7: Voice-Powered Grocery Ordering Agent

A natural voice-based grocery shopping assistant built using **LiveKit Agents**, **Murf AI TTS**, **Deepgram STT**, and **Google Gemini 2.5 Flash**, featuring **real-time cart visualization** and **smart recipe intelligence**.

---

# 🎯 Features

## 🧠 Smart Shopping Capabilities

* **80+ Grocery Items** across **8 major categories**
* **35+ Smart Recipes** → “I want to make pasta” automatically adds all required ingredients
* **Natural Language Conversation** (no rigid commands)
* **Multi-Item Parsing** → “Milk, eggs, and bread” → 3 items added correctly
* **Real-Time Cart Visualization** with beautiful animations
* **Accurate Price Lookup** from a structured catalog

---

## 🗂️ Categories & Items

* **Groceries:** Bread, Flour, Sugar, Salt, Atta, Besan
* **Dairy & Eggs:** Milk, Eggs, Butter, Cheese, Yogurt, Paneer, Cream
* **Condiments:** Ketchup, Mayo, Soy Sauce, Olive Oil, Honey, Ghee, Pickle
* **Pasta & Grains:** Spaghetti, Rice, Noodles, Oats, Poha, Dal, Chickpeas
* **Snacks:** Chips, Cookies, Biscuits, Namkeen, Nuts, Popcorn
* **Beverages:** Juice, Coffee, Tea, Soft Drinks, Water, Lassi
* **Prepared Foods:** Pizza, Sandwiches, Samosa, Spring Rolls
* **Fruits & Vegetables:** 20+ fresh produce items

---

## 🥘 Recipe Intelligence (35+ Recipes)

### 🇮🇳 Indian Recipes

Dal, Roti, Paratha, Biryani, Pulao, Aloo Gobi, Paneer Curry, Chole, Rajma, Sambar, Raita, Poha

### 🌍 International

Pasta, Spaghetti, Pizza, Salad, Soup, Pancakes, Omelet, Smoothie

### ☕ Beverages

Tea, Coffee, Lassi, Juice

---

## 🎤 Voice Integration

* **Murf AI Falcon TTS** (Ryan voice, 1.15x speed)
* **Deepgram STT** — real-time, accurate recognition
* **Gemini 2.5 Flash** — conversation + function calls

---

## 🖥️ UI Highlights

* Interactive **animated welcome screen**
* **Live cart display** that updates with every spoken command
* Item cards with name, quantity, price
* Auto-updating **total amount**
* **Smooth transitions** using Framer Motion
* **Success animation** after order placement

---

# 🚀 Quick Start

## ✔️ Prerequisites

* Python 3.11+
* Node.js 18+
* pnpm (recommended) or npm
* API Keys: Murf AI, Deepgram, Google Gemini
* LiveKit Server

---

## 📥 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/vikasyadav097/AI-Voice-Agent-Day-7-Food-Grocery-Ordering
```

---

## 🛠️ Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### Create `backend/.env.local`:

```
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
DEEPGRAM_API_KEY=your_deepgram_key
GOOGLE_API_KEY=your_gemini_key
MURF_API_KEY=your_murf_key
```

---

## 🌐 Frontend Setup

```bash
cd ../frontend
pnpm install
# or
npm install
```

### Create `frontend/.env.local`:

```
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
```

---

# ▶️ Running the Application

### 1. Start LiveKit Server

```bash
./livekit-server.exe --dev   # Windows
./livekit-server --dev       # Mac/Linux
```

### 2. Start Grocery Agent

```bash
cd backend
.venv\Scripts\activate
python src/agent.py dev
```

### 3. Start Frontend

```bash
cd frontend
pnpm dev
# or
npm run dev
```

### 4. Open Browser

👉 [http://localhost:3000](http://localhost:3000)

---

# 💬 Example Conversations

## 🛍️ Simple Shopping

**You:** “I need milk and eggs”
**Agent:** “Added 1 litre milk and 1 dozen eggs to your cart”

---

## 🍝 Recipe Request

**You:** “I want to make pasta”
**Agent:** “Adding spaghetti, tomato sauce, olive oil, garlic…”

---

## 🧺 Multi-Item Order

**You:** “Add milk, eggs, and bread”
**Agent:** “Added all three items to your cart”

---

## 🔄 Update Cart

**You:** “Make that 2 litres of milk”
**Agent:** “Updated milk quantity to 2”

---

## ✔️ Checkout

**You:** “Place my order”
**Agent:** “Order placed! ID: abc123. Delivery in 30–45 minutes.”

---

# 📁 Project Structure

```
.
├── backend/
│   ├── src/
│   │   ├── agent.py
│   │   └── murf_tts.py
│   ├── .env.local
│   └── pyproject.toml
├── frontend/
│   ├── app/
│   ├── components/
│   │   └── app/
│   │       ├── cart-display.tsx
│   │       ├── welcome-view.tsx
│   │       └── session-view.tsx
│   ├── .env.local
│   └── package.json
├── shared-data/
│   ├── catalog.json
│   └── orders/
│       ├── order_*.json
│       └── order_history.json
├── challenges/
│   └── Day 7 Task.md
└── livekit-server.exe
```

---

# 🔧 Customization

### ➕ Add New Catalog Items

```json
{
  "id": "NEW001",
  "name": "Your Item",
  "category": "Category",
  "price": 99,
  "unit": "unit",
  "brand": "Brand Name",
  "tags": ["organic"]
}
```

### 🍽️ Add New Recipes

```json
"recipes": {
  "your recipe": ["ITEM1", "ITEM2", "ITEM3"]
}
```

### 🎙️ Modify Voice Settings

```python
tts = murf_tts.TTS(
    voice="en-US-ryan",
    style="Conversational",
)
```

---

# 📊 Viewing Orders

### View individual orders:

```
type shared-data\orders\order_*.json  # Windows
cat shared-data/orders/order_*.json   # Mac/Linux
```

### View order history:

```
type shared-data\orders\order_history.json
```

---

# 🛠️ Tech Stack

* **Backend:** Python 3.11, LiveKit Agents SDK
* **Frontend:** Next.js 15, React, TypeScript
* **Voice:** Murf AI Falcon TTS, Deepgram STT
* **LLM:** Google Gemini 2.5 Flash
* **Real-time:** LiveKit WebRTC
* **Storage:** JSON-based
* **UI:** Tailwind CSS + Framer Motion

---

# 🎮 Testing Tips

* “I need milk”
* “Add eggs”
* “Show my cart”
* “I want to make biryani”
* “Remove butter”
* “Update milk to 3 litres”
* “Place my order”

---

# 📝 API Keys Required

* Murf AI
* Deepgram
* Google Gemini

---

# 📚 Learning Resources

* LiveKit Agents Documentation
* Murf AI API Docs
* Deepgram Docs
* Gemini API Docs
* Framer Motion Docs

---

# 🤝 Contributing

Feel free to fork and adapt this project!

---

# 📄 License

MIT License

---

# 🙏 Acknowledgments

Built for **Murf AI Voice Agent Challenge – Day 7**
Inspired by Blinkit, Zepto, Swiggy Instamart

---
| Day      | Status         |
| -------- | -------------- |
| Day 1    | ✅ Completed    |
| Day 2    | ✅ Completed    |
| Day 3    | ✅ Completed    |
| Day 4    | ✅ Completed    |
| Day 5    | ✅ Completed    |
| Day 6    | ✅ Completed    |
| Day 7    | ✅ Completed    |
| Day 8–10 | 🔜 Coming soon |



Just tell me!
