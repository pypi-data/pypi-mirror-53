# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pylunch']

package_data = \
{'': ['*'], 'pylunch': ['static/*', 'templates/*', 'templates/admin/*']}

install_requires = \
['aiodns',
 'aiohttp',
 'beautifulsoup4',
 'click',
 'flask',
 'flask-jwt-extended',
 'fuzzywuzzy',
 'html2text',
 'ipython',
 'lxml',
 'pdfminer-six',
 'pillow',
 'pytesseract',
 'python-levenshtein',
 'python-telegram-bot>=12.0.0b1,<13.0.0',
 'pyyaml',
 'pyzomato',
 'requests',
 'toml>=0.10.0,<0.11.0',
 'unidecode',
 'werkzeug']

entry_points = \
{'console_scripts': ['pylunch = pylunch:cli']}

setup_kwargs = {
    'name': 'pylunch',
    'version': '0.2.2',
    'description': 'Pylunch cli and web tool to get lunch info',
    'long_description': '# Pylunch\n\n``PyLunch`` was designed to scrape restaurants for it\'s daily menus and show them in multiple ways and formats.\n\n## Getting stated\n`PyLunch` is a scraper, to use it, you have to install it. It is available at [PyLunch](https://gitlab.com/pestanko/pylunch)\n\n### Install the released version\n\nYou can install the `PyLunch` using the `pip`:\n```bash\n$ pip install pylunch\n```\n\n\n### Install the development version from github\n- Python 3.7 or later\n- (Optional) [pipenv](https://github.com/pypa/pipenv)\n\nOr you can add it as a development dependency using the ``pipenv``\n\n```bash\n$ git clone https://github.com/pestanko/pylunch.git\n$ cd pylunch\n$ pipenv install # install the dependencies\n```\n\n### Install Tesseract for OCR support\nTo support extracting text from images you need to install [Tesseract](https://github.com/tesseract-ocr/tesseract/wiki).\nThen you need to download trained models for your language [Tesseract data files wiki](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files) \n(English is supported by default).\n\nRecommended are the [best (most accurate) trained models](https://github.com/tesseract-ocr/tessdata_best).\nSave downloaded trained models to a dictionary with name `tessdata`. \nExpose environment variable `TESSDATA_PREFIX` with path to `tessdata` directory (i.e. `TESSDATA_PREFIX=/tmp/tessdata`).\n\nYou can specify different language when extracting data from the image for any restaurant with attribute `language: <Lang code>` in `restaurants.yml` file. \n\n#### Dockerfile supported languages:\n\n| Language | Lang code |\n| ---------|:---:| \n| English  | eng | \n| Czech    | ces | \n| Slovak   | slk | \n\n\n### First Run\nIn order to run the tool correctly you need to configure it.\n\nAt first run the tool will create config folder in the home directory with restaurants database, \nby default it will be empty.\n\nTo use the `zomato` resolver you need to add the `zomato_key` to your configuration.\nIn order to get the zomato key you need to go to the [Zomato Api documentation](https://developers.zomato.com/api)\n\n```bash\n$ pylunch cfg-set zomato_key "<YOUR_KEY>"\n```\n\nTo use the telegram integration, you need to set the telegram bot token property ``telegram_token``.\nTo get the telegram bot token please take a look [here](https://core.telegram.org/bots).\n\n```bash\n$ pylunch cfg-set telegram_token "<YOUR_KEY>"\n```\n\nAlso if you have already created or exported database of the restaurants, you an import it using the command `import`:\nExample file is located in: `resources/restaurants.yml` available [here](https://gitlab.com/pestanko/pylunch/raw/master/resources/restaurants.yml).\n\n```bash\n$ pylunch import restaurants.yml\n```\n\nIn order to export the restaurants database file, you can use the export command.\n```bash\n$ pylunch export -f exported.yml\n```\n\n## Run the cli tool\n\nHera is a help output with available commands.\n\n```bash\n# Show the help\n$ pylunch --help\n\nUsage: pylunch [OPTIONS] COMMAND [ARGS]...\n\n  PyLunch CLI tool\n\nOptions:\n  --version              Show the version and exit.\n  -L, --log-level TEXT   Set log level (d|i|w|e) - default=w\n  -C, --no-cache         Disable cache\n  -c, --config-dir TEXT  Location to the configuration directory\n  -F, --format TEXT      Set output format\n  --help                 Show this message and exit.\n\nCommands:\n  add            Adds a new restaurant\n  cache-clear    Clear a current cache for a day\n  cache-content  Show the current cache for a day\n  cfg-edit       Edit a configuration using the editor (Ex: VIM)\n  cfg-set        Set a config value in the user configuration\n  config         Shows the current configuration\n  console        Start the interactive console (IPython)\n  disable        Disables the restaurants\n  edit           Edits restaurants DB file\n  enable         Enables the restaurants\n  export         Export restaurants\n  import         Import restaurants\n  info           Get info for the restaurant\n  ls             List all available restaurants\n  menu           Get menu for a restaurant\n  rm             Removes the restaurant\n  telegram-bot   Start the telegram bot\n```\n\n### Runnig the server\n\nAs a server is used the Flask.\nTo run the flask server please take a look to the documnetation.\n\nIn order to start the pylunch server take a look at the `run_flask.ps1` or `run_flask.sh` scripts.\n\nFor access to the admin pages - in order to import restaurants or invalidate (refresh cache) you will need to set env variables:\n```\nPYLUNCH_SECRET=<JWT_SECRET>\nPYLUNCH_USERS=PATH_TO_USERS_FILE\n```\n\n',
    'author': 'Peter Stanko',
    'author_email': 'peter.stanko0@gmail.com',
    'url': 'https://gitlab.com/pestanko/pylunch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
