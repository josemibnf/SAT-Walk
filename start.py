import grpc, time
from concurrent import futures
import walksat
from api_pb2 import Interpretation
import api_pb2_grpc

class Solver(api_pb2_grpc.Solver):
    def Solve(self, request, context):
        return walksat.ok( cnf = request)

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))

api_pb2_grpc.add_SolverServicer_to_server(
    Solver(), server=server
)

print('Starting server. Listening on port 8080.')
server.add_insecure_port('[::]:8080')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)