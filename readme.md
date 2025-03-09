# Activate the environment 

`./backend .venv/bin/activate`

# Install Flask and Dependencies

`pip install Flask Flask-PyMongo Flask-Cors pip install bcrypt` // Check this before submit

# Start Mongo 

`brew services start mongodb-community@6.0`


# Seed Database 1st time using:

`python seed.py `

# Run Flask

`flask --app app run` || `python3 app.py`
