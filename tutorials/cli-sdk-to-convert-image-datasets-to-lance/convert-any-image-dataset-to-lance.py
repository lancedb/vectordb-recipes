import os
import argparse
import pandas as pd
import pyarrow as pa
import lance
import time
from tqdm import tqdm


def process_images(images_folder, split, schema):
    # Iterate over the categories within each data type
    label_folder = os.path.join(images_folder, split)
    for label in os.listdir(label_folder):
        label_folder = os.path.join(images_folder, split, label)

        # Iterate over the images within each label
        for filename in tqdm(
            os.listdir(label_folder), desc=f"Processing {split} - {label}"
        ):
            # Construct the full path to the image
            image_path = os.path.join(label_folder, filename)

            # Read and convert the image to a binary format
            with open(image_path, "rb") as f:
                binary_data = f.read()

            image_array = pa.array([binary_data], type=pa.binary())
            filename_array = pa.array([filename], type=pa.string())
            label_array = pa.array([label], type=pa.string())
            split_array = pa.array([split], type=pa.string())

            # Yield RecordBatch for each image
            yield pa.RecordBatch.from_arrays(
                [image_array, filename_array, label_array, split_array], schema=schema
            )


# Function to write PyArrow Table to Lance dataset
def write_to_lance(images_folder, dataset_name, schema):
    for split in ["train", "test", "val"]:
        lance_file_path = os.path.join(images_folder, f"{dataset_name}_{split}.lance")

        reader = pa.RecordBatchReader.from_batches(
            schema, process_images(images_folder, split, schema)
        )
        lance.write_dataset(
            reader,
            lance_file_path,
            schema,
        )


def loading_into_pandas(images_folder, dataset_name):
    data_frames = {}  # Dictionary to store DataFrames for each data type

    batch_size = args.batch_size
    for split in ["test", "train", "val"]:
        uri = os.path.join(images_folder, f"{dataset_name}_{split}.lance")

        ds = lance.dataset(uri)

        # Accumulate data from batches into a list
        data = []
        for batch in tqdm(
            ds.to_batches(
                columns=["image", "filename", "label", "split"], batch_size=batch_size
            ),
            desc=f"Loading {split} batches",
        ):
            tbl = batch.to_pandas()
            data.append(tbl)

        # Concatenate all DataFrames into a single DataFrame
        df = pd.concat(data, ignore_index=True)

        # Store the DataFrame in the dictionary
        data_frames[split] = df

        print(f"Pandas DataFrame for {split} is ready")
        print("Total Rows: ", df.shape[0])

    return data_frames


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process image dataset.")
    parser.add_argument(
        "--batch_size", type=int, default=10, help="Batch size for processing images"
    )
    parser.add_argument("--dataset", type=str, help="Path to the image dataset folder")

    try:
        args = parser.parse_args()
        dataset_path = args.dataset
        if dataset_path is None:
            raise ValueError(
                "Please provide the path to the image dataset folder using the --dataset argument."
            )

        # Extract dataset name
        dataset_name = os.path.basename(dataset_path)

        start = time.time()
        schema = pa.schema(
            [
                pa.field("image", pa.binary()),
                pa.field("filename", pa.string()),
                pa.field("label", pa.string()),
                pa.field("split", pa.string()),
            ]
        )
        write_to_lance(dataset_path, dataset_name, schema)
        data_frames = loading_into_pandas(dataset_path, dataset_name)
        end = time.time()
        print(f"Time(sec): {end - start:.2f}")

    except ValueError as e:
        print(e)
        print("Example:")
        print(
            "python3 convert-any-image-dataset-to-lance.py --batch_size 10 --dataset image_dataset_folder"
        )
        exit(1)

    except FileNotFoundError:
        print("The provided dataset path does not exist.")
        exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)
