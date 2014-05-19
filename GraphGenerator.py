import random
import json
from YenKSP.graph import DiGraph

# class for generating a random graph, as per Jellyfish algorithm
class GraphGenerator:
  def __init__(self, numNodes, edgesPerNode):
    self.numNodes = numNodes
    self.edgesPerNode = edgesPerNode
    self.open = [] # nodes that still have open links
    self.closed = [] # nodes that have no open links
    self.graph = DiGraph("jesse")
    for i in range(numNodes):
      self.graph.add_node(i)
      self.open.append(i)

  # move nodes around open, closed if necessary
  def relocateNodes(self, nodes):
    for node in nodes:
      if self.graph.num_edges(node) < self.edgesPerNode and node in self.closed:
        self.closed.remove(node)
        self.open.append(node)
      elif (not self.graph.num_edges(node) < self.edgesPerNode) and node in self.open:
        self.open.remove(node)
        self.closed.append(node)

  # find a pair of unlinked nodes and link them
  def linkNodes(self):
    random.shuffle(self.open)
    for a in self.open:
      for b in self.open:
        if (not a is b) and (not self.graph.has_edge(a, b)):
          self.graph.add_edge(a, b, 1)
          self.graph.add_edge(b, a, 1)
          self.relocateNodes([a, b])
          return True
    return False

  # find a pair of linked nodes and unlink them
  # link is selected uniformly at random from existing links
  def unlinkNodes(self):
    removeNum = random.randint(0, self.graph.num_total_edges() - 1)
    for node in self.open + self.closed:
      if self.graph.num_edges(node) > removeNum:
        other = self.graph.get_nth_edge(node, removeNum)
        self.graph.delete_edge(node, other)
        self.graph.delete_edge(other, node)
        self.relocateNodes([node, other])
        return
      removeNum -= self.graph.num_edges(node)

  # generates the graph, so that export() can be called next
  def generate(self):
    while len(self.open) > 0:
      while self.linkNodes():
        pass
      if len(self.open) > 0:
        self.unlinkNodes()

  # write JSON representing graph to file
  def export(self, fileName):
    dump = {}
    for node in self.closed:
      linkedWeights = {}
      for linkedTo in node.linkedNodes:
        linkedWeights[linkedTo.id] = 1
      dump[node.id] = linkedWeights
    f = open(fileName, "w")
    f.write(json.dumps(dump))
    f.close()