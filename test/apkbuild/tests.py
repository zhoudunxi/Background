# -*- coding: utf-8 -*-
from django.test import TestCase
import time, os, sys

class TestMain():
	def testrun(self,run_user, version, *lists):
		tmp_userpath = sys.path[0] + os.sep + 'runtime' + os.sep + run_user.encode('utf-8')
		if not os.path.isdir(tmp_userpath):
			os.mkdir(tmp_userpath)
		print ('\033[32mBegin....username:%s..version:%s..\033[0m' %(run_user,version )) 
		print lists
		time.sleep(30)
		
		print ('\033[32m---time Done....!!!-------------\033[0m')
		os.rmdir(tmp_userpath)
