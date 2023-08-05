# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['windmill',
 'windmill.cli',
 'windmill.config',
 'windmill.http',
 'windmill.http.api',
 'windmill.models',
 'windmill.models.dags',
 'windmill.models.operators',
 'windmill.models.schemas',
 'windmill.tasks',
 'windmill.utils']

package_data = \
{'': ['*'],
 'windmill': ['templates/*'],
 'windmill.http': ['app/*',
                   'app/dist/*',
                   'app/public/*',
                   'app/src/*',
                   'app/src/components/*',
                   'app/src/components/Airflow/*',
                   'app/src/components/Navbar/*',
                   'app/src/components/Page/*',
                   'app/src/components/Sidebar/*',
                   'app/src/misc/*']}

install_requires = \
['black>=18.3-alpha.0,<19.0',
 'decli>=0.5.1,<0.6.0',
 'docstring-parser>=0.3.0,<0.4.0',
 'flask-cors>=3.0.8,<4.0.0',
 'inflection>=0.3.1,<0.4.0',
 'jinja2>=2.10.1,<3.0.0',
 'marshmallow>=3.0,<4.0',
 'networkx>=2.3,<3.0',
 'pyyaml>=5.1.2,<6.0.0']

extras_require = \
{'airflow': ['apache-airflow==1.10.4']}

entry_points = \
{'console_scripts': ['windmill = windmill:cli.cli.Cli.run_cli',
                     'windmill-dev = windmill:cli.cli.DevCli.run_cli']}

setup_kwargs = {
    'name': 'airflow-windmill',
    'version': '0.0.2',
    'description': "Drag'N'Drop Web Frontend for Building and Managing Airflow DAGs",
    'long_description': "# Windmill\n\n[![Build Status](https://travis-ci.org/mayansalama/windmill.svg?branch=master)](https://travis-ci.org/mayansalama/windmill)\n\nDrag'n'drop web app to manage and create Airflow DAGs. The goal is to\nhave a Web UI that can generate YML Dag Definitions, integrating with\ncustom operators and potentially existing DAGs. YML DAGs can then be\nsynced to a remote repo\n\n- Front end is built using React on Typescript\n- Back end is built using Flask on Python 3.6+\n\n## Getting Started\n\n1. Install with `pip install airflow-windmill`\n   1. Airflow is expected to be installed on the system. This allows Windmill to run with arbitrary versions of Airflow\n   2. Otherwise it can be packaged with windmill using `pip install airflow-windmill[airflow]`. The version is defined in `pyproject.toml`\n2. Run `windmill init` to create a local Windmill project\n3. `cd windmill-project`\n4. Run `windmill run` from this folder to run the app locally\n\n## MVP Required Features\n\n### Front-End Features\n\n- [x] Dynamic Operators\n- [x] Menu Dropdowns\n- [x] Load Operators from App\n- [x] Format operator display into classes\n- [x] Search functionality for operators\n- [x] Basic operator level properties\n- [x] Implement DAG level properties\n- [x] New DAG Functionality\n- [x] Parameter Tooltips\n- [x] Render arbitrary viewport windows for New/Save/Load etc\n- [x] Overwrite/Save prompt on New\n- [x] DAG renaming and save functionality\n- [x] Open dag from menu\n- [x] Make save/load more efficient by removing non-essential values\n- [x] Switch nav menu to icons \n- [x] Add convert DAG call\n- [ ] Add hotkeys to menu functions\n- [ ] Make input/output nodes more clear\n- [ ] Check if file already exists on rename\n- [ ] Prompt save if there are nodes on open\n- [x] Fix loss of state on refresh bug\n- [ ] Put File details in File Browse\n- [ ] Make Flask Backend URI configurable\n- [ ] Add a last saved time to NavBar\n- [ ] Add error handling to backend calls\n- [ ] Add tests\n- [ ] Get task descriptions from Operator list\n\n### Back-End Features\n\n- [x] Generate Operator Lists\n- [x] CLI to start Web and Front End\n- [x] Generate DAG Spec\n- [x] CLI to create new windmill project\n- [x] CLI to start windmill from a windmill project\n- [x] Implement windmill-dev start\n- [x] Save/Load Windmill Files functionality\n- [x] Get default values\n- [x] Pull parameters from parent classes\n- [x] Move airflow dependency as extra\n- [x] Convert WML into Python DAG\n- [x] API Endpoint to trigger WML -> DAG\n- [ ] Edge cases for WML -> DAG\n- [ ] Get WML owner and last-modified details during wml list\n- [ ] Allow custom operators\n- [ ] Add defaults to CLI --help commands\n- [ ] Strategy for Python Opjects (e.g. callables) - allow either a import ref or an inline statement\n- [ ] Backport existing Python DAGs to WMLs\n- [ ] Allow DAG updates to propogate to WMLs\n- [ ] Add tests for different airflow version\n\n### Other features\n\n- [ ] Validate on backend or front end or both?\n- [ ] Doco\n- [ ] Add permission restrictions for valid tags \n\n## Dev User Guide\n\nTo run as a dev:\n\n1. Clone from git\n2. Run `poetry install -E airflow`\n3. Run `windmill-dev start-backend`\n4. Run `windmill-dev start-frontend`\n\n## Future Usage Patterns\n\n- Auto-sync for windmill project to git\n\n## Deployment\n\nDeployment to PyPi is managed using Travis and should be done in the following steps:\n\n1. Run `poetry version {patch|minor|major}`\n2. Increment the version number in `windmill/__init__.py`\n3. Commit and merge code into the master branch\n4. Ensure that the travis build is green\n5. Create a git tag for the new build\n6. Push the tag to origin\n",
    'author': 'mayansalama',
    'author_email': 'micsalama@gmail.com',
    'url': 'https://github.com/mayansalama/windmill',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
