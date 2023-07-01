import pytest
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nirvana_challenge.settings')
parent_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent_dir)
from data_merge import constants
from data_merge import helpers
from rest_framework.test import APIClient


MEMBER_ID = 1


@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()


"""
retrieve_api_data gets data from the available external APIs, calculates all possible 
strategies, and stores results to compare with the results from the main API call (/get_data/)
"""
@pytest.fixture(scope="class", autouse=True)
def retrieve_api_data(request):
    response_fields = {}

    for url in constants.API_URLS:
        res = helpers.get_from_api(f"{url}?member_id={MEMBER_ID}")
        if res:
            response_body = helpers.APIResponse.model_validate(res)

            for key, value in response_body:
                if key not in response_fields:
                    response_fields[key] = []

                response_fields[key].append(value)

    manual_results = {
        "averages": {},
        "sums": {},
        "max": {},
        "mins": {},
    }

    # for each field in the data set, and for each available strategy, calculate results.
    manual_results["averages"]["deductible"] = sum(response_fields["deductible"]) / len(response_fields["deductible"])
    manual_results["averages"]["stop_loss"] = sum(response_fields["stop_loss"]) / len(response_fields["stop_loss"])
    manual_results["averages"]["oop_max"] = sum(response_fields["oop_max"]) / len(response_fields["oop_max"])

    manual_results["sums"]["deductible"] = sum(response_fields["deductible"])
    manual_results["sums"]["stop_loss"] = sum(response_fields["stop_loss"])
    manual_results["sums"]["oop_max"] = sum(response_fields["oop_max"])

    manual_results["max"]["deductible"] = max(response_fields["deductible"])
    manual_results["max"]["stop_loss"] = max(response_fields["stop_loss"])
    manual_results["max"]["oop_max"] = max(response_fields["oop_max"])

    manual_results["mins"]["deductible"] = min(response_fields["deductible"])
    manual_results["mins"]["stop_loss"] = min(response_fields["stop_loss"])
    manual_results["mins"]["oop_max"] = min(response_fields["oop_max"])

    request.cls.manual_results = manual_results


class TestAPI:
    # setting manual_results to be available for the rest of the tests
    def setup_method(self, manual_results):
        self.manual_results = getattr(self, "manual_results", None)

    # testing for error response when not specifying a member_id
    def test_invalid_member_id(self, api_client):
        response = api_client.get('/get_data/')
        assert response.status_code != 200

    # testing for error response when using a non valid strategy
    def test_invalid_strategy(self, api_client):
        response = api_client.get('/get_data/', {'member_id': 1, 'strategy': 'some_strategy'})
        assert response.status_code != 200

    # testing for default strategy "average"
    def test_default_strategy(self, api_client):
        response = api_client.get('/get_data/', {'member_id': 1})
        assert response.status_code == 200
        data = response.json()

        assert data["oop_max"] == self.manual_results["averages"]["oop_max"]
        assert data["deductible"] == self.manual_results["averages"]["deductible"]
        assert data["stop_loss"] == self.manual_results["averages"]["stop_loss"]

    # testing for SUM strategy
    def test_sum(self, api_client):
        response = api_client.get('/get_data/', {'member_id': 1, 'strategy': 'sum'})
        assert response.status_code == 200
        data = response.json()

        assert data["oop_max"] == self.manual_results["sums"]["oop_max"]
        assert data["deductible"] == self.manual_results["sums"]["deductible"]
        assert data["stop_loss"] == self.manual_results["sums"]["stop_loss"]

    # testing for MAX strategy
    def test_max(self, api_client):
        response = api_client.get('/get_data/', {'member_id': 1, 'strategy': 'max'})
        assert response.status_code == 200
        data = response.json()

        assert data["oop_max"] == self.manual_results["max"]["oop_max"]
        assert data["deductible"] == self.manual_results["max"]["deductible"]
        assert data["stop_loss"] == self.manual_results["max"]["stop_loss"]

    # testing for MIN strategy
    def test_mim(self, api_client):
        response = api_client.get('/get_data/', {'member_id': 1, 'strategy': 'min'})
        assert response.status_code == 200
        data = response.json()

        assert data["oop_max"] == self.manual_results["mins"]["oop_max"]
        assert data["deductible"] == self.manual_results["mins"]["deductible"]
        assert data["stop_loss"] == self.manual_results["mins"]["stop_loss"]
