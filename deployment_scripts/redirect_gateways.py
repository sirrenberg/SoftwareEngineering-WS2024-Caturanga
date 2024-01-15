# This script is used to redirect the API Gateway to the most recent task of an aws ecs service.
# It is used in the deployment process of the backend and frontend by the github actions workflow.
import boto3
import sys
import logging

logging.basicConfig(level=logging.INFO)

ecs = boto3.client('ecs')

# parse arguments
CLUSTER_NAME = sys.argv[1]
SERVICE_NAME = sys.argv[2]
API_GATEWAY_ID = sys.argv[3]

# fetch running tasks
tasks_arns = [task.split("/")[-1] for task in ecs.list_tasks(cluster=CLUSTER_NAME, serviceName=SERVICE_NAME)['taskArns']]
logging.info("tasks_arns: " + str(tasks_arns))
tasks_with_deployment_time = []
for ta in tasks_arns:
    deployment_time = ecs.describe_tasks(cluster=CLUSTER_NAME, tasks=[ta])["tasks"][0]["createdAt"]
    tasks_with_deployment_time.append((ta,deployment_time))

# determine most recent task
tasks_with_deployment_time.sort(key=lambda x: x[1], reverse=True)
most_recent_task = tasks_with_deployment_time[0][0]
logging.info("most_recent_task: " + most_recent_task)

# fetch eni of most recent task
details = ecs.describe_tasks(cluster=CLUSTER_NAME, tasks=[most_recent_task])["tasks"][0]["attachments"][0]["details"]
for d in details:
    if d["name"] == "networkInterfaceId":
        eni = d["value"]
        logging.info("eni: " + str(eni))
        break

# fetch public ip of eni
public_ip = boto3.client('ec2').describe_network_interfaces(NetworkInterfaceIds=[eni])["NetworkInterfaces"][0]["Association"]["PublicIp"]
logging.info("public_ip: " + str(public_ip))

# compute new uris for the api gateway
api_gateway = boto3.client('apigatewayv2')
integrations = api_gateway.get_integrations(ApiId=API_GATEWAY_ID)["Items"]
integration_id_and_uri = []
for integration in integrations:
    new_uri = "http://" + public_ip + "/" + integration["IntegrationUri"].split("http://")[1].split("/")[1]
    integration_id_and_uri.append((integration["IntegrationId"],new_uri))
    logging.info("New uri: " + new_uri)

# update integrations of the api gateway
for integration_id, new_uri in integration_id_and_uri:
    response = api_gateway.update_integration(ApiId=API_GATEWAY_ID, IntegrationId=integration_id, IntegrationUri=new_uri)
    logging.info("Updated integration: " + str(response))




#deployment_time = [(arn,(ecs.describe_services(cluster=cluster_name, services=[service_name])['services'][0]['deployments'][0]['createdAt']