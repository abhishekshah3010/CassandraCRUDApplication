#docker run -p 127.0.0.1:9042:9042 --name cassandra -d cassandra
#docker restart/stop cassandra
#docker exec -it cassandra cqlsh
import json

class MoviesDAO:

    def __init__(self, session) -> None:
        self.session = session
    
    def getMovieById(self, id):
        searchQuery = 'SELECT JSON * FROM movies WHERE movie_id='+id
        rs = self.session.execute(searchQuery)
        if rs:
            return [json.loads(row[0]) for row in rs]
        return 'No results found for id: '+id
    
    def getAllMovies(self):
        searchQuery = 'SELECT JSON * FROM movies'
        rs = self.session.execute(searchQuery)
        if rs:
            return [json.loads(row[0]) for row in rs]
        return 'Table is empty'


    def searchMovieByTitle(self, title):
        searchQuery = 'SELECT JSON * FROM movies WHERE primaryTitle = \''+title+'\' ALLOW FILTERING;'
        print(searchQuery)
        rs = self.session.execute(searchQuery)
        if rs:
            return [json.loads(row[0]) for row in rs]
        return 'No result found for title: '+title

    def deleteMovie(self, id):
        deleteQuery = 'DELETE FROM movies WHERE movie_id='+id
        rs = self.session.execute(deleteQuery)
        return 'Sucessfully deleted movie with movie_id: '+id
    
    def addMovieDetails(self, movie):
        movies = self.getMovieById(str(movie['movie_id']))
        if movies == 'No results found for id: '+str(movie['movie_id']):
            return self.insert(movie)
        return 'Movie with id:'+str(movie['movie_id'])+' already present.'
    
    def updateMovieDetails(self, movie):
        movies = self.getMovieById(str(movie['movie_id']))
        if movies != 'No results found for id: '+str(movie['movie_id']):
            return self.update(movie)
        return 'Movie with details '+movie+' not present'
    
    def insert(self, movie):
        insertQuery = "INSERT INTO movies (movie_id, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genre) VALUES(<MOVIE_ID>, 'movie', $$<PRIMARY_TITLE>$$,$$<ORIGINAL_TITLE>$$,<IS_ADULT>,<START_YEAR>,<END_YEAR>,<RUNTIME>,<GENRE>)"
        insertQuery = insertQuery.replace('<MOVIE_ID>',str(movie['movie_id'])).replace('<PRIMARY_TITLE>',str(movie['primaryTitle'])).replace('<ORIGINAL_TITLE>',str(movie['originalTitle'])).replace('<IS_ADULT>',str(movie['isAdult'])).replace('<START_YEAR>',str(movie['startYear'])).replace('<END_YEAR>',str(movie['endYear'])).replace('<RUNTIME>',str(movie['runtimeMinutes'])).replace('<GENRE>',str(movie['genre']))
        self.session.execute(insertQuery)
        return movie

    def update(self, movie):
        updateQuery = "UPDATE movies SET titleType = 'movie', primaryTitle = $$<PRIMARY_TITLE>$$, originalTitle = $$<ORIGINAL_TITLE>$$, isAdult = <IS_ADULT>, startYear = <START_YEAR>, endYear = <END_YEAR>, runtimeMinutes = <RUNTIME>, genre = <GENRE> WHERE movie_id = "+str(movie['movie_id'])
        updateQuery = updateQuery.replace('<PRIMARY_TITLE>',str(movie['primaryTitle'])).replace('<ORIGINAL_TITLE>',str(movie['originalTitle'])).replace('<IS_ADULT>',str(movie['isAdult'])).replace('<START_YEAR>',str(movie['startYear'])).replace('<END_YEAR>',str(movie['endYear'])).replace('<RUNTIME>',str(movie['runtimeMinutes'])).replace('<GENRE>',str(movie['genre']))
        self.session.execute(updateQuery)
        return movie