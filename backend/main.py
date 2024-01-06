from fastapi import FastAPI, Path, Request, BackgroundTasks
from flee_controller.controller import Controller
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, AnyStr, List, Union

app = FastAPI()
controller = Controller()

# allow CORS (Cross Origin Resource Sharing) - allows us to access the API from a different origin
# e.g. if we have a frontend on localhost:3000 and the API on localhost:8000, we need to allow the frontend to access the API

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # allow cookies
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)


@app.get("/")
def read_root():
    return {"data": "Welcome to the Caturanga API!"}


# this runs the Burundi simulation and returns the result
# TODO - this should take a simulation ID as a parameter and run that simulation
@app.get("/run_simulation")
async def run_simulation(background_tasks: BackgroundTasks):
    """
    Runs the simulation using the controller module.

    Returns:
        The object id of the dummy simulation result.

    Background Tasks:
        The simulation is run in the background using FastAPI's BackgroundTasks.
        This allows the user to continue using the application without waiting for the simulation to complete.

    References:
        - FastAPI Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
        - Celery: https://docs.celeryproject.org/en/stable/
            Celery is an alternative to FastAPI's BackgroundTasks that provides more complex setup but can be used
            for heavy background computation.

    """
    object_id = await controller.store_dummy_simulation()

    background_tasks.add_task(controller.run_simulation, object_id)

    return {"dummy simulation": str(object_id)}


@app.get("/simulation_results")
async def get_all_simulation_results():
    """
    Retrieves all simulation results.

    Returns:
        A list of simulation results.
    """
    return await controller.get_all_simulation_results()



@app.get("/simulation_results/{simulation_result_id}")
async def get_simulation_result(
    simulation_result_id: str = Path(
        description="The ID of the simulation whose data you want to view."
    ),
):
    """
    Retrieve the data of a simulation result based on its ID.

    Args:
        simulation_result_id (str): The ID of the simulation result.

    Returns:
        The data of the simulation result.
    """
    return await controller.get_simulation_result(simulation_result_id)


@app.get("/simulations")
async def get_all_simulations():
    """
    Return the data of all simulations.
    """
    return await controller.get_all_simulations()


@app.get("/simulations/{simulation_id}")
async def get_simulation(
    simulation_id: str = Path(
        description="The ID of the simulation whose data you want to view."
    ),
):
    """
    Return the data of a simulation based on its ID.

    Parameters:
        simulation_id (str): The ID of the simulation.

    Returns:
        dict: The data of the simulation.
    """
    return await controller.get_simulation(simulation_id)


class SimulationSetting(BaseModel):
    log_levels: str
    spawn_rules: str
    move_rules: str
    optimizations: str


JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


@app.get("/simsettings")
async def get_all_simsettings():
    """
    Return the data of all simsettings.
    """
    return await controller.get_all_simsettings()


@app.get("/simsettings/{simsetting_id}")
async def get_simulation(
    simsetting_id: str = Path(
        description="The ID of the simsetting whose data you want to view."
    ),
):
    return await controller.get_simsetting(simsetting_id)


@app.post("/simsettings")
async def post_simsettings(simsetting: JSONStructure = None):
    """
    Example:
        # curl -X POST "http://127.0.0.1:8080/simsettings" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"test_key\":\"test_val\"}"
    """
    await controller.post_simsettings(simsetting)
    return {"data": simsetting}

@app.get("/migrate-from-atlas")
def migrate_from_atlas():
    """
    Insert all data from the Atlas database into the Amazon DocumentDB database.
    """
    return controller.migrate_from_atlas()



@app.delete("/simsettings/{simsetting_id}")
async def delete_simsetting(
    simsetting_id: str = Path(
        description="The ID of the simsetting you want to delete."
    ),
):
    return await controller.delete_simsetting(simsetting_id)
