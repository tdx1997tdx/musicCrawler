from flask import Flask, json, request, jsonify
from container import Container
from download import Download

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/search', methods=['POST'])
def search():
    data = json.loads(request.get_data(as_text=True))
    name = data['name']
    author = data['author']
    con = Container(name, author)
    all_music = con.get_music()
    ret = {'music_list': all_music}
    return jsonify(ret)


@app.route('/download', methods=['POST'])
def download():
    data = json.loads(request.get_data(as_text=True))
    url_id = data['url_id']
    name = data['name']
    author = data['author']
    source = data['source']
    d = Download(name, author, url_id, source)
    is_ok = d.download()
    if is_ok:
        ret = {'state': 1}
    else:
        ret = {'state': 0}
    return jsonify(ret)


@app.route('/listening_test', methods=['POST'])
def listening_test():
    data = json.loads(request.get_data(as_text=True))
    url_id = data['url_id']
    name = data['name']
    author = data['author']
    source = data['source']
    d = Download(name, author, url_id, source)
    url = d.listening_test()
    ret = {'url': url}
    return jsonify(ret)


if __name__ == '__main__':
    app.debug = True  # 设置调试模式，生产模式的时候要关掉debug
    app.run(port=3000)
