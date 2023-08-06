faculty-models
==============

``faculty-models`` is a tool to help you use models from the model registry in
Faculty Platform.

.. warning::

    This library's API is subject to change as new functionality is added to
    the model registry feature in Faculty Platform.

Installation
------------

``faculty-models`` comes preinstalled in Python environments available in
Faculty platform. To use it externally, install it from PyPI with ``pip``:

.. code-block:: bash

    pip install faculty-models

If you've not already done so on the computer you're using, you'll also need to
generate and store CLI credentials for the Platform. You can do this with
`the Faculty CLI
<https://docs.faculty.ai/user-guide/command_line_interface.html#initialising-faculty>`_.

Usage
-----

The model registry in Faculty Platform includes a feature that helps you
generate the snippets you need. It will help you get the project and model IDs
you need to use ``faculty-models``.

If your model is in the `MLmodel format
<https://mlflow.org/docs/latest/models.html>`_ (likely because you used `MLflow
<https://mlflow.org/>`_ to store it), you can load it directly back into Python
with:

.. code-block:: python

    import faculty_models

    model = faculty_models.load_mlmodel(
        project_id="998328c3-23df-4225-a3ee-0a53d1409fbd",
        model_id="c998fca9-e093-47ea-9896-8f75db695b91"
    )

Otherwise, you can use the following to download the contents of the model to
the local filesystem. ``download`` returns the path of the downloaded model
files:

.. code-block:: python

    import faculty_models

    path = faculty_models.download(
        project_id="998328c3-23df-4225-a3ee-0a53d1409fbd",
        model_id="c998fca9-e093-47ea-9896-8f75db695b91"
    )

The above examples always download the latest version of a model. To get a
specific verion, pass the version number when calling either function:

.. code-block:: python

    import faculty_models

    model = faculty_models.load_mlmodel(
        project_id="998328c3-23df-4225-a3ee-0a53d1409fbd",
        model_id="c998fca9-e093-47ea-9896-8f75db695b91",
        version=4
    )

If you only wish to download part of the model, or if you wish to load an
MLmodel that is in a subdirectory of the model, pass the path argument to
either function:

.. code-block:: python

    import faculty_models

    model = faculty_models.load_mlmodel(
        project_id="998328c3-23df-4225-a3ee-0a53d1409fbd",
        model_id="c998fca9-e093-47ea-9896-8f75db695b91",
        path="sub/path"
    )
