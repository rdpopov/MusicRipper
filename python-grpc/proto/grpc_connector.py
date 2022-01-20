#!/usr/bin/python3

from grpc_requests import StubClient
# import "./python-grpc/proto/helloworld_pb2.py"
from helloworld_pb2 import *




# NOTE: this might be better asa a singleton
class MetadataManager():
    def __init__(self):
        service_descriptor = DESCRIPTOR.services_by_name['Greeter'] # or you can just use _GREETER
        client = StubClient.get_by_endpoint("localhost:50051",service_descriptors=[service_descriptor,])
        # NOTE: this is very specific, can be made generic but dont wanna bother
        assert client.service_names == ["helloworld.Greeter"]
        self.__service = client.service("helloworld.Greeter")

    def QueryCachedMetadata(self,song_name:str) -> dict: 
        req = {"song_name": song_name}
        res = self.__service.QueryMeta(req)
        # print(res)
        return res

    def UpdateMeta(self,song_meta : dict) -> bool:
        res = self.__service.UpdateMeta(song_meta)
        # print(res)
        return bool(int(res['result']))

    def AddMeta(self,song_meta : dict) -> bool:
        res = self.__service.AddMeta(song_meta)
        # print(res)
        return bool(int(res['result']))


    ### Api methods end

    def SongAddIfNotExist(self,song_meta:dict) -> bool:
        res = self.QueryCachedMetadata(song_meta['fname'])
        if res['fname'] == "None":
            # print('added meta')
            res = self.AddMeta(song_meta)
                

    def UpdateMetaOrAdd(self,song_meta:dict) -> bool:
        res = self.QueryCachedMetadata(song_meta['fname'])
        if res['fname'] == "None":
            # print('added meta')
            self.AddMeta(song_meta)
        else:
            self.UpdateMeta(song_meta)

if __name__ == "__main__":
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
    song_meta = {
            "fname": "Wildfire.mp3",
            "name": "Wildfireeeeee",
            "artist": "ATC",
            "album": "LEC",
            "artwork": "Wildfire.jpg",
            "lyrics": "ala bala portokala"
    }
    t.UpdateMetaOrAdd(song_meta)
    t.QueryCachedMetadata(song_meta['fname'])
