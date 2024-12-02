# %%

# import the required libraries
import neo4j
import pandas as pd

# %%
# connect to the database
def connect_db():
    # driver = neo4j.GraphDatabase.driver(uri="neo4j://localhost:7687", auth=("neo4j","password"))
    driver = neo4j.GraphDatabase.driver(uri="bolt://neo4j:7687", auth=("neo4j","password"))
    session = driver.session(database="neo4j")
    return session

# %%
# wipe out the database    
def wipe_out_db(session):
    # wipe out database by deleting all nodes and relationships
    
    # similar to SELECT * FROM graph_db in SQL
    query = "match (node)-[relationship]->() delete node, relationship"
    session.run(query)
    
    query = "match (node) delete node"
    session.run(query)

session = connect_db()
wipe_out_db(session) 

# %%


# Load the dataset
file_path = './archive/IMDbMovies-Clean.csv' 
# use columns: Title	Summary	Director	Writer	Main Genres	Motion Picture Rating	Release Year	Runtime (Minutes)	Rating (Out of 10)	Number of Ratings (in thousands)
df = pd.read_csv(file_path, usecols=['Title', 'Summary', 'Director', 'Writer', 'Main Genres', 'Motion Picture Rating', 'Release Year', 'Runtime (Minutes)', 'Rating (Out of 10)', 'Number of Ratings (in thousands)'])


# Keep only unique movie titles
df_unique = df.drop_duplicates(subset=['Title'])

df_unique= df_unique[:1000] # limit to 1000 records

# Save the cleaned dataset to a new CSV file

df_unique.to_csv("./archive/IMDbMovies-CleanFinal.csv", index=False)




# %%

# create movie nodes
query = '''
    LOAD CSV WITH HEADERS FROM 'file:///IMDbMovies-CleanFinal.csv' AS row
    WITH row WHERE row.Title IS NOT NULL
    CREATE (m:Movie {
        title: row.Title,
        summary: coalesce(row.Summary, "Unknown"),
        motionPictureRating: coalesce(row.`Motion Picture Rating`, "Unknown"),
        releaseYear: coalesce(toInteger(row.`Release Year`), 0),
        runtime: coalesce(toInteger(row.`Runtime (Minutes)`), 0),
        rating: coalesce(toFloat(row.`Rating (Out of 10)`), 0.0),
        numRatings: coalesce(toFloat(row.`Number of Ratings (in thousands)`), 0.0)
    })
'''
session.run(query)


# %%
# create genre nodes
query = '''
    LOAD CSV WITH HEADERS FROM 'file:///IMDbMovies-CleanFinal.csv' AS row
    WITH row, split(row.`Main Genres`, ',') AS genres
    UNWIND genres AS genre
    WITH row, trim(genre) AS genre_name
    WHERE genre_name IS NOT NULL
    MERGE (g:Genre {name: genre_name})
    WITH g, row
    MATCH (m:Movie {title: row.Title})
    MERGE (m)-[:BELONGS_TO]->(g)
'''
session.run(query)


# %%
# create director nodes
query = '''
    LOAD CSV WITH HEADERS FROM 'file:///IMDbMovies-CleanFinal.csv' AS row
    WITH row, split(row.Director, ',') AS directors
    UNWIND directors AS director
    WITH row, trim(director) AS director_name
    WHERE director_name IS NOT NULL
    MERGE (d:Director {name: director_name})
    WITH d, row
    MATCH (m:Movie {title: row.Title})
    MERGE (m)-[:DIRECTED_BY]->(d)
'''
session.run(query)


# %%
# create writer nodes
query = '''
    LOAD CSV WITH HEADERS FROM 'file:///IMDbMovies-CleanFinal.csv' AS row
    WITH row, split(row.Writer, ',') AS writers
    UNWIND writers AS writer
    WITH row, trim(writer) AS writer_name
    WHERE writer_name IS NOT NULL
    MERGE (w:Writer {name: writer_name})
    WITH w, row
    MATCH (m:Movie {title: row.Title})
    MERGE (m)-[:WRITTEN_BY]->(w)
'''
session.run(query)


# %%
# close the session
session.close()



