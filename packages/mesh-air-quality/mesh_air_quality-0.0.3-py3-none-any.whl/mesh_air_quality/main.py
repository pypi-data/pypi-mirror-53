import grpc
from mesh_rpc.mesh import MeshRPC
from mesh_rpc.exp import MeshRPCException

from .lib.air_quality_pb2 import FeedMessage, DataPoint
from .defaults import Default

import dict_to_protobuf

class MeshAirQuality(MeshRPC):
    def __init__(self, endpoint='127.0.0.1:5555'):
        super().__init__(endpoint)

    def subscribe(self, geospace):
        s = super().subscribe(Default.topic, geospace)

        feed = FeedMessage()

        try:
            for msg in s:
                feed.ParseFromString(msg.raw)
                yield feed
        except grpc.RpcError as e:
            raise MeshRPCException(e.details())
    
    def registerToPublish(self, geospace):
        try:
            super().registerToPublish(Default.topic, geospace)
        except MeshRPCException as e:
            raise 

    def publish(self, geospace, d):
        d["header"]["air_quality_version"] = "0.0.1"
        
        feed = FeedMessage()

        dict_to_protobuf.dict_to_protobuf(d, feed)

        raw = feed.SerializeToString()

        try:
            res = super().publish(Default.topic, geospace, raw)
        except MeshRPCException as e:
            raise 
    
