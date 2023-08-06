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


import uuid

import pytest

import faculty_models


PARAMETRIZE_FUNCTION = pytest.mark.parametrize(
    "faculty_models_function, mlflow_function_name",
    [
        (
            faculty_models.download,
            "mlflow.tracking.artifact_utils._download_artifact_from_uri",
        ),
        (faculty_models.load_mlmodel, "mlflow.pyfunc.load_model"),
    ],
    ids=["download", "load_mlmodel"],
)


PROJECT_ID = uuid.uuid4()
MODEL_ID = uuid.uuid4()


@PARAMETRIZE_FUNCTION
@pytest.mark.parametrize(
    "version, version_mock_index",
    [(None, -1), (3, 3)],
    ids=["version=None", "version=3"],
)
@pytest.mark.parametrize("artifact_path_suffix", ["", "/"])
@pytest.mark.parametrize("path", [None, "sub/path", "/sub/path"])
def test_function(
    mocker,
    faculty_models_function,
    mlflow_function_name,
    version,
    version_mock_index,
    artifact_path_suffix,
    path,
):

    model_versions = [
        mocker.Mock(
            version_number=i,
            artifact_path="faculty-datasets:model/{}/artifacts{}".format(
                i, artifact_path_suffix
            ),
        )
        for i in range(5)
    ]

    mock_client = mocker.Mock()
    mock_client.list_versions.return_value = model_versions
    mocker.patch("faculty.client", return_value=mock_client)

    mlflow_function_mock = mocker.patch(mlflow_function_name)

    return_value = faculty_models_function(
        PROJECT_ID, MODEL_ID, version=version, path=path
    )

    assert return_value == mlflow_function_mock.return_value

    mock_client.list_versions.assert_called_once_with(PROJECT_ID, MODEL_ID)

    if path is None:
        expected_uri = model_versions[version_mock_index].artifact_path
    else:
        expected_uri = (
            model_versions[version_mock_index].artifact_path.rstrip("/")
            + "/"
            + path.lstrip("/")
        )
    mlflow_function_mock.assert_called_once_with(expected_uri)


@PARAMETRIZE_FUNCTION
def test_function_missing_version(
    mocker, faculty_models_function, mlflow_function_name
):

    model_versions = [mocker.Mock(version_number=i) for i in range(5)]

    mock_client = mocker.Mock()
    mock_client.list_versions.return_value = model_versions
    mocker.patch("faculty.client", return_value=mock_client)

    mlflow_function_mock = mocker.patch(mlflow_function_name)

    with pytest.raises(
        ValueError, match="No version .* with version number 6 found"
    ):
        faculty_models_function(PROJECT_ID, MODEL_ID, version=6)

    mock_client.list_versions.assert_called_once_with(PROJECT_ID, MODEL_ID)
    mlflow_function_mock.assert_not_called()


@PARAMETRIZE_FUNCTION
def test_function_duplicate_version(
    mocker, faculty_models_function, mlflow_function_name
):

    model_versions = [mocker.Mock(version_number=i) for i in [0, 1, 2, 2, 3]]

    mock_client = mocker.Mock()
    mock_client.list_versions.return_value = model_versions
    mocker.patch("faculty.client", return_value=mock_client)

    mlflow_function_mock = mocker.patch(mlflow_function_name)

    with pytest.raises(
        ValueError, match="Multiple versions .* with version number 2 found"
    ):
        faculty_models_function(PROJECT_ID, MODEL_ID, version=2)

    mock_client.list_versions.assert_called_once_with(PROJECT_ID, MODEL_ID)
    mlflow_function_mock.assert_not_called()
