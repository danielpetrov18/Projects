import socket
import logging
import constants
from tqdm import tqdm
from Cryptodome.PublicKey import RSA
from helper_functions import generate_symmetric_key, generate_symmetric_key_nonce, encrypt_symmetric_key, create_aes_cipher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            try:
                # Bind the socket to the address and port
                server.bind((constants.IP_ADDR, constants.PORT))
                server.listen(1)  # Listen for incoming connections
                logging.info('Server is listening')

                # Accept a client connection
                client, _ = server.accept()
                with client:
                    logging.info('Connection established')

                    try:
                        # Receive the client's public key
                        client_public_key = client.recv(constants.BUFF_SIZE)
                        rsa_key = RSA.import_key(client_public_key)
                        logging.info('Server received public key')

                        # Generate symmetric key and nonce, then encrypt the symmetric key using the client's public key
                        symmetric_key = generate_symmetric_key()
                        nonce = generate_symmetric_key_nonce()
                        encrypted_symmetric_key = encrypt_symmetric_key(rsa_key, symmetric_key)

                        # Send the encrypted symmetric key and nonce to the client
                        client.send(encrypted_symmetric_key)
                        client.send(nonce)
                        logging.info('Server sent the encrypted symmetric key and the nonce')

                        # Receive the encrypted metadata and the tag
                        tag = client.recv(constants.BUFF_SIZE)
                        cipher_metadata = client.recv(constants.BUFF_SIZE)

                        # Decrypt and verify the metadata
                        aes_cipher = create_aes_cipher(symmetric_key, nonce)
                        metadata = aes_cipher.decrypt_and_verify(cipher_metadata, tag)
                        logging.info('Server received and verified metadata')

                        # Parse the metadata to extract file information
                        metadata_fields = metadata.decode(constants.ENCODING).split(':')
                        filename, extension, file_size = metadata_fields

                        # Initialize a buffer to store the received file data
                        file_bytes = b''
                        with tqdm(total=float(file_size), unit='B', unit_scale=True, desc='Receiving file', ncols=75, ascii=' ░▒▓█', colour='red') as progress_bar:
                            while True:
                                # Receive and decrypt the file chunks
                                encrypted_file_chunk = client.recv(constants.BUFF_SIZE)
                                if not encrypted_file_chunk:
                                    break
                                aes_cipher = create_aes_cipher(symmetric_key, nonce)
                                file_chunk = aes_cipher.decrypt(encrypted_file_chunk)
                                file_bytes += file_chunk
                                progress_bar.update(len(file_chunk))

                        # Write the received file data to a new file
                        with open(f'new_{filename}.{extension}', 'wb') as f:
                            f.write(file_bytes)
                            logging.info(f'Server received and saved new_{filename}.{extension}')
                    except ValueError as e:
                        logging.error(f'Decryption failed: {e}')
                    except (socket.error, EOFError) as e:
                        logging.error(f'Communication error: {e}')
                    except Exception as e:
                        logging.error(f'Unexpected error: {e}')
            except socket.error as e:
                logging.error(f'Socket error: {e}')
            except Exception as e:
                logging.error(f'Error initializing server: {e}')
    except Exception as e:
        logging.error(f'Failed to create server socket: {e}')
        exit(1)

    logging.info('Server terminated successfully')

if __name__ == '__main__':
    main()
