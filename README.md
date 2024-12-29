
# Website with Database - Python Flask

This project is a simple web app designed to help me gain practical experience in development. The app includes the following features:
- User logins
- A simple API request to fetch animal data
- A database where users can store animal data

### Technologies Used
- Backend: Python with Flask, MYSQL, Docker, HTML, CSS

## Requirements

Before running the app, make sure you have Docker installed and activated on your system. You can verify that Docker is working by typing the following command in your terminal:

```bash
docker --version
```

Additionally, you will need an **API key** for openai.

If you do not want to use the ai-functionality, no worries! The rest of the app will work perfectly fine without it.

## Setup Instructions

### Step 1: Clone the Repository

Navigate to your workspace directory and clone the repository:

```bash
git clone https://github.com/JuliusKaufhold/simple_flask_website
```

After cloning the repository, navigate into the project folder.

### Step 2: Build the Docker Image

Run the following command to build the Docker image for the web server:

```bash
docker build -t webserver:latest .
```

### Step 3: Create a Docker Network

Next, create a network for the database and server containers:

```bash
docker network create webserver-network
```

### Step 4: Set Up the Database Container

To create the database container, run:

```bash
docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=webserver -e MYSQL_USER=webserver -e MYSQL_PASSWORD=changeme --network webserver-network mysql:latest
```

> **Note**: You can change the `MYSQL_PASSWORD` to any password of your choice. Make sure to update the `DATABASE_URL` accordingly in the next step.

### Step 5: Start the Server Container

Now, start the Flask server container. If you have an API key, replace `<your-api-key>` with your actual API key:

```bash
docker run --name webserver -d -p 8000:5000 --rm -e SECRET_KEY=my-secret-key -e DATABASE_URL=mysql+pymysql://webserver:changeme@mysql/webserver -e API_KEY=<your-api-key> webserver:latest
```

If you don’t want to use the external API, you can omit the `-e API_KEY=<your-api-key>` part.

### Step 6: Access the Web Application

Once both containers are running, you can access the web app by navigating to the following URL in your browser:

```
http://localhost:8000
```

You should see the website and be able to interact with it, including logging in, making API requests, and storing animal data in the database.

## Troubleshooting

- **API Key Error**: If you see an "Invalid API Key" error, make sure you have correctly set the `API_KEY` environment variable in the server container. If you still have issues, try priting out the error code and visit openai for more information.
- **Docker Network Issues**: If you encounter any issues with Docker networks, ensure that the containers are on the same network (`webserver-network`).
- **Database Issues**: Make sure to wait at least a few seconds after creating and starting the database container. It needs to be fully set up so that the server container can successfully connect to it.
