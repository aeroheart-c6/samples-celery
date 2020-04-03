# Setup project

```
./localctl compose build worker
```

# Run services

Redis need to run
```
./localctl compose up -d redis
```

Then we start the worker, we do some other operations in this worker so we do the ff:
```
./localctl run worker bash

airflow worker
```

Then we start another terminal and just make the worker do some stuff
```
docker exec -it $(docker ps --format="{{.Names}}" | grep airflow-mini_worker_run) bash

# run a task for 10 seconds
airflow execute-task 10

# get stats of the worker
airflow stats

# send SIGABRT to worker
airflow worker-abort
```
