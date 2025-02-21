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

def test_cryptor_bad(random_path, random_name):
    key = utils.random(SecretBox.KEY_SIZE)
    cryptor = Cryptor(secret_key=key)

    with pytest.raises(TypeError):
        derive = cryptor.derive(None)
