## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
def get_provider_info():
    return {
        "package-name": "airflow-provider-label-studio",
        "name": "Label Studio Airflow Provider",
        "description": 'Airflow package provider to perform actions on Label Studio.',
        "hook": [
            {
                "integration-name": "Label Studio Hook",
                "python-modules": ["airflow.providers.label_studio.hooks.label_studio_hook.LabelStudioHook",
                ]
            }
            ],
        "operators":[
                        {
                            "integration-name": "Label Studio Sync Task Operation",
                            "python-modules":"airflow.providers.label_studio.operators.sync_operator.SyncTask"
                        },
        ],
        'connection-types': [
            {
                'hook-class-name': 'airflow.providers.label_studio.hooks.label_studio_hook.LabelStudioHook',
                'connection-type': 'label_studio',
            },
        ],
        "versions": ["0.0.1"] # Required
    }