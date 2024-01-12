from runscripts.runner import Simulation


class Adapter:
    """
    Adapter class for running simulations using the FLEE library.
    """

    def __init__(self):
        # This method is intentionally left empty
        pass

    def run_simulation_config(self,
                              simulation_dir: str,
                              simsettings_file: str,
                              validation_dir: str):
        """
        Runs a simulation using custom simulation and simsettings.

        Parameters:
        - simulation_dir (str): The path to the simulation directory.
        - simsettings_file (str): The path to the simsettings file.

        Returns:
        -dict: The result of the simulation.
        """
        sim = Simulation(simulation_dir,
                         validation_dir,
                         0,
                         simsettings_file)

        try:
            result = sim.run()
        except Exception as e:
            result = {"error": "{}".format(e)}
        except SystemExit as e:
            result = {"error": "{}".format(e)}

        return result
