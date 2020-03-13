import requests, json
import os


class Download:
    def __init__(self, name, author, url_id, source):
        self.name = name
        self.author = author
        self.url_id = url_id
        self.source = source
        self.url = ''
        self.content = None
        self.download_path = r'F:\download'

    def get_url(self):
        url = 'http://music.lkxin.cn/api.php'
        headers = {}
        headers[
            'Accept'] = 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
        headers['Connection'] = 'keep-alive'
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36'
        data = {}
        data['types'] = 'url'
        data['id'] = self.url_id
        data['source'] = self.source
        request = requests.post(url, headers=headers, data=data)
        print(json.loads(request.text))
        self.url = json.loads(request.text).get('url')

    def get_raw_data(self):
        headers = {}
        headers[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        headers['Accept-Encoding'] = 'gzip, deflate'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
        headers['Cache-Control'] = 'max-age=0'
        headers['Connection'] = 'keep-alive'
        headers[
            'User-Agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36'
        request = requests.get(self.url, headers=headers)
        self.content = request.content  # mp3二进制数据

    def save(self):
        if (not os.path.exists(self.download_path)):
            os.makedirs(self.download_path)
        path_url = r'%s\%s,%s.mp3' % (self.download_path, self.name, self.author)
        f = open(path_url, "wb")
        f.write(self.content)
        f.close()
        return path_url

    def open_focus(self, url):
        os.system('start %s' % (self.download_path))

    def download(self):
        self.get_url()
        if (self.url == ''):
            return False
        self.get_raw_data()
        url = self.save()
        self.open_focus(url)
        return True

    def listening_test(self):
        self.get_url()
        return self.url
