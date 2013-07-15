'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.util import irange

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # Add your logic here ...

        chooser = lambda dict, para, default: para in dict and dict[para] or default
        #add core switch:
        core_switch = self.addSwitch('c1')
        #add agg switch
        for i in irange(1, fanout):
            agg_switch = self.addSwitch('a%s'%i)
            loss = chooser(linkopts1, 'loss', 1)
            max_queue_size = chooser(linkopts1, 'max_queue_size', 1000)
            use_htb = chooser(linkopts1, 'use_htb', True)
            self.addLink(core_switch, agg_switch, bw=linkopts1['bw'], delay=linkopts1['delay'], loss=loss, max_queue_size=max_queue_size, use_htb=use_htb)
            #add edge switches
            for j in irange(1, fanout):
                edge_switch = self.addSwitch('e%s'%((i-1)*fanout+j))
                loss = chooser(linkopts2, 'loss', 1)
                max_queue_size = chooser(linkopts2, 'max_queue_size', 1000)
                use_htb = chooser(linkopts2, 'use_htb', True)
                self.addLink(agg_switch, edge_switch, bw=linkopts2['bw'], delay=linkopts2['delay'], loss=loss, max_queue_size=max_queue_size, use_htb=use_htb)
                #add hosts:
                for k in irange(1, fanout):
                    host = self.addHost('h%s'%(((i-1)*fanout+j-1)*fanout+k))
                    loss = chooser(linkopts3, 'loss', 1)
                    max_queue_size = chooser(linkopts3, 'max_queue_size', 1000)
                    use_htb = chooser(linkopts3, 'use_htb', True)
                    self.addLink(edge_switch, host, bw=linkopts3['bw'], delay=linkopts3['delay'], loss=loss, max_queue_size=max_queue_size, use_htb=use_htb)



topos = { 'custom': ( lambda: CustomTopo() ) }
