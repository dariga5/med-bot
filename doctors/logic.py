import json
import os

def read_json(path: str) -> dict:
    with open(path) as json_file:
        return json.load(json_file)

def get_plan(name: str) -> dict:
    file_name = "doctors/" + name + ".json"
    return read_json(file_name)


def GetPlanAllDoctor() -> dict:
    all_plans = {}

    for name in ["ivanov", "petrov", "sidorov"]:
        all_plans[name] = get_plan(name)


    return all_plans


def Save(doctor: str, date: str, time: str, state: bool):
    
    file_name = "doctors/" + doctor + ".json"
    
    plan = get_plan(doctor)

    for day in plan['plan']:
        if day['day'] == date:
            for item in day['timetable']:
                if item['time'] == time:
                    item['state'] = state


    with open(file_name, "w") as json_file:
        json.dump(plan, json_file)
