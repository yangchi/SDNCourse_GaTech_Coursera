'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Joshua Reich (jreich@cs.princeton.edu)                               #
################################################################################
# Licensed to the Pyretic Project by one or more contributors. See the         #
# NOTICES file distributed with this work for additional information           #
# regarding copyright and ownership. The Pyretic Project licenses this         #
# file to you under the following license.                                     #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided the following conditions are met:       #
# - Redistributions of source code must retain the above copyright             #
#   notice, this list of conditions and the following disclaimer.              #
# - Redistributions in binary form must reproduce the above copyright          #
#   notice, this list of conditions and the following disclaimer in            #
#   the documentation or other materials provided with the distribution.       #
# - The names of the copyright holds and contributors may not be used to       #
#   endorse or promote products derived from this work without specific        #
#   prior written permission.                                                  #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT    #
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the     #
# LICENSE file distributed with this work for specific language governing      #
# permissions and limitations under the License.                               #
################################################################################


################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import learn

from resonance_policy import *
from resonance_states import *
from resonance_handlers import EventListener
from multiprocessing import Process, Queue
import threading

DEBUG = True

""" Dynamic resonance policy """
def resonance(self):

  # updating policy
  def update_policy(pkt=None):
    self.policy = self.lbPolicy.default_policy()
    if DEBUG is True:
      print self.policy
  self.update_policy = update_policy

  # Listen for state transitions.
  def transition_signal_catcher(queue):
    while 1:
      try:  
        line = queue.get_nowait() # or q.get(timeout=.1)
      except:
        continue
      else: # Got line. 
        self.update_policy()

  def initialize():

    # Create queue for receiving state transition notification
    queue = Queue()

    # Create a load balancing Finite State Machine 
    self.LBFSM = LBStateMachine()

    # Initialize policies
    self.lbPolicy = LBPolicy(self.LBFSM)

    # Spawn an EventListener, which listens for events and keeps track of 
    # the state of each host.
    # default is:
    
    self.eventListener = EventListener(self.LBFSM)
    self.eventListener.start(queue)

    # Create a daemon thread to track the state transitions
    t = threading.Thread(target=transition_signal_catcher, args=(queue,))
    t.daemon = True
    t.start()

    # Set a default policy
    self.update_policy()

  initialize()


""" Main Method """
def main():
  return dynamic(resonance)() >> dynamic(learn)()
