# Secure File Transfer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

## Overview

The **Secure File Transfer** project is a client-server application designed to securely transfer files over a network. It leverages RSA and AES encryption to ensure the confidentiality of the data being transmitted.

- **RSA Encryption** is used to securely exchange a symmetric key.
- **AES Encryption** (with EAX mode) is used for the actual encryption and decryption of files during transfer.

This project is suitable for scenarios where sensitive files need to be transferred securely between a client and a server over an unsecured network.

## Features

- **Public-Private Key Exchange:** RSA keys are generated on the client side. The public key is sent to the server to securely transfer the symmetric key.
- **Symmetric Key Encryption:** AES encryption is used to encrypt files, providing both speed and security.
- **Metadata Encryption:** File metadata (filename, extension, size) is encrypted to ensure privacy.
- **Progress Tracking:** File transfer progress is displayed using a progress bar.
- **Error Handling:** The application is equipped with fine-grained exception handling to manage errors gracefully.

## Technology Stack

- **Python 3.9+**
- **PyCryptodome** for cryptography
- **Socket Programming** for networking
- **TQDM** for progress bars
- **Argparse** for command-line argument parsing
- **Logging** for debugging and monitoring