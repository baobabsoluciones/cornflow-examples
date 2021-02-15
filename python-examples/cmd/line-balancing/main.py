from input_data import data as default_data
from pulp import *
from cornflow_client import CornFlow, group_variables_by_name
import time
import click


class PythonJsonOption(click.Option):

    def type_cast_value(self, ctx, value):
        try:
            return json.loads(value)
        except:
            raise click.BadParameter(value)


@click.group()
def cli():
    pass

@cli.command()
@click.option('--cornflow-url', required=True, help='URL to Cornflow server')
@click.option('--email', required=True, help='Username')
@click.option('--password', required=True, help='Password for the user.')
@click.option('--name', required=True, help='Name of the user.')
def signup(name, email, password, cornflow_url):
    config = dict(email=email, pwd=password, name=name)
    client = CornFlow(url=cornflow_url)
    try:
        client.sign_up(**config)
        print("Username {} created correctly".format(email))
    except Exception as e:
        print("There was an error creating username {}: {}".format(email, e))
    return


@cli.command()
@click.option('--cornflow-url', required=True, help='URL to Cornflow server')
@click.option('--email', required=True, help='Username')
@click.option('--password', required=True, help='Password for the user.')
@click.option('--data', default='{}', cls=PythonJsonOption, help='Input data to solve the problem. See the default for reference.')
@click.option('--debug/--no-debug', default=True, help='If true prints details in console.')
@click.option('--wait/--no-wait', default=True, help='If true waits for the solution to be ready.')
def solve_problem(email, password, cornflow_url, data, debug, wait):
    if not data:
        data = default_data
    client = CornFlow(url=cornflow_url)
    client.login(email, password)
    model_data = generate_model(data)

    instance = client.create_instance(model_data)

    solve_config = dict(
        solver="PULP_CBC_CMD",
        timeLimit=10,
    )
    execution = client.create_execution(instance['id'], solve_config)
    if not wait:
        print("Instance id is: {}".format(instance['id']))
        print("Execution id is: {}".format(execution['id']))
        return
    _load_solution(client, execution['id'], debug, wait)


@cli.command()
@click.option('--cornflow-url', required=True, help='URL to Cornflow server')
@click.option('--email', required=True, help='Username')
@click.option('--password', required=True, help='Password for the user.')
@click.option('--execution-id', required=True, help='Execution id to download solution from.')
@click.option('--debug/--no-debug', default=True, help='If true prints details in console.')
@click.option('--wait/--no-wait', default=True, help='If true waits for the solution to be ready.')
def load_solution(email, password, cornflow_url, execution_id, debug, wait):

    client = CornFlow(url=cornflow_url)
    client.login(email, password)
    _load_solution(client, execution_id, debug, wait)


def _load_solution(client, execution_id, debug, wait):

    status = client.get_status(execution_id)
    while not status['state'] != 0 :
        time.sleep(2)
        status = client.get_status(execution_id)
        if not wait:
            print("Solution is not ready, yet")
            break
    if status['state'] != 1:
        print("There was an error with your solving and results are not available")

    results = client.get_solution(execution_id)
    log_json = client.get_log(execution_id)

    _vars, model_cycle_time = LpProblem.from_dict(results['data'])
    actual_vars = group_variables_by_name(_vars, ['TaskInStation'], replace_underscores_with_spaces=True)

    # Print variables
    if debug:
        print("All variables:")
        print(actual_vars['TaskInStation'])

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[model_cycle_time.status])

    # Each of the variables is printed with it's resolved optimum value
    print("Basic variables:")
    for v in model_cycle_time.variables():
        if v.varValue:
            print(v.name, "=", v.varValue)

    # The optimised objective function value is printed to the screen
    print("Total Cost of Tasks = ", pulp.value(model_cycle_time.objective))

    # get the values for the variables:
    if debug:
        print({k: v.value() for k, v in _vars.items()})

    # # get the log in text format
    # if debug:
    #     print(results['log_text'])
    #
    # get the log in json format
    if debug:
        print(log_json)


def generate_model(data):
    tasks = data['tasks']
    stations = data['stations']
    precedences = data['precedences']
    no_position_station = data['no_position_station']
    tasks_duration = data['tasks_duration']
    station_order = data['station_order']

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

    for (t1, t2_list) in precedences.items():
        for t2 in t2_list:
            model_cycle_time += sum(v01TaskInStation[t1, s] * station_order[s] for s in stations) \
                                <= sum(v01TaskInStation[t2, s] * station_order[s] for s in stations), "c3" + str(t1) + str(t2)

    model_cycle_time += vCycleTime, "Objective"
    return model_cycle_time.to_dict()


if __name__ == '__main__':
    cli()
