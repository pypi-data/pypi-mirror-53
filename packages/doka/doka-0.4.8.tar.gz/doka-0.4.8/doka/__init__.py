import fire
from doka.commands import *

__version__ = "0.4.8"


def main():
    fire.Fire({
        'version': __version__,
        'project': Project,
        'unit': Unit,
        "stack": Stack,
        "inspect": Inspect,
        "portainer": Portainer,
        "config": Config,
        "nginx": Nginx
    })
