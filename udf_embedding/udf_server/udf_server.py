# Import components from the risingwave.udf module
from risingwave.udf import udf, udtf, UdfServer
from remote_embed import RemoteEmbedingClient

import pyarrow.flight as flight


# Define a scalar functio that returns a single value
@udf(input_types=['INT', 'INT'], result_type='INT')
def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x

# pgvector中的VECTOR实现是单精度浮点数
@udf(input_types=['VARCHAR'], result_type='FLOAT4[]')
def embed(str):
    embedding = RemoteEmbedingClient().do_embed(str)
    return embedding

# Start a UDF server
if __name__ == '__main__':
    server = UdfServer(location="0.0.0.0:8815") # You can use any available port in your system. Here we use port 8815.
    server.add_function(gcd)
    server.add_function(embed)
    server.serve()
