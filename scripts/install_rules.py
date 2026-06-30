#!/usr/bin/env python3
import json, time, requests
SWITCH_COUNT = 196
FLOODLIGHT_URL = "http://floodlight:8080/wm/staticflowpusher/json"
H1_MAC = "00:00:00:00:00:01"
H91_MAC = "00:00:00:00:00:5b"

def dpid(index: int) -> str:
    h = f"{index:016x}"
    return ":".join(h[i:i+2] for i in range(0, 16, 2))

def push_flow(flow):
    r = requests.post(FLOODLIGHT_URL, data=json.dumps(flow), headers={"Content-Type": "application/json"})
    print(f"{flow['name']}: {r.status_code} {r.text}")

def create_flow(name, switch, eth_dst, out_port):
    return {"switch": switch, "name": name, "cookie": "0", "priority": "32768", "active": "true", "eth_dst": eth_dst, "actions": f"output={out_port}"}

def main():
    print("Waiting for Floodlight REST API...")
    time.sleep(5)
    print("Installing bidirectional static rules between h1 and h91...")
    for i in range(1, SWITCH_COUNT + 1):
        sw = dpid(i)
        out_to_h91 = 3 if i == SWITCH_COUNT else 2
        out_to_h1 = 3 if i == 1 else 1
        push_flow(create_flow(f"h1-to-h91-s{i}", sw, H91_MAC, out_to_h91))
        push_flow(create_flow(f"h91-to-h1-s{i}", sw, H1_MAC, out_to_h1))
    print("Done. In Mininet CLI run: h1 ping -c 3 h91")

if __name__ == "__main__":
    main()
