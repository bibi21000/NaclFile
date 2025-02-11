# -*- encoding: utf-8 -*-
"""Test module

"""
import os
import io
from random import randbytes
import tarfile
import struct

from nacl import utils
from nacl.secret import SecretBox

import pyzstd

import cofferfile
import naclfile
from naclfile.zstd import NaclFile, open as nacl_open, CParameter

import pytest
from unittest import mock

@pytest.mark.parametrize("chunk_size, file_size",
    [
        (1024 * 1, 1024 * 10), (1024 * 1, 1024 * 10 + 4), (1024 * 1, 1024 * 10 + 5),
        (1024 * 10, 1024 * 10), (1024 * 10, 1024 * 10 + 7), (1024 * 10, 1024 * 10 + 3),
        (1024 * 100, 1024 * 10), (1024 * 100, 1024 * 10 + 9), (1024 * 100, 1024 * 10 + 11),
    ])
def test_buffer_nacl_file(random_path, random_name, chunk_size, file_size):

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

    level_or_option = {
        CParameter.compressionLevel : 19,
    }
    with NaclFile(dataf, mode='wb', secret_key=key, level_or_option=level_or_option, chunk_size=chunk_size) as ff:
        ff.write(data)
    with open(dataf, "rb") as ff:
        datar = ff.read()
    assert data != datar
    with NaclFile(dataf, "rb", secret_key=key) as ff:
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

    level_or_option = {
        CParameter.compressionLevel : 19,
    }
    with nacl_open(dataf, mode='wb', secret_key=key, level_or_option=level_or_option, chunk_size=chunk_size) as ff:
        ff.write(data)
    with open(dataf, "rb") as ff:
        datar = ff.read()
    assert data != datar
    with nacl_open(dataf, "rb", secret_key=key) as ff:
        datar = ff.read()
    assert data == datar

    data = random_name * (file_size // len(random_name))
    dataf = os.path.join(random_path, random_name)
    with nacl_open(dataf, mode='wt', secret_key=key, chunk_size=chunk_size) as ff:
        ff.write(data)
    with open(dataf, "rb") as ff:
        datar = ff.read()
    assert data != datar
    with nacl_open(dataf, "rt", secret_key=key) as ff:
        datar = ff.read()
    assert data == datar

def test_bad(random_path, random_name, mocker):
    key = utils.random(SecretBox.KEY_SIZE)
    data = randbytes(128)
    dataf = os.path.join(random_path, 'test_bad_%s.frnt'%random_name)
    dataok = os.path.join(random_path, 'test_ok_%s.frnt'%random_name)

    with NaclFile(dataok, mode='wb', secret_key=key) as ff:
        assert repr(ff).startswith('<ZstdNacl')

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

    with pytest.raises(TypeError):
        with nacl_open(dataf, mode='wb', fernet_key=key, zstd_dict=1) as ff:
            ff.write(data)

    with mock.patch('pyzstd.ZstdFile.__init__') as mocked:
        mocked.side_effect = AssertionError('Boooooom')
        with pytest.raises(AssertionError):
            with NaclFile(dataok, mode='wb', secret_key=key) as ff:
                assert repr(ff).startswith('<ZstdFernet')
