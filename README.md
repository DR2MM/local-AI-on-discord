# Discord Ollama AI Bot

A Discord bot that connects to a **local Ollama server** to run AI models for chat.

---

## Supported Commands

| Command           | Description                          |
| ----------------- | ------------------------------------ |
| `/ask`            | Ask the general model                |
| `/code`           | Ask the coding model                 |
| `/analyze`        | Analyze an uploaded image            |
| `/active_models`  | Show currently running Ollama models |

---

## Requirements

* Python **3.10+**
* A running **Ollama server**
* Discord bot token

Python packages:

```
pip install discord.py aiohttp
```

---

## Required Models by default

Install the models you want to use:

```
ollama pull phi3:mini
ollama pull deepseek-coder:6.7b
ollama pull moondream:latest
```

You can change models inside the bot code.

---

## Setup

### 1. Clone the repository

```
git clone https://github.com/yourname/discord-ollama-bot
cd discord-ollama-bot
```

### 2. Add your Discord token

Inside the script:

```
TOKEN = "YOOUR_TOKEN"
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

## bot Management

The bot automatically:

* stops other models when a new one is used
* tracks model usage
* shuts down models after **2 minutes of inactivity**

helps reducing **VRAM usage**.

---

## Logging

Logs are written to:

```
bot.log
```

They also appear in the console.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## ⚠️ Disclaimer

This bot runs AI models locally through Ollama.
Performance depends on your hardware and available VRAM.
