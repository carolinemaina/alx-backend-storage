#!/usr/bin/env python3
from pymongo import MongoClient

def log_stats():
    """Retrieve stats from the nginx logs in MongoDB."""
    # Connect to MongoDB
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    # 1. Count total number of logs
    total_logs = collection.count_documents({})

    # 2. Count occurrences of each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts[method] = collection.count_documents({"method": method})

    # 3. Count GET requests to /status
    status_check = collection.count_documents({"method": "GET", "path": "/status"})

    # 4. Print the stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check} status check")

if __name__ == "__main__":
    log_stats()
