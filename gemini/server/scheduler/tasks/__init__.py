from dagster import Definitions

from tasks.jobs import hello_cereal_job, complex_job

defs = Definitions(
    jobs=[hello_cereal_job, complex_job]
)