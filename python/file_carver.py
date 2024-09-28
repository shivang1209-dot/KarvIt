import argparse
import os

# Define headers for each file type
FILE_HEADERS = {
    'png': bytes([0x89, 0x50, 0x4e, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
    'jpeg': bytes([0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46]),
    'pdf': bytes([0x25, 0x50, 0x44, 0x46, 0x2D, 0x31, 0x2E]),
    'evtx': bytes([0x45, 0x6C, 0x66, 0x46, 0x69, 0x6C, 0x65])
}

# Define footers for each file type
FILE_FOOTERS = {
    'png': bytes([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]),
    'jpeg': bytes([0xFF, 0xD9]),
    'pdf': bytes([0x25, 0x25, 0x45, 0x4F, 0x46]),
    'evtx': bytes([0x68, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x68, 0x03, 0x00, 0x00])
}

def carve_files(src_file, dst_dir, file_type):
    """
    Carves specific file types (png, jpeg, pdf, evtx) from a disk image.

    Parameters:
    src_file (str): Path to the disk image file (e.g., .img, .iso, .dd)
    dst_dir (str): Directory to save the carved files
    file_type (str): The type of files to carve ('png', 'jpeg', 'pdf', 'evtx')
    """
    print(f"Carving {file_type.upper()} files from {src_file}...")

    header = FILE_HEADERS[file_type]
    footer = FILE_FOOTERS[file_type]
    chunk_size = 1024 * 1024  # 1 MB chunks for efficient reading
    count = 0
    leftover = b''  # To handle cases where data crosses chunks

    # Ensure destination directory exists
    os.makedirs(dst_dir, exist_ok=True)

    with open(src_file, "rb") as file:
        while True:
            chunk = leftover + file.read(chunk_size)
            if not chunk:
                break  # End of file

            header_index = chunk.find(header)
            while header_index != -1:
                footer_index = chunk.find(footer, header_index)
                if footer_index != -1:
                    count += 1
                    # Carve the data between header and footer
                    dst_data = chunk[header_index:footer_index + len(footer)]
                    dst_file_name = os.path.join(dst_dir, f"carved_{file_type}_{count}.{file_type}")
                    with open(dst_file_name, "wb") as dst_file:
                        dst_file.write(dst_data)
                    print(f"Carved: {dst_file_name}")

                    # Move past the current footer to find more files
                    header_index = chunk.find(header, footer_index + len(footer))
                else:
                    # No complete footer in current chunk; carry leftover to next
                    leftover = chunk[header_index:]
                    break

            if header_index == -1:
                leftover = b''  # Reset leftover if no header found in this chunk

    print(f"Successfully carved {count} {file_type.upper()} files.")


def main():
    """
    Main function to parse arguments and invoke file carving process.
    """
    parser = argparse.ArgumentParser(
        description="File Carving Tool to extract specific file types from disk images. "
                    "Supported file types: png, jpeg, pdf, evtx."
    )
    parser.add_argument(
        '--file', required=True, help="Path to the disk image file (e.g., .img, .iso, .dd)"
    )
    parser.add_argument(
        '--type', choices=['png', 'jpeg', 'pdf', 'evtx'], required=True, help="Type of files to carve (png, jpeg, pdf, evtx)"
    )
    parser.add_argument(
        '--output-dir', default="./carved_files", help="Directory to save the carved files (default: ./carved_files)"
    )
    parser.add_argument(
        '--example', help="python3 file_carver.py --file=image.img --type=png"
    )

    args = parser.parse_args()

    # Start the carving process based on user inputs
    carve_files(args.file, args.output_dir, args.type)


if __name__ == "__main__":
    main()
