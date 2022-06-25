from flask import Flask, request
from MoviesAPIService import MoviesAPIService as mAS
from DBConnect import DBConnect as dbConnect
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Movies API',
    description='An API to add/update/delete and search movies.',
)
cluster, session = dbConnect('127.0.0.1',9042).getDBSession()
session.execute('USE movies_ks')
mas = mAS(session)
movie = api.model('Movie', {
    'movie_id': fields.Integer,
    'titleType': fields.String,
    'primaryTitle': fields.String,
    'originalTitle': fields.String,
    'isAdult': fields.Integer,
    'startYear': fields.Integer,
    'endYear': fields.Integer,
    'runtimeMinutes': fields.Float,
    'genre': fields.List(fields.String)
})


@api.route('/imdb/get-all-movies')
class GetAllMovies(Resource):
    def get(self):
        return mas.getAllMovies()

@api.route('/imdb/get-movie-by-id/<movie_id>')
@api.doc(params={'movie_id': 'Movie ID'})
class GetMovieById(Resource):
    def get(self, movie_id):
        return mas.getMovieById(movie_id)

@api.route('/imdb/get-movie-by-title/<title>')
@api.doc(params={'title': 'Movie title'})
class GetMovieByTitle(Resource):
    def get(self, title):
        return mas.getMovieByTitle(title)

@api.route('/imdb/add-movie/')
class AddMovie(Resource):
    @api.expect(movie)
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            movie = request.json
            if mas.validate(movie):
                print('Validated')
                return mas.addMovie(movie)
            else:
                return 'Movie object not valid'
        else:
            return 'Content-Type not supported!'

@api.route('/imdb/update-movie/')
class UpdateMovie(Resource):
    @api.expect(movie)
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            movie = request.json
            if mas.validate(movie):
                print('Validate')
                return mas.updateMovie(movie)
        else:
            return 'Content-Type not supported!'

@api.route('/imdb/delete-movie/<movie_id>')
@api.doc(params={'movie_id': 'Movie Id'})
class DeleteMovie(Resource):
    def get(self, movie_id):
        return mas.deleteTitle(movie_id)

if __name__ == '__main__':
    app.run(debug=True)