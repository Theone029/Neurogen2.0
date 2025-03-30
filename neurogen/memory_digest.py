#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
memory_digest.py

Distills log entries into a concise summary.
"""
def distill_logs(logs):
    return " | ".join(logs)


def test_self():
    return {'valid': True, 'state': None, 'logs': [], 'next': []}
