# Image Hash Spoofing Tool

## Problem Statement
This Python tool modifies the binary data of an image so that its SHA-512 hash starts with a user-specified hexadecimal prefix, while ensuring the image remains visually unchanged. The modification is achieved by making small adjustments to the binary data of the image, specifically in non-visual parts (like metadata), until the hash meets the required conditions.

For example, if you input:
```bash
0x24 original.jpg
```
The tool should modify `original.jpg` and create `altered.jpg` such that when you run:
```bash
sha512sum altered.jpg
```
The output hash starts with `24`.

## Solution Overview
This script iteratively modifies the binary content of an image by flipping the least significant bit (LSB) of random bytes in a non-critical section of the file (such as image metadata or other areas not affecting visual content). This process continues until the SHA-512 hash of the altered image matches the desired prefix.

### Key Challenges and Solutions:
1. **Ensuring the Image is Unaltered Visually**:
   The key challenge was to modify the image without affecting its visual representation. This is achieved by only altering bytes that do not contribute to the rendering of the image (e.g., metadata or other auxiliary sections).

2. **Generating the Correct Hash**:
   The main objective is to generate a SHA-512 hash that starts with a specific hexadecimal prefix. This is done by repeatedly modifying random bytes in the non-visual section and recalculating the hash until the prefix matches the user input.

3. **Performance Considerations**:
   Due to the nature of hashing, modifying even a single byte changes the hash completely. The tool uses a trial-and-error approach to test different small modifications efficiently until it finds one that works. The number of attempts is limited by a user-defined `max_attempts` parameter.

## How It Works
- The user provides an image file and a hexadecimal target prefix.
- The tool computes the SHA-512 hash of the image.
- It modifies non-critical parts of the image (e.g., metadata) by flipping bits, saving a new copy each time.
- After each modification, the hash is recalculated. If the hash starts with the required prefix, the modified image is saved.

### Code Details
- **`compute_hash(file_path)`**: This function computes the SHA-512 hash of the input file.
- **`modify_image_binary(image_path, target_prefix)`**: This function iteratively modifies the image until the SHA-512 hash starts with the target prefix. It modifies only non-visual parts of the image to maintain visual fidelity.
- **`main()`**: The entry point for user interaction, which handles inputs and calls the appropriate functions.

## Usage Instructions

### Prerequisites:
- Python 3.x
- hashlib (Python standard library)
- random (Python standard library)

### Setup:
No external dependencies are required for this script. Just clone the repository, navigate to the project directory, and run the Python script.

### Running the Tool:
```bash
python3 image_hash_spoofing.py
```

The script will prompt for:
1. A target hex prefix (e.g., `0x24`).
2. The path to the original image (e.g., `original.jpg`).

The modified image will be saved as `altered.jpg` in the current directory.

### Example:
```bash
$ python3 image_hash_spoofing.py
Enter target hex prefix (e.g., 0x24): 0x24
Enter the original image path (e.g., original.JPG): original.JPG
Original hash: f7c4a711d72f790409f1967d7832b9105f20f62b716f3ece4cae8b21a553a6c4fb69d7f3acf54a4f59a6faaa8f82cf9f935133c4d456792e99bd0574db34ca52
Success! The modified image hash starts with 0x24
Modified hash: 24c13dce164d3a625b57e7f9976fcf28456a38a09124acd0d01d42e3deb511492fd945fccf609fe05b74d23d180300fdb76a5c19cda32ad80a02e0772c0e415
Modified image saved as: altered.jpg
```

### Limitations:
- The current implementation limits the number of modification attempts to 100,000 (`max_attempts`). This can be adjusted as needed, though higher limits may lead to longer runtimes.
- Modifications are restricted to non-visual sections, which may limit the effectiveness in highly compressed or minimalistic image files.

## Lessons Learned
This problem presented an interesting challenge in manipulating the non-visual portions of a file without corrupting it. Additionally, the project demonstrates how even tiny changes in file contents can lead to vastly different hash values.

## Future Work
- **Support for More Hash Functions**: Extend the tool to allow the user to choose from a variety of hash algorithms.
- **More Targeted Modifications**: Investigate more precise techniques for modifying specific metadata regions to reduce the number of attempts required.
