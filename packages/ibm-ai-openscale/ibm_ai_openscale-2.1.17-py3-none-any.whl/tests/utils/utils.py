def check_if_binding_exists(ai_client, credentials, type):
    bindings = ai_client.data_mart.bindings.get_details()

    for binding in bindings['service_bindings']:
        if binding['entity']['service_type'] == type:
            if binding['entity']['credentials'] == credentials:
                return binding['metadata']['guid']
