import time
from threading import Thread, Lock, BoundedSemaphore
import requests

from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.app import App

class ThreadCall(Thread,EventDispatcher):
	def __init__(self,target, args=(), kwargs={}):
		Thread.__init__(self)
		EventDispatcher.__init__(self)
		self.register_event_type('on_result')
		self.register_event_type('on_error')
		self.rez = None
		self.daemon = False
		self.target = target
		self.args = args
		self.timing = None
		self.kwargs = kwargs
	
	def start(self):
		Thread.start(self)
		self.timing = Clock.schedule_once(self.checkStop,0)

	def run(self):
		try:
			self.rez = self.target(*self.args,**self.kwargs)
			self.dispatch('on_result',self.rez)
		except Exception as e:
			self.dispatch('on_error',e)

	def on_result(self, v):
		pass
		print('on_result dispatched',v)

	def on_error(self,e):
		print('ThreadCall() on_error',e)

	def checkStop(self,timestamp):
		x = self.join(timeout=0.0001)
		if self.is_alive():
			self.timing = Clock.schedule_once(self.checkStop,0)
			return

class Workers(Thread):
	def __init__(self,maxworkers):
		super().__init__()
		self.max_workers = maxworkers
		self.tasks = []
		# task = [callee,callback,kwargs]
		self.lock = Lock()
		self.work_sema = BoundedSemaphore(value=self.max_workers)
		self.running = False
	def run(self):
		self.running = True
		print('Working running ..........')
		while self.running:
			if len(self.tasks) == 0:
				time.sleep(0.001)
				continue
			task = None
			with self.lock:
				task = self.tasks.pop()
			if task is None:
				continue
			with self.work_sema:
				callee,callback,kwargs = task
				x = ThreadCall(callee,kwargs=kwargs)
				x.bind(on_result=callback)
				x.start()

	def add(self,callee,callback,kwargs={}):
		with self.lock:
			self.tasks.insert(0,[callee,callback,kwargs])

class HttpClient:
	def __init__(self):
		self.s = requests.Session()
		self.workers = App.get_running_app().workers
		
	def webcall(self,url,method="GET",params={},headers={}):
		req = requests.Request(method,url,data=params,headers=headers)
		prepped = self.s.prepare_request(req)
		resp = self.s.send(prepped)
		if resp.status_code == 200:
			try:
				data = resp.json()
				if type(data) != type({}):
					return data
				status = data.get('status',None)
				if status is None:
					return data
				if status == 'OK':
					return data['data']
				return data
			except:
				return resp.text
		print('Error', url, method, params, resp.status_code,type(resp.status_code))
		raise Exception('error')
		
	def __call__(self,url,method="GET",params={},headers={},callback=None):
		def cb(t,resp):
			return resp

		if callback is None:
			resp = self.webcall(url, method=method,
					params=params, headers=headers)
			return cb(None,resp)

		kwargs = {
			"url":url,
			"method":method,
			"params":params,
			"headers":headers
		}
		self.workers.add(self.webcall,callback,kwargs=kwargs)

	def get(self, url, params={}, headers={}, callback=None):
		return self.__call__(url,method='GET',params=params,
				headers=headers, callback=callback)
	def post(self, url, params={}, headers={}, callback=None):
		return self.__call__(url,method='POST',params=params,
				headers=headers, callback=callback)

	def put(self, url, params={}, headers={}, callback=None):
		return self.__call__(url,method='PUT',params=params,
				headers=headers, callback=callback)

	def delete(self, url, params={}, headers={}, callback=None):
		return self.__call__(url,method='DELETE',params=params,
				headers=headers, callback=callback)

	def option(self, url, params={}, headers={}, callback=None):
		return self.__call__(url,method='OPTION',params=params,
				headers=headers, callback=callback)
	
if __name__ == '__main__':
	from kivy.uix.textinput import TextInput
	from kivy.app import App
	from kivy.uix.boxlayout import BoxLayout
	from kivy.uix.button import Button
	class MyApp(App):
		def build(self):
			self.hc = HttpClient()
			x = BoxLayout(orientation='vertical')
			y = BoxLayout(orientation='horizontal',size_hint_y=0.07)
			self.ti = TextInput(size_hint_x=0.95,multiline=False)
			btn = Button(size_hint_x=0.05,text='go')
			y.add_widget(self.ti)
			y.add_widget(btn)
			btn.bind(on_press=self.getHtml)
			self.texti = TextInput(multiline=True,readonly=True)
			x.add_widget(y)
			x.add_widget(self.texti)
			
			return x
	
		def getHtml(self,v=None):
			url = self.ti.text
			self.hc.get(url,callback=self.showResult)
			self.texti.text = 'loading...'

		def showResult(self,target,resp):
			if resp.status_code==200:
				self.texti.text = resp.text
			else:
				print(reps.status_code,'...............')
	MyApp().run()
