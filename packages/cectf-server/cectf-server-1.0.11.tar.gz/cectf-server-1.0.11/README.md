# cectf-server

You need Python 3 and pip installed to set up this project.

Navigate to the project repository and run `./setup_workspace.sh`. This will set up the python virtual environment and install the python dependencies.

You will need to install MariaDB (https://mariadb.com/downloads/#aptyum) and have it running on localhost. For testing purposes, the user `travis` with no password needs to be created (`CREATE USER 'travis'@'localhost' IDENTIFIED BY '';`)

Run `db_setup.sh` to set up the `test` database with dummy data. Right now this provisions a user `a` with password `b`, and an admin user `abc` with password `123`. You will need to use these credentials to log in to the app.

Run `run.sh` to launch the Flask server. It is configured to run the server on `http://127.0.0.1:5001` by default.

Configuration can be done by adding variables to `instance/config.py`.

For testing, first do `pip install pytest coverage`. Run `pip install -e .` to install the project in the local virtual environment (the `-e` ensures that it is updated as the project is modified). Run `pytest` to run all tests. Run `coverage run -m pytest` to generate a code coverage report. Run `coverage report` to get the report in the command line, or run `coverage html` to generate an interactive HTML page in `htmlcov/index.html`.
