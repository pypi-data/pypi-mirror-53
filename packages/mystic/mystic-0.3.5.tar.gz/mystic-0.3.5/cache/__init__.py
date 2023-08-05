#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 2013-2016 California Institute of Technology.
# Copyright (c) 2016-2019 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/mystic/blob/master/LICENSE
'''decorators for caching function outputs, with function inputs as the keys

Notes:
    This module has been deprecated in favor of the ``klepto`` package.
'''

# backward compatability
from klepto import lru_cache, lfu_cache, mru_cache
from klepto import rr_cache, inf_cache, no_cache

# end of file
