from input_data import stations, no_position_station, tasks, tasks_duration, precedences, station_order, email, pwd,\
    name
from pulp import *
from cornflow_client import CornFlow, group_variables_by_name
import time

# creating the model
model_cycle_time = LpProblem("MinCost", LpMinimize)

# creating the variables
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

client = CornFlow(url="CORNFLOW_WEB_SERVER_URL")
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
t = time.time()
execution_id = client.create_execution(instance_id, config)
status = client.get_status(execution_id)
while not status['finished']:
    time.sleep(2)
    status = client.get_status(execution_id)

print("Elapsed time: " + str(time.time() - t))
results = client.get_results(execution_id)

_vars, model_cycle_time = LpProblem.from_dict(results['execution_results'])
actual_vars = group_variables_by_name(_vars, ['TaskInStation'], replace_underscores_with_spaces=True)
actual_vars.keys()

# Print variables
print(actual_vars['TaskInStation'])

# The status of the solution is printed to the screen
print("Status:", LpStatus[model_cycle_time.status])

# Each of the variables is printed with it's resolved optimum value
for v in model_cycle_time.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total Cost of Tasks = ", pulp.value(model_cycle_time.objective))

# get the values for the variables:
print({k: v.value() for k, v in _vars.items()})

# get the log in text format
print(results['log_text'])

# get the log in json format
print(results['log_json'])
