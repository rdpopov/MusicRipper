#!/usr/bin/python3

from grpc_requests import StubClient
from helloworld_pb2 import DESCRIPTOR




# NOTE: this might be better asa a singleton
class MetadataManager():
    def __init__(self):
        # self.__client = StubClient.get_by_endpoint("localhost:50051",service_descriptors=[service_descriptor,])
        service_descriptor = DESCRIPTOR.services_by_name['Greeter'] # or you can just use _GREETER
        client = StubClient.get_by_endpoint("localhost:50051",service_descriptors=[service_descriptor,])
        # NOTE: this is very specific, can be made generic but dont wanna bother
        assert client.service_names == ["helloworld.Greeter"]
        self.__service = client.service("helloworld.Greeter")

    def QueryCachedMetadata(self,song_name):
        req = {"song_name": song_name}
        res = self.__service.QueryMeta(req)
        print(res)
        return res

    def AddMeta(self,song_meta : dict):
        res = self.__service.AddMeta(song_meta)
        print(res)

    def SongAddIfNotExist(self,song_meta):
        res = self.QueryCachedMetadata(song_meta['fname'])
        if res['fname'] == "None":
            print('added meta')
            self.AddMeta(song_meta)




t = MetadataManager()

song_meta = {
        "fname": "Wildfire.mp3",
        "name": "Wildfire",
        "artist": "ATC",
        "album": "LEC",
        "artwork": "Wildfire.jpg",
        "lyrics": "ala bala"
}

t.SongAddIfNotExist(song_meta)


