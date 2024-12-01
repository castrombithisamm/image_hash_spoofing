import hashlib
from PIL import Image

def compute_hash(file_path):
    """Compute the SHA-512 hash of the file."""
    with open(file_path, "rb") as f:
        file_data = f.read()
    return hashlib.sha512(file_data).hexdigest()

def tweak_image(input_path, output_path, target_prefix):
    """
    Adjust the image to produce a hash with the specified prefix.
    This version modifies pixel data minimally.
    """
    img = Image.open(input_path)
    pixels = img.load()
    
    # Example adjustment: Modify the least significant bit of a pixel
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = pixels[x, y][:3]
            # Adjust red channel slightly (ensure it stays valid)
            new_r = (r + 1) % 256
            pixels[x, y] = (new_r, g, b)
            
            # Save and check the hash
            img.save(output_path)
            new_hash = compute_hash(output_path)
            if new_hash.startswith(target_prefix):
                print(f"Success! New hash: {new_hash}")
                return

    print("Failed to achieve the desired prefix with the adjustments.")

if __name__ == "__main__":
    input_image = "original.JPG"
    output_image = "altered.jpg"
    target_hash_prefix = "2448a6"
    
    print("Original hash:", compute_hash(input_image))
    tweak_image(input_image, output_image, target_hash_prefix)
    print("Altered hash:", compute_hash(output_image))
