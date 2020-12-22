#!/usr/bin/python

import sqlite3
import os.path
from os import path
from getpass import getpass
from base64 import b64decode, b64encode
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes


op = 1
master = ""
db = 0

print("Python Password Manager")

if not os.path.exists("keystorage.db"):
    db = sqlite3.connect("keystorage.db")
    db.execute("""CREATE TABLE Hashes(
        ID       INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
        service  STRING,
        username STRING,
        nonce    STRING,
        header   STRING,
        tag      STRING,
        hash     STRING);""")

    print("Since there is no suitable database, a new one will be created, you must set the master password now\n")
    temp = getpass("New master password: ")
else:
    db = db = sqlite3.connect("keystorage.db")
    temp = getpass(b"Master password: ")

while op != 0:

    print("> 1 - Add password\n> 2 - Retrive password\n> 3 - Edit password\n> 4 - List services\n> 5 - Generate password\n> 0 - Exit")
    op = int(input(": "))

    if op == 1:
        print("New password")
        serv = input("Service name: ")
        user = input("Username: ")
        pw = getpass(b"Password to be stored: ")

        nonce, header, tag, encpw = encrypt(pw)

        db.execute("INSERT INTO Hashes (service, username, nonce, header, tag, hash) \ VALUES('%s','%s','%s','%s','%s','%s')",
                   b64encode(serv).decode('utf-8'), b64encode(user).decode('utf-8'), nonce, header, tag, encpw)

    elif op == 2:
        print("Retrive password")
        sch = input("Service name: ")
        schu = input("Username: ")

        row = db.execute(
            "SELECT nonce, header, tag, hash from Hashes WHERE (service='%s' AND username='%s')", sch, schu)

        decpw = decrypt(row[0], row[1], row[2], row[3])

        print("Your password is: %s", decpw)

    # elif op == 3:
    # elif op == 4:
    # elif op == 5:


def encrypt(pw):
    header = b""
    sl = get_random_bytes(16)

    # Password Key Derivation Function with master password
    key = scrypt(master, sl, 32, N=2**16, r=8, p=1)

    ch = ChaCha20_Poly1305.new(key=key)
    ch.update(header)
    chpw, tag = ch.encrypt_and_digest(pw)

    # return nonce, header, tag and encrypted password
    return b64encode(ch.nonce).decode('utf-8'), b64encode(header).decode('utf-8'), b64encode(tag).decode('utf-8'), b64encode(chpw).decode('utf-8')


def decrypt(nonce, header, tag, hash):
    key = scrypt(master, sl, 32, N=2**16, r=8, p=1)

    ch = ChaCha20_Poly1305.new(key=key, nonce=b64decode(nonce))
    ch.update(b64decode(header))

    return ch.decrypt_and_verify(b64decode(hash), b64decode(tag))
