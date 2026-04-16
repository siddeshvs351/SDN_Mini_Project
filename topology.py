from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.link import TCLink

class MyTopo(Topo):
    def build(self):
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add switch
        s1 = self.addSwitch('s1')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

if __name__ == '__main__':
    topo = MyTopo()
    net = Mininet(topo=topo, controller=None, link=TCLink)

    # Add remote controller
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    net.start()
    CLI(net)
    net.stop()