"""
Este archivo ejemplifica la creacion de una topologia de mininet
En este caso estamos creando una topologia de fat tree
"""

from mininet.topo import Topo

class FatTree( Topo ):
  def __init__( self, half_ports = 2, **opts ):
    Topo.__init__(self, **opts)

    switches_by_level = self.create_tree(half_ports)
    self.initialize_root_hosts(switches_by_level)
    self.initialize_leaf_hosts(switches_by_level)

  def create_tree(self, half_ports):
    switches_by_level = []
    counter = 1
    for level in range (0, half_ports):
      switches_amount = 2 ** level
      switches = []
      for switch in range (0, switches_amount):
        switch = self.addSwitch('sw{}'.format(str(counter)))
        switches.append(switch)
        counter += 1
        if level > 0:
          parent_switches = switches_by_level[level - 1]
          for parent_switch in parent_switches:
            self.addLink(parent_switch, switch)
      switches_by_level.append(switches)
    return switches_by_level

  def initialize_root_hosts(self, switches_by_level):
    root_switch = switches_by_level[0][0]
    h1 = self.addHost('h1')
    h2 = self.addHost('h2')
    h3 = self.addHost('h3')
    self.addLink(root_switch, h1)
    self.addLink(root_switch, h2)
    self.addLink(root_switch, h3)

  def initialize_leaf_hosts(self, switches_by_level):
    leaf_switches = switches_by_level[-1]
    host_id = 4
    for leaf in leaf_switches:
      host = self.addHost('h{}'.format(host_id))
      self.addLink(leaf, host)
      host_id += 1

topos = { 'fat-tree': FatTree }
