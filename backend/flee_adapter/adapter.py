from runscripts.runner import Simulation

class Adapter:
    def __init__(self):
        # This method is intentionally left empty
        pass
    
    def run_simulation(self):
        sim = Simulation("flee/conflict_input/burundi", "flee/conflict_validation/burundi2015", 0, "flee/test_data/simsetting.yml")
        result = sim.run()
        return result

    def run_simulation(self, simsettings_file: str):
        sim = Simulation("flee/conflict_input/burundi", "flee/conflict_validation/burundi2015", 0, simsettings_file)
        result = sim.run()
        return result
