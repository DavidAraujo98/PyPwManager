# PyManager

[![Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org/)

## What is PyManager ?

 PyManager is a simple password manager using [Argon2](https://pypi.org/project/argon2-cffi/) hashing, with [ChaCha20](https://pycryptodome.readthedocs.io/en/latest/src/cipher/chacha20.html) encryption using a password derived key generated with [Scrypt](https://cryptobook.nakov.com/mac-and-key-derivation/scrypt) from a master and a login passwords 
 
#
## Features
 - Storage is made possible with a SQLite database
 - Only encrypted version of a password is keeped
 - Access requires log in
 - Simple console GUI

#
## How it works ?

- ### First run

    Running the script for the first time, or everytime the database is deleted and there is a need to create a new one, you will be asked to provide a new master and login passwords. Of this two, **only the hash version of the *login* one will be stored** for future logins

    This allows you to save passwords encrypted with different master keys, and keeping the master password totally secret

- ### Once the database is created
    
    Now that the database is created, *login password* will be necessary everytime you want to access it.

    At login ou will be asked the master password also, in case you want to process a password (encrypt a new one or decrypt an existing one)
    
    > **!! Attention !!**  
    > *Master* password is asked **only at login**, soo if you have passwords encrypted with a *master* different from the one you just provided you wont be able to decrypt them. So pay attention to what passwords you may want to access to encrypt or decrypt when providing the master password at login

#
## Images


