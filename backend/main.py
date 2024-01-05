from fastapi import FastAPI, Path, BackgroundTasks, Query
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


### General: -----------------------------------------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {"data": "Welcome to the Caturanga API!!"}

### Run Simulations: ---------------------------------------------------------------------------------------------------

# this runs the Burundi simulation and returns the result
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


# Run a simulation with the simsettins for a specific simulation:
@app.get("/run_simulation_simsettings/{simsetting_id}")
async def run_simulation_simsettings(
        simsetting_id: str = Path(
            description="The ID of the simulation you want to run"
        ),
):
    return await controller.run_simulation_simsettings(simsetting_id)

'''
# Run a simulation with the simsettings_id and the location name:
@app.get("/run_simulation/config/")  # E.g. /run/simulation/config/?location=Ethipia&simsettings_id=abcde
async def run_simulation_config(
        simulation_id: str = '658dec24819bd1bc1ff738cd',
        simsettings_id: str = '6570f624987cdd647c68bc7d'  # Default ID der Simulation Settings
):
    return await controller.run_simulation_config(simulation_id, simsettings_id)
    '''

# Run a simulation with the simsettings_id and the location name:
# E.g. /run_simulation/config/?simulation_id=658dec24819bd1bc1ff738cd&simsettings_id=6570f624987cdd647c68bc7d
@app.get("/run_simulation/config/")
async def run_simulation_config(
        simulation_id: str = Query(
            description="Id der config simulation",
            example="658dec24819bd1bc1ff738cd"
        ),
        simsettings_id: str = Query(
            description="Id der Id der simsetttings",
            example="6570f624987cdd647c68bc7d"
        )
):
    return await controller.run_simulation_config(simulation_id, simsettings_id)


### Simulation: --------------------------------------------------------------------------------------------------------

## Return all simulations:
@app.get("/simulations")
async def get_all_simulations():
    """
    Return the data of all simulations.
    """
    return await controller.get_all_simulations()


## Return a single simulation by id:
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


### Simulation results: ------------------------------------------------------------------------------------------------

## Return all simulation results:
@app.get("/simulation_results")
async def get_all_simulation_results():
    """
    Retrieves all simulation results.

    Returns:
        A list of simulation results.
    """
    return await controller.get_all_simulation_results()


## Return simulation results of a specific simulation:
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


### Simulation inputs: -------------------------------------------------------------------------------------------------

class SimulationSetting(BaseModel):
    log_levels: str
    spawn_rules: str
    move_rules: str
    optimizations: str


JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


## Return all simsettings:
@app.get("/simsettings")
async def get_all_simsettings():
    """
    Return the data of all simsettings.
    """
    return await controller.get_all_simsettings()


## Return simsettings for a specific simulation:
@app.get("/simsettings/{simsetting_id}")
async def get_simulation(
        simsetting_id: str = Path(
            description="The ID of the simsetting whose data you want to view."
        ),
):
    return await controller.get_simsetting(simsetting_id)


## Post new simsettings:
@app.post("/simsettings")
async def post_simsettings(simsetting: JSONStructure = None):
    """
    Example:
        # curl -X POST "http://127.0.0.1:8080/simsettings" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"test_key\":\"test_val\"}"
    """
    await controller.post_simsettings(simsetting)
    return {"data": simsetting}


## Delete simsettings for a specific simulation:
@app.delete("/simsettings/{simsetting_id}")
async def delete_simsetting(
        simsetting_id: str = Path(
            description="The ID of the simsetting you want to delete."
        ),
):
    return await controller.delete_simsetting(simsetting_id)


# Helper Functions -----------------------------------------------------------------------------------------------------

# Retrieve simsettings from the DB and store them in a .yml file in the filesystem:
@app.get("/teststore/{simsetting_id}")
async def teststore(
    simsetting_id: str = Path(
        description="The ID of the simsetting you want to delete."
    )
):
    """
    Store a simsetting, given by the simsetting_id in the filesystem
    """
    return await controller.teststore_ss(simsetting_id)

# Read a stored simsettings.yml file from the filesystem:
@app.get("/testread_ss/{simsetting_id}")
def testread(
        simsetting_id: str = Path(
            description="The ID of the simsetting you want to read the yml file from."
        )
):
    """
    Read a simsettings.yml file for a given simsettings_id, stored in the filesystem
    """
    return controller.testread_ss(simsetting_id)

# Store all data (in the DB) in .csv files in the filesystem, for a given simulation_id:
@app.get("/test_csv/{simulation_id}")
async def test_csv(
        simulation_id: str = '658dec24819bd1bc1ff738cd'
):
    """
    Convert all data in DB, stored for given simulation, to .csv files and store them in filesystem
    """
    return await controller.convert_simulations_to_csv(simulation_id)


# Read all stored .csv in the filesystem for given simulation_id:
@app.get("/testread_csv/{simulation_id}")
def testread(
        simulation_id = Path(
            description="ID of simulation of .csv file, which should be returned"
        )
):
    """
    Read all data for given simulation from stored .csv files in filesystem
    """
    return controller.testread_csv(simulation_id)
