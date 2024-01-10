from fastapi import FastAPI, Path, BackgroundTasks, Query
from flee_controller.controller import Controller
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, AnyStr, List, Union

app = FastAPI()
controller = Controller()


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


@app.get("/run_simulation/config/")
async def run_simulation_config(
        background_tasks: BackgroundTasks,
        simulation_id: str = Query(),
        simsettings_id: str = Query()
):
    """
    Run simulation with specified simulation input and settings.

    Parameters:
    - background_tasks (BackgroundTasks): The background tasks object used to
      run the simulation asynchronously.
    - simulation_id (str): The ID of the simulation input.
    - simsettings_id (str): The ID of the simulation settings.

    Returns:
        dict: A dictionary containing the object ID of the dummy simulation.

    Example:
        To query this endpoint, use the following URL format:
        /run_simulation/config/?simulation_id=<simulation_id>&simsettings_id=<simsettings_id>
    """
    data = await controller.initialize_simulation(
        simulation_id=simulation_id,
        simsettings_id=simsettings_id
    )

    background_tasks.add_task(
        controller.run_simulation_config,
        simulation_id,
        simsettings_id,
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


# Simulation results: -------------------------------------------------------


@app.get("/simulation_results")
async def get_all_simulation_results():
    """
    Retrieves all simulation results.

    Returns:
    - list: A list of all simulation results.
    """
    return await controller.get_all_simulation_results()


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


# Simulation Settings: --------------------------------------------------------


JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


@app.get("/simsettings")
async def get_all_simsettings():
    """
    Return all simsettings.

    Returns:
    - list: A list of all simulation settings.
    """
    return await controller.get_all_simsettings()


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
    Posts the simulation settings to the controller.

    Parameters:
    - simsetting (JSONStructure, optional): The simulation settings.

    Returns:
    - dict: A dictionary containing the posted simulation settings.
    """
    await controller.post_simsettings(simsetting)
    return {"data": simsetting}


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
