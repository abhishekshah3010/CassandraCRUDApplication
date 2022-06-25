#docker run -p 127.0.0.1:9042:9042 --name cassandra -d cassandra
#docker restart cassandra
from MoviesDAO import MoviesDAO as mDAO

class MoviesAPIService:

    def __init__(self, session) -> None:
        self.mDAO = mDAO(session)
    
    def getAllMovies(self):
        return self.mDAO.getAllMovies()
    
    def getMovieById(self, id):
        return self.mDAO.getMovieById(id)
    
    def getMovieByTitle(self, title):
        return self.mDAO.searchMovieByTitle(title)
    
    def deleteTitle(self, id):
        return self.mDAO.deleteMovie(id)
    
    def addMovie(self, movie):
        return self.mDAO.addMovieDetails(movie)

    def updateMovie(self, movie):
        return self.mDAO.updateMovieDetails(movie)
    
    def validate(self, movie):
        if movie and movie.get('movie_id'):
            return True
        return False