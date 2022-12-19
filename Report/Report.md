------------------------------------------------------------------------
# RESULTS
------------------------------------------------------------------------

We gathered all the results of the project testing under this report.

------------------------------------------------------------------------
> INITIAL TESTS
------------------------------------------------------------------------

We run all the pytests under this project for the following services:
- api
- model  
- integration (all together)

All tests passed. 

------------------------------------------------------------------------
> INITIAL STRESS TEST FAILURES
------------------------------------------------------------------------

We have seen that an unstable behavior was ocurring some time after 
running the locusttest. This was cause due to many users trying to access 
the same file ('dog.jpeg') and the same time, so the model crashed and we 
started observing failures in the test.
To correct this, we added a try-except block under `ml_service.predict` 
function to catch the failure and return a HTTP ERROR CODE 400 and a 
generic prediction to make sure the docker container didn't crash.

------------------------------------------------------------------------
> FINAL PERFORMANCE TEST
------------------------------------------------------------------------
In the report below, you will see the results of the locust stress test
in detail, for different number of users and spawn rates.

The supporting charts can be seen in the following Github repo:
_https://github.com/SanNicoSan/AnyoneAI/tree/main/Sprint4%20Project/Report_

These have also been added under the `Report` dolder. 


    | #Run | Number of users | Spawn Rate | RPS (max) | Failures (max) |
    |------|-----------------|------------|-----------|----------------|
    | #1   | 25              | 3          | 8         | 0              |
    | #2   | 50              | 5          | 9.5       | 0              |
    | #3   | 75              | 10         | 10.6      | 0              |
    | #4   | 75              | 25         | 9.1       | 2%             |
    | #5   | 100             | 10         | 6.7       | 0              |
