import os
import tarfile


def tar_directories(src_dir, output_dir):
    # Get a list of all directories in the source directory
    directories = [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]

    # Create tar archives for each directory
    for directory in directories:
        input_path = os.path.join(src_dir, directory)
        output_filename = os.path.join(output_dir, f"{directory}.tar")

        with tarfile.open(output_filename, "w") as tar:
            tar.add(input_path, arcname="")

if __name__ == "__main__":
    source_directory = input("/path/to/source\n")
    output_directory = input("/path/to/output\n")

    tar_directories(source_directory, output_directory)
    print("Tar archives created successfully.")
