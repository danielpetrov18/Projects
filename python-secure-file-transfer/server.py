import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes

PORT = 4444
BUFF_SIZE = 1024
ENCODING = 'utf-8'
IP_ADDR = 'localhost'
SYMMETRIC_KEY_NONCE = 16  # bytes
SYMMETRIC_KEY_LENGTH = 32  # bytes

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((IP_ADDR, PORT))
    server_socket.listen(1)
    print('** SERVER IS LISTENING **')
    
    conn, addr = server_socket.accept()
    with conn:
        print('** CONNECTION ESTABLISHED **')
        
        # Receive and process the public key
        client_public_key = conn.recv(BUFF_SIZE)
        rsa_key = RSA.import_key(client_public_key)
        
        # Generate and send symmetric key and nonce
        symmetric_key = get_random_bytes(SYMMETRIC_KEY_LENGTH)
        nonce = get_random_bytes(SYMMETRIC_KEY_NONCE)
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)
        
        conn.sendall(encrypted_symmetric_key)
        conn.sendall(nonce)

        # Receive and decrypt metadata
        tag = conn.recv(BUFF_SIZE)
        client_cipher_text = conn.recv(BUFF_SIZE)
        
        metadata_header = 'File metadata in the following format - filename:extension:filesize'.encode(ENCODING)
        aes_cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=nonce)
        aes_cipher.update(metadata_header)
        
        try:
            client_plain_text = aes_cipher.decrypt_and_verify(client_cipher_text, tag).decode(ENCODING)
            print('** SERVER RECEIVED AND VERIFIED METADATA **')
        except (ValueError, KeyError) as e:
            print('Decryption failed:', e)
            conn.close()
            exit(1)
        
        # Extract metadata
        metadata_contents = client_plain_text.split(':')
        filename, extension, filesize = metadata_contents
        
        # Receive and decrypt the file in chunks
        file_bytes = b''
        chunk_counter = 0
        
        while True:
            chunk_tag = conn.recv(BUFF_SIZE)
            encrypted_file_chunk = conn.recv(BUFF_SIZE)
            if not encrypted_file_chunk:
                break
            
            # Generate the corresponding nonce for each chunk
            chunk_nonce = nonce[:12] + chunk_counter.to_bytes(4, 'big')
            aes_cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=chunk_nonce)
            
            try:
                file_chunk = aes_cipher.decrypt_and_verify(encrypted_file_chunk, chunk_tag)
                file_bytes += file_chunk
                print(f'Received chunk {chunk_counter} with nonce {chunk_nonce.hex()}')

                # Send ACK back to client
                conn.sendall("ACK".encode(ENCODING))
            except ValueError:
                print("Chunk decryption failed. Integrity check failed.")
                conn.sendall("NACK".encode(ENCODING))  # Negative acknowledgment
                conn.close()
                exit(1)
            
            chunk_counter += 1
        
        with open(f'new_{filename}.{extension}', 'wb') as f:
            f.write(file_bytes)
            
        print(f'** SERVER RECEIVED new_{filename}.{extension} **')

print('** CONNECTION CLOSED **')
