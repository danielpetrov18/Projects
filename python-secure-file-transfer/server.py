import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes

PORT = 4444
BUFF_SIZE = 1024
ENCODING = 'utf-8'
EOT_MARKER = b'EOF'
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
        
        client_public_key = conn.recv(BUFF_SIZE)
        rsa_key = RSA.import_key(client_public_key)
        print('** SERVER RECEIVED PUBLIC KEY **')
        
        symmetric_key = get_random_bytes(SYMMETRIC_KEY_LENGTH)
        nonce = get_random_bytes(SYMMETRIC_KEY_NONCE)
        
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)
        
        conn.send(encrypted_symmetric_key)
        conn.send(nonce)
        print('** SERVER SENT THE ENCRYPTED SYMMETRIC KEY AND THE NONCE **')

        tag = conn.recv(16)
        cipher_metadata = conn.recv(BUFF_SIZE)
        
        aes_cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=nonce)
        try:
            metadata = aes_cipher.decrypt_and_verify(cipher_metadata, tag)
            print('** SERVER RECEIVED AND VERIFIED METADATA **')
        except (ValueError, KeyError) as e:
            print(f'Decryption failed: {e}')
            conn.close()
            exit(1)
        
        metadata_fields = metadata.decode(ENCODING).split(':')
        filename, extension = metadata_fields
        
        file_bytes = b''
        while True:
            encrypted_file_chunk = conn.recv(BUFF_SIZE)
            if not encrypted_file_chunk or encrypted_file_chunk.endswith(EOT_MARKER):
                break

            aes_cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=nonce)
            try:
                file_chunk = aes_cipher.decrypt(encrypted_file_chunk)
                file_bytes += file_chunk
                print('Receiving data ...')
            except (ValueError, KeyError) as e:
                print(f'Decryption failed for chunk: {e}')
                conn.close()
                exit(1)
        
        # Save the decrypted file
        with open(f'new_{filename}.{extension}', 'wb') as f:
            f.write(file_bytes)
        
        print(f'** SERVER RECEIVED AND SAVED new_{filename}.{extension} **')
        
        # Sending acknowledgment back to the client
        conn.send('ACK'.encode(ENCODING))

print('** SERVER TERMINATED SUCCESSFULLY **')
