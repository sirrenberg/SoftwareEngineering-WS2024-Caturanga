from fastapi.testclient import TestClient
from pathlib import Path
import sys

# add backend directory to PYTHONPATH
backend = Path(__file__).parent.parent
sys.path.append(str(backend))

from main import app, expected_simsettings  # noqa: E402


class TestClass:
    """
    This class contains unit tests for the Caturanga API endpoints.
    """

    client = TestClient(app)

    def test_root(self):
        """
        Test the root endpoint ("/") of the API.
        """
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"data": "Welcome to the Caturanga API!"}

    def test_run_simulation(self):
        """
        Test the "/run_simulation" endpoint of the API.
        """
        response = self.client.get("/run_simulation")
        assert response.status_code == 200
        assert "dummy simulation" in response.json()

    def test_get_simulation_result_bad_id(self):
        """
        Test the "/simulation_results/{id}" endpoint of the API with a
        non-existent ID.
        """
        response = \
            self.client.get("/simulation_results/65843761aef0c55ae04c33ad")
        assert response.status_code == 404
        assert response.json() == {"detail": "Simulation result not found"}

    def test_get_simulation_result(self):
        """
        Test the "/simulation_results/{id}" endpoint of the API with a
        valid ID.
        """
        response = \
            self.client.get("/simulation_results/65856b0c4661431a0f92969b")
        assert response.status_code == 200
        '''
        the structure of the responses differ a lot from one simulation to
        another, which makes it hard to write more specific tests
        '''
        assert "data" in response.json()

    def test_get_all_simulation_results(self):
        """
        Test the "/simulation_results" endpoint of the API.
        """
        response = self.client.get("/simulation_results")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_simulation_bad_id(self):
        """
        Test the "/simulations/{id}" endpoint of the API with a
        non-existent ID.
        """
        response = self.client.get("/simulations/65856b0c4661431a0f92969b")
        assert response.status_code == 404
        assert response.json() == {"detail": "Simulation input not found"}

    def test_get_simulation(self):
        """
        Test the "/simulations/{id}" endpoint of the API with a valid ID.
        """
        expected_keys = ["_id", "name", "region", "closures", "conflicts",
                         "locations", "registration_corrections", "routes",
                         "sim_period"]
        response = self.client.get("/simulations/658dec24819bd1bc1ff738cd")
        assert response.status_code == 200
        assert all(key in expected_keys for key in response.json().keys())

    def test_get_all_simulations(self):
        """
        Test the "/simulations" endpoint of the API.
        """
        response = self.client.get("/simulations")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_simsetting_bad_id(self):
        """
        Test the "/simsettings/{id}" endpoint of the API with a
        non-existent ID.
        """
        response = self.client.get("/simsettings/65856b0c4661431a0f92969c")
        assert response.status_code == 404
        assert response.json() == {"detail": "Simulation settings not found"}

    def test_get_simsetting(self):
        """
        Test the "/simsettings/{id}" endpoint of the API with a valid ID.
        """
        response = self.client.get("/simsettings/6570f624987cdd647c68bc7d")
        assert response.status_code == 200
        assert all(key in expected_simsettings
                   for key in response.json().keys())

    def test_get_all_simsettings(self):
        """
        Test the "/simsettings" endpoint of the API.
        """
        response = self.client.get("/simsettings")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_post_simsettings(self):
        """
        Test the POST request to the "/simsettings" endpoint of the API.
        """
        response = \
            self.client.post("/simsettings",
                             json={"name": "dummy"})
        assert response.status_code == 200
        assert response.json()["data"] == {"name": "dummy"}
        # clean up
        self.client.delete(f"/simsettings/{response.json()['ID']}")

    def test_post_simsettings_bad_structure(self):
        """
        Test the POST request to the "/simsettings" endpoint of the API with
        an invalid JSON structure.
        """
        response = self.client.post("/simsettings", json={"hasten": 5})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid simsetting structure"}

    def test_delete_simsettings_bad_id(self):
        """
        Test the DELETE request to the "/simsettings/{id}" endpoint of the API
        with a non-existent ID.
        """
        response = self.client.delete("/simsettings/65856b0c4661431a0f92969b")
        assert response.status_code == 404
        assert response.json() == {"detail": "Simulation settings not found"}

    def test_delete_simsettings(self):
        """
        Test the DELETE request to the "/simsettings/{id}" endpoint of the API
        with a valid ID.
        """
        # create a dummy simsetting
        post_response = \
            self.client.post("/simsettings",
                             json={"name": "dummy"})
        dummy_simsetting_id = post_response.json()["ID"]
        response = \
            self.client.delete(f"/simsettings/{dummy_simsetting_id}")
        assert response.status_code == 200
        assert response.json() == {"ID": dummy_simsetting_id,
                                   "deleted": True}
