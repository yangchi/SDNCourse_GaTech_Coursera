'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
import json
from multiprocessing import Process, Manager

DEBUG = True

EVENT_TYPE_LB = 0

class ResonanceStateMachine():

    def __init__(self):
        manager = Manager()
        self.flow_state_map = manager.dict()
        self.flow_state_map.clear()
        return

    def transition_callback(self, cb, arg):
        self.cb = cb
        self.cbarg = arg

    def parse_json(self, msg):
        json_msg = json.loads(msg)

        event_msg = json_msg['event']
        state = event_msg['data']

        msgtype = event_msg['event_type']
        host  = state['data']
        next_state = state['value']

        return (msgtype, host, next_state)

    def handleMessage(self, msg, queue):

        msgtype, host, next_state = self.parse_json(msg)

        if DEBUG == True:
            print "HANDLE", next_state, host

        # In the parent class, we just do the transition.
        # We don't type check the message type
        self.state_transition(next_state, host, queue)


    def check_state(self, host):

        host_str = str(host)

        if self.flow_state_map.has_key(host_str):
            state = self.flow_state_map[host_str]
        else:
            state = 'default'

        if DEBUG == True:
            print "check_state", host_str, state

        return state

    def get_hosts_in_state(self, state):

        hosts = []

        for host in self.flow_state_map.keys():
            if (self.flow_state_map[host] == state):
                hosts.append(host)

        return hosts


    def state_transition(self, next_state, host, queue, previous_state=None):

        state = self.check_state(host)
        if previous_state is not None:
            if state != previous_state:
                print 'Given previous state is incorrect! Do nothing.'
                return
        else:
            print "state_transition ->", str(host), next_state
            queue.put('transition')
            self.flow_state_map[str(host)] = next_state
            if DEBUG == True:
                print "CURRENT STATES: ", self.flow_state_map

# --------- Update the code below ------------

class LBStateMachine(ResonanceStateMachine):

    def handleMessage(self, msg, queue):

        print "In the handleMsg function"
        msgtype, host, next_state = self.parse_json(msg)

        # Add the state transition logic
        # hint: use the state_transition function
        if msgtype == EVENT_TYPE_LB:
            self.state_transition(next_state, host, queue)
        else:
            pass


    def get_portA_hosts(self):
        print "In the get_portA_hosts fun"
        return self.get_hosts_in_state('portA')

    def get_portB_hosts(self):
        print "In the get_postB_hosts fun"
        return self.get_hosts_in_state('portB')
