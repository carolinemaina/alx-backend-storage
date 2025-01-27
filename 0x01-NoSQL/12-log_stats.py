#!/usr/bin/python3
"""
Script that provides statistics about Nginx logs stored in MongoDB.
"""
from pymongo import MongoClient

def print_nginx_stats():
    # Connect to MongoDB server
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    # Count total logs
    total_logs = collection.count_documents({})

    # Count methods
    methods = {
        "GET": collection.count_documents({"method": "GET"}),
        "POST": collection.count_documents({"method": "POST"}),
        "PUT": collection.count_documents({"method": "PUT"}),
        "PATCH": collection.count_documents({"method": "PATCH"}),
        "DELETE": collection.count_documents({"method": "DELETE"})
    }

    # Count the GET requests with path /status
    status_check = collection.count_documents({"method": "GET", "path": "/status"})

    # Print the total number of logs
    print(f"{total_logs} logs")

    # Print methods
    print("Methods:")
    for method, count in methods.items():
        print(f"\tmethod {method}: {count}")

    # Print status check (GET method with /status path)
    print(f"{status_check} status check")

if __name__ == "__main__":
    print_nginx_stats()
