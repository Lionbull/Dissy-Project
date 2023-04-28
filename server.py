from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sqlite3

# Notifying the server owner that the server has started
print("Server started")

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
        
    
    def example(example):
        """Checks if a topic exists in the database"""

        return example
    
    server.register_function(example, "example")


    # Run the server's main loop
    server.serve_forever()