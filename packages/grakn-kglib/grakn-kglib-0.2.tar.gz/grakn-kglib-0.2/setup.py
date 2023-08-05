#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from setuptools import setup
from setuptools import find_packages

packages = find_packages()

setup(
    name = "grakn-kglib",
    version = "0.2",
    description = "A Machine Learning Library for the Grakn knowledge graph.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers = ["Programming Language :: Python :: 3", "Programming Language :: Python :: 3.6", "License :: OSI Approved :: Apache Software License", "Operating System :: OS Independent", "Intended Audience :: Developers", "Intended Audience :: Science/Research", "Topic :: Scientific/Engineering", "Topic :: Scientific/Engineering :: Information Analysis", "Topic :: Scientific/Engineering :: Artificial Intelligence", "Topic :: Software Development :: Libraries", "Topic :: Software Development :: Libraries :: Python Modules"],
    keywords = "machine learning logical reasoning knowledege graph grakn database graph knowledgebase knowledge-engineering",
    url = "https://github.com/graknlabs/kglib",
    author = "Grakn Labs",
    author_email = "community@grakn.ai",
    license = "Apache-2.0",
    packages=packages,
    install_requires=["enum-compat==0.0.2", "grakn-client==1.5.4", "absl-py==0.8.0", "astor==0.8.0", "cloudpickle==1.2.2", "contextlib2==0.5.5", "cycler==0.10.0", "decorator==4.4.0", "dm-sonnet==1.35", "future==0.17.1", "gast==0.3.1", "google-pasta==0.1.7", "graph-nets==1.0.4", "grpcio==1.23.0", "h5py==2.10.0", "Keras-Applications==1.0.8", "Keras-Preprocessing==1.1.0", "kiwisolver==1.1.0", "Markdown==3.1.1", "matplotlib==3.1.1", "networkx==2.3", "numpy==1.17.2", "pandas==0.25.1", "protobuf==3.9.1", "pyparsing==2.4.2", "python-dateutil==2.8.0", "pytz==2019.2", "semantic-version==2.8.2", "six==1.12.0", "tensorboard==1.14.0", "tensorflow==1.14.0", "tensorflow-estimator==1.14.0", "tensorflow-probability==0.7.0", "termcolor==1.1.0", "Werkzeug==0.15.6", "wrapt==1.11.2"],
    zip_safe=False,
)
