import argparse
import constants
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.Random import get_random_bytes

def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments including file name, extension, and password.
    """
    parser = argparse.ArgumentParser(description='Secure File Transfer Client')
    parser.add_argument('-f', '--file', required=True, help='File name to be sent (without extension)')
    parser.add_argument('-e', '--extension', required=True, help='File extension (e.g., txt, mp3)')
    parser.add_argument('-p', '--password', required=True, help='Passphrase for encrypting the RSA private key')
    return parser.parse_args()

def generate_key_pair(password: str) -> tuple[bytes, bytes]:
    """
    Generate an RSA key pair (public and private keys).
    
    Args:
        password (str): Passphrase for encrypting the private key.
    
    Returns:
        tuple[bytes, bytes]: The public key and the encrypted private key.
    """
    client_key_pair = RSA.generate(constants.RSA_KEY_LENGTH)
    client_public_key = client_key_pair.public_key().export_key()
    client_private_key = client_key_pair.export_key(
        passphrase=password,
        pkcs=8,
        protection='PBKDF2WithHMAC-SHA512AndAES256-CBC',
        prot_params={'iteration_count': 131072}
    )
    return client_public_key, client_private_key

def decrypt_symmetric_key(private_key: bytes, password: str, encrypted_symmetric_key: bytes) -> bytes:
    """
    Decrypt the symmetric key using the private RSA key.
    
    Args:
        private_key (bytes): The encrypted private RSA key.
        password (str): The passphrase for decrypting the private RSA key.
        encrypted_symmetric_key (bytes): The encrypted symmetric key received from the server.
    
    Returns:
        bytes: The decrypted symmetric key.
    """
    private_key_obj = RSA.import_key(private_key, password)
    cipher_rsa = PKCS1_OAEP.new(private_key_obj)
    decrypted_symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)
    return decrypted_symmetric_key

def create_aes_cipher(key: bytes, nonce: bytes):
    """
    Create an AES cipher object for encryption and decryption.
    
    Args:
        key (bytes): The symmetric key used for AES encryption.
        nonce (bytes): The nonce value for AES encryption.
    
    Returns:
        AES: The AES cipher object.
    """
    return AES.new(key=key, mode=AES.MODE_EAX, nonce=nonce)

def generate_symmetric_key() -> bytes:
    """
    Generate a random symmetric key for AES encryption.
    
    Returns:
        bytes: The generated symmetric key.
    """
    return get_random_bytes(constants.SYMMETRIC_KEY_LENGTH)

def generate_symmetric_key_nonce() -> bytes:
    """
    Generate a random nonce for AES encryption.
    
    Returns:
        bytes: The generated nonce.
    """
    return get_random_bytes(constants.SYMMETRIC_KEY_NONCE)

def encrypt_symmetric_key(client_pub_key: RSA.RsaKey, key: bytes) -> bytes:
    """
    Encrypt the symmetric key using the client's RSA public key.
    
    Args:
        client_pub_key (RSA.RsaKey): The client's public RSA key.
        key (bytes): The symmetric key to be encrypted.
    
    Returns:
        bytes: The encrypted symmetric key.
    """
    cipher_rsa = PKCS1_OAEP.new(client_pub_key)
    encrypted_symmetric_key = cipher_rsa.encrypt(key)
    return encrypted_symmetric_key
