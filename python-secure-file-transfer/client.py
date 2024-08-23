import os
import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes

PORT = 4444
BUFF_SIZE = 1024
ENCODING = 'utf-8'
IP_ADDR = 'localhost'
RSA_KEY_LENGTH = 3072
PWD = b'I like turtles'  # TODO: load from a file (encrypted one)

client_key_pair = RSA.generate(RSA_KEY_LENGTH)
client_private_key = client_key_pair.export_key(
    passphrase=PWD,
    pkcs=8,
    protection='PBKDF2WithHMAC-SHA512AndAES256-CBC',
    prot_params={'iteration_count': 131072}
)
client_public_key = client_key_pair.public_key().export_key()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((IP_ADDR, PORT))
    print('** CONNECTED TO SERVER **')

    # Send public key
    client_socket.send(client_public_key)
    print('** SENT PUBLIC KEY **')
    
    # Receive symmetric key and nonce
    encrypted_symmetric_key = client_socket.recv(BUFF_SIZE)
    nonce = client_socket.recv(BUFF_SIZE)
    print('** RECEIVED SYMMETRIC KEY AND NONCE **')
    
    # Decrypt symmetric key
    client_private_key_obj = RSA.import_key(client_private_key, passphrase=PWD)
    cipher_rsa = PKCS1_OAEP.new(client_private_key_obj)
    decrypted_symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)
    
    # Prepare metadata
    filename = 'file'
    extension = 'mp3'
    filesize = os.path.getsize(f'{filename}.{extension}')
    metadata = f'{filename}:{extension}:{filesize}'.encode(ENCODING)
    metadata_header = 'File metadata in the following format - filename:extension:filesize'.encode(ENCODING)
    
    # Encrypt and send metadata
    aes_cipher = AES.new(key=decrypted_symmetric_key, mode=AES.MODE_EAX, nonce=nonce)
    aes_cipher.update(metadata_header)
    cipher_text, tag = aes_cipher.encrypt_and_digest(metadata)
    client_socket.send(tag)
    client_socket.send(cipher_text)
    print('** SENT METADATA **')
    
    # Read and encrypt the file in chunks
    chunk_counter = 0
    with open(f'{filename}.{extension}', 'rb') as f:
        while True:
            chunk = f.read(BUFF_SIZE)
            if not chunk:
                break

            # Generate a unique nonce for each chunk
            chunk_nonce = nonce[:12] + chunk_counter.to_bytes(4, 'big')
            aes_cipher = AES.new(key=decrypted_symmetric_key, mode=AES.MODE_EAX, nonce=chunk_nonce)
            encrypted_chunk, chunk_tag = aes_cipher.encrypt_and_digest(chunk)
            
            # Send the encrypted chunk and its tag
            client_socket.send(chunk_tag)
            client_socket.send(encrypted_chunk)
            print(f'Sent chunk {chunk_counter} with nonce {chunk_nonce.hex()}')
            
            # Wait for ACK from server
            ack = client_socket.recv(BUFF_SIZE).decode(ENCODING)
            if ack == "ACK":
                print(f"Received ACK for chunk {chunk_counter}")
            else:
                print(f"Failed to receive ACK for chunk {chunk_counter}. Terminating.")
                break
            
            chunk_counter += 1
        
    print(f'** SENT FILE {filename}.{extension} **')

print('** CONNECTION CLOSED **')
