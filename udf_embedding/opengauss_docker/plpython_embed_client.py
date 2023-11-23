CREATE OR REPLACE FUNCTION
embed(slice text)
RETURNS FLOAT4[]
AS $$

# python

for arg in [slice]:
    if arg == "" or arg is None:
        return []


import pyarrow as pa
import pyarrow.flight as flight

class EmbeddingClient:
    def __init__(self, host='localhost', port=8815):
        self.client = flight.FlightClient(f"grpc://{host}:{port}")
        
    def embed(self, str):
        data = pa.Table.from_arrays([pa.array([str])], names=["str"])
        batches = data.to_batches(max_chunksize=512)
        
        with self.client as client:
            flight_info = flight.FlightDescriptor.for_path(b"embed")
            writer, reader = client.do_exchange(descriptor=flight_info)
            with writer:
                writer.begin(schema=data.schema)
                for batch in batches:
                    writer.write_batch(batch)
                writer.done_writing()

                chunk = reader.read_chunk()
                embedding = chunk.data.column("output").to_pylist()[0]
                return embedding
            
client = EmbeddingClient()
embedding = client.embed(slice)
# end python

return embedding 
$$ LANGUAGE plpython3u;