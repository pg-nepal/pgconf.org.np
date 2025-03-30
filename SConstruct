import os
import base64

from SCons.Script import (
    Command,
    Default,
    Environment,
)

env = Environment(
    ENV = {
        k : os.getenv(k, v) for k, v in [
            ('DEBUG', True),
            ('BAUTH', 'Basic {}'.format(base64.b64encode('root:0'.encode()).decode())),
        ]
    }
)


env.Command('run', [], './run.py')
Default('run')
