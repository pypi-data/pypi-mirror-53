

def print_wml_tags(wml_client):
    instance_details = wml_client.service_instance.get_details()
    if 'entity' in instance_details.keys() and 'tags' in instance_details['entity'].keys():
        print(instance_details['entity']['tags'])


def get_wml_model_and_deployment_id(wml_client, model_name, deployment_name):
    for deployment in wml_client.deployments.get_details()['resources']:
        if deployment['entity']['name'] == deployment_name:
            print("--> Deployment already exists: {}".format(deployment))
            return deployment['entity']['deployable_asset']['guid'], deployment['metadata']['guid']

    return None, None