import lance
import pyarrow as pa

def producer():
    yield pa.RecordBatch.from_pylist([{"name": "Alice", "age": 20}])
    yield pa.RecordBatch.from_pylist([{"name": "Blob", "age": 30}])

# schema = pa.schema([
#             pa.field("name", pa.string()),
#             pa.field("age", pa.int32()),
#         ])

lance.write_dataset(producer, "./alice_and_bob.lance")