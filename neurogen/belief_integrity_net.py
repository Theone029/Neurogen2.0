#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
belief_integrity_net.py

Validates the new belief before it is committed.
"""
def validate_belief(belief):
    # Accept non-empty beliefs that don't echo the unproductive pattern.
    return bool(belief) and "same message" not in belief.lower()


def test_self():
    return {'valid': True, 'state': None, 'logs': [], 'next': []}
