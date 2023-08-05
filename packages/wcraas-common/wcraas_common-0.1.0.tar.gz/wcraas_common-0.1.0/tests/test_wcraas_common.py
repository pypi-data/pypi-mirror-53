#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wcraas_common` package."""

import os
import pytest

from collections import namedtuple

from wcraas_common.config import AMQPConfig
from wcraas_common.wcraas_common import WcraasWorker


def test_default_env_load():
    conf = AMQPConfig.fromenv()
    assert isinstance(conf, tuple)
    assert conf._fields == ("host", "port", "user", "password")
    assert conf.host == "localhost"
    assert conf.port == 5672
    assert conf.user == "guest"
    assert conf.password == "guest"

def test_custom_env_load():
    os.environ["COTTONTAIL_HOST"] = "127.0.0.1"
    os.environ["COTTONTAIL_PORT"] = "5673"
    os.environ["COTTONTAIL_USER"] = "admin"
    os.environ["COTTONTAIL_PASS"] = "admin"
    conf = AMQPConfig.fromenv()
    assert conf.host == "127.0.0.1"
    assert conf.port == 5673
    assert conf.user == "admin"
    assert conf.password == "admin"

def test_worker_creation():
    conf = AMQPConfig.fromenv()
    worker = WcraasWorker(conf, 20)
    assert str(worker) == f"{worker.__class__.__name__}(amqp={worker.amqp}, loglevel={worker.loglevel})"
    assert worker._amqp_pool is not None
