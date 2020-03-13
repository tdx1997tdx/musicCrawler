import requests, json


class Music:
    def __init__(self, name, author, url_id, source):
        self.name = name
        self.author = author
        self.priority = 0
        self.url_id = url_id
        self.source = source

    def __str__(self):
        return '{name:%s,author:%s,url:%s}' % (self.name, self.author, self.url_id)


class Container:
    def __init__(self, name, author):
        self.name = name
        self.author = author
        self.container = []

    def get_music(self):
        sources = ['netease', 'tencent', 'xiami', 'kugou', 'baidu']
        url = 'http://music.lkxin.cn/api.php'
        headers = self.get_header()
        for i in sources:
            data = {}
            data['types'] = 'search'
            data['count'] = '12'
            data['source'] = i
            data['pages'] = '1'
            data['name'] = '%s%s' % (self.name, self.author)
            request = requests.post(url, headers=headers, data=data)
            data = json.loads(request.text)
            for key, value in enumerate(data):
                if self.name not in value.get('name'):
                    continue
                author = ','.join(value.get('artist'))
                m = Music(value.get('name'), author, value.get('url_id'), value.get('source'))
                self.container.append(m)
                m.priority = key
                if self.author not in author:
                    m.priority += 2
        self.container.sort(key=lambda x: x.priority)
        return self.serialize(self.container)

    def get_header(self):
        headers = {}
        headers[
            'Accept'] = 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
        headers['Cache-Control'] = 'max-age=0'
        headers['Connection'] = 'keep-alive'
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36'
        return headers

    def serialize(self, music_list):
        res = []
        for i in music_list:
            res.append(i.__dict__)
        return res
