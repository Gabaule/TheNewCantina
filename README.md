# TheNewCantina
web development project carried out as part of our international mobility program at Uniza (SK). 

A modern web application for ordering meals from campus cafeterias. Built with Flask, HTMX, and Tailwind CSS.

## Installation

To launch the app download the repository. Use a command line interpreter with docker installed and simply use ```docker compose -f docker/docker-compose.yml up --build -d``` to start the app.

Wait for the building and then go to your browser and use http://localhost:8081 to access the project. 
If you want to fully restart the project do ```docker compose -f docker/docker-compose.yml down -v``` and then remove the docker-data/postgres directory.

All credentials are directly on the login page. 