import base64

from SCons.Script import (
    Command,
    Default,
    Environment,
)

env = Environment(
    ENV = {
        'DEBUG' : True,
        'BAUTH' : 'Basic {}'.format(
            base64.b64encode('root:0'.encode()).decode()
        ),
        'KHALTI_API_KEY': 'key d0c233f24d12490ebe0b592535a662a4',
        'KHALTI_API_URL': 'https://dev.khalti.com/api/v2/epayment/initiate/'
    }
)


env.Command('run', [], './run.py')
Default('run')
