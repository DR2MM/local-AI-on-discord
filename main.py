import asyncio, base64, subprocess, logging, time, aiohttp, discord
from discord import app_commands
from discord.ext import commands

#vars
TOKEN = "YOUR_TOKEN"
logging.basicConfig( level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", handlers=[logging.FileHandler("bot.log", encoding="utf-8"),logging.StreamHandler()])
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)  
MODEL_IDLE_TIMEOUT = 600 
CHECK_EVERY = 10           
last_used = {}
last_used_lock = asyncio.Lock()
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
active_models = set()
#functions
def check_runnig_model(model: str):
    output = subprocess.check_output(["ollama", "ps"], text=True)
    lines = output.strip().split("\n")[1:]
    models = [line.split()[0] for line in lines if line]
    for m in models:
        if not models or m == model:
            continue
        subprocess.run(["ollama", "stop", m])

async def ollama_chat(model, messages, timeout_s = 180):
    timeout = aiohttp.ClientTimeout(total=timeout_s)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(
            OLLAMA_CHAT_URL,
            json={"model": model, "messages": messages, "stream": False},
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
    return data["message"]["content"]

def chunk(text: str, size: int = 1900):
    """Discord hard limit is 2000; keep margin for safety."""
    for i in range(0, len(text), size):
        yield text[i : i + size]

async def ollama_ps_models():
    def _ps():
        out = subprocess.check_output(["ollama", "ps"], text=True)
        lines = out.strip().split("\n")[1:]
        return [line.split()[0] for line in lines if line.strip()]
    return await asyncio.to_thread(_ps)

async def ollama_stop(model: str):
    def _stop():
        subprocess.run(["ollama", "stop", model], check=False)
    await asyncio.to_thread(_stop)

async def mark_model_used(model: str):
    async with last_used_lock:
        last_used[model] = time.monotonic()

async def model_idle_killer():
    while True:
        try:
            running = await ollama_ps_models()
            now = time.monotonic()
            async with last_used_lock:
                to_stop = []
                for m in running:
                    last = last_used.get(m)
                    if last is None:
                        last_used[m] = now
                        continue
                    if now - last > MODEL_IDLE_TIMEOUT:
                        to_stop.append(m)
            for m in to_stop:
                print(f"[Idle Killer] Stopping idle model: {m}")
                await ollama_stop(m)
                async with last_used_lock:
                    last_used.pop(m, None)
        except Exception as e:
            print("Idle killer error:", e)

        await asyncio.sleep(CHECK_EVERY)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(model_idle_killer())
    await bot.tree.sync()

@bot.tree.command(name="running_models", description="Show currently running Ollama models")
async def running_models(interaction: discord.Interaction):
    output = subprocess.check_output(["ollama", "ps"], text=True)
    lines = output.strip().split("\n")[1:]
    models = [line.split()[0] for line in lines if line]
    await interaction.response.send_message(f"running models: {models}", ephemeral=False)

@bot.tree.command(name="ask", description="Ask the small general model")
@app_commands.describe(text="Your question")
async def ask(interaction: discord.Interaction, text: str):
    model = "llava:7b"
    active_models.add(model)
    await mark_model_used(model)
    check_runnig_model(model)
    await interaction.response.send_message("Thinking...")
    try:
        reply = await ollama_chat(model, [{"role": "user", "content": text}], timeout_s=180)
        active_models.discard(model)
    except asyncio.TimeoutError:
        await interaction.edit_original_response(content="Timed out waiting for Ollama.")
        return
    except Exception as e:
        await interaction.edit_original_response(content=f"Error: {type(e).__name__}: {e}")
        return

    # handle long replies
    parts = list(chunk(reply))
    await interaction.edit_original_response(content=parts[0])
    for p in parts[1:]:
        await interaction.followup.send(p)

@bot.tree.command(name="code", description="Ask the coding model")
@app_commands.describe(text="Your coding question")
async def code(interaction: discord.Interaction, text: str):
    model = "qwen2.5-coder:7b"
    active_models.add(model)
    await mark_model_used(model)
    check_runnig_model(model)
    await interaction.response.send_message("Thinking...")
    try:
        reply = await ollama_chat(model, [{"role": "user", "content": text}], timeout_s=240)
        active_models.discard(model)
    except asyncio.TimeoutError:
        await interaction.edit_original_response(content="Timed out waiting for Ollama.")
        return
    except Exception as e:
        await interaction.edit_original_response(content=f"Error: {type(e).__name__}: {e}")
        return

    parts = list(chunk(reply))
    await interaction.edit_original_response(content=parts[0])
    for p in parts[1:]:
        await interaction.followup.send(p)

@bot.tree.command(name="analyze", description="Analyze an uploaded image")
@app_commands.describe(image="Upload an image", prompt="Optional prompt")
async def analyze(
    interaction: discord.Interaction,image: discord.Attachment,prompt: str = "Describe this image:"):
    model = "moondream:latest"
    active_models.add(model)
    await mark_model_used(model)
    check_runnig_model(model)
    await interaction.response.send_message("Thinking...")
    timeout = aiohttp.ClientTimeout(total=300)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(image.url) as resp:
                resp.raise_for_status()
                image_bytes = await resp.read()
        img_b64 = base64.b64encode(image_bytes).decode("utf-8")
        reply = await ollama_chat( model, [{"role": "user", "content": prompt, "images": [img_b64]}], timeout_s=300,)
        active_models.discard(model)
    except asyncio.TimeoutError:
        await interaction.edit_original_response(content="Timed out waiting for Ollama.")
        return
    except Exception as e:
        await interaction.edit_original_response(content=f"Error: {type(e).__name__}: {e}")
        return

    parts = list(chunk(reply))
    await interaction.edit_original_response(content=parts[0])
    for p in parts[1:]:
        await interaction.followup.send(p)

logger = logging.getLogger("discord_bot")
bot.run(TOKEN)
