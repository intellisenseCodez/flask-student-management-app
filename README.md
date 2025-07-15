

## Setup Virtual Environment
1. install a virtual environment
pip install virtualenv

2. create a virual environment
python3 -m venv venv

3. activate virtual environment
source venv/bin/activate

4. install libraries
pip install -r requirements.txt

Source: https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/

## Setup Database Migration
1. Install Flask-Migrate with pip:
pip install Flask-Migrate

2. Integrate with App
```bash
...
...
from flask_migrate import Migrate


migrate = Migrate(app, db)
...
```

3. Initialize
flask db init

4. perform migration
flask db migrate -m "Initial migration."

5. upgrade
flask db upgrade


docker-compose --env-file dev.env up --build

docker-compose --env-file prod.env up --build -d
