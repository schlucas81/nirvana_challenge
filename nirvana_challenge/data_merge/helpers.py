from .constants import *
import httpx
from httpx import HTTPError
from pydantic import BaseModel


def apply_strategy(strategy, nums):
    result = None
    strats={
        "average": lambda nums: sum(nums) / len(nums),
        "sum": lambda nums: sum(nums),
        "max": lambda nums: max(nums),
        "min": lambda nums: min(nums),
    }
    
    strategy_function = strats.get(strategy, None)
    if strategy_function:
        result = strategy_function(nums)
    
    return result


class APIResponse(BaseModel):
    oop_max: int
    stop_loss: int
    deductible: int
    

def get_from_api(url):
    res = None
    try:
        res = httpx.get(url)
        res.raise_for_status()
        return res.json()
    except HTTPError as e:
        raise e
    except (httpx.RequestError, ValueError) as e:
        raise e


def process_data(member_id: int, strategy: str) -> APIResponse:
    response_fields = {}

    for url in API_URLS:
        try:
            res = get_from_api(f"{url}?member_id={member_id}")
            if res:
                response_body = APIResponse.parse_obj(res)

                for key, value in response_body:
                    if not key in response_fields:
                        response_fields[key] = []
                    
                    response_fields[key].append(value)
        except Exception as e:
            raise e
        
    return {key: apply_strategy(strategy, value) for key, value in response_fields.items()}

