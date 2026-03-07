# Discord Ollama AI Bot 🤖

A Discord bot that connects to a **local Ollama server** to run AI models for chat, coding help, and image analysis.

Supports multiple models and automatically manages VRAM by stopping unused models.

---

## ✨ Features

* 💬 Ask AI questions with `/ask`
* 🧑‍💻 Coding assistant with `/code`
* 🖼️ Image analysis with `/analyze`
* 🧠 Automatic model management
* ⏱️ Idle model shutdown to free VRAM
* 📜 Logging system
* ⚡ Async requests for better performance

---

## 🧠 Supported Commands

| Command           | Description                          |
| ----------------- | ------------------------------------ |
| `/ask`            | Ask the small general model          |
| `/code`           | Ask the coding model                 |
| `/analyze`        | Analyze an uploaded image            |
| `/running_models` | Show currently running Ollama models |

---

## 📦 Requirements

* Python **3.10+**
* A running **Ollama server**
* Discord bot token

Python packages:

```
pip install discord.py aiohttp
```

---

## 🤖 Required Models

Install the models you want to use:

```
ollama pull phi3:mini
ollama pull deepseek-coder:6.7b
ollama pull moondream:latest
```

You can change models inside the bot code.

---

## 🚀 Setup

### 1. Clone the repository

```
git clone https://github.com/yourname/discord-ollama-bot
cd discord-ollama-bot
```

### 2. Add your Discord token

Inside the script:

```
TOKEN = "your_discord_bot_token"
```

### 3. Start Ollama

```
ollama serve
```

### 4. Run the bot

```
python bot.py
```

---

## ⚙️ Model Management

The bot automatically:

* stops other models when a new one is used
* tracks model usage
* shuts down models after **2 minutes of inactivity**

This helps reduce **VRAM usage**.

---

## 📜 Logging

Logs are written to:

```
bot.log
```

They also appear in the console.

---

## 🛠️ Possible Improvements

* Streaming responses
* Multi-user conversation memory
* Per-server model settings
* Model load balancing
* Web dashboard

---

## 📄 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for details.

---

## ⚠️ Disclaimer

This bot runs AI models locally through Ollama.
Performance depends on your hardware and available VRAM.

---

## ⭐ Contributing

Pull requests and improvements are welcome.
Feel free to open an issue if you find bugs or want new features.
