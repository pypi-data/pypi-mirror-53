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

import inspect
import os

import numpy as np
from grakn.client import GraknClient

from kglib.utils.grakn.synthetic.statistics.pmf import PMF
import subprocess as sp


def get_example_queries(pmf, example_id):

    variable_values = pmf.select()

    queries = [f'insert $p isa person, has example-id {example_id};']

    if variable_values['Meningitis']:
        queries.append(inspect.cleandoc(f'''match
                       $d isa disease, has name "meningitis";
                       $p isa person, has example-id {example_id};
                       insert
                       (patient: $p, diagnosed-disease: $d) 
                       isa diagnosis;'''))

    if variable_values['Flu']:
        queries.append(inspect.cleandoc(f'''match
                       $p isa person, has example-id {example_id};
                       $d isa disease, has name "flu";
                       insert
                       (patient: $p, diagnosed-disease: $d) 
                       isa diagnosis;'''))

    if variable_values['Light Sensitivity']:
        queries.append(inspect.cleandoc(f'''match
                       $p isa person, has example-id {example_id};
                       $s isa symptom, has name "light-sensitivity";
                       insert
                       (presented-symptom: $s, symptomatic-patient: $p) isa 
                       symptom-presentation;'''))

    if variable_values['Fever']:
        queries.append(inspect.cleandoc(f'''match
                       $p isa person, has example-id {example_id};
                       $s isa symptom, has name "fever";
                       insert
                       (presented-symptom: $s, symptomatic-patient: $p) isa 
                       symptom-presentation;'''))

    return queries


def generate_example_graphs(num_examples, keyspace="diagnosis", uri="localhost:48555"):

    client = GraknClient(uri=uri)
    session = client.session(keyspace=keyspace)

    pmf_array = np.zeros([2, 2, 2, 2], dtype=np.float)
    pmf_array[0, 1, 0, 1] = 0.1
    pmf_array[1, 0, 1, 0] = 0.15
    pmf_array[0, 1, 1, 0] = 0.05
    pmf_array[1, 0, 0, 1] = 0.34
    pmf_array[1, 1, 1, 1] = 0.01
    pmf_array[0, 1, 1, 1] = 0.3
    pmf_array[1, 0, 1, 1] = 0.05

    pmf = PMF({
        'Flu':                  [False, True],
        'Meningitis':           [False, True],
        'Light Sensitivity':    [False, True],
        'Fever':                [False, True]
    }, pmf_array, seed=0)

    print(pmf.to_dataframe())

    for example_id in range(0, num_examples):
        tx = session.transaction().write()
        for query in get_example_queries(pmf, example_id):
            print(query)
            tx.query(query)
        tx.commit()

    session.close()
    client.close()


if __name__ == '__main__':
    generate_example_graphs(20, keyspace="diagnosis", uri="localhost:48555")
