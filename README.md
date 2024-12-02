# Flask Movie Recommendation App with Neo4j

This project provides a Flask API for querying and recommending movies from a Neo4j graph database. The application is containerized using Docker for easy setup and deployment.

---

## Features

- **Neo4j Database Preloaded with a Movie Dataset**
- **Query Movies by Genre, Director, Duration, and Ratings**
- **Recommend Movies Based on Shared Writers or Directors**
- **Filter Movies by Release Year or Decade**

---

## Starting the Docker Containers

To start the application using Docker, follow these steps:

### Bring Up the Docker Containers

Run the following commands to start the containers using Docker Compose and Run the app:

```bash
docker-compose up

# from different cli
docker exec -it slim-python bash

pip install -r requirements.txt

python import_dataset.py
python app.py
```

---
## Routes

### 1. Welcome Message

- **Endpoint**: `http://localhost:5000/` (GET)
- **Description**: Access the root URL to receive a friendly welcome message from the Flask Movie Recommendation App.

---

### 2. Find Movies by Genre

- **Endpoint**: `http://localhost:5000/movies/genre` (GET)
- **Description**: Retrieve a list of movies that belong to a specific genre.
- **Query Parameters**:
  - `genre` (string): The genre to filter movies by (e.g., "Action", "Comedy").

---

### 3. List Movies by Director

- **Endpoint**: `http://localhost:5000/movies/director` (GET)
- **Description**: Get all movies directed by a specific director.
- **Query Parameters**:
  - `director` (string): The name of the director.

---

### 4. Find Top-Rated Movies by Genre

- **Endpoint**: `http://localhost:5000/movies/top-rated/genre` (GET)
- **Description**: Retrieve the top 10 highest-rated movies within a given genre.
- **Query Parameters**:
  - `genre` (string): The genre to filter movies by.

---

### 5. Recommend Movies by Shared Director

- **Endpoint**: `http://localhost:5000/movies/recommend/director` (GET)
- **Description**: Recommend movies directed by the same director as a specified movie.
- **Query Parameters**:
  - `movieTitle` (string): The title of the movie to base recommendations on.

---

### 6. Recommend Movies by Shared Writer

- **Endpoint**: `http://localhost:5000/movies/recommend/writer` (GET)
- **Description**: Recommend movies written by the same writer as a specified movie.
- **Query Parameters**:
  - `movieTitle` (string): The title of the movie to base recommendations on.

---

### 7. List Movies by Motion Picture Rating

- **Endpoint**: `http://localhost:5000/movies/rating` (GET)
- **Description**: List movies that have a specific motion picture rating (e.g., "PG-13", "R").
- **Query Parameters**:
  - `rating` (string): The motion picture rating to filter movies by.

---

### 8. Find Movies by Duration Range

- **Endpoint**: `http://localhost:5000/movies/duration` (GET)
- **Description**: Find movies within a specified runtime duration range.
- **Query Parameters**:
  - `minDuration` (integer): Minimum runtime in minutes.
  - `maxDuration` (integer): Maximum runtime in minutes.

---

### 9. Recommend Movies by Release Year

- **Endpoint**: `http://localhost:5000/movies/recommend/release-year` (GET)
- **Description**: Recommend movies released in a specific year.
- **Query Parameters**:
  - `year` (integer): The release year to filter movies by.

---

### 10. Recommend Movies by Decade

- **Endpoint**: `http://localhost:5000/movies/recommend/decade` (GET)
- **Description**: Recommend movies released within a specific decade.
- **Query Parameters**:
  - `startYear` (integer): The starting year of the decade (e.g., use 1990 for the 1990s).

---

### Error Handling

- **Description**: Returns a JSON-formatted error message for undefined routes, indicating that the route is not supported (HTTP status code 404).

---

### Running the Flask App

- **Description**: The Flask application is configured to run in debug mode and is accessible from any network interface.


---

## How to Use the API

You can interact with the API using tools like **Postman**. Below are some example requests:

- **Find Movies by Genre**:
  ```bash
  GET http://localhost:5000/movies/genre?genre=Action
  ```

- **List Movies by Director**:
  ```bash
  GET http://localhost:5000/movies/director?director=Christopher%20Nolan
  ```

- **Find Top-Rated Movies by Genre**:
  ```bash
  GET http://localhost:5000/movies/top-rated/genre?genre=Drama
  ```

- **Recommend Movies by Shared Director**:
  ```bash
  GET http://localhost:5000/movies/recommend/director?movieTitle=Inception
  ```


- **Recommend Movies by Shared Writer**:
  ```bash
  GET http://localhost:5000/movies/recommend/writer?movieTitle=Inception
  ```

- **List Movies by Motion Picture Rating**:
  ```bash
  GET http://localhost:5000/movies/rating?rating=PG-13
  ```


- **Find Movies by Duration Range**:
  ```bash
  GET http://localhost:5000/movies/duration?minDuration=90&maxDuration=120
  ```

- **Recommend Movies by Release Year**:
  ```bash
  GET http://localhost:5000/movies/recommend/release-year?year=1994
  ```

- **Recommend Movies by Decade**:
  ```bash
  GET http://localhost:5000/movies/recommend/decade?startYear=1980
  ```


---

## Conclusion

This application provides a robust API for querying and recommending movies from a Neo4j graph database. It allows users to find movies based on genre, director, duration, and more, as well as receive recommendations based on shared directors or writers.

