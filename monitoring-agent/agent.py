import argparse
import psutil
import requests
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Monitoring Agent")
    parser.add_argument('--server', required=True, help='Backend server URL e.g. http://localhost:8000')
    parser.add_argument('--token', required=True, help='Device token')
    parser.add_argument('--interval', type=int, default=30, help='Telemetry interval in seconds')
    parser.add_argument('--heartbeat-interval', type=int, default=5, help='Heartbeat interval in seconds')
    return parser.parse_args()

def collect_telementry():
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
    }


def send_telementry(server, token, data):
    try:
        response = requests.post(
            f'{server}/api/telementry/',
            headers={'Authorization': f'Token {token}'},
            json=data,
            timeout=10
        )
        response.raise_for_status()
        print(f"[telemetry] sent: {data}")
    except requests.exceptions.RequestException as e:
        print(f"[telemetry] failed: {e}")

def send_heartbeat(server, token):
    try:
        response = requests.post(
            f'{server}/api/heartbeat/',
            headers={'Authorization': f'Token {token}'},
            timeout=10
        )
        response.raise_for_status()
        print("[heartbeat] sent")
    except requests.exceptions.RequestException as e:
        print(f"[heartbeat] failed: {e}")


def main():
    args = parse_args()
    last_telementry = 0
    last_heartbeat = 0
    
    print(f"Agent started. Server {args.server}")

    while True:
        now = time.time()

        if now - last_heartbeat >= args.heartbeat_interval:
            send_heartbeat(args.server, args.token)
            last_heartbeat = now

        if now - last_telementry >= args.interval:
            data = collect_telementry()
            send_telementry(args.server, args.token, data)
            last_telementry = now

        time.sleep(1)

if __name__ == '__main__':
    main()