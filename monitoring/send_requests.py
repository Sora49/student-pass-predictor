"""Generate traffic for the monitoring experiment (works on Windows/Mac/Linux).

Run:  python monitoring/send_requests.py            (20 valid + 5 invalid)
      python monitoring/send_requests.py 100 10     (100 valid + 10 invalid)
"""
import json
import random
import sys
import urllib.error
import urllib.request

URL = "http://localhost:5000/predict"


def post(payload):
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read())


def main(valid=20, invalid=5):
    for _ in range(valid):
        payload = {
            "study_hours": round(random.uniform(0, 10), 1),
            "attendance": random.randint(40, 100),
            "previous_score": random.randint(20, 100),
            "extra_classes": random.choice(["yes", "no"]),
        }
        print(post(payload))
    bad_inputs = [{"study_hours": 15, "attendance": 80, "previous_score": 70,
                   "extra_classes": "yes"},
                  {"attendance": 80},
                  {"study_hours": "abc", "attendance": 80, "previous_score": 70,
                   "extra_classes": "no"}]
    for i in range(invalid):
        print(post(bad_inputs[i % len(bad_inputs)]))


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:3]]
    main(*args)
