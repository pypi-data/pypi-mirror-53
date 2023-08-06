# rawpipe

[![Build Status](https://travis-ci.org/toaarnio/rawpipe.svg?branch=master)](https://travis-ci.org/toaarnio/rawpipe)

A collection of reference ISP algorithms, sufficient for producing a reasonably
good looking image from raw sensor data. Each algorithm takes in a frame in RGB
or raw format and returns a modified copy of the frame. The frame is expected to
be a NumPy float array with either 2 or 3 dimensions, depending on the function.

**Example:**
```
import rawpipe
...
algs = rawpipe.Algorithms(verbose=True)
raw = algs.linearize(raw, blacklevel=64, whitelevel=1023)
rgb = algs.demosaic(raw, "RGGB")
rgb = algs.wb(rgb, [1.5, 2.0])
rgb = algs.quantize(rgb, 255)
```

**Installing on Linux:**
```
pip install rawpipe
```

**Documentation:**
```
pydoc rawpipe
```

**Building & installing from source:**
```
make install
```

**Building & releasing to PyPI:**
```
make release
```
