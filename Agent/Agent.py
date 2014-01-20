'''
Created on 2014-1-18

@author: sdz
'''

from PyQt4 import QtCore

class Agent(QtCore.QObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(Agent, self).__init__()    
    
    def noticeToReceiver(self, signal, receiver):
        
        signal.connect(receiver)
        
        
        
        