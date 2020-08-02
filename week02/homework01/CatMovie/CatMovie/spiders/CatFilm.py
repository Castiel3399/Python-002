import scrapy
from scrapy.selector import Selector

from CatMovie.items import CatmovieItem


class DoubanSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    # 起始URL列表
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        # for i in range(0, 10):

        url = f'https://maoyan.com/films?showType=3&offset=30'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)
        # url 请求访问的网址
        # callback 回调函数，引擎回将下载好的页面(Response对象)发给该方法，执行数据解析
        # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数

    def parse(self, response):
        # 打印网页的url
        print(response.url)
        # 打印网页的内容
        # print(response.text)

        # soup = BeautifulSoup(response.text, 'html.parser')
        # title_list = soup.find_all('div', attrs={'class': 'hd'})
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        item = CatmovieItem()
        for movie in movies:
            #     title = i.find('a').find('span',).text
            #     link = i.find('a').get('href')
            # 路径使用 / .  .. 不同的含义　

            title = movie.xpath('./div[@class="movie-hover-title"]/span/text()')
            kind = movie.xpath('./div[@class="movie-hover-title"]/text()')
            time = movie.xpath('./div[@class="movie-hover-title movie-hover-brief"]/text()')
            item['title'] = title[0].extract().strip()
            item['kind'] = kind[4].extract().strip()
            item['time'] = time[1].extract().strip()
            yield item
