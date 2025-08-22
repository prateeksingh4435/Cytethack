

BACKEND_URL = "http://127.0.0.1:8000/api/process/"
API_KEY = "Hello"
import psutil
import platform
import requests
import json
import os

def get_system_details():
    return {
        "os": platform.system() + " " + platform.release(),
        "processor": platform.processor(),
        "ram_total": psutil.virtual_memory().total / (1024**3),  # Convert bytes to GB
        "ram_used": psutil.virtual_memory().used / (1024**3),
        "ram_available": psutil.virtual_memory().available / (1024**3),
        "storage_total": psutil.disk_usage('/').total / (1024**3),
        "storage_free": psutil.disk_usage('/').free / (1024**3),
    }

def get_processes():
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'ppid', 'cpu_percent', 'memory_percent', 'memory_info']):
        info = proc.info
        try:
            has_children = len(proc.children(recursive=False)) > 0
        except psutil.Error:
            has_children = False
        process_list.append({
            "pid": info['pid'],
            "name": info['name'],
            "parent_pid": info['ppid'],
            "cpu_percent": info['cpu_percent'],
            "memory_percent": info['memory_percent'],
            "memory_usage": info['memory_info'].rss / (1024**2),  # Convert bytes to MB
            "has_children": has_children
        })
    return process_list

def send_data():
    data = {
        "hostname": platform.node(),
        "system_details": get_system_details(),
        "processes": get_processes()
    }
    headers = {'Content-Type': 'application/json', 'API-Key': API_KEY}
    try:
        response = requests.post(BACKEND_URL, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")

if __name__ == "__main__":
    send_data()