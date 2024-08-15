from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),  # Default to 'db' if environment variable is not set to any
    'port': int(os.getenv('DB_PORT', 3306)),  # Default to 3306
    'user': os.getenv('DB_USER', 'root'),  # Default to 'root'
    'password': os.getenv('DB_PASSWORD', 'mysecretpassword'),  # Default to 'mysecretpassword'
    'database': os.getenv('DB_NAME', 'movies_db')  # Default to 'movies_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table_if_not_exists():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                year VARCHAR(4),
                genre VARCHAR(255),
                director VARCHAR(255),
                plot TEXT
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

with app.app_context():
    create_table_if_not_exists()

@app.route('/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM movies')
        movies = cursor.fetchall()
    except Error as e:
        print(f"Database query error: {e}")
        return jsonify({'error': 'Database query failed'}), 500
    finally:
        conn.close()
    return jsonify(movies)

@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM movies WHERE id = %s', (movie_id,))
        movie = cursor.fetchone()
    except Error as e:
        print(f"Database query error: {e}")
        return jsonify({'error': 'Database query failed'}), 500
    finally:
        conn.close()
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(movie)

@app.route('/movies', methods=['POST'])
def add_movie():
    new_movie = request.json
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movies (title, year, genre, director, plot)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            new_movie['title'],
            new_movie.get('year'),
            new_movie.get('genre'),
            new_movie.get('director'),
            new_movie.get('plot')
        ))
        conn.commit()
    except Error as e:
        print(f"Database query error: {e}")
        return jsonify({'error': 'Database query failed'}), 500
    finally:
        conn.close()
    return jsonify(new_movie), 201

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    updated_movie = request.json
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE movies
            SET title = %s, year = %s, genre = %s, director = %s, plot = %s
            WHERE id = %s
        ''', (
            updated_movie['title'],
            updated_movie.get('year'),
            updated_movie.get('genre'),
            updated_movie.get('director'),
            updated_movie.get('plot'),
            movie_id
        ))
        conn.commit()
    except Error as e:
        print(f"Database query error: {e}")
        return jsonify({'error': 'Database query failed'}), 500
    finally:
        conn.close()
    return jsonify(updated_movie)

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movies WHERE id = %s', (movie_id,))
        conn.commit()
    except Error as e:
        print(f"Database query error: {e}")
        return jsonify({'error': 'Database query failed'}), 500
    finally:
        conn.close()
    return jsonify({'message': 'Movie deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
