from flask import Flask, json, request, jsonify
from driver import MusicDriver
from download import Download

app = Flask(__name__)


@app.route('/lib/bootstrap.css')
def bootstrap():
    return app.send_static_file('lib/bootstrap.css')


@app.route('/lib/vue.js')
def vue():
    return app.send_static_file('lib/vue.js')


@app.route('/lib/axios.js')
def axios():
    return app.send_static_file('lib/axios.js')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/search', methods=['POST'])
def search():
    data = json.loads(request.get_data(as_text=True))
    name = data['name']
    author = data['author']
    music_driver = MusicDriver(name, author)
    all_music = music_driver.get_all_music()
    music_driver.close()
    ret = {'music_list': all_music}
    return jsonify(ret)


@app.route('/download', methods=['POST'])
def download():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    url = data['url']
    name = data['name']
    author = data['author']
    d = Download(name, author,url)
    d.dowmload()
    d.save()
    ret = {'state': 1}
    return jsonify(ret)


if __name__ == '__main__':
    app.debug = True  # 设置调试模式，生产模式的时候要关掉debug
    app.run(port=3000)
