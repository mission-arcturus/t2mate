import asyncio
from flask import Flask, render_template, request

from y2mate import Y2MateClient

app = Flask(__name__)
client = Y2MateClient()

async def get_video_info(url):
    video_metadata = await client.from_url(url)
    return video_metadata

async def get_download_info(video_id, key):
    download_info = await client.get_download_info(video_id, key)
    return download_info

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_url', methods=['POST'])
def process_url():
    video_url = request.form['video_url']
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    video_metadata = loop.run_until_complete(get_video_info(video_url))
    
    if video_metadata:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        download_info = loop.run_until_complete(get_download_info(video_metadata.video_id, video_metadata.video_links[0].key))
        return render_template('result.html', video_metadata=video_metadata, download_info=download_info)
    else:
        return render_template('result.html', error="Unable to fetch video information.")

if __name__ == '__main__':
    app.run(debug=True)
