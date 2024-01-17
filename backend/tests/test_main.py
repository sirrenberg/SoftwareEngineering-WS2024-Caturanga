from fastapi.testclient import TestClient
from pathlib import Path
import sys
import pytest

# add backend directory to PYTHONPATH
BACKEND = Path(__file__).resolve().parent.parent
sys.path.append(str(BACKEND))
sys.path.append(str(BACKEND / "flee"))

from main import app  # noqa: E402


class TestClass:
    """
    This class contains unit tests for the Caturanga API endpoints.
    """

    client = TestClient(app)
    INVALID_ID = "aaaaaaaaaaaaaaaaaaaaaaaa"
    VALID_INPUT_ID = "65a6d3eb9ae2636fa2b3e3c6"
    VALID_SETTING_ID = "6599846eeb8f8c36cce8307a"
    VALID_RESULT_IT = "65a722c0e95bd59c24943951"

    def test_root(self):
        """
        Test the root endpoint ("/") of the API.
        """
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"data": "Welcome to the Caturanga API!!"}

    # Tests for the "/run_simulation_config" endpoint

    def test_run_simulation_config(self):
        simulation_config = {
            "input": {
                "input_id": self.VALID_INPUT_ID,
                "input_name": "test_input_name"
            },
            "settings": {
                "simsettings_id": self.VALID_SETTING_ID,
                "simsettings_name": "test_simsettings_name"
            }
        }
        response = self.client.post("/run_simulation/config",
                                    json=simulation_config)
        assert response.status_code == 200
        assert "dummy simulation" in response.json()

    # Tests for the "/simulation_results" endpoint

    @pytest.mark.asyncio
    async def test_get_simulation_result_bad_id(self):
        """
        Test the "/simulation_results/{id}" endpoint of the API with an
        ID that does not exist in that collection.
        """
        await self.get_data_bad_id("simulation_results",
                                   self.INVALID_ID)

    @pytest.mark.asyncio
    async def test_get_simulation_result(self):
        """
        Test the "/simulation_results/{id}" endpoint of the API with a
        valid ID.
        """
        expected_keys = ["_id", "name",
                         "simulation_id", "simsettings_id", "status", "data"]
        await self.get_data("simulation_results",
                            self.VALID_RESULT_IT,
                            expected_keys)

    @pytest.mark.asyncio
    async def test_get_all_simulation_results(self):
        """
        Test the "/simulation_results" endpoint of the API.
        """
        await self.get_all_data("simulation_results")

    # Tests for the "/simulations" endpoint

    @pytest.mark.asyncio
    async def test_get_simulation_bad_id(self):
        """
        Test the "/simulations/{id}" endpoint of the API with an
        ID that does not exist in that collection.
        """
        await self.get_data_bad_id("simulations",
                                   self.INVALID_ID)

    @pytest.mark.asyncio
    async def test_get_simulation(self):
        """
        Test the "/simulations/{id}" endpoint of the API with a valid ID.
        """
        expected_keys = ["_id", "name", "region", "closures", "conflicts",
                         "locations", "registration_corrections", "routes",
                         "sim_period", "validation", "data_sources"]
        await self.get_data("simulations",
                            self.VALID_INPUT_ID,
                            expected_keys)

    @pytest.mark.asyncio
    async def test_get_all_simulations(self):
        """
        Test the "/simulations" endpoint of the API.
        """
        await self.get_all_data("simulations")

    @pytest.mark.asyncio
    async def test_post_simulation(self):
        """
        Test the POST request to the "/simulations" endpoint of the API.
        """
        await self.post_data("simulations")

    @pytest.mark.asyncio
    async def test_delete_simulation_bad_id(self):
        """
        Test the DELETE request to the "/simulations/{id}" endpoint of the API
        with an ID that does not exist in that collection.
        """
        await self.delete_data_bad_id("simulations",
                                      self.INVALID_ID)

    @pytest.mark.asyncio
    async def test_delete_simulation(self):
        """
        Test the DELETE request to the "/simulations/{id}" endpoint of the API
        with a valid ID.
        """
        await self.delete_data("simulations")

    # Test for the "/simsettings" endpoint

    @pytest.mark.asyncio
    async def test_get_simsetting_bad_id(self):
        """
        Test the "/simsettings/{id}" endpoint of the API with an
        ID that does not exist in that collection.
        """
        await self.get_data_bad_id("simsettings",
                                   self.VALID_RESULT_IT)

    @pytest.mark.asyncio
    async def test_get_simsetting(self):
        """
        Test the "/simsettings/{id}" endpoint of the API with a valid ID.
        """
        expected_simsettings = ["_id", "name", "log_levels", "spawn_rules",
                                "move_rules", "optimisations"]
        await self.get_data("simsettings",
                            self.VALID_SETTING_ID,
                            expected_simsettings)

    @pytest.mark.asyncio
    async def test_get_all_simsettings(self):
        """
        Test the "/simsettings" endpoint of the API.
        """
        await self.get_all_data("simsettings")

    @pytest.mark.asyncio
    async def test_post_simsettings(self):
        """
        Test the POST request to the "/simsettings" endpoint of the API.
        """
        await self.post_data("simsettings")

    @pytest.mark.asyncio
    async def test_delete_simsettings_bad_id(self):
        """
        Test the DELETE request to the "/simsettings/{id}" endpoint of the API
        with an ID that does not exist in that collection.
        """
        await self.delete_data_bad_id("simsettings", self.VALID_INPUT_ID)

    @pytest.mark.asyncio
    async def test_delete_simsettings(self):
        """
        Test the DELETE request to the "/simsettings/{id}" endpoint of the API
        with a valid ID.
        """
        await self.delete_data("simsettings")

    # Utility Functions

    async def get_data(self,
                       data: str,
                       object_id: str,
                       expected_keys: list):
        """
        Test the GET endpoints for the data collections.
        """
        response = self.client.get(f"/{data}/{object_id}")
        assert response.status_code == 200
        assert all(key in expected_keys
                   for key in response.json().keys())

    async def get_data_bad_id(self, data: str, object_id: str):
        """
        Test the GET endpoints for the data collections with a bad ID.
        """
        response = self.client.get(f"/{data}/{object_id}")
        assert response.status_code == 404
        assert response.json() is None

    async def get_all_data(self, data: str):
        """
        Test the GET all endpoints for the data collections.
        """
        response = self.client.get(f"/{data}")
        assert response.status_code == 200
        if data == "simsettings":
            assert isinstance(response.json()["data"], list)
        else:
            assert isinstance(response.json(), list)

    async def post_data(self, data: str):
        """
        Test the POST endpoints for the data collections.
        Creates a dummy data entry and deletes it afterwards.
        """
        response = \
            self.client.post(f"/{data}",
                             json={"_id": "123",
                                   "name": "dummy"})

        print(response.json())

        assert response.status_code == 200
        assert "id" in response.json().keys()

        # delete the dummy simsetting
        self.client.delete(f"/{data}/{response.json()['id']}")

    async def delete_data(self, data: str):
        """
        Test the DELETE endpoints for the data collections.
        Creates a dummy data entry and deletes it afterwards.
        """
        # create a dummy data entry to delete
        post_response = \
            self.client.post(f"/{data}",
                             json={"_id": "123",
                                   "name": "dummy"})

        dummy_data_id = post_response.json()["id"]
        response = \
            self.client.delete(f"/{data}/{dummy_data_id}")

        assert response.status_code == 200
        assert response.json() == {"status": "success"}

    async def delete_data_bad_id(self, data: str, object_id: str):
        """
        Test the DELETE endpoints for the data collections with a bad ID.
        """
        response = self.client.delete(f"/{data}/{object_id}")
        assert response.status_code == 404
