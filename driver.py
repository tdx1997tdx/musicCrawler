from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

types = ['netease', 'qq', 'kugou', 'kuwo', 'xiami', 'baidu', '1ting', 'migu', 'lizhi', 'qingting', 'ximalaya', 'kg']


class Music:
    def __init__(self, name, author, url):
        self.name = name
        self.author = author
        self.url = url
        self.priority = 0

    def set_priority(self, real_name, real_author):
        if real_name in self.name:
            self.priority += 2
        if real_author in self.author:
            self.priority += 1

    def __str__(self):
        return '{name:%s,author:%s,url:%s}' % (self.name, self.author, self.url)


class MusicDriver:
    def __init__(self, input_name, input_author, chrome_driver=r".\chromedriver.exe"):
        self.driver = webdriver.Chrome(executable_path=chrome_driver)
        self.input_name = input_name
        self.input_author = input_author

    def open_url(self, type):
        # 打开页面
        url = 'https://www.769sc.com/?name=%s&type=%s' % (self.input_name + self.input_author, type)
        self.driver.get(url)
        # self.driver.implicitly_wait(5)
        self.wait(5)

    def wait(self, wait_time):
        start = time.time()
        while True:
            try:
                elem = self.driver.find_element_by_css_selector("[class='am-alert am-alert-danger am-animation-shake']")
                if (elem.get_attribute('style') == 'display: block;'):
                    break
                if (self.driver.find_elements_by_css_selector('.aplayer-list ol li')):
                    break
                if (time.time() - start > wait_time):
                    break
            except Exception as e:
                continue

    def click(self, elem):
        action = ActionChains(self.driver)
        action.click(elem)
        action.perform()

    # 输入一个li元素，输出一个Music类
    def create_music(self, li_elem):
        name = li_elem.find_element_by_class_name('aplayer-list-title').get_attribute("innerHTML")
        author = li_elem.find_element_by_class_name('aplayer-list-author').get_attribute("innerHTML")
        self.click(li_elem)
        url = self.driver.find_element_by_id('j-src-btn').get_attribute('href')
        m = Music(name, author, url)
        m.set_priority(self.input_name, self.input_author)
        return m

    def get_music_list(self):
        liList = self.driver.find_elements_by_css_selector('.aplayer-list ol li')
        music_list = []
        for i in liList:
            m = self.create_music(i)
            if (m.priority != 0):
                music_list.append(m)
                print(m)
        return music_list

    def get_all_music(self):
        all_music = []
        for i in types:
            self.open_url(i)
            music_list = self.get_music_list()
            all_music.extend(music_list)
        all_music.sort(key=lambda x: x.priority, reverse=True)
        return self.serialize(all_music)

    def close(self):
        self.driver.quit()

    def serialize(self,music_list):
        res=[]
        for i in music_list:
            res.append(i.__dict__)
        return res
