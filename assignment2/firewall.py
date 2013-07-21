'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 4 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        with open(policyFile) as f:
            for lines in f:
                id, mac1, mac2 = lines.split(',')
                if id != 'id':
                    for i in range(2):
                        fm = of.ofp_flow_mod(#action = of.ofp_action_output(port = of.OFPP_NONE), 
                                             priority = 1000)
                        if i == 0:
                            fm.match.dl_src = EthAddr(mac1)
                            fm.match.dl_dst = EthAddr(mac2)
                        else:
                            fm.match.dl_src = EthAddr(mac2)
                            fm.match.dl_dst = EthAddr(mac1)
                        event.connection.send(fm)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
