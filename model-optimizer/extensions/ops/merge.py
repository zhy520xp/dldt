"""
 Copyright (c) 2018 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import networkx as nx

from mo.graph.graph import Node
from mo.ops.op import Op


class Merge(Op):
    op = 'Merge'

    def __init__(self, graph: nx.MultiDiGraph, attrs: dict):
        mandatory_props = {
            'type': __class__.op,
            'op': __class__.op,
            'infer': Merge.merge_infer
        }
        super().__init__(graph, mandatory_props, attrs)

    @staticmethod
    def merge_infer(node: Node):
        # we infer only through executable input nodes
        in_executables = [n for n in node.in_nodes().values() if n.has_and_set('executable') and n.executable]
        assert len(in_executables) == 1
        tensor = in_executables[0]
        node.out_node().shape = tensor.shape
        node.out_node().value = tensor.value
