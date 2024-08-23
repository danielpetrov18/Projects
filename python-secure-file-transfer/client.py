import sys
import socket
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes

PORT = 4444
BUFF_SIZE = 1024
ENCODING = 'utf-8'
EOT_MARKER = b'EOF'
IP_ADDR = 'localhost'
RSA_KEY_LENGTH = 3072
PWD = b'I like turtles'

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

    client_socket.send(client_public_key)
    print('** SENT PUBLIC KEY **')
    
    encrypted_symmetric_key = client_socket.recv(BUFF_SIZE)
    nonce = client_socket.recv(BUFF_SIZE)
    print('** RECEIVED THE ENCRYPTED SYMMETRIC KEY AND THE NONCE **')
    
    client_private_key_obj = RSA.import_key(client_private_key, passphrase=PWD)
    cipher_rsa = PKCS1_OAEP.new(client_private_key_obj)
    decrypted_symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)
    print('** DECRYPTED THE SYMMETRIC KEY **')
    
    filename = sys.argv[1]
    extension = sys.argv[2]
    metadata = f'{filename}:{extension}'.encode(ENCODING)
    
    aes_cipher = AES.new(key=decrypted_symmetric_key, mode=AES.MODE_EAX, nonce=nonce)
    cipher_text, tag = aes_cipher.encrypt_and_digest(metadata)
    
    client_socket.send(tag)
    client_socket.send(cipher_text)
    print('** SENT METADATA **')
    
    with open(f'{filename}.{extension}', 'rb') as f:
        file_data = f.read()
    
    aes_cipher = AES.new(key=decrypted_symmetric_key, mode=AES.MODE_EAX, nonce=nonce)
    encrypted_file_data, tag = aes_cipher.encrypt_and_digest(file_data)
    
    client_socket.send(encrypted_file_data)
    client_socket.send(EOT_MARKER)
    print(f'** SENT FILE {filename}.{extension} **')
    
    print('** WAITING FOR ACK FROM SERVER **')
    response = client_socket.recv(BUFF_SIZE).decode()
    if response != 'ACK':
        print('Something went wrong after sending the file to the server!')
        client_socket.close()
        exit(1)

print('** CLIENT TERMINATED SUCCESSFULLY **')
