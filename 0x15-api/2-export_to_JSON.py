#!/usr/bin/python3
"""
Fetches employees todo details from an api
"""
import json
import requests
import sys


BASE_URL = "https://jsonplaceholder.typicode.com/users/{}"
TODO_URL = BASE_URL + '/todos'


def get_employee_info(employee_id):
    """Fetches employee name"""
    employee_info_url = BASE_URL.format(employee_id)
    try:
        employee_info_response = requests.get(employee_info_url).json()
        return employee_info_response.get('username')
    except requests.exceptions.RequestException as e:
        print("Error fetching employee information: %s", e)
        sys.exit(1)


def fetch_employee_todo_progress(employee_id):
    """
    Given employee ID, returns information about his/her
    TODO list progress
    """
    todo_url = TODO_URL.format(employee_id)
    try:
        todo_response = requests.get(todo_url).json()
        return todo_response
    except requests.exceptions.RequestException as e:
        print("Error fetching employee TODO information: %s", e)
        sys.exit(1)


def write_to_json_file(employee_id, employee_name, todo_data, json_file):
    """Writes to a json file"""
    try:
        user_tasks = {employee_id: []}
        for res in todo_data:
            user_tasks[employee_id].append({
                "task": res.get('title'),
                "completed": res.get('completed'),
                "username": employee_name
            })
        with open(json_file, 'w') as f:
            json.dump(user_tasks, f)
    except requests.exceptions.RequestException as e:
        print("Error occurred while writing to a file: {}".format(e))
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: {} <employee_id>".format(sys.argv[0]))
        exit(1)

    employee_id = int(sys.argv[1])
    json_file = "{}.json".format(employee_id)
    try:
        employee_name = get_employee_info(employee_id)
        todo_data = fetch_employee_todo_progress(employee_id)
        write_to_json_file(employee_id=employee_id,
                           employee_name=employee_name,
                           todo_data=todo_data, json_file=json_file)
    except Exception as e:
        print("An error occurred: %s", e)
        sys.exit(1)
