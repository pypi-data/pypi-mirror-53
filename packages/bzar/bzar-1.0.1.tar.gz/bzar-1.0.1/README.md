# bzar-python

A python implementation for [the bzar format](https://github.com/gwappa/bzar).

## Basic usage

```
import numpy as np
import bzar

orig = np.arange(10).reshape((2,5))
bzar.save('out', orig, dict(desc="test")) # output saved to 'out.bzar', with optional metadata

read, meta = bzar.load('out.bzar', with_metadata=True) # reads the content of file as an array
```

## License

The MIT license
