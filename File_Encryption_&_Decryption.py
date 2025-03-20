from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


def generate_key():
    return os.urandom(32)


def save_key(key, key_file_name="aes_key.key"):
    with open(key_file_name, 'wb') as key_file:
        key_file.write(key)
    print(f"Key saved to {key_file_name}")


def load_key(key_file_name="aes_key.key"):
    with open(key_file_name, 'rb') as key_file:
        return key_file.read()


def encrypt_file(file_name, key):
    iv = os.urandom(16)

    with open(file_name, 'rb') as file:
        file_data = file.read()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(file_data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    encrypted_file_name = file_name + ".enc"
    with open(encrypted_file_name, 'wb') as enc_file:
        enc_file.write(iv + encrypted_data)

    print(f"File encrypted successfully, saved as {encrypted_file_name}")


def decrypt_file(encrypted_file_name, key):
    with open(encrypted_file_name, 'rb') as enc_file:
        iv = enc_file.read(16)
        encrypted_data = enc_file.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    decrypted_file_name = encrypted_file_name.replace('.enc', '.dec')
    with open(decrypted_file_name, 'wb') as dec_file:
        dec_file.write(decrypted_data)

    print(f"File decrypted successfully, saved as {decrypted_file_name}")


def main():
    action = input("Do you want to (e)ncrypt or (d)ecrypt a file?: ").lower()
    file_name = input("Enter the file name: ")

    if not os.path.exists(file_name):
        print(f"File '{file_name}' not found.")
        return

    if action == 'e':
        key = generate_key()
        save_key(key)
        encrypt_file(file_name, key)

    elif action == 'd':
        key_file = input("Enter the key file name (default: aes_key.key): ") or "aes_key.key"
        if not os.path.exists(key_file):
            print(f"Key file '{key_file}' not found.")
            return

        key = load_key(key_file)
        decrypt_file(file_name, key)

    else:
        print("Invalid option. Please choose either 'e' or 'd'.")
main()