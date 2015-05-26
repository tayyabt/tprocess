import sys
from threading  import Thread
import re
import subprocess
import time
import ctypes
import logging

try:
	from Queue import Queue, Empty
except ImportError:
	from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

logging.basicConfig()  
LOG = logging.getLogger("TPROCESS")
LOG.setLevel("INFO")

def terminate_thread(thread):
	"""Terminates a python thread from another thread.

	:param thread: a threading.Thread instance
	"""
	if not thread.isAlive():
		LOG.info("The thread isn't alive")
		return False

	exc = ctypes.py_object(SystemExit)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
		ctypes.c_long(thread.ident), exc)
	LOG.info("this is the result %d " % res)
	if res == 0:
		raise ValueError("nonexistent thread id")
	elif res > 1:
		# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
		raise SystemError("PyThreadState_SetAsyncExc failed")
	return True


class tprocess:
	def __init__(self, command, encoding='utf-8'):
		self.proc = None
		self.encoding = encoding
		self.before = None
		self.command = command
		self.proc = subprocess.Popen( self.command , stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1, close_fds=ON_POSIX, shell=True )

	def expect( self, exp, timeout=None ):
		self.timedout_occured = False
		self.exp_index = 0
		self.before = ''
		t = Thread(target=self.get_output, args=(exp, ))
		t.daemon = True

		# if timeout:
		# 	t_timeout = Thread(target=self.timeout_method, args=(timeout, t ))
		# 	t_timeout.start()

		t.start()
		t.join()
		# if self.timedout_occured:
		# 	raise Exception("Operation timed out")
		return self.exp_index

	def get_output( self, exp ):
		start_time = None
		while True:
			ch = self.proc.stdout.read(1)
			if start_time == None:
				start_time = time.time() 
			ch = ch.decode(self.encoding)
			self.before = self.before + ch
			m = re.search( exp, self.before )
			if m:
				self.exp_index = m.start()
				self.before = re.sub( exp, '', self.before )
				#LOG.info("Took: %0.2f" % (time.time() - start_time) ) 
				break
	def timeout_method(self, timeout, th):
		try:
			time.sleep(timeout)
			LOG.info("Just got up from sleep, will try to kill the thread now")
		except Exception as e:
			a = 0
			return None
		try:
			LOG.info("This is the thread i am trying to kill %s", th)
			if terminate_thread(th):
		 		self.timedout_occured = True
			else:
		 		LOG.info("Thread already dead...")
		except Exception as e:
		 	a = ''
		
	
	def sendline(self, text):
		return self.send(text+"\n")

	def send(self, text):
		text_bytes = text.encode(self.encoding)
		c = self.proc.stdin.write( text_bytes )
		self.proc.stdin.flush()
		return c

	def __del__(self):
		if 'proc' in dir(self):
			#LOG.info("Terminating process")
			self.proc.terminate()


# p = '/Users/Apple/Documents/datascription/stanford-corenlp-full-2015-01-30/'
# import os
# os.chdir(p)
# c = 'java -cp "*" -Xmx8g edu.stanford.nlp.sentiment.SentimentPipeline -stdin'


# tp = tprocess(c)
# x = 'abcd '*5000
# x = x + " yadayada"
# tp.sendline(x)
# tp.expect("\(0 yadayada", timeout=0.1)