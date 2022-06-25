from cassandra.cluster import Cluster

class DBConnect:
    def __init__(self, ip, port) -> None:
        self.cluster = Cluster([ip], port=port)
        self.session = self.cluster.connect()
    
    def getDBSession(self):
        return self.cluster, self.session
    
    def closeConnection(self):
        if self.cluster:
            self.cluster.shutdown()