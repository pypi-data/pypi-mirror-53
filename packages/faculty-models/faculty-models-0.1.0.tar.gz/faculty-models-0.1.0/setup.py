# Copyright 2019 Faculty Science Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from setuptools import setup


def load_readme():
    path = os.path.join(os.path.dirname(__file__), "README.rst")
    with open(path) as fp:
        return fp.read()


setup(
    name="faculty-models",
    description="Python library for retrieving models from Faculty platform.",
    long_description=load_readme(),
    url="https://faculty.ai/products-services/platform/",
    author="Faculty",
    author_email="opensource@faculty.ai",
    license="Apache Software License",
    py_modules=["faculty_models"],
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    install_requires=["faculty>=0.25.4", "mlflow==1.2.0"],
)
