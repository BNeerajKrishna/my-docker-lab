from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'movies.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    conn.close()
    return jsonify([dict(movie) for movie in movies])

@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
    movie = cursor.fetchone()
    conn.close()
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(dict(movie))

@app.route('/movies', methods=['POST'])
def add_movie():
    new_movie = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO movies (title, year, genre, director, plot)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        new_movie['title'],
        new_movie.get('year'),
        new_movie.get('genre'),
        new_movie.get('director'),
        new_movie.get('plot')
    ))
    conn.commit()
    conn.close()
    return jsonify(new_movie), 201

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    updated_movie = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE movies
        SET title = ?, year = ?, genre = ?, director = ?, plot = ?
        WHERE id = ?
    ''', (
        updated_movie['title'],
        updated_movie.get('year'),
        updated_movie.get('genre'),
        updated_movie.get('director'),
        updated_movie.get('plot'),
        movie_id
    ))
    conn.commit()
    conn.close()
    return jsonify(updated_movie)

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Movie deleted'})

if __name__ == '__main__':
    app.run(debug=True)
