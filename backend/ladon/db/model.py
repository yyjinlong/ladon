# -*- coding:utf-8 -*-
#
# Copyright @ 2019 OPS Inc.
#
# Author: Jinlong Yang
#

import sqlalchemy.types
from osmo.db import BASE
from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON


class LTree(sqlalchemy.types.UserDefinedType):

    def python_type(self):
        return basestring

    def get_col_spec(self):
        return 'LTREE'


class Tpl(BASE):

    __tablename__ = 'tb_tpl'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, default='default')
    alias = Column(String(100), nullable=False)
    create_at = Column(DateTime, server_default=func.now())

    nodes = relationship('Node', back_populates='tpl')
    keys = relationship('Key', back_populates='tpl')

    def __repr__(self):
        return self.name


class Node(BASE):

    __tablename__ = 'tb_node'

    id = Column(Integer, primary_key=True)
    tpl_id = Column(Integer, ForeignKey('tb_tpl.id'), nullable=False)
    node = Column(LTree(), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    leaf = Column(Boolean, default=True)
    metainfo = Column(JSON)
    op = Column(String(30))
    rd = Column(String(30))
    create_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, onupdate=func.now())

    tpl = relationship('Tpl', back_populates='nodes')
    instances = relationship('Instance', back_populates='node')

    def __repr__(self):
        return self.node


class Instance(BASE):

    __tablename__ = 'tb_instance'

    id = Column(Integer, primary_key=True)
    node_id = Column(Integer, ForeignKey('tb_node.id'), nullable=False)
    ip = Column(String(20), nullable=False)
    hostname = Column(String(50), nullable=False)
    active = Column(Boolean, default=False)
    create_at = Column(DateTime, server_default=func.now())
    update_at = Column(DateTime, onupdate=func.now())

    node = relationship('Node', back_populates='instances')
    vals = relationship('Val', back_populates='instance')

    def __repr__(self):
        return self.ip


class Key(BASE):

    __tablename__ = 'tb_key'

    id = Column(Integer, primary_key=True)
    tpl_id = Column(Integer, ForeignKey('tb_tpl.id'), nullable=False)
    key = Column(String(50), nullable=False)
    create_at = Column(DateTime, server_default=func.now())

    tpl = relationship('Tpl', back_populates='keys')
    vals = relationship('Val', back_populates='key')

    def __repr__(self):
        return self.key


class Val(BASE):

    __tablename__ = 'tb_val'

    id = Column(Integer, primary_key=True)
    key_id = Column(Integer, ForeignKey('tb_key.id'), nullable=False)
    instance_id = Column(Integer, ForeignKey('tb_instance.id'), nullable=False)
    value = Column(String(100), nullable=False)
    create_at = Column(DateTime, server_default=func.now())

    key = relationship('Key', back_populates='vals')
    instance = relationship('Instance', back_populates='vals')

    def __repr__(self):
        return self.value
