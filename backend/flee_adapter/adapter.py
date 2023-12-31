import pathlib
import sys

# add flee directory to PYTHONPATH
backend = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(backend / "flee"))

from flee.runscripts.runner import Simulation  # noqa: E402

class Adapter:
    def __init__(self):
        # This method is intentionally left empty
        pass
    
    def run_simulation(self):
        sim = Simulation("flee/conflict_input/burundi", "flee/conflict_validation/burundi2015", 0, "flee/test_data/simsetting.yml")
        result = sim.run()
        
        return result
    
