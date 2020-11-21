import logging
import grpc
from rpc.pubsub_pb2 import mes2client, mes2server
from rpc.pubsub_pb2_grpc import pubsubStub

def run():
    # 创建通信信道
    with grpc.insecure_channel('localhost:50000') as channel:
        # 客户端通过stub来实现rpc通信
        stub = pubsubStub(channel)
        # 客户端必须使用定义好的类型
        while 1:
            try:	    
                mes = stub.pubsubServe(mes2server(mes1='client'), timeout=500)
                print(mes)
	    # 遇到ctrl+c时推出
            except KeyboardInterrupt:
                exit(0)

if __name__ == "__main__":
    logging.basicConfig()
    run()
