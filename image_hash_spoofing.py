import hashlib
import random

def compute_hash(file_path):
    """Compute the hash of an image file using SHA-512."""
    sha512_hash = hashlib.sha512()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha512_hash.update(byte_block)
    return sha512_hash.hexdigest()

def modify_image_binary(image_path, target_prefix, max_attempts=100000):
    """Modify the image to make its hash start with the target_prefix."""
    # Read the original image binary
    with open(image_path, 'rb') as f:
        img_data = bytearray(f.read())

    original_hash = compute_hash(image_path)
    print(f"Original hash: {original_hash}")
    
    # Convert the target prefix (hex) to bytes
    target_prefix_bytes = bytes.fromhex(target_prefix[2:])  # Remove the '0x' prefix
    
    # Focus on modifying non-critical parts (e.g., metadata or less visible parts of the image)
    metadata_start = len(img_data) // 2  # Adjust starting point for modification, e.g., near end
    
    # Try to modify the image until the hash starts with the desired prefix
    attempt = 0
    while attempt < max_attempts:
        # Modify bytes in a safe region (e.g., metadata or unused sections)
        random_index = random.randint(metadata_start, len(img_data) - 1)
        original_byte = img_data[random_index]
        
        # Change the least significant bit of the byte
        img_data[random_index] = original_byte ^ 1  # Flip the least significant bit

        # Save the modified image to a temporary file
        modified_image_path = "altered.jpg"
        with open(modified_image_path, 'wb') as f:
            f.write(img_data)
        
        # Compute the hash of the modified image
        modified_hash = compute_hash(modified_image_path)
        
        # Check if the modified hash matches the desired prefix
        if modified_hash.startswith(target_prefix[2:]):
            print(f"Success! The modified image hash starts with {target_prefix}")
            print(f"Modified hash: {modified_hash}")
            return modified_image_path
        
        # Restore the original byte if hash doesn't match
        img_data[random_index] = original_byte
        attempt += 1

    print(f"Failed to generate a hash with the desired prefix after {max_attempts} attempts.")
    return None

def main():
    # Input the target hash prefix and the image to modify
    target_prefix = input("Enter target hex prefix (e.g., 0x24): ").strip()
    original_image = input("Enter the original image path (e.g., original.JPG): ").strip()
    
    modified_image_path = modify_image_binary(original_image, target_prefix)
    
    if modified_image_path:
        print(f"Modified image saved as: {modified_image_path}")
    else:
        print("Failed to generate an image with the desired hash prefix.")

if __name__ == "__main__":
    main()
