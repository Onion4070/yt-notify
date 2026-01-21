import time
from dataclasses import asdict

from waitress import serve
from flask import Flask
from flask import request

import bot
import handler 

app = Flask(__name__)


@app.route("/")
def root():
    return "Hello Flask Server", 200


@app.route("/webhook", methods=["GET", "POST"])
def callback():
    # GET: challengeでの検証(購読確認)
    if request.method == "GET":
        challenge = request.args.get("hub.challenge")
        return challenge, 200
    
    # POST: ハブからの更新通知
    if request.method == "POST":
        xml = request.data # Atom/RSS XML
        #bot.notify(xml.decode())
        print("\n========== New Notify ==========\n")
        time.sleep(3)
        video_data = handler.xml_parse(xml)
        msg = '\n'.join(
            f'{k}: {v}' for k, v in asdict(video_data).items()
        )
        print(msg)
        bot.notify(msg)

        #print('\n==========  RAW XML  ==========\n')
        #print(request.data.decode())

        return "", 204


if __name__ == "__main__":
    print("Server listening localhost:8080...")
    app.run("0.0.0.0", port=8080)
    #serve(app, host="0.0.0.0", port=8080, threads=4)
