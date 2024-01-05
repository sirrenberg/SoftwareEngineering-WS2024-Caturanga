from runscripts.runner import Simulation


class Adapter:
    """
    Adapter class for running simulations using the FLEE library.
    """

    def __init__(self):
        # This method is intentionally left empty
        pass

    def run_simulation(self):
        """
        Runs a default simulation using the FLEE library.

        Returns:
        - dict: The result of the simulation.
        """
        sim = Simulation("flee/conflict_input/burundi",
                         "flee/conflict_validation/burundi2015",
                         0,
                         "flee/test_data/simsetting.yml")
        result = sim.run()

        return result

    def run_simulation_ss(self,
                          simsettings_file: str):
        """
        Runs a simulation using custom simsettings.

        Parameters:
        - simsettings_file (str): The path to the simsettings file.

        Returns:
        - dict: The result of the simulation.
        """
        sim = Simulation("flee/conflict_input/burundi",
                         "flee/conflict_validation/burundi2015",
                         0,
                         simsettings_file)
        result = sim.run()

        return result

    def run_simulation_config(self,
                              simulation_dir: str,
                              simsettings_file: str):
        """
        Runs a simulation using custom simulation and simsettings.

        Parameters:
        - simulation_dir (str): The path to the simulation directory.
        - simsettings_file (str): The path to the simsettings file.

        Returns:
        -dict: The result of the simulation.
        """
        sim = Simulation(simulation_dir,
                         "flee/conflict_validation/burundi2015",
                         0,
                         simsettings_file)
        result = sim.run()

        return result
