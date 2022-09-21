import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os
from OpenSSL import crypto

#getting
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

#Storing private Keys
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
with open('private_key.pem', 'wb') as f:
    f.write(pem)

#storing public
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('public_key.pem', 'wb') as f:
    f.write(pem)

#reading private
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

#reading public
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

print(public_key)

#encripting
message = str.encode('terra')

encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)


#decrypting

original_message = private_key.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
original_message
original_message.decode("utf-8")
###


#cert is the encrypted certificate int this format -----BEGIN -----END
crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, pem)
pubKeyObject = crtObj.get_pubkey()
pubKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pubKeyObject)
print(pubKeyString)