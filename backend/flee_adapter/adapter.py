import subprocess
import os
import pandas as pd
from runscripts.run import Simulation

class Adapter:
    def __init__(self):
        # This method is intentionally left empty
        pass
    
    def run_simulation(self):
        sim = Simulation("flee/test_data/test_input_csv", "flee/test_data/test_input_csv/refugee_data", 0, "flee/test_data/simsetting.yml")
        result = sim.run()
        
        return result
    
