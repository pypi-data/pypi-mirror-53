import pytest
import numpy as np
import pandas as pd
from sonata.circuit import File
from sonata.circuit.population import NodePopulation
from sonata.circuit.types_table import NodeTypesTable

"""
def net():
    return File(data_files=['examples/v1_nodes.h5', 'examples/lgn_nodes.h5', 'examples/v1_v1_edges.h5'],
                data_type_files=['examples/lgn_node_types.csv', 'examples/v1_node_types.csv',
                                 'examples/v1_v1_edge_types.csv'],
                gid_table='examples/gid_table.h5')


nodes = net().nodes
v1_nodes = nodes['v1']
v1_nodes[0]
exit()
"""


class MockGroup(pd.DataFrame):
    pass

node_types_table_df = pd.DataFrame({
    'node_type_id': 100,
    'attr1': [1],
    'attr2': [20.0],
    'attr3': 'bio'
})#.set_index('node_type_id')


class MockHDF5File(object):

    def __init__(self):
        self.df = pd.DataFrame({
            'node_id': np.arange(101),
            'node_type_id': 100,
            'node_group_id': 0,
            'node_group_index': np.arange(101)
        })

    def items(self):
        return [(u'0', pd.DataFrame({'x': np.linspace(5.0, 100.0, 101), 'y': np.linspace(-50.0, 5.0, 101)}))]


    def __getitem__(self, item):
        return self.df[item]

"""
types_table = NodeTypesTable()
types_table.add_table(node_types_table_df)
nodes_h5 = MockHDF5File()
pop = NodePopulation('mypop', pop_group=nodes_h5, node_types_tables=types_table)
print(len(pop))
print(pop.name)
print(pop[6])
print(pop.get_node_id(6))
print(list(pop.filter(attr2=20.0)))
"""