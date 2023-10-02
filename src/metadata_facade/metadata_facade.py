class MetadataFacade:
    def __init__(self):
        self.connection = None # open db connection

    def isInDb(self, song_fname:str) -> dict | None :
        if self.connection is not None:
        return None

    def isInDb(self, ytId:str) -> dict | None :
        if self.connection is not None:
        return None

    def putInDb(self, song:dict):
        # query db for the song id
        # TODO: implement
        self.connection = None

    def scrape(self, scrapeStrategy, fname:str) -> dict:
        # query db for the song id
        # TODO: implement
        scraper = scrapeStrategy()
        contents = scraper.get()
        self.putInDb(contents)
        return contents
