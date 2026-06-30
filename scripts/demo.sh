#!/usr/bin/env bash
set -e
service openvswitch-switch start || true
python3 /scripts/topology.py
