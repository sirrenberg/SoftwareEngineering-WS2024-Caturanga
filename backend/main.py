from fastapi import FastAPI, Path, Request
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

# Run the Burundi simulation and returns the result
@app.get("/run_simulation/")
def run_simulation():
    """
    Runs the simulation using the controller module.

    Returns:
        The result of the simulation.
    """
    return controller.run_simulation()


# Run a simulation with the simsettins for a specific simulation:
@app.get("/run_simulation_simsettings/{simsetting_id}")
async def run_simulation_simsettings(
        simsetting_id: str = Path(
            description="The ID of the simulation you want to run"
        ),
):
    return await controller.run_simulation_simsettings(simsetting_id)


# Run a simulation with the simsettings_id and the location name:
@app.get("/run_simulation/config/")  # E.g. /run/simulation/config/?location=Ethipia&simsettings_id=abcde
async def run_simulation_config(
        location: str = 'Burundi',
        simsettings_id: str = '65843761aef0c55ae04c33ad'  # Default ID der Simulation Settings
):

    location_list = ['burundi', 'car', 'ethiopia', 'mali', 'ssudan', 'syria']

    if location in location_list:
        return await controller.run_simulation_config(location, simsettings_id)
    else:
        return "No proper location provided"



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
