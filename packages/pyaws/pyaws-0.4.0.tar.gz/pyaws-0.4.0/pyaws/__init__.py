import inspect
from pyaws._version import __version__ as version
from pyaws import environment
from pyaws.statics import local_config


__author__ = 'Blake Huber'
__version__ = version
__credits__ = []
__license__ = "GPL-3.0"
__maintainer__ = "Blake Huber"
__email__ = "blakeca00@gmail.com"
__status__ = "Development"


## the following imports require __version__  ##

try:

    from libtools import Colors
    from libtools import logd

    # shared, global logger object
    logd.local_config = local_config
    logger = logd.getLogger(__version__)

    from pyaws.core import exit_codes

except Exception:
    pass
