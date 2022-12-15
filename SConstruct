from SCons.Script import (
    Command,
    Default,
    Environment,
)

env = Environment(
    ENV = {
        'DEBUG' : True,
    }
)


env.Command('run', [], './run.py')
Default('run')
