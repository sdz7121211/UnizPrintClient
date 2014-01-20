# -*- coding: utf-8 -*-  
from distutils.core import setup
import py2exe

setup(
#    options = {  
#
#      "py2exe": {  
#
#        "dll_excludes": ["MSVCP90.dll"],
#		"includes":["sip","ctypes", "logging"],
##		"excludes": ["OpenGL"],
##		'bundle_files':1,
#
#      }  
#	  		
#	  }
#	  , 

windows=['OneClickPrint.py']
#console=['OneClickPrint.py']
)