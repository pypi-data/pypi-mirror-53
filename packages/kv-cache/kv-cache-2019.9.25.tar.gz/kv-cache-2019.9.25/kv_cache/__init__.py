#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import public

XDG_CACHE_HOME = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
KV_CACHE = os.getenv("KV_CACHE", os.path.join(XDG_CACHE_HOME,'kv-cache'))

def getpath(key):
    return os.path.join(KV_CACHE,key)


@public.add
def exists(key):
    """return True if key exists, else False"""
    fullpath = getpath(key)
    return os.path.exists(fullpath)



@public.add
def get(key):
    """get cache value"""
    path = getpath(key)
    if os.path.exists(path):
        return open(path).read()

@public.add
def update(key,string):
    """update cache value"""
    path = getpath(key)
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    open(path,"w").write(string)



@public.add
def rm(key):
    """remove cache key"""
    path = getpath(key)
    if os.path.exists(path):
        os.unlink(path)

@public.add
def rm(key):
    """remove cache key"""
    path = getpath(key)
    if os.path.exists(path):
        os.unlink(path)
