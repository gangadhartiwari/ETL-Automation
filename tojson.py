import base64
import json
import zlib
from Crypto.Cipher import AES

# -----------------------------
# Functions
# -----------------------------

def decrypt_data(data: str, key: str) -> str:
    """
    Decrypt AES-CBC with PKCS7 padding, key and IV are same.
    Equivalent to C# RijndaelManaged logic.
    """
    key_bytes = key.encode('utf-8')
    key_bytes = key_bytes[:16].ljust(16, b'\0')  # Ensure 16 bytes

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=key_bytes)
    encrypted_bytes = base64.b64decode(data)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    
    # Remove PKCS7 padding
    pad_len = decrypted_bytes[-1]
    decrypted_bytes = decrypted_bytes[:-pad_len]
    return decrypted_bytes.decode('utf-8')

def decompress_data(data: str) -> str:
    """
    Decompress base64 zlib/deflate string (like DeflateStream in C#)
    """
    compressed_bytes = base64.b64decode(data)
    decompressed_bytes = zlib.decompress(compressed_bytes, -zlib.MAX_WBITS)
    return decompressed_bytes.decode('utf-8')

# -----------------------------
# Main
# -----------------------------

# 1️⃣ Read the encrypted string from TXT file
with open(r"C:/Users/synchem/Desktop/MargtoSQL/api_response.txt", "r", encoding="utf-8") as f:
    encrypted_string = f.read().strip()

# 2️⃣ Provide your decryption key
decryption_key = "9YR2PJ8WOE3Y"

# 3️⃣ Decrypt
decrypted = decrypt_data(encrypted_string, decryption_key)

# 4️⃣ Decompress
decompressed = decompress_data(decrypted)

if decompressed.startswith('\ufeff'):
    decompressed = decompressed.replace('\ufeff', '', 1)

data = json.loads(decompressed)

# 5️⃣ Save to JSON file
with open(r"C:/Users/synchem/Desktop/MargtoSQL/decrypted_output.json", "w", encoding="utf-8") as f:
    json.dump(json.loads(decompressed), f, indent=4)

print(" Decryption and decompression complete. JSON saved as 'decrypted_output.json'.")
