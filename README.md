# Site Reliability Engineering - Fetch Take-Home Exercise

## Overview

This Python application monitors the availability of HTTP endpoints defined in a YAML configuration file. It performs health checks every **15 seconds** and calculates the **cumulative availability percentage by domain**, ignoring port numbers.

### An endpoint is considered available if:
- HTTP status code is between **200–299**
- Response time is **≤ 500ms**

Availability percentages are truncated to whole numbers.

---

## Requirements

- Python 3.8+
- pip (Python package installer)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/7srik/sre-take-home-exercise-python.git
   cd sre-take-home-exercise-python
2. **(Optional) Create and activate a virtual environment**

bash
Copy
Edit
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
3. **Install dependencies**

bash
Copy
Edit
pip install -r requirements.txt

## Usage
Run the program with a YAML file that lists your endpoints.

bash
Copy
Edit
python main.py sample.yaml
The application will check the endpoints and log output every 15 seconds.

## YAML Format
yaml
Copy
Edit
- name: Get Root
  url: https://example.com/
  method: GET
  headers:
    Accept: application/json

- name: Post Search
  url: https://example.com/search
  method: POST
  body: '{"query": "python"}'
### Field Descriptions
name (required): A descriptive name for the endpoint.

url (required): Full HTTP or HTTPS URL.

method (optional): HTTP method. Defaults to GET.

headers (optional): Dictionary of request headers.

body (optional): JSON string sent in the request body.

## Example Output
yaml
Copy
Edit
[WARN] https://example.com/ is DOWN. Status: 200, Time: 518ms
[ERROR] https://example.com/error connection failed: Read timed out.
example.com has 67% availability percentage
---
## Implementation Details
###  YAML Parsing
Accepts and parses a YAML file using argparse and PyYAML.

Supports optional headers, method, and body fields.

### Availability Tracking
Groups endpoints by domain (ignores port).

Only successful responses (status 2xx & under 500ms) count as available.

Availability is tracked cumulatively per domain and updated every cycle.

### HTTP Checks
Uses requests with a 500ms timeout.

Logs connection errors, slow responses, and unsuccessful status codes.

### Scheduler
Check cycle runs exactly every 15 seconds, independent of endpoint count or delays.

### Logging
Each check cycle outputs warnings, errors, and a summary of availability for each domain.

Availability percentage drops decimals per requirements.

## Notes
Stop monitoring with Ctrl+C.

Make sure URLs are reachable over the internet if testing publicly.

### License
This code is intended solely for technical evaluation purposes and is not production-ready.