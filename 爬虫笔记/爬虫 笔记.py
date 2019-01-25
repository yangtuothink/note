需求： 
	1. 爬取汽车之家新闻咨询
		- 什么都不带
	2. 爬抽屉新热榜
		- 带请求头
		- 带cookie
		- 登录：
			- 获取cookie
			- 登录：携带cookie做授权
			- 带cookie去访问
	3. 爬取GitHub
		- 带请求头
		- 带cookie
		- 请求体中：
			commit:Sign in
			utf8:✓
			authenticity_token:hmGj4oS9ryOrcwoxK83raFqKR4sFG1yC09NxnDJg3B/ycUvCNZFPs4AxTsd8yPbm1F3i38WlPHPcRGQtyR0mmw==
			login:asdfasdfasdf
			password:woshiniba8
	
	4. 登录拉勾网 
		- 密码加密
			- 找js，通过python实现加密方式
			- 找密文，密码<=>密文
		
		- Referer头， 上一次请求地址，可以用于做防盗链。
	
总结：
	请求头：
		user-agent
		referer
		host
		cookie
		特殊请起头，查看上一次请求获取内容。
			'X-Anit-Forge-Code':...
			'X-Anit-Forge-Token':...
	请求体：
		- 原始数据
		- 原始数据 + token
		- 密文
			- 找算法 
			- 使用密文

	套路：
		- post登录获取cookie，以后携带cookie 
		- get获取未授权cookie，post登录携带cookie去授权，以后携带cookie 

基础用法：

	requests
		- url
		- headers
		- cookies 
		- data 
		- json 
		- params 
		- proxy

	bs4 
		- find 		
		- find_all	
		- text 
		- attrs


- scrapy框架 
	介绍：大而全的爬虫组件。
	
	安装：
		- Win:
			下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
			
			pip3 install wheel 
			pip install Twisted‑18.4.0‑cp36‑cp36m‑win_amd64.whl
			
			pip3 install pywin32
			
			pip3 install scrapy 
		- Linux:
			pip3 install scrapy 


	使用：
		Django:
			# 创建project
			django-admin startproject mysite 
			
			cd mysite
			
			# 创建app
			python manage.py startapp app01 
			python manage.py startapp app02 
			
			# 启动项目
			python manage.runserver 
			
		Scrapy：
			# 创建project
			scrapy  startproject xdb 
			
			cd xdb 
			
			# 创建爬虫
			scrapy genspider chouti chouti.com 
			scrapy genspider cnblogs cnblogs.com 
			
			# 启动爬虫
			scrapy crawl chouti


目录结构
	项目名称
	   项目名称/
			- spiders				# 爬虫文件 
				- chouti.py 
				- cnblgos.py 
				....
			- items.py 				# 持久化
			- pipelines				# 持久化
			- middlewares.py		# 中间件
			- settings.py 			# 配置文件（爬虫）
	   scrapy.cfg

scrapy 
	命令：
		scrapy startproject xx 
		cd xx 
		scrapy genspider chouti chouti.com 
		
		scrapy crawl chouti --nolog 
	
	编写：
		def parse(self,response):
			# 1.响应
			# response封装了响应相关的所有数据：
				- response.text 
				- response.encoding
				- response.body 
				- response.request # 当前响应是由那个请求发起；请求中 封装（要访问的url，下载完成之后执行那个函数）
			# 2. 解析器 
			# // 子子孙孙 / 儿子 .// 当前往下找子子孙孙 
			# response.xpath('//div[@href="x1"]/a').extract_first()
			# response.xpath('//div[@href="x1"]/a').extract()
			# response.xpath('//div[@href="x1"]/a/text()').extract()
			# response.xpath('//div[@href="x1"]/a/@href').extract()
			# tag_list = response.xpath('//div[@href="x1"]/a')
			for tag in tag_list:
				tag.xpath('.//p/text()').extract_first()
				
			# 3. 再次发起请求
			# 回调函数 callback 可以在继续执行下一个函数 可以递归
			# from scrapy.http import Request
			# yield Request(url='xxxx',callback=self.parse) 
			
持久化相关：
	pipeline/items
		a. 先写pipeline类
			class XXXPipeline(object):
				def process_item(self, item, spider):
					return item
					
		b. 写Item类
			class XdbItem(scrapy.Item):
				href = scrapy.Field()
				title = scrapy.Field()
						
		c. 配置
			ITEM_PIPELINES = {
			   'xdb.pipelines.XdbPipeline': 300, # 优先级数值 0-1000 越小越优先执行 
			}
		
		d. 爬虫，yield每执行一次，process_item就调用一次。
			
			yield Item对象

	编写pipeline：
		"""
		源码执行顺序 ：
			1. 判断当前XdbPipeline类中是否有from_crawler
				有：
					obj = XdbPipeline.from_crawler(....)
				否：
					obj = XdbPipeline()
			2. obj.open_spider()
			
			3. obj.process_item()/obj.process_item()/obj.process_item()/obj.process_item()/obj.process_item()
			
			4. obj.close_spider()
		
		解析:
			如果不先执行 from_crawler 
			init 里面的 path 就获取不到值了
			先通过 from_crawler 将 path 获取到返回给 init 
			然后 init 才能争取的实例化对象 
		"""
		from scrapy.exceptions import DropItem

		class FilePipeline(object):

			def __init__(self,path):
				self.f = None
				self.path = path	
				# 写入文件的路径参数 ，放在 setting 中了。
				# 通过 from_crawler 来拿到 path 

			@classmethod
			def from_crawler(cls, crawler): 
				"""
				初始化时候，用于创建pipeline对象
				:param crawler:
				:return:
				"""
				print('File.from_crawler')
				path = crawler.settings.get('HREF_FILE_PATH') 
				return cls(path)

			def open_spider(self,spider):
				"""
				爬虫开始执行时，调用 
				用于 文件的打开
				:param spider:
				:return:
				"""
				# if spider.name == "chouti":  # spider参数 用于筛选个性化定制 
				print('File.open_spider')
				self.f = open(self.path,'a+')

			def process_item(self, item, spider):
				# f = open('xx.log','a+')
				# f.write(item['href']+'\n')
				# f.close() 
				# 这样写太low了，每次都要打开关闭文件
				# 因此选择 将 文件操作绕开每次循环。
				print('File',item['href'])
				self.f.write(item['href']+'\n')
				
				# return item  	# 交给下一个pipeline的process_item方法
				raise DropItem()# 后续的 pipeline的process_item方法不再执行

			def close_spider(self,spider):
				"""
				爬虫关闭时，被调用
				用于 文件的关闭 
				:param spider:
				:return:
				"""
				print('File.close_spider')
				self.f.close()


		注意：pipeline是所有爬虫公用，如果想要给某个爬虫定制需要使用spider参数自己进行处理。

