# Nirvana take home Project

## Notes
General overview

* The tools chosen for this project are DjangoRestFramework and Pytest, being DRF a fast, efficient way of generating the hosted API, and Pytest the most used unit-testing framework. Fast-API would have been another valid choice.
* The "process_data" function in "helpers.py" is the heart of the solution. It generates the necessary calls to the external APIs and the result based on the selected "strategy"
* 3 dummy APIs were created in AWS to simulate the external endpoints, using API Gateway in "Mock Endpoint" mode.

## WishList
A list of things I would add or would like to explore in more detail, if time was not a constraint, and this was a production solution.

* Tests: There is always room for more tests, for example, what would happen if: 
  * the external APIs fail
  * the external APIs return data with contents different from expected
  * there were more or less than 3 external APIs
* Error checking upon calling external APIs could be way better.
* Deploy: I would have liked to deploy the solution over Docker.
* Admin: Django Admin could be user to manage the external endpoints URLs
* Repo: I would have liked to be a lot more meticulous about documenting each stage of the development through incremental commits to the repository (unfortunately my development was interrupted a few times by unforeseen job-related circumstances)