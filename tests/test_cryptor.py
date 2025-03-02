# -*- encoding: utf-8 -*-
"""Test module

"""
import os
import io

from nacl import utils
from nacl.secret import SecretBox

from naclfile import NaclCryptor as Cryptor

import pytest


def test_cryptor(random_path, random_name):
    key = utils.random(SecretBox.KEY_SIZE)
    cryptor = Cryptor(secret_key=key)
    derive = cryptor.derive('test')

def test_cryptor_class(random_path, random_name):
    derive = Cryptor.derive('test')
    with pytest.raises(TypeError):
        derive = Cryptor.derive(None)

def test_cryptor_bad(random_path, random_name):
    key = utils.random(SecretBox.KEY_SIZE)
    cryptor = Cryptor(secret_key=key)

    with pytest.raises(TypeError):
        derive = cryptor.derive(None)

def test_cryptor_derive(random_path, random_name):
    import secrets
    salt, derive1 = Cryptor.derive('test')
    _, derive2 = Cryptor.derive('test', salt=salt)
    crypt1 = Cryptor(secret_key=derive1)
    crypt2 = Cryptor(secret_key=derive2)
    text = secrets.token_bytes(1785)
    crypted = crypt1._encrypt(text)
    uncrypted = crypt1._decrypt(crypted)
    assert uncrypted == text
    uncrypted = crypt2._decrypt(crypted)
    assert uncrypted == text

def test_cryptor_derive_2(random_path, random_name):
    import secrets
    password = secrets.token_bytes(43)
    salt, derive1 = Cryptor.derive(password)
    _, derive2 = Cryptor.derive(password, salt=salt)
    crypt1 = Cryptor(secret_key=derive1)
    crypt2 = Cryptor(secret_key=derive2)
    text = secrets.token_bytes(27)
    crypted = crypt1._encrypt(text)
    uncrypted = crypt1._decrypt(crypted)
    assert uncrypted == text
    uncrypted = crypt2._decrypt(crypted)
    assert uncrypted == text
