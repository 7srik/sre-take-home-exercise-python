import yaml
import requests
import time
from collections import defaultdict
import sys
from urllib.parse import urlparse

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    if not isinstance(config, list):
        raise ValueError("YAML config must be a list of endpoint dictionaries.")
    return config

# Function to extract domain name
def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=0.5)
        duration = (time.time() - start_time) * 1000
        if 200 <= response.status_code < 300 and duration <= 500:
            return "UP"
        else:
            print(f"[WARN] {url} is DOWN. Status: {response.status_code}, Time: {int(duration)}ms")
            return "DOWN"
    except requests.RequestException as e:
        print(f"[ERROR] {url} connection failed: {e}")
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        cycle_start = time.time()
        for endpoint in config:
            if "url" not in endpoint:
                print(f"[SKIP] Malformed endpoint missing 'url': {endpoint}")
                continue
            domain = extract_domain(endpoint["url"])
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            total = stats["total"]
            up = stats["up"]
            availability = (100 * up) // total if total > 0 else 0
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        elapsed = time.time() - cycle_start
        sleep_duration = max(0, 15 - elapsed)
        time.sleep(sleep_duration)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")