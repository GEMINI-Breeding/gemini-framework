task_queues = {
    'default': {
        'exchange': 'default',
        'exchange_type': 'direct',
        'binding_key': 'default',
        'default_module': 'gemini.tasks.src.system',
    },
    'sensor_processing': {
        'exchange': 'sensor_processing',
        'exchange_type': 'direct',
        'binding_key': 'sensor_processing',
        'default_module': 'gemini.tasks.src.sensor_processing',
    },
    'plot_processing': {
        'exchange': 'plot_processing',
        'exchange_type': 'direct',
        'binding_key': 'plot_processing',
        'default_module': 'gemini.tasks.src.plot_processing',
    },
    'trait_processing': {
        'exchange': 'trait_processing',
        'exchange_type': 'direct',
        'binding_key': 'trait_processing',
        'default_module': 'gemini.tasks.src.trait_processing',
    },
    'file_upload': {
        'exchange': 'file_upload',
        'exchange_type': 'direct',
        'binding_key': 'file_upload',
        'default_module': 'gemini.tasks.src.file_upload',
    },
}