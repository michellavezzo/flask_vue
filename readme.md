# Activate the environment

`cd backend`
`.venv/bin/activate`

# Install Flask and Dependencies

`pip install Flask Flask-PyMongo Flask-Cors bcrypt` // Check this before submit

# Start Mongo (macos)

`brew services start mongodb-community@6.0`

# Seed Database 1st time using

`python parser.py` || `python3 parser.py`

# Run Flask

`flask --app app run` || `python3 app.py`

# Run Frontend (Vue)

#### Frontend has its own readme.md

`cd frontend`
`npm install`
`npm run serve`

# Things I would like to add

- Auth on frontend and Backend + Protected Routes
- Dockerize the app
- (Front) Add an option on frontend to choose if the user wants to see its own timezone or the timezone of the user in the list.
- Improve componentization, avoid repeat some code as I did for the Tags on the frontend.
- There is a bug on users/:user_name. As I passed the user as props, when you edit an user from there data is not rerrendered as it should be. I would like to fix this. (If this not happened to you, I fixed that already)
- Better Documentation
- Setup .env file for better code management

- This test was very fun, congratulations for who did it. I would like to add more features and improve the code, but I have to submit it now. I hope you like it. Thank you for the opportunity.
