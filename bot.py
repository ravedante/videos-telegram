import os, json
from flask import Flask, send_file, abort
from pyrogram import Client, filters
from threading import Thread

api_id = 21545360
api_hash = "25343abde47196a7e4accaf9e6b03437"
bot_token = "7883080708:AAFq9VPKJXQCHJzUfVCthjtYBMK2SStRGbs"

app = Flask(__name__)
download_dir = "videos"
os.makedirs(download_dir, exist_ok=True)

bot = Client("video_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def atualizar_cache(nome, link):
    with open("db.json", "r+") as f:
        try:
            data = json.load(f)
        except:
            data = []
        data.append({"nome": nome, "link": link})
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    os.system("git add db.json && git commit -m 'Atualizado' && git push -f")

@bot.on_message(filters.video | filters.document)
async def salvar_video(client, message):
    msg = await message.reply("⏬ Baixando vídeo...")
    file_name = message.video.file_name if message.video else message.document.file_name
    path = os.path.join(download_dir, file_name)
    await message.download(file_name=path)
    link = f"https://ravedante.github.io/CDNRAVE/video/{file_name}"
    atualizar_cache(file_name, link)
    await msg.edit(f"✅ Pronto!\n🎬 {file_name}\n🔗 {link}")

@app.route('/video/<filename>')
def servir(filename):
    path = os.path.join(download_dir, filename)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path, mimetype="video/mp4", as_attachment=False)

def start_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    Thread(target=start_flask).start()
    bot.run()
