#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

import numpy as np

from kglib.utils.graph.iterate import multidigraph_data_iterator, multidigraph_node_data_iterator, \
    multidigraph_edge_data_iterator


def encode_types(graph, node_types, edge_types):
    node_iterator = multidigraph_node_data_iterator(graph)
    encode_categorically(node_iterator, node_types, 'type', 'categorical_type')

    edge_iterator = multidigraph_edge_data_iterator(graph)
    encode_categorically(edge_iterator, edge_types, 'type', 'categorical_type')
    return graph


def create_input_graph(graph, features_field="features"):
    input_graph = graph.copy()
    augment_data_fields(multidigraph_data_iterator(input_graph),
                        ("input", "categorical_type", "encoded_value"),
                        features_field)
    input_graph.graph[features_field] = np.array([0.0] * 5, dtype=np.float32)
    return input_graph


def create_target_graph(graph, features_field="features"):
    target_graph = graph.copy()
    target_graph = encode_solutions(target_graph, solution_field="solution", encoded_solution_field="encoded_solution",
                                    encodings=np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]))
    augment_data_fields(multidigraph_data_iterator(target_graph),
                        ("encoded_solution",),
                        features_field)
    target_graph.graph[features_field] = np.array([0.0] * 5, dtype=np.float32)
    return target_graph


def augment_data_fields(graph_data_iterator, fields_to_augment, augmented_field):
    """
    Returns a graph with features built from augmenting data fields found in the graph

    Args:
        graph_data_iterator: iterator over the data for elements in a graph
        fields_to_augment: the fields of the data dictionaries to augment together
        augmented_field: the field in which to store the augmented fields

    Returns:
        None, updates the graph in-place

    """

    for data in graph_data_iterator:
        data[augmented_field] = np.hstack([np.array(data[field], dtype=float) for field in fields_to_augment])


def encode_solutions(graph, solution_field="solution", encoded_solution_field="encoded_solution",
                     encodings=np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])):
    """
    Determines the encoding to use for a solution category
    Args:
        graph: Graph to update
        solution_field: The property in the graph that holds the value of the solution
        encoded_solution_field: The property in the graph to use to hold the new solution value
        encodings: An array, a row from which will be picked as the new solution based on using the current solution
            as a row index

    Returns: Graph with updated `encoded_solution_field`

    """

    for data in multidigraph_data_iterator(graph):
        solution = data[solution_field]
        data[encoded_solution_field] = encodings[solution]

    return graph


def encode_categorically(graph_data_iterator, all_categories, category_field, encoding_field):
    """
    Encodes the type found in graph data as an integer according to the index it is found in `all_types`
    Args:
        graph_data_iterator: An iterator of data in the graph (node data, edge data or combined node and edge data)
        all_categories: The full list of categories to be encoded in this order
        category_field: The data field containing the category to encode
        encoding_field: The data field to use to store the encoding

    Returns:

    """
    for data in graph_data_iterator:
        data[encoding_field] = all_categories.index(data[category_field])
