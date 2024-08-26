import os
import socket
import logging
import constants
from tqdm import tqdm
from helper_functions import parse_arguments, generate_key_pair, decrypt_symmetric_key, create_aes_cipher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Parse command-line arguments
        args = parse_arguments()
    except Exception as e:
        logging.error(f'Error parsing arguments: {e}')
        exit(1)

    try:
        # Generate RSA key pair (public and private keys)
        public_key, private_key = generate_key_pair(args.password)
    except Exception as e:
        logging.error(f'Error generating key pair: {e}')
        exit(1)
    
    try:
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                # Connect to the server
                client.connect((constants.IP_ADDR, constants.PORT))
                logging.info('Connected to server')

                # Send the public key to the server
                client.send(public_key)
                logging.info('Sent public key')

                # Receive the encrypted symmetric key and nonce from the server
                encrypted_symmetric_key = client.recv(constants.BUFF_SIZE)
                nonce = client.recv(constants.BUFF_SIZE)
                logging.info('Received the encrypted symmetric key and the nonce')

                # Decrypt the symmetric key using the private key
                symmetric_key = decrypt_symmetric_key(private_key, args.password, encrypted_symmetric_key)
                logging.info('Decrypted the symmetric key')

                # Prepare the file metadata and encrypt it
                filename = args.file
                extension = args.extension
                file_size = os.path.getsize(f'{filename}.{extension}')
                metadata = f'{filename}:{extension}:{file_size}'.encode(constants.ENCODING)

                cipher = create_aes_cipher(symmetric_key, nonce)
                cipher_metadata, tag = cipher.encrypt_and_digest(metadata)

                # Send the encrypted metadata and tag to the server
                client.send(tag)
                client.send(cipher_metadata)
                logging.info('Sent metadata')

                # Open the file and send its content to the server in chunks
                with open(f'{filename}.{extension}', 'rb') as f, tqdm(total=file_size, unit='B', unit_scale=True, desc='Sending file', ncols=75, ascii=' ░▒▓█', colour='green') as progress_bar:
                    while True:
                        file_chunk = f.read(constants.BUFF_SIZE)
                        if not file_chunk:
                            break
                        cipher = create_aes_cipher(symmetric_key, nonce)
                        encrypted_chunk = cipher.encrypt(file_chunk)
                        client.send(encrypted_chunk)
                        progress_bar.update(len(file_chunk))
                
                logging.info(f'Sent file {filename}.{extension}')
            except (ConnectionRefusedError, TimeoutError) as e:
                logging.error(f'Network error: {e}')
            except socket.error as e:
                logging.error(f'Socket error: {e}')
            except Exception as e:
                logging.error(f'Error during file transfer: {e}')
    except Exception as e:
        logging.error(f'Failed to create or connect socket: {e}')
        exit(1)

    logging.info('Client terminated successfully')

if __name__ == '__main__':
    main()
