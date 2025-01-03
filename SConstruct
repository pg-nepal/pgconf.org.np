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
    }
)


env.Command('run', [], './run.py')
Default('run')
