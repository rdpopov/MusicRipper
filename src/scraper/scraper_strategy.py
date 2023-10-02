class ProxyAdressDbSchema:
    proxy_addr_table = """ CREATE TABLE IF NOT EXISTS ip (
            ip_addr text PRIMARY KEY,
            useful integer
            );"""

class ScraperStrategyInt:
    def __init__(self,dbConnect):
        conn = sqlite3.connect(ProxyAdressDbSchema.proxy_addr_table)
        if conn is not None:
            conn.execute(ProxyAdressDbSchema.proxy_addr_table)
        else:
            print("Error! cannot create the database connection.")
        self.connection = conn

    def get(self,filename:str) -> dict:
        # TODO: implement
        return {}
    def fnameCleanup(str):
        # TODO: implement
        pass

class GeniusLyricsScraper(ScraperStrategyInt):
    def get(self,filename:str) -> dict:
        # TODO: implement
        return {}
    def fnameCleanup(self):
        # TODO: implement
        pass

class AzlDiscogsScraper(ScraperStrategyInt):
    def get(self,filename:str) -> dict:
        # TODO: implement
        return {}
    def fnameCleanup(self):
        # TODO: implement
        pass
