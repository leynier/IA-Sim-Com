from random import normalvariate, randint
from simulation.environment import Environment


class Race:
    def __init__(self, environment: Environment, agents, laps):
        self.environment = environment
        self.agents = agents
        self.laps = laps
        self.current_lap = 0
        self.rank = agents
        for agent in agents:
            agent.update_agent_initial_parameters(self.environment.weather, self.environment.track.sections[0])
            agent.bike.select_configuration(environment)

    def change_lap(self):
        self.current_lap += 1
        if self.current_lap == self.laps:
            print("\nCarrera terminada\n")
            self.print_ranking()
            return True
        elif self.current_lap == self.laps - 1:
            self.environment.change_weather_status()
            for agent in self.agents:
                if agent.flag_to_pits:
                    agent.bike.select_configuration(self.environment)
                agent.update_agent_initial_parameters(self.environment.weather, self.environment.track.sections[0])
            print("\nUltima vuelta\n")
            self.print_ranking()
            return False
        else:
            self.environment.change_weather_status()
            for agent in self.agents:
                if agent.flag_to_pits:
                    agent.bike.select_configuration(self.environment)
                agent.update_agent_initial_parameters(self.environment.weather, self.environment.track.sections[0])
            print("\nVuelta {}\n".format(self.current_lap))
            self.print_ranking()
            return False

    def print_ranking(self):
        i = 1
        for x in self.rank:
            print("{}: {}".format(i, x.rider.name))
            i += 1
        print()

    def ranking(self):
        self.agents.sort(key=lambda agent: agent.time_lap)

    def continuous_variable_generator(self):
        return normalvariate(0.5, 0.16)

    def discrete_variable_generator(self):
        return randint(1, 10)
