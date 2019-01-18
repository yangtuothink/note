	
# 启动流程 

# 启动入口简约版代码  
from werkzeug.wrappers import Response
from werkzeug.serving import run_simple

class Flask(object):
	def __call__(self,environ, start_response):
		response = Response('hello')
		return response(environ, start_response)

	def run(self):
		run_simple('127.0.0.1', 8000, self)




from flask import Flask 

"""
1 实例化对象 app 
""" 
app = Flask(__name__)

"""
2 设置路由
	将路由关系放在 app.url_map = {} 中
"""
@app.route("/index")
def index():
	return "index"

if —__name__ == "__main__":
"""
3 启动socket服务端 
"""
	app.run()

"""
4 用户请求到来就会执行 __call__ 方法 
"""




"""
run_simple(host,port,self,**options) 
	会对第三个传入的参数加()进行执行
	第三个参数如果是对象就执行其 __call__ 方法
"""

	
def __call__(self,environ, start_response):
	# environ 请求相关的所有数据 第一手的数据，由wsgi进行的初步封装
	# start_response 用于设置响应相关数据 
	return wsgi_app(environ,start_response)

def wsgi_app(environ,start_response):

	ctx = self.request_context(environ) 
		"""
		def request_context(...)
			return RequestContext(self, environ)

		RequestContext()
			def __init__(...)
				...
				request = app.request_class(environ)
				self.request = request	# 创建 request
				self.session = None	# 创建 session 

		request_class = Request  
		"""
	...
	ctx.push() 
		"""
		def push(...):
			_request_ctx_stack.push(self) 	# 放空调 
			self.session = session_interface.open_session() # 取写 session 

		def open_session(...):
			val = request.cookies.get(app.session_cookie_name)	# 通过配置文件的session_cookie_name来取
			
		"""
		
	response = self.full_dispatch_request()
		"""
		def full_dispatch_request(self): 
			rv = self.dispatch_request() # 调用视图函数 
			return self.finalize_request(rv) # 进行善后工作 


		def finalize_request(...):
			response = self.process_response(response)

		def process_response(...):
			self.session_interface.save_session(....) 
			

		def save_session(...):
			val = self.get_sighing_serializer(app).dumps(dict(session))
			response.set_cookie( # 写入cookie 
			...
			val 
			)
		"""









"""
以上就是所有的Flack 的源码流程 
"""

__call__() -> 对 environ 第一次封装 
wsgi_app () ->  
	request_context() ->  environ第二次封装 ，具体实现 ： 封装了 request 以及 session（空的）
		RequestContext() -> init 初始化  1.通过 request_class 创建了 Request 对象 2 .创建空的 self.session
			request_class() ->  创建 Request 对象具体操作实现 
	push -> 1. 将 ctx 放空调上 2. 执行 open_session 将self.session 重新赋值
		open_session -->通过配置文件的 配置名字 取到 session 然后解密反序列化生成字典重新赋值 ctx.session 的具体操作实现
	full_dispatch_request --> 1.调用执行视图函数  2.善后工作 
		dispatch_request--> 调用执行视图函数具体操作 
			finalize_request--> 善后工作具体操作
				process_response-->
					save_session-->	写入cookie的具体操作  


 上下文管理（第一次）
		请求到来时候：
			# ctx = RequestContext(self, environ) # self是app对象，environ请求相关的原始数据
			# ctx.request = Request(environ)
			# ctx.session = None
			
			# 将包含了request/session的ctx对象放到“空调”
				{
					1232：{ctx:ctx对象}
					1231：{ctx:ctx对象}
					1211：{ctx:ctx对象}
					1111：{ctx:ctx对象}
					1261：{ctx:ctx对象}
				}
				
		视图函数：
			from flask import reuqest,session 
			
			request.method 
			
			
		请求结束：
			根据当前线程的唯一标记，将“空调”上的数据移除。


		










































	