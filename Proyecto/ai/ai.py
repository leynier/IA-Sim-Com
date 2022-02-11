from subprocess import run, PIPE, STDOUT
from os.path import exists
from shutil import rmtree

from pyke import knowledge_engine


def call_ai(script: str):
    ans = run(script, stdout=PIPE, stderr=STDOUT)
    return int(ans.stdout.decode("utf-8")[-3])


def edit_moto(environment):
    weather = environment.weather
    front = 0
    back = 0
    side = 0
    for section in environment.track.sections:
        if weather.is_front_wind(section[3]):
            front += 1
        elif weather.is_back_wind(section[3]):
            back += 1
        else:
            side += 1
    if front > back and front > side:
        direction = 1
    elif back > front and back > side:
        direction = 3
    else:
        direction = 2
    with open("ai/moto_facts.kfb", "w+") as facts:
        facts.write("# moto_facts.kfb\n\n")
        facts.write(
            "rainy({})\n".format(
                bool(weather.weather_status.name.__contains__("Rainy"))
            )
        )

        facts.write("humidity({})\n".format(weather.humidity > 6))
        facts.write("windy({})\n".format(weather.wind_intensity > 6))
        facts.write("wind_direction({})\n".format(direction))


def moto():
    engine = restart("bc_moto_rules")
    tires = [[], []]
    with engine.prove_goal("bc_moto_rules.select_type($select)") as gen:
        for ans, plan in gen:
            tires[0].append(ans["select"])
    with engine.prove_goal("bc_moto_rules.select_tires($select)") as gen:
        for ans, plan in gen:
            tires[1].append(ans["select"])
    for i in range(len(tires[0])):
        for j in range(len(tires[1])):
            comb = tires[0][i] + tires[1][j]
            print(comb if comb < 5 else 4)


def restart(rules: str):
    if exists("compiled_krb"):
        rmtree("compiled_krb")
    if exists("ai/compiled_krb"):
        rmtree("ai/compiled_krb")
    engine = knowledge_engine.engine(__file__)
    engine.reset()
    engine.activate(rules)
    return engine


def edit_action(speed, bike_max_speed, section_max_speed, section_type, tires, weather):
    with open("ai/action_facts.kfb", "w") as facts:
        facts.write("# action_facts.kfb\n\n")
        if speed > bike_max_speed or speed > section_max_speed:
            speed_cmp = 1
        elif speed < bike_max_speed and speed < section_max_speed:
            speed_cmp = 3
        else:
            speed_cmp = 2
        facts.write("speed({})\n".format(speed_cmp))
        facts.write("curve({})\n".format(section_type == "Curve"))
        facts.write("tires({})\n".format(bool(tires.__contains__("Slick"))))
        facts.write(
            "rainy({})\n".format(
                bool(weather.weather_status.name.__contains__("Rainy"))
            )
        )

        facts.write("humidity({})\n".format(weather.humidity > 6))


def action():
    engine = restart("bc_action_rules")
    actions = []
    with engine.prove_goal("bc_action_rules.select_action($select)") as gen:
        actions.extend(int(ans["select"]) for ans, plan in gen)
    print(sum(actions))


def acceleration(max_acceleration, weather, section, bike, rider):
    weather_status = [weather.weather_status == 1,
                      3 < weather.humidity < 7,
                      3 < weather.temperature < 7,
                      3 < weather.visibility < 7,
                      3 < weather.wind_intensity < 7]
    for w in weather_status:
        if not w:
            max_acceleration -= 1
    if section[4].name == "Straight":
        if bike.brakes < 9 and bike.chassis_stiffness < 9:
            max_acceleration -= 1
        if rider.step_by_line < 9:
            max_acceleration -= 1
    else:
        if bike.brakes != 5 and bike.chassis_stiffness != 5:
            max_acceleration -= 1
        if rider.cornering < 9:
            max_acceleration -= 1
    return max_acceleration