去重相关
	系统自动的 去重规则在  scrapy.dupefilter.BaseDupeFilter，如果想自定义重写即可
	自定义去重规则
		from scrapy.dupefilter import BaseDupeFilter
		from scrapy.utils.request import request_fingerprint

		class XdbDupeFilter(BaseDupeFilter):

			def __init__(self):
				self.visited_fd = set()
				# 这里是放在本机内存里面了。也可以放在 redis 里面 

			@classmethod
			def from_settings(cls, settings):
				return cls()

			def request_seen(self, request):
				fd = request_fingerprint(request=request)	# 内置的去重规则在这里再次调用 
				if fd in self.visited_fd:
					return True # 表示已经看过了 
				self.visited_fd.add(fd)	# 未看过的观看后加入到集合中

			def open(self):  # can return deferred
				print('开始')

			def close(self, reason):  # can return a deferred
				print('结束')

			# def log(self, request, spider):  # log that a request has been filtered
			#     print('日志')

	配置 
		# 修改默认的去重规则
		# DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'
		DUPEFILTER_CLASS = 'xdb.dupefilters.XdbDupeFilter'


	爬虫使用：
		# dont_filter 控制是否遵循去重规则 为 False 才可以遵循 ，当然默认是 fales 因此scrapy 是自带去重的
		
		class ChoutiSpider(scrapy.Spider):
			name = 'chouti'
			allowed_domains = ['chouti.com']
			start_urls = ['https://dig.chouti.com/']

			def parse(self, response):
				print(response.request.url)
				
				page_list = response.xpath('//div[@id="dig_lcpage"]//a/@href').extract()
				for page in page_list:
					from scrapy.http import Request
					page = "https://dig.chouti.com" + page
					# yield Request(url=page,callback=self.parse,dont_filter=False) # https://dig.chouti.com/all/hot/recent/2
					yield Request(url=page,callback=self.parse,dont_filter=True) # https://dig.chouti.com/all/hot/recent/2
	
深度 
	爬取网页的时候会基于访问深度体现。比如基于分页，第二页的时候深度即为2
		
		response.meta.get("depth") 可以看到具体的深度 默认为 0 每次yield时，会根据原来请求中的depth + 1
	配置文件：
		# 限制深度
		DEPTH_LIMIT = 3

		# 优先级 
		# 请求被下载的优先级 -= 深度 * 配置 DEPTH_PRIORITY 
		DEPTH_PRIORITY = 1

cookie 
	方式一：
		- 携带 
			yield Request(
				url='https://dig.chouti.com/login',
				method='POST',
				body="phone=8613121758648&password=woshiniba&oneMonth=1",	# 必须要用 body 格式，如果不适应非要字典那就用 urlencode 转换
				# body=urlencode({})"phone=8615131255555&password=12sdf32sdf&oneMonth=1"
				# urlencode 需要导入 from urllib.parse import urlencode
				# urlencode 可以将字典格式 转换成 body 格式 
				cookies=self.cookie_dict,
				headers={
					'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
				},
				callback=self.check_login # 成功后的回调函数 
			)
			 
			def check_login(self,response):
				print(response.text)
				yield Request(...)
		
		- 解析：
				cookie_dict = {} # 最好写在全局。这样子大家都可以拿
				cookie_jar = CookieJar() # 先实例化 
				cookie_jar.extract_cookies(response, response.request)	# 传入参数，将请求的和响应的 cookie 都拿到 

				# 去对象中将cookie解析到字典
				for k, v in cookie_jar._cookies.items():
					for i, j in v.items():
						for m, n in j.items():
							cookie_dict[m] = n.value
	方式二：meta
	
start_urls
	- 内部原理：
			"""
			scrapy引擎来爬虫中取起始URL：
				1. 调用start_requests并获取返回值
				2. v = iter(返回值)
				3. 
					req1 = 执行 v.__next__()
					req2 = 执行 v.__next__()
					req3 = 执行 v.__next__()
					...
				4. req全部放到调度器中
			"""
	- 编写
		class ChoutiSpider(scrapy.Spider):
			name = 'chouti'
			allowed_domains = ['chouti.com']
			start_urls = ['https://dig.chouti.com/']
			cookie_dict = {}
			
			def start_requests(self):
				# 方式一：
				for url in self.start_urls:
					yield Request(
						url=url,
						callback=self.parse,
						method='POST' 	# 自己写的优先级更高。因此在这里可以指定 post 请求也可以作为起始了
						)	
				# 方式二：
				# req_list = []
				# for url in self.start_urls:
				#     req_list.append(Request(url=url))
				# return req_list
	- 定制：可以去redis中获取


















		