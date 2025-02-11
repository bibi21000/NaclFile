# -*- encoding: utf-8 -*-
"""Test module

"""
import os
import io
from random import randbytes
import tarfile
import zipfile
import struct

from nacl import utils
from nacl.secret import SecretBox

import cofferfile
from naclfile import NaclFile, open as nacl_open

import pytest

@pytest.mark.parametrize("chunk_size, file_size",
    [
        (1024 * 1, 1024 * 10), (1024 * 1, 1024 * 10 + 4), (1024 * 1, 1024 * 10 + 5),
        (1024 * 10, 1024 * 10), (1024 * 10, 1024 * 10 + 7), (1024 * 10, 1024 * 10 + 3),
        (1024 * 100, 1024 * 10), (1024 * 100, 1024 * 10 + 9), (1024 * 100, 1024 * 10 + 11),
    ])
def test_buffer_nacl(random_path, random_name, chunk_size, file_size):

    key = utils.random(SecretBox.KEY_SIZE)
    data = randbytes(file_size)
    dataf = os.path.join(random_path, random_name)

    with NaclFile(dataf, mode='wb', secret_key=key, chunk_size=chunk_size) as ff:
        ff.write(data)
    with open(dataf, "rb") as ff:
        datar = ff.read()
    assert data != datar
    with NaclFile(dataf, "rb", secret_key=key) as ff:
        datar = ff.read()
    assert data == datar

    data = random_name * 2
    dataf = os.path.join(random_path, random_name)
    with nacl_open(dataf, mode='wt', secret_key=key, chunk_size=chunk_size) as ff:
        ff.write(data)
    with open(dataf, "rb") as ff:
        datar = ff.read()
    assert data != datar
    with nacl_open(dataf, "rt", secret_key=key) as ff:
        datar = ff.read()
    assert data == datar

@pytest.mark.parametrize("chunk_size, file_size",
    [
        (1024 * 1, 1024 * 10), (1024 * 1, 1024 * 10 + 4), (1024 * 1, 1024 * 10 + 5),
        (1024 * 10, 1024 * 10), (1024 * 10, 1024 * 10 + 7), (1024 * 10, 1024 * 10 + 3),
        (1024 * 100, 1024 * 10), (1024 * 100, 1024 * 10 + 9), (1024 * 100, 1024 * 10 + 11),
    ])
def test_buffer_nacl_open(random_path, random_name, chunk_size, file_size):

    key = utils.random(SecretBox.KEY_SIZE)

    data = randbytes(file_size)
    dataf = os.path.join(random_path, random_name)
    with nacl_open(dataf, mode='wb', secret_key=key, chunk_size=chunk_size) as ff:
        ff.write(data)
    with open(dataf, "rb") as ff:
        datar = ff.read()
    assert data != datar
    with nacl_open(dataf, "rb", secret_key=key) as ff:
        datar = ff.read()
    assert data == datar

    data = random_name * 2
    dataf = os.path.join(random_path, random_name)
    with nacl_open(dataf, mode='wt', secret_key=key, chunk_size=chunk_size) as ff:
        ff.write(data)
    with open(dataf, "rb") as ff:
        datar = ff.read()
    assert data != datar
    with nacl_open(dataf, "rt", secret_key=key) as ff:
        datar = ff.read()
    assert data == datar

def test_bad(random_path, random_name):
    key = utils.random(SecretBox.KEY_SIZE)
    data = randbytes(128)
    dataf = os.path.join(random_path, 'test_bad_%s.frnt'%random_name)
    dataok = os.path.join(random_path, 'test_ok_%s.frnt'%random_name)

    with NaclFile(dataok, mode='wb', secret_key=key) as ff:
        assert repr(ff).startswith('<NaclFile')

    with pytest.raises(ValueError):
        with NaclFile(dataf, mode='wbt', secret_key=key) as ff:
            ff.write(data)

    with pytest.raises(ValueError):
        with NaclFile(dataf, mode='zzz', secret_key=key) as ff:
            ff.write(data)

    with pytest.raises(FileNotFoundError):
        with NaclFile(None, mode='wb', secret_key=key) as ff:
            ff.write(data)

    with pytest.raises(FileNotFoundError):
        with NaclFile(dataf, secret_key=key) as ff:
            data = ff.read()

    with pytest.raises(ValueError):
        with nacl_open(dataf, mode='wbt', secret_key=key) as ff:
            ff.write(data)

    with pytest.raises(ValueError):
        with nacl_open(dataf, mode='wb', secret_key=key, encoding='utf-8') as ff:
            ff.write(data)

    with pytest.raises(ValueError):
        with nacl_open(dataf, mode='wb', secret_key=key, errors=True) as ff:
            ff.write(data)

    with pytest.raises(ValueError):
        with nacl_open(dataf, mode='wb', secret_key=key, newline='\n') as ff:
            ff.write(data)

    with pytest.raises(TypeError):
        with nacl_open(None, mode='wb', secret_key=key) as ff:
            ff.write(data)

    with pytest.raises(ValueError):
        with nacl_open(dataf, mode='wb', secret_key=None) as ff:
            ff.write(data)
