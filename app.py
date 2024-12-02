from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# Initialize Neo4j driver
# this is for outside of docker
# driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
# Here, we are connecting to a Neo4j instance using the Bolt protocol in docker
driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

# Utility function to run queries
# Accepts a Cypher query and optional parameters
def run_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record.data() for record in result]

# welcome message
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask Movie Recommendation App!"})

# 1. Find Movies by Genre
@app.route('/movies/genre', methods=['GET'])
def find_movies_by_genre():
    """
    Find movies by genre.

    Example: GET /movies/genre?genre=Action
    """
    genre = request.args.get('genre')
    query = '''
        MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre {name: $genre})
        RETURN m.title AS title, m.rating AS rating
    '''
    result = run_query(query, {"genre": genre})
    return jsonify(result)

# 2. List Movies by Director
@app.route('/movies/director', methods=['GET'])
def list_movies_by_director():
    """
    List all movies directed by a specific director.

    Example: GET /movies/director?director=Christopher%20Nolan
    """
    director = request.args.get('director')
    query = '''
        MATCH (d:Director {name: $director})<-[:DIRECTED_BY]-(m:Movie)
        RETURN m.title AS title, m.releaseYear AS releaseYear
    '''
    result = run_query(query, {"director": director})
    return jsonify(result)

# 3. Find Top-Rated Movies by Genre
@app.route('/movies/top-rated/genre', methods=['GET'])
def find_top_rated_movies_by_genre():
    """
    Find the top 10 highest-rated movies within a specific genre.

    Example: GET /movies/top-rated/genre?genre=Drama
    """
    genre = request.args.get('genre')
    query = '''
        MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre {name: $genre})
        RETURN m.title AS title, m.rating AS rating
        ORDER BY m.rating DESC
        LIMIT 10
    '''
    result = run_query(query, {"genre": genre})
    return jsonify(result)

# 4. Recommend Movies by Shared Director
@app.route('/movies/recommend/director', methods=['GET'])
def recommend_movies_by_director():
    """
    Recommend movies by the same director as a given movie.

    Example: GET /movies/recommend/director?movieTitle=Inception
    """
    movie_title = request.args.get('movieTitle')
    query = '''
        MATCH (m:Movie {title: $movieTitle})-[:DIRECTED_BY]->(d:Director)
        MATCH (other:Movie)-[:DIRECTED_BY]->(d)
        WHERE other.title <> m.title
        RETURN DISTINCT other.title AS recommendedTitle, other.rating AS rating
    '''
    result = run_query(query, {"movieTitle": movie_title})
    return jsonify(result)

# 5. Recommend Movies by Shared Writer
@app.route('/movies/recommend/writer', methods=['GET'])
def recommend_movies_by_writer():
    """
    Recommend movies by the same writer as a given movie.

    Example: GET /movies/recommend/writer?movieTitle=Inception
    """
    movie_title = request.args.get('movieTitle')
    query = '''
        MATCH (m:Movie {title: $movieTitle})-[:WRITTEN_BY]->(w:Writer)
        MATCH (other:Movie)-[:WRITTEN_BY]->(w)
        WHERE other.title <> m.title
        RETURN DISTINCT other.title AS recommendedTitle, other.rating AS rating
    '''
    result = run_query(query, {"movieTitle": movie_title})
    return jsonify(result)

# 6. List Movies by Motion Picture Rating
@app.route('/movies/rating', methods=['GET'])
def list_movies_by_motion_picture_rating():
    """
    List movies by their motion picture rating (e.g., PG-13, R).

    Example: GET /movies/rating?rating=PG-13
    """
    rating = request.args.get('rating')
    query = '''
        MATCH (m:Movie {motionPictureRating: $rating})
        RETURN m.title AS title, m.releaseYear AS releaseYear
    '''
    result = run_query(query, {"rating": rating})
    return jsonify(result)

# 7. Find Movies by Duration Range
@app.route('/movies/duration', methods=['GET'])
def find_movies_by_duration():
    """
    Find movies within a specified duration range.

    Example: GET /movies/duration?minDuration=90&maxDuration=120
    """
    min_duration = int(request.args.get('minDuration'))
    max_duration = int(request.args.get('maxDuration'))
    query = '''
        MATCH (m:Movie)
        WHERE m.runtime >= $minDuration AND m.runtime <= $maxDuration
        RETURN m.title AS title, m.runtime AS runtime
    '''
    result = run_query(query, {"minDuration": min_duration, "maxDuration": max_duration})
    return jsonify(result)

# 8. Recommend Movies by Release Year
@app.route('/movies/recommend/release-year', methods=['GET'])
def recommend_movies_by_release_year():
    """
    Recommend movies released in a specific year.

    Example: GET /movies/recommend/release-year?year=1994
    """
    year = int(request.args.get('year'))
    query = '''
        MATCH (m:Movie)
        WHERE m.releaseYear = $year
        RETURN m.title AS title, m.rating AS rating
    '''
    result = run_query(query, {"year": year})
    return jsonify(result)

# 9. Recommend Movies by Decade
@app.route('/movies/recommend/decade', methods=['GET'])
def recommend_movies_by_decade():
    """
    Recommend movies released within a specific decade.

    Example: GET /movies/recommend/decade?startYear=1980
    """
    start_year = int(request.args.get('startYear'))
    query = '''
        MATCH (m:Movie)
        WHERE m.releaseYear >= $startYear AND m.releaseYear < $startYear + 10
        RETURN m.title AS title, m.releaseYear AS releaseYear, m.rating AS rating
    '''
    result = run_query(query, {"startYear": start_year})
    return jsonify(result)


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user if route is not defined."""

    message = {
        "error": {
            "message": "This route is currently not supported.",
            "status_code": 404
        }
    }

    resp = jsonify(message)
    # Setting the status code to 404 (not found)
    resp.status_code = 404
    return resp

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
