from gemini.scheduler.flows import all_flow_deployments

from prefect import serve

if __name__ == "__main__":
    serve(*all_flow_deployments)
