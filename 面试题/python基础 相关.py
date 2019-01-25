如何变成迭代器？
	"""
	li = [11,22,33]
		
	iter(li)	
	"""
	
生成器怎么变成迭代器 ？
	"""
	def func():
		yield 11
		yield 22
		yield 33
	
	li = func()
	
	iter(li)	
	"""
