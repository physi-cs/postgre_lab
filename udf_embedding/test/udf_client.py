import pyarrow as pa
import pyarrow.flight as flight

class EmbeddingClient:
    def __init__(self, host='localhost', port=8815):
        self.client = flight.FlightClient(f"grpc://{host}:{port}")
        
    def test_gcd(self):
        LEN = 64
        data = pa.Table.from_arrays(
            [pa.array(range(0, LEN)), pa.array(range(0, LEN))], names=["x", "y"]
        )

        batches = data.to_batches(max_chunksize=512)

        with self.client as client:
            flight_info = flight.FlightDescriptor.for_path(b"gcd")
            writer, reader = client.do_exchange(descriptor=flight_info)
            with writer:
                writer.begin(schema=data.schema)
                for batch in batches:
                    writer.write_batch(batch)
                writer.done_writing()

                chunk = reader.read_chunk()
                # print(len(chunk))
                print(chunk.data.column("output"))
                
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
                print(embedding)

if __name__ == '__main__':
    client = EmbeddingClient()
    # Example usage
    # client.test_gcd()
    client.embed('hello world')
