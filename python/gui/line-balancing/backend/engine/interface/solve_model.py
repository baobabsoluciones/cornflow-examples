from pulp import *
from cornflow_client import CornFlow, group_variables_by_name
from interface.models import Tasks, Stations, Precedences, Solution
from interface.const import email, name, pwd
import time


def solve():

    model_cycle_time = LpProblem("MinCost", LpMinimize)

    # creating the variables
    read_tasks = Tasks.objects.all()
    read_stations = Stations.objects.all()
    tasks = [t.name for t in read_tasks]
    stations = [s.name for s in read_stations]
    tasks_duration = {t.name: t.duration for t in read_tasks}
    no_position_station = {s.name: s.no_position for s in read_stations}
    station_order = {s.name: s.order for s in read_stations}
    precedences = [(p.before.name, p.after.name) for p in Precedences.objects.all()]


    v01TaskInStation = LpVariable.dicts("TaskInStation", [(t, s) for t in tasks for s in stations], cat=LpBinary)
    vCycleTime = LpVariable("CycleTime")

    for t in tasks:
        model_cycle_time += sum(v01TaskInStation[t, s] for s in stations) == 1, "c1" + str(t)

    for s in stations:
        model_cycle_time += vCycleTime >= sum(v01TaskInStation[t, s] * tasks_duration[t] for t in tasks) \
                            / no_position_station[s], "c2" + str(s)

    for (t1, t2) in precedences:
        model_cycle_time += sum(v01TaskInStation[t1, s] * station_order[s] for s in stations) \
                            <= sum(v01TaskInStation[t2, s] * station_order[s] for s in stations), "c3" + str(t1) + str(t2)

    model_cycle_time += vCycleTime, "Objetive"

    # model_cycle_time.solve()

    # Starting up cornflow client
    config = dict(email=email, pwd=pwd, name=name)

    client = CornFlow(url="CORNFLOW_WEBSERVER_URL")
    # client.sign_up(**config)
    client.login(email, pwd)

    data = model_cycle_time.to_dict()
    instance_id = client.create_instance(data)

    config = dict(
        solver="PULP_CBC_CMD",
        mip=True,
        msg=True,
        warmStart=True,
        timeLimit=10,
        options=["donotexist", "thisdoesnotexist"],
        keepFiles=0,
        gapRel=0,
        gapAbs=0,
        threads=1,
        logPath="test_export_solver_json.log"
    )

    execution_id = client.create_execution(instance_id, config)
    status = client.get_status(execution_id)
    while not status['finished']:
        time.sleep(2)
        status = client.get_status(execution_id)

    results = client.get_results(execution_id)

    _vars, model_cycle_time = LpProblem.from_dict(results['execution_results'])
    actual_vars = group_variables_by_name(_vars, ['TaskInStation'], replace_underscores_with_spaces=True)
    actual_vars.keys()
    values = {k: v.value() for k, v in _vars.items()}

    Solution.objects.all().delete()
    for var in actual_vars['TaskInStation'].keys():
        if values[str(actual_vars['TaskInStation'][var])] != 0:
            Solution(station=Stations.objects.get(name=var[1]), task=Tasks.objects.get(name=var[0])).save()



