from fastapi import FastAPI, HTTPException, Path, BackgroundTasks
from flee_controller.controller import Controller
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, AnyStr, List, Union

app = FastAPI()
controller = Controller()

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


# TODO: adjust this for production as allowing all origins is not secure
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # allow cookies
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)


# General: --------------------------------------------------------------------


@app.get("/")
def read_root():
    """
    Root of the Caturanga API.

    :return: A dictionary containing the welcome message.
    """
    return {"data": "Welcome to the Caturanga API!!"}


# Simulation Execution: -------------------------------------------------------


@app.post("/run_simulation/config")
async def run_simulation_config(
        background_tasks: BackgroundTasks,
        simulation_config: JSONStructure = None
):
    """
    Run simulation with specified simulation input and settings.

    Parameters:
    - background_tasks (BackgroundTasks): The background tasks object used to
      run the simulation asynchronously.
    - simulation_config (JSONStructure, optional) containing:
        - input_id (str): The ID of the simulation input.
        - input_name (str): The name of the simulation input.
        - simsettings_id (str): The ID of the simulation settings.
        - simsettings_name (str): The name of the simulation settings.

    Returns:
        dict: A dictionary containing the object ID of the dummy simulation.

    Example:
        To query this endpoint, use the following URL format:
        /run_simulation/config/

        The body has to have following format:

        {
            input: {
                input_id: <input_id>,
                input_name: <input_name>
            },
            settings: {
                simsettings_id: <simsettings_id>,
                simsettings_name: <simsettings_name>
            }
        }

    """
    data = await controller.initialize_simulation(
        simulation_config=simulation_config
    )

    background_tasks.add_task(
        controller.run_simulation_config,
        data["name"],
        data["simulation_id"],
        data["simsettings_id"],
        data["objectid"],
        data["simsettings_filename"],
        data["simulation_dir"],
        data["validation_dir"])

    return {"dummy simulation": str(data["objectid"])}


# Simulations: ---------------------------------------------------------------


@app.get("/simulations")
async def get_all_simulations():
    """
    Return the data of all simulations.

    Returns:
    - list: The data of the all simulations.
    """
    return await controller.get_all_simulations()


@app.get("/simulations/summary")
async def get_all_simulation_summaries():
    """
    Retrieves all simulation summaries.
    A simulation summary contains the simulation ID and the simulation name.

    Returns:
    - list of simulation summaries.
    """
    return await controller.get_all_simulation_summaries()


@app.get("/simulations/{simulation_id}")
async def get_simulation(
        simulation_id: str = Path(),
):
    """
    Return the data of a simulation based on its ID.

    Parameters:
    - simulation_id (str): The ID of the simulation.

    Returns:
    - dict: The data of the simulation.
    """
    return await controller.get_simulation(simulation_id)


@app.post("/simulations")
async def post_simulation(
        simulation: JSONStructure = None):
    """
    Posts the simulation input to the controller.

    Parameters:
    - simulation (JSONStructure, optional): The simulation input.

    Returns:
    - dict: A dictionary containing the posted simulation input.
    """
    try:
        simulation_id = await controller.post_simulation(simulation)
        return {"id": simulation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Simulation results: -------------------------------------------------------


@app.get("/simulation_results")
async def get_all_simulation_results():
    """
    Retrieves all simulation results.

    Returns:
    - list: A list of all simulation results.
    """
    return await controller.get_all_simulation_results()


@app.get("/simulation_results/summary")
async def get_all_simulation_result_summaries():
    """
    Retrieves all simulation result summaries.
    A simulation result summary contains the
    simulation result ID and the simulation result name.

    Returns:
    - list of simulation result summaries.
    """
    return await controller.get_all_simulation_result_summaries()


@app.get("/simulation_results/{simulation_result_id}")
async def get_simulation_result(
        simulation_result_id: str = Path(),
):
    """
    Retrieve the data of a simulation result based on its ID.

    Parameters:
    - simulation_result_id (str): The ID of the simulation result.

    Returns:
    - dict: The data of the simulation result.
    """
    return await controller.get_simulation_result(simulation_result_id)


@app.delete("/simulation_results/{simulation_result_id}")
async def delete_simulation_results(
        simulation_result_id: str = Path(),
):
    """
    Delete the data of a simulation result based on its ID.

    Parameters:
    - simulation_result_id (str): The ID of the simulation result.

    Returns:
    - dict: The data of the simulation result.
    """
    return await controller.delete_simulation_results(simulation_result_id)


# Simulation Settings: --------------------------------------------------------


@app.get("/simsettings")
async def get_all_simsettings():
    """
    Return all simsettings.

    Returns:
    - list: A list of all simulation settings.
    """
    return await controller.get_all_simsettings()


@app.get("/simsettings/summary")
async def get_all_simsetting_summaries():
    """
    Retrieves all simsetting summaries.
    A simsetting summary contains the simsetting ID and the simsetting name.

    Returns:
    - list of simsetting summaries.
    """
    return await controller.get_all_simsetting_summaries()


@app.get("/simsettings/{simsetting_id}")
async def get_simsetting(
        simsetting_id: str = Path(),
):
    """
    Retrieve the data of a simulation setting based on its ID.

    Parameters:
    - simsetting_id (str): The ID of the simulation setting.

    Returns:
    - dict: The data of the simulation setting.
    """
    return await controller.get_simsetting(simsetting_id)


@app.post("/simsettings")
async def post_simsettings(
        simsetting: JSONStructure = None):
    """
    Posts the simulation settings to the database.

    Parameters:
    - simsetting (JSONStructure, optional): The simulation settings.

    Returns:
    - dict: A dictionary containing the posted simulation settings id.
    """
    try:
        simsetting_id = await controller.post_simsettings(simsetting)
        return {"id": simsetting_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/simsettings/{simsetting_id}")
async def delete_simsetting(
        simsetting_id: str = Path(),
):
    """
    Deletes a simulation setting with the given ID.

    Parameters:
    - simsetting_id (str): The ID of the simulation setting to delete.

    Returns:
    - The result of the deletion operation.
    """
    return await controller.delete_simsetting(simsetting_id)
