from fastapi import FastAPI, HTTPException, Path, BackgroundTasks
from controller.handler.database_handler import DatabaseHandler
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, AnyStr, List, Union
from controller.simulation_executor import SimulationExecutor

app = FastAPI()

default_input_id = "65a6d3eb9ae2636fa2b3e3c6"
default_setting_id = "6599846eeb8f8c36cce8307a"

database_handler = DatabaseHandler(default_input_id, default_setting_id)
simulation_executor = SimulationExecutor(database_handler)

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

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
    data = await simulation_executor.initialize_simulation(
        simulation_config=simulation_config
    )

    background_tasks.add_task(
        simulation_executor.run_simulation,
        data["name"],
        data["simulation_id"],
        data["simsettings_id"],
        data["objectid"],
        data["simsettings_filename"],
        data["simulation_dir"],
        data["validation_dir"])

    return {"dummy simulation": str(data["objectid"])}

# /simulations


@app.get("/simulations")
async def get_all_simulations():
    """
    Return the data of all simulations.

    Returns:
    - list: The data of the all simulations.
    """
    return await database_handler.get_all("simulations")


@app.get("/simulations/summary")
async def get_all_simulation_summaries():
    """
    Retrieves all simulation summaries.
    A simulation summary contains the simulation ID and the simulation name.

    Returns:
    - list of simulation summaries.
    """
    summary = await database_handler.get_summaries("simulations")
    return {"data": summary,
            "protectedIDs": [default_input_id]}


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
    return await database_handler.get("simulations", simulation_id)


@app.delete("/simulations/{simulation_id}")
async def delete_simulation_and_associated_results(
        simulation_id: str = Path(),
):
    """
    Deletes a simulation (called "input" in the GUI) with the given ID.

    Parameters:
    - simulation_id (str): The ID of the simulation to delete.

    Returns:
    - The result of the deletion operation.
    """
    return await database_handler.delete_simulation_and_associated_results(
        simulation_id)


@app.post("/simulations")
async def post_simulation(
        simulation: JSONStructure = None):
    """
    Posts the simulation input to the api_service.

    Parameters:
    - simulation (JSONStructure, optional): The simulation input.

    Returns:
    - dict: A dictionary containing the posted simulation input.
    """
    try:
        basic_input = await database_handler.get(
            "simulations",
            default_input_id)
        simulation_id = await database_handler.post(
            simulation,
            "simulations",
            basic_input)
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
    return await database_handler.get_all("simulations_results")


@app.get("/simulation_results/summary")
async def get_all_simulation_result_summaries():
    """
    Retrieves all simulation result summaries.
    A simulation result summary contains the
    simulation result ID and the simulation result name.

    Returns:
    - list of simulation result summaries.
    """
    return await database_handler.get_summaries("simulations_results")


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
    return await database_handler.get("simulations_results", 
                                      simulation_result_id)


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
    return await database_handler.delete("simulations_results",
                                         simulation_result_id)


# Simulation Settings: --------------------------------------------------------


@app.get("/simsettings")
async def get_all_simsettings():
    """
    Return all simsettings.

    Returns:
    - list: A list of all simulation settings.
    """
    simsettings = await database_handler.get_all("simsettings")
    return {"data": simsettings,
            "protectedIDs": [default_setting_id]}


@app.get("/simsettings/summary")
async def get_all_simsetting_summaries():
    """
    Retrieves all simsetting summaries.
    A simsetting summary contains the simsetting ID and the simsetting name.

    Returns:
    - list of simsetting summaries.
    """
    summary = await database_handler.get_summaries("simsettings")
    return {"data": summary,
            "protectedIDs": [default_setting_id]}


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
    return await database_handler.get("simsettings", simsetting_id)


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
        basic_setting = await database_handler.get(
            "simsettings",
            default_setting_id)
        simsetting_id = await database_handler.post(
            simsetting,
            "simsettings",
            basic_setting)
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
    return await database_handler.delete("simsettings", simsetting_id)
