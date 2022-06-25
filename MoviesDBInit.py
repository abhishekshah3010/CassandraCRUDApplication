import gzip
import sys
from DBConnect import DBConnect as db

class MoviesDBInit:

    def __init__(self, ip, port, maxCount) -> None:
        self.cluster, self.session = None, None
        try:
            self.maxCount = int(maxCount)
            self.cluster, self.session = db(ip, port).getDBSession()
            self.dropTMoviesTable()
            self.createKeySpace()
            self.createMoviesTable()
            self.readFromFileAndInsertToTable()
            print('Data insterted successfully to table')
        except Exception as e:
            print('Error! ',e)
        finally:
            if self.cluster:
                self.cluster.shutdown()

    def createKeySpace(self):
        ksQuery = "CREATE KEYSPACE IF NOT EXISTS movies_ks WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor':'1'};"
        self.session.execute(ksQuery)
        self.session.execute('USE movies_ks')

    def createMoviesTable(self):
        self.session.execute('CREATE TABLE IF NOT EXISTS movies (movie_id int PRIMARY KEY, titleType text, primaryTitle text, originalTitle text, isAdult int, startYear int, endYear int, runtimeMinutes float, genre list<text>)')

    def dropTMoviesTable(self):
        return self.session.execute('DROP TABLE IF EXISTS movies_ks.movies')

    def insertMovieDataToTable(self, data, insertQuery):
        data[0] = int(data[0][2:])
        data[2] = data[2] if data[2] and data[2] != '' else 'None'
        data[3] = data[3] if data[3] and data[3] != '' else 'None'
        data[4] = int(data[4]) if data[4] and data[4] != '\\N' else 0
        data[5] = int(data[5]) if data[5] and data[5] != '\\N' else 0
        data[6] = int(data[6]) if data[6] and data[6] != '\\N' else 0
        data[7] = float(data[7]) if data[7] and data[7] != '\\N' else 0
        data[8] = data[8].split(',') if data[8] and data[8] != '\\N' else []
        insertQuery = insertQuery.replace('<MOVIE_ID>',str(data[0])).replace('<PRIMARY_TITLE>',str(data[2])).replace('<ORIGINAL_TITLE>',str(data[3])).replace('<IS_ADULT>',str(data[4])).replace('<START_YEAR>',str(data[5])).replace('<END_YEAR>',str(data[6])).replace('<RUNTIME>',str(data[7])).replace('<GENRE>',str(data[8]))
        self.session.execute(insertQuery)
                

    def readFromFileAndInsertToTable(self):
        insertQuery = "INSERT INTO movies (movie_id, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genre) VALUES(<MOVIE_ID>, 'movie', $$<PRIMARY_TITLE>$$,$$<ORIGINAL_TITLE>$$,<IS_ADULT>,<START_YEAR>,<END_YEAR>,<RUNTIME>,<GENRE>)"
        count = 0
        with gzip.open('title.basics.tsv.gz') as lines:
            lines.readline()
            for line in lines:
                if self.maxCount > 0 and count == self.maxCount: break
                data = line.decode('UTF-8').strip().split('\t')
                if data[1].lower() == 'movie':
                    print(count,' => ',data)
                    self.insertMovieDataToTable(data, insertQuery)
                    count+=1


def main():
    args = sys.argv[1:]
    if len(args) == 3:
        MoviesDBInit(args[0],args[1],args[2])
    else:
        print('Error!')

if __name__=='__main__':
    main()
        
