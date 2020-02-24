import requests
import os


class Download:
    def __init__(self, name, author, url):
        self.name = name
        self.author = author
        self.url = url
        self.content = None

    def dowmload(self):
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
        # 将mp3的二进制数据保存到本地的mp3

    def save(self, path=r'F:\download'):
        if (not os.path.exists(path)):
            os.makedirs(path)
        path_url = r'%s\%s,%s.mp3' % (path, self.name, self.author)
        print(path_url)
        f = open(path_url, "wb")
        f.write(self.content)
        f.close()
