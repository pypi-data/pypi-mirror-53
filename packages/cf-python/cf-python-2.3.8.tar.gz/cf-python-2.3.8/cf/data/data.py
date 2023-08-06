from collections import namedtuple

from numpy import argsort       as numpy_argsort
from numpy import array         as numpy_array
from numpy import asanyarray    as numpy_asanyarray
from numpy import ceil          as numpy_ceil
from numpy import cos           as numpy_cos
from numpy import count_nonzero as numpy_count_nonzero
from numpy import dtype         as numpy_dtype
from numpy import e             as numpy_e
from numpy import empty         as numpy_empty
from numpy import empty_like    as numpy_empty_like
from numpy import exp           as numpy_exp
from numpy import floor         as numpy_floor
from numpy import isclose       as numpy_isclose
from numpy import log           as numpy_log
from numpy import log10         as numpy_log10
from numpy import log2          as numpy_log2
from numpy import ndarray       as numpy_ndarray
from numpy import ndenumerate   as numpy_ndenumerate
from numpy import ndim          as numpy_ndim
from numpy import newaxis       as numpy_newaxis
from numpy import ones          as numpy_ones
from numpy import ravel_multi_index as numpy_ravel_multi_index
from numpy import reshape       as numpy_reshape
from numpy import result_type   as numpy_result_type
from numpy import rint          as numpy_rint
from numpy import round         as numpy_round
from numpy import seterr        as numpy_seterr
from numpy import shape         as numpy_shape
from numpy import sin           as numpy_sin
from numpy import size          as numpy_size
from numpy import tan           as numpy_tan
from numpy import tile          as numpy_tile
from numpy import trunc         as numpy_trunc
from numpy import unique        as numpy_unique
from numpy import unravel_index as numpy_unravel_index
from numpy import where         as numpy_where
from numpy import vectorize     as numpy_vectorize
from numpy import zeros         as numpy_zeros
from numpy import floating         as numpy_floating
from numpy import bool_         as numpy_bool_
from numpy import integer         as numpy_integer

from numpy.ma import array          as numpy_ma_array
from numpy.ma import count          as numpy_ma_count
from numpy.ma import empty          as numpy_ma_empty
from numpy.ma import is_masked      as numpy_ma_is_masked
from numpy.ma import isMA           as numpy_ma_isMA
from numpy.ma import masked         as numpy_ma_masked
from numpy.ma import masked_all     as numpy_ma_masked_all
from numpy.ma import masked_invalid as numpy_ma_masked_invalid
from numpy.ma import masked_where   as numpy_ma_masked_where
from numpy.ma import MaskedArray    as numpy_ma_MaskedArray
from numpy.ma import nomask         as numpy_ma_nomask
from numpy.ma import ones           as numpy_ma_ones
from numpy.ma import var            as numpy_ma_var
from numpy.ma import where          as numpy_ma_where
from numpy.ma import zeros          as numpy_ma_zeros

import operator

from json import dumps as json_dumps
from json import loads as json_loads

from functools import partial
from operator  import mul as operator_mul
from math      import ceil as math_ceil
from sys       import byteorder, getrefcount
from itertools import izip
from itertools import product as itertools_product

#from .filearray import SubArray

from ..netcdf.filearray import NetCDFFileArray
from ..um.filearray     import UMFileArray

from ..cfdatetime import st2dt, dt2rt, rt2dt, st2rt
from ..units      import Units
from ..constants  import masked as cf_masked
from ..functions import (CHUNKSIZE, FM_THRESHOLD, RTOL, ATOL,
                         FREE_MEMORY, COLLAPSE_PARALLEL_MODE,
                         parse_indices, _numpy_allclose,
                         _numpy_isclose, abspath, pathjoin,
                         hash_array, get_subspace, set_subspace,
                         broadcast_array)
from ..functions  import inspect as cf_inspect
from ..functions  import _section

from .filearray          import FileArray, FilledArray
from .partition          import Partition
from .partitionmatrix    import PartitionMatrix
from .collapse_functions import *

from .. import mpi_on
if mpi_on:
    from .. import mpi_comm
    from .. import mpi_size
    from .. import mpi_rank
#--- End: if

def _convert_to_builtin_type(x):
    '''

Convert a non-JSON-encodable object to a JSON-encodable built-in type.

Possible conversions are:

==============  =============  ======================================
Input object    Output object  numpy data types covered
==============  =============  ======================================
numpy.bool_     bool           bool
numpy.integer   int            int, int8, int16, int32, int64, uint8,
                               uint16, uint32, uint64
numpy.floating  float          float, float16, float32, float64
==============  =============  ======================================

:Parameters:

    x : 
        
:Returns: 

    out :

:Raises:

    TypeError :
        If *x* can't be converted to a JSON serializableis type.

:Examples:

>>> type(_convert_to_netCDF_datatype(numpy.bool_(True)))
bool
>>> type(_convert_to_netCDF_datatype(numpy.array([1.0])[0]))
double
>>> type(_convert_to_netCDF_datatype(numpy.array([2])[0]))
int

''' 
    if isinstance(x, numpy_bool_):
        return bool(x)

    if isinstance(x, numpy_integer):
        return int(x)
     
    if isinstance(x, numpy_floating):
        return float(x)

    raise TypeError(
        "{0!r} object is not JSON serializable: {1!r}".format(type(x), x))
#--- End: def

_debug = True

# --------------------------------------------------------------------
# _seterr = How floating-point errors in the results of arithmetic
#           operations are handled. These defaults are those of 
#           numpy 1.10.1.
# --------------------------------------------------------------------
_seterr = {'divide' : 'warn',
           'invalid': 'warn',
           'over'   : 'warn',
           'under'  : 'ignore',
           }

# --------------------------------------------------------------------
# _seterr_raise_to_ignore = As _seterr but with any values of 'raise'
#                           changed to 'ignore'.
# --------------------------------------------------------------------
_seterr_raise_to_ignore = _seterr.copy()
for key, value in _seterr.iteritems():
    if value == 'raise':
        _seterr_raise_to_ignore[key] = 'ignore'

# --------------------------------------------------------------------
# _mask_fpe[0] = Whether or not to automatically set
#                FloatingPointError exceptions to masked values in
#                arimthmetic.
# --------------------------------------------------------------------
_mask_fpe = [False]

_xxx = numpy_empty((), dtype=object)

_empty_set = set()

_units_None    = Units()
_units_1       = Units('1')
_units_radians = Units('radians')

_dtype_object = numpy_dtype(object)
_dtype_float  = numpy_dtype(float)
_dtype_bool   = numpy_dtype(bool)

_cached_axes = {0: []}
def _initialise_axes(ndim):
    '''

:Parameters:

    ndim : int

:Returns:

    out: list

:Examples:

>>> _initialise_axes(0)
[]
>>> _initialise_axes(1)
['dim1']
>>> _initialise_axes(3)
['dim1', 'dim2', 'dim3']
>>> _initialise_axes(3) is _initialise_axes(3)
True

'''
    axes = _cached_axes.get(ndim, None)
    if axes is None:
        axes = ['dim%d' % i for i in xrange(ndim)]
        _cached_axes[ndim] = axes

    return axes
#--- End: def


# ====================================================================
#
# Data object
#
# ====================================================================

class Data(object):
    '''

An N-dimensional data array with units and masked values.

* Contains an N-dimensional, indexable and broadcastable array with
  many similarities to a `numpy` array.

* Contains the units of the array elements.

* Supports masked arrays, regardless of whether or not it was
  initialised with a masked array.

* Stores and operates on data arrays which are larger then the
  available memory.

**Indexing**

A data array is indexable in a similar way to numpy array:

>>> d.shape
(12, 19, 73, 96)
>>> d[...].shape
(12, 19, 73, 96)
>>> d[slice(0, 9), 10:0:-2, :, :].shape
(9, 5, 73, 96)

There are three extensions to the numpy indexing functionality:

* Size 1 dimensions are never removed bi indexing.

  An integer index i takes the i-th element but does not reduce the
  rank of the output array by one:

  >>> d.shape
  (12, 19, 73, 96)
  >>> d[0, ...].shape
  (1, 19, 73, 96)
  >>> d[:, 3, slice(10, 0, -2), 95].shape
  (12, 1, 5, 1)

  Size 1 dimensions may be removed with the `squeeze` method.

* The indices for each axis work independently.

  When more than one dimension's slice is a 1-d boolean sequence or
  1-d sequence of integers, then these indices work independently
  along each dimension (similar to the way vector subscripts work in
  Fortran), rather than by their elements:

  >>> d.shape
  (12, 19, 73, 96)
  >>> d[0, :, [0, 1], [0, 13, 27]].shape
  (1, 19, 2, 3)

* Boolean indices may be any object which exposes the numpy array
  interface.

  >>> d.shape
  (12, 19, 73, 96)
  >>> d[..., d[0, 0, 0]>d[0, 0, 0].min()]

**Cyclic axes**

**Miscellaneous**

A `Data` object is picklable.

A `Data` object is hashable, but note that, since it is mutable, its
hash value is only valid whilst the data array is not changed in
place.

    '''

    def __init__(self, data=None, units=None, fill_value=None,
                 hardmask=True, chunk=True, loadd=None, loads=None, dt=False):
        '''**Initialization**

:Parameters:

    data: array-like, optional
        The data for the array.

    units : str or Units, optional
        The units of the data. By default the array elements are
        dimensionless.

    fill_value: optional 
        The fill value of the data. By default, or if None, the numpy
        fill value appropriate to the array's data type will be used.

    hardmask: `bool`, optional
        If False then the mask is soft. By default the mask is hard.

    chunk: `bool`, optional
        If False then the data array will be stored in a single
        partition. By default the data array will be partitioned if it
        is larger than the chunk size, as returned by the
        `cf.CHUNKSIZE` function.

    dt: `bool`, optional
        If True then strings (such as ``'1990-12-1 12:00'``) given by
        the *data* argument are interpreted as date-times. By default
        they are not interpreted as date-times.

    loadd: `dict`, optional
        Initialise the data array from a dictionary serialization of a
        `cf.Data` object. All other arguments are ignored.
    
    loads: `str`, optional
        Initialise the data array from a JSON string serialization of
        a `Data` object. All other arguments are ignored.
    
:Examples:

>>> d = cf.Data(5)
>>> d = cf.Data([1,2,3], units='K')
>>> import numpy   
>>> d = cf.Data(numpy.arange(10).reshape(2,5), units=cf.Units('m/s'), fill_value=-999)
>>> d = cf.Data(tuple('fly'))

        '''      
        empty_list = []

        # The _flip attribute is an unordered subset of the data
        # array's axis names. It is a subset of the axes given by the
        # _axes attribute. It is used to determine whether or not to
        # reverse an axis in each partition's sub-array during the
        # creation of the partition's data array. DO NOT CHANGE IN
        # PLACE.
        self._flip = empty_list

        # The _all_axes attribute must be None or a tuple
        self._all_axes = None 

        self._hardmask = hardmask
#        self._isdt     = False

        # The _HDF_chunks attribute is.... Is either None or a
        # dictionary. DO NOT CHANGE IN PLACE.
        self._HDF_chunks = None

        # ------------------------------------------------------------
        # Attribute: _auxiliary_mask
        #
        # Must be None or a (possibly empty) list of Data objects.
        # ------------------------------------------------------------
        self._auxiliary_mask = None

        if loadd is not None:
            self.loadd(loadd, chunk=chunk)
            return

        if loads is not None:
            self.loads(loads, chunk=chunk)
            return

        # The _cyclic attribute contains the axes of the data array
        # which are cyclic (and therefore allow cyclic slicing). It is
        # a subset of the axes given by the _axes attribute. DO NOT
        # CHANGE IN PLACE.
        self._cyclic = _empty_set

        units       = Units(units)
        self._Units = units

        self._fill_value = fill_value
 
        if data is None:
            self._dtype = None
            return

        if not isinstance(data, FileArray):
            check_free_memory = True

            if isinstance(data, self.__class__):
                self.loadd(data.dumpd(), chunk=chunk)
                return

            if not isinstance(data, numpy_ndarray):
                data = numpy_array(data)

            if (data.dtype.kind == 'O' and not dt and 
                hasattr(data.item((0,)*data.ndim), 'timetuple')):
                # We've been given one or more date-time objects
                dt = True

            
        else:
            check_free_memory = False

        dtype = data.dtype

        if dt or units.isreftime:
            kind = dtype.kind
            if kind == 'S':
                # Convert date-time strings to reference time floats
                if not units:
                    YMD = str(data.item((0,)*data.ndim)).partition('T')[0]
                    units = Units('days since '+YMD, units._calendar)
                    self._Units = units
            
                data = st2rt(data, units, units)
                dtype = data.dtype
            elif kind == 'O':
                # Convert date-time objects to reference time floats
                if not units:
                    # Set the units to something that is (hopefully)
                    # close to all of the datetimes, in an attempt to
                    # reduce errors arising from the conversion to
                    # reference times
                    x = data.item((0,)*data.ndim)
                    YMD = '-'.join(map(str, (x.year, x.month, x.day)))
                    units = Units('days since '+YMD, units._calendar)
                    self._Units = units

                data = dt2rt(data, None, units)

            dtype = data.dtype

            if not units.isreftime:
                raise ValueError(
"Can't initialise a reference time array with units {!r}".format(units))

#            self._isdt = dtype.kind in 'SO'
#
#            if self._isdt:
#                if not units:
#                    units = Units('days since 1970-1-1', units._calendar)
#                    self._Units = units
#            elif not units:
#                raise ValueError(
#                    "Can't initialise a numeric reference-time array with %r" %
#                    units)
#
#            if not units.isreftime:
#                raise ValueError(
#                    "Can't initialise a date-time array with %r" % units)
#
#            if dtype.kind == 'S':
#                # Convert date-time strings to date-time objects
#                data = st2dt(data, units)
#                dtype = data.dtype
#
##            dtype = _dtype_float
        #--- End: if

        shape = data.shape
        ndim  = data.ndim
        size  = data.size
        axes  = _initialise_axes(ndim)

        # The _axes attribute is the ordered list of the data array's
        # axis names. Each axis name is an arbitrary, unique
        # string. DO NOT CHANGE IN PLACE.
        self._axes = axes
            
        matrix = _xxx.copy()

        matrix[()] = Partition(location = [(0, n) for n in shape],
                               shape    = list(shape),
                               axes     = axes,
                               flip     = empty_list,
                               Units    = units,
                               subarray = data,
                               part     = empty_list)
        
        self.partitions = PartitionMatrix(matrix, empty_list)

        self._dtype = dtype
        self._ndim  = ndim
        self._shape = shape
        self._size  = size

        if chunk:
            self.chunk()

        if check_free_memory and FREE_MEMORY() < FM_THRESHOLD():
            self.to_disk()
    #--- End: def

    def __array__(self, *dtype):
        '''

Returns a numpy array copy the data array.

If the data array is stored as date-time objects then a numpy array of
numeric reference times will be returned.

:Returns:

    out: numpy.ndarray
        The numpy array copy the data array.

:Examples:

>>> (d.array == numpy.array(d)).all()
True
 
'''
        if not dtype:
            return self.array
        else:
            return self.array.astype(dtype[0]) #, copy=False) OUght to work!
    #--- End: def

    def __contains__(self, value):
        '''Membership test operator ``in``

x.__contains__(y) <==> y in x

Returns True if the value is contained anywhere in the data array. The
value may be a `cf.Data` object.

:Examples:

>>> d = cf.Data([[0.0, 1,  2], [3, 4, 5]], 'm')
>>> 4 in d
True
>>> cf.Data(3) in d
True
>>> cf.Data([2.5], units='2 m') in d
True
>>> [[2]] in d
True
>>> numpy.array([[[2]]]) in d
True
>>> cf.Data(2, 'seconds') in d
False

        '''
        if isinstance(value, self.__class__):
            self_units  = self.Units
            value_units = value.Units
            if value_units.equivalent(self_units):
                if not value_units.equals(self_units):                    
                    value = value.copy()                    
                    value.Units = self_units
            elif value_units:
                return False

            value = value.unsafe_array
        #--- End: if

        config = self.partition_configuration(readonly=True)

        for partition in self.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            partition.close()

            if value in array:
                return True
        #--- End: for

        return False
    #--- End: def

    def _auxiliary_mask_from_1d_indices(self, compressed_indices):
        '''

:Parameters:

    compressed_indices: 

:Returns:

    out: `list` of `cf.Data`

    '''
        auxiliary_mask = []

        for i, (compressed_index, size) in enumerate(zip(compressed_indices, self._shape)):

            if isinstance(compressed_index, slice) and compressed_index.step in (-1, 1):
                # Compressed index is a slice object with a step of
                # +-1 => no auxiliary mask required for this axis
                continue

            index = numpy_zeros(size, dtype=bool)
            index[compressed_index] = True                
            
            compressed_size = index.sum() 

            ind = numpy_where(index)

            ind0 = ind[0]
            start = ind0[0]
            envelope_size = ind0[-1] - start + 1
            
            if 0 < compressed_size < envelope_size:
                jj = [None] * self._ndim                            
                jj[i] = envelope_size

                if start:
                    ind0 -= start

                mask = self._auxiliary_mask_component(jj, ind, True)
                auxiliary_mask.append(mask)
        #--- End: for

        return auxiliary_mask
    #--- End: def 

    def _auxiliary_mask_return(self):
        '''Return the auxiliary mask.

:Examples 1:

>>> m = d._auxiliary_mask_return()

:Returns:

    out: `cf.Data` or `None`
        The auxiliary mask, or `None` if there isn't one.

        '''
        _auxiliary_mask = self._auxiliary_mask
        if not _auxiliary_mask:
            shape = getattr(self, '_shape', None)
            if shape is not None:
                return type(self).full(shape, False, bool)
            else:
                return None

        mask = _auxiliary_mask[0]
        for m in _auxiliary_mask[1:]:
            mask = mask | m

        return mask
    #-- End: def

    def _auxiliary_mask_add_component(self, mask):
        '''Add a new auxiliary mask.

:Examples 1:

>>> d._auxiliary_mask_add_component(m)

:Parameters:

    mask: `cf.Data` or `None`

:Returns:

    `None`

        '''
        if mask is None:
            return

        # Check that this mask component has the correct number of
        # dimensions
        if mask.ndim != self._ndim:
            raise ValueError(
"Auxiliary mask must have same number of axes as the data array ({}!={})".format(
    mask.ndim, self.ndim))

        # Check that this mask component has an appropriate shape
        mask_shape = mask.shape
        for i, j in zip(mask_shape, self._shape):
            if not (i == j or i == 1):
                raise ValueError(
"Auxiliary mask shape {} is not broadcastable to data array shape {}".format(
    mask.shape, self._shape))

        # Merge this mask component with another, if possible.
        append = True
        if self._auxiliary_mask is not None:
            for m0 in self._auxiliary_mask:
                if m0.shape == mask_shape:
                    # Merging the new mask with an existing auxiliary
                    # mask component
                    m0 |= mask
                    append = False
                    break
        #--- End: if

        if append:
            mask = mask.copy()
            
            # Make sure that the same axes are cyclic for the data
            # array and the auxiliary mask
            indices = [self._axes.index(axis) for axis in self._cyclic]
            mask._cyclic = set([mask._axes[i] for i in indices])
            
            if self._auxiliary_mask is None:
                self._auxiliary_mask = [mask]
            else:
                self._auxiliary_mask.append(mask)
    #--- End: def

    def _auxiliary_mask_subspace(self, indices):
        '''Subspace the new auxiliary mask.

:Examples 1:

>>> d._auxiliary_mask_subspace((slice(0, 9, 2))

:Returns:

    `None`

        '''
        if not self._auxiliary_mask:
            # There isn't an auxiliary mask
            return

        new = []
        for mask in self._auxiliary_mask:
            mask_indices = [(slice(None) if n == 1 else index)
                            for n, index in zip(mask.shape, indices)]
            new.append(mask[tuple(mask_indices)])
            
        self._auxiliary_mask = new
    #--- End: def
        
    def _create_auxiliary_mask_component(self, mask_shape, ind, compress):
        '''asdasdasdas

:Parameters:

    mask_shape: `tuple`
        The shape of the mask component to be created. This will
        contain `None` for axes not spanned by the *ind* parameter.

          :Example:
              ``mask_shape=(3, 11, None)``

    ind: `numpy.ndarray`
        As returned by a single argument call of
        ``numpy.array(numpy[.ma].where(....))``.

    compress: `bool`
        If True then remove whole slices which only contain masked
        points.

:Returns:

    out: `cf.Data`

        '''
        # --------------------------------------------------------
        # Find the shape spanned by ind
        # --------------------------------------------------------
        shape = [n for n in mask_shape if n]

        # Note that, for now, auxiliary_mask has to be numpy array
        # (rather than a cf.Data object) because we're going to index
        # it with fancy indexing which a cf.Data object might not
        # support - namely a non-monotonic list of integers.
        auxiliary_mask = numpy_ones(shape, dtype=bool)

        auxiliary_mask[tuple(ind)] = False

        if compress:
            # For compressed indices, remove slices which only
            # contain masked points. (Note that we only expect to
            # be here if there were N-d item criteria.)
            for iaxis, (index, n) in enumerate(zip(ind, shape)):
                index = set(index)
                if len(index) < n:
                    auxiliary_mask = auxiliary_mask.take(sorted(index), axis=iaxis)
        #--- End: if

        # Add missing size 1 axes to the auxiliary mask
        if auxiliary_mask.ndim < self.ndim:
            i = [(slice(None) if n else numpy_newaxis) for n in mask_shape]
            auxiliary_mask = auxiliary_mask[tuple(i)]

        return type(self)(auxiliary_mask)
    #--- End: def 

    def _auxiliary_mask_tidy(self):
        '''Remove unnecessary auxiliary mask components.

:Examples 1:

>>> d._auxiliary_mask_tidy()

:Returns:

    `None`

        '''
        auxiliary_mask = self._auxiliary_mask
        if auxiliary_mask:
            # Get rid of auxiliary mask components which are all False
            auxiliary_mask = [m for m in auxiliary_mask if m.any()]
            if not auxiliary_mask:
                auxiliary_mask = None
        else:
            auxiliary_mask = None

        self._auxiliary_mask = auxiliary_mask
    #--- End: def
    
#    @property
#    def subspace(self):
#        '''
#
#Return a new object which will get or set a subspace of the array.
#
#``e=d.subspace[indices]`` is equivalent to
#``e=d[indices]``. ``d.subspace[indices]=x`` is equivalent to
#``d[indices]=x``.
#
#'''
#        return SubspaceData(self)
#    #--- End: def

    def __data__(self):
        '''
Returns a new reference to self.
'''
        return self
    #--- End: def

    def __deepcopy__(self, memo):
        '''

Used if copy.deepcopy is called.

''' 
        return self.copy()
    #--- End: def

#    def __getstate__(self):
#        '''
#
#Called when pickling.
#
#:Parameters:
#
#    None
#
#:Returns:
#
#    out: dict
#        A dictionary of the instance's attributes
#
#:Examples:
#
#'''
#        return dict([(attr, getattr(self, attr))
#                     for attr in self.__slots__ if hasattr(self, attr)])
#    #--- End: def        

#    def __setstate__(self, odict):
#        '''
#
#Called when unpickling.
#
#:Parameters:
#
#    odict : dict
#        The output from the instance's `__getstate__` method.
#
#:Returns:
#
#    None
#
#'''
#        for attr, value in odict.iteritems():
#            setattr(self, attr, value)
#    #--- End: def

    def __hash__(self):
        '''

The built-in function `hash`

Generating the hash temporarily realizes the entire array in memory,
which may not be possible for large arrays.

The hash value is dependent on the data type and shape of the data
array. If the array is a masked array then the hash value is
independent of the fill value and of data array values underlying any
masked elements.

The hash value may be different if regenerated after the data array
has been changed in place.

The hash value is not guaranteed to be portable across versions of
Python, numpy and cf.

:Returns:

    out: int
        The hash value.

:Examples:

>>> print d.array
[[0 1 2 3]]
>>> d.hash()
-8125230271916303273
>>> d[1, 0] = numpy.ma.masked
>>> print d.array
[[0 -- 2 3]]
>>> hash(d)
791917586613573563
>>> d.hardmask = False
>>> d[0, 1] = 999
>>> d[0, 1] = numpy.ma.masked
>>> d.hash()
791917586613573563
>>> d.squeeze()
>>> print d.array
[0 -- 2 3]
>>> hash(d)
-7007538450787927902
>>> d.dtype = float
>>> print d.array
[0.0 -- 2.0 3.0]
>>> hash(d)
-4816859207969696442

'''
        return hash_array(self.unsafe_array)
    #--- End: def

    def __float__(self):
        if self.size != 1:
            raise TypeError(
                "only length-1 arrays can be converted to Python scalars")
        return float(self.datum())
    #--- End: def

    def __round__(self, *n):
        if self.size != 1:
            raise TypeError(
                "only length-1 arrays can be converted to Python scalars")
        return round(self.datum(), *n)
    #--- End: def

    def __int__(self):
        if self.size != 1:
            raise TypeError(
                "only length-1 arrays can be converted to Python scalars")
        return int(self.datum())
    #--- End: def

    def __iter__(self):
        '''

Efficient iteration.

x.__iter__() <==> iter(x)

:Examples:

>>> d = cf.Data([1, 2, 3], 'metres')
>>> for e in d:
...    print repr(e)
...
1
2
3

>>> d = cf.Data([[1, 2], [4, 5]], 'metres')
>>> for e in d:
...    print repr(e)
...
<CF Data: [1, 2] metres>
<CF Data: [4, 5] metres>

>>> d = cf.Data(34, 'metres')
>>> for e in d:
...     print repr(e)
..
TypeError: iteration over a 0-d Data

'''
        ndim = self._ndim

        if not ndim:
            raise TypeError(
                "Iteration over 0-d {}".format(self.__class__.__name__))
            
        elif ndim == 1:
            if self.fits_in_memory(self.dtype.itemsize):
                i = iter(self.unsafe_array)
                while 1:
                    yield i.next()
            else:
                for n in xrange(self._size):
                    yield self[n].unsafe_array[0]

        else:
            # ndim > 1
            for n in xrange(self._shape[0]):
                yield self[n, ...].squeeze(0, i=True)
    #--- End: def

    def __len__(self):
        '''

The built-in function `len`

x.__len__() <==> len(x)

:Examples:

>>> len(cf.Data([1, 2, 3]))
3
>>> len(cf.Data([[1, 2, 3]]))
1
>>> len(cf.Data([[1, 2, 3], [4, 5, 6]])
2
>>> len(cf.Data(1))
TypeError: len() of scalar Data

'''
        shape = self._shape
        if shape:
            return shape[0]

        raise TypeError("len() of scalar {}".format(self.__class__.__name__))
    #--- End: def

    def __nonzero__(self):
        '''

Truth value testing and the built-in operation `bool`

x.__nonzero__() <==> x != 0

:Examples:

>>> bool(cf.Data(1))
True
>>> bool(cf.Data([[False]]))
False
>>> bool(cf.Data([1, 2]))
ValueError: The truth value of Data with more than one element is ambiguous. Use d.any() or d.all()

'''
        if self._size == 1:
            return bool(self.unsafe_array)

        raise ValueError(
"The truth value of Data with more than one element is ambiguous. Use d.any() or d.all()")
    #--- End: def

    def __repr__(self):
        '''

The built-in function `repr`

x.__repr__() <==> repr(x)

'''
        return '<CF {0}: {1}>'.format(self.__class__.__name__, str(self))
    #--- End: def

    def __str__(self):
        '''

The built-in function `str`

x.__str__() <==> str(x)

'''
        self_units = self.Units
        isreftime = self_units.isreftime

        if not self_units or self_units.equals(_units_1):
            units = None
        elif not isreftime:
            units = self_units.units
        else:
            calendar = getattr(self_units, 'calendar', '')
            if calendar == 'none':
                units = self_units.units
            else:
                units = calendar
        #--- End: if
        
        size = self._size
        ndim = self._ndim
        open_brackets  = '[' * ndim
        close_brackets = ']' * ndim

        try:
            first = self.datum(0)
        except:            
            out = ''
            if units:
                out += ' {0}'.format(units)
                
            return out
        #--- End: try
        
        if size == 1:
            if isreftime:
                if calendar != 'none':
                    # Convert reference time to date-time
                    first = rt2dt(first, self_units).item()

            out = '{0}{1}{2}'.format(open_brackets, first, close_brackets)
        else:
            last = self.datum(-1)
            if isreftime:
                if calendar != 'none':
                    # Convert reference times to date-times
                    first, last = rt2dt(numpy_ma_array((first, last)), self_units)
            #--- End: if
            
            if size >= 3:
                out = '{0}{1}, ..., {2}{3}'.format(open_brackets, first,
                                                   last, close_brackets)

            else:
                out = '{0}{1}, {2}{3}'.format(open_brackets, first,
                                              last, close_brackets)
        #--- End: if
        
        if units:
            out += ' {0}'.format(units)
            
        return out
    #--- End: def

    def __getitem__(self, indices):
        '''

Implement indexing

x.__getitem__(indices) <==> x[indices]

'''
        size = self._size
        if size == 1 or indices is Ellipsis:
            return self.copy()
        
        d = self

        axes           = d._axes
        flip           = d._flip
        shape          = d._shape
        cyclic_axes    = d._cyclic
        auxiliary_mask = []

        try:
            arg0 = indices[0]
        except (IndexError, TypeError):
            pass
        else:
            if isinstance(arg0, basestring) and arg0 == 'mask':
                auxiliary_mask = indices[1]
                indices        = tuple(indices[2:])
            else:
                pass

        indices, roll, flip_axes = parse_indices(shape, indices, True, True)

        if roll:
            for axis, shift in roll.iteritems():
                if axes[axis] not in cyclic_axes:
                    raise IndexError(
"Can't take a cyclic slice of a non-cyclic axis (axis {})".format(axis))

                d = d.roll(axis, shift)
        #--- End: if

        new_shape = tuple(map(_size_of_index, indices, shape))
        new_size  = long(reduce(operator_mul, new_shape, 1))

        new = Data.__new__(Data)

        new._shape      = new_shape
        new._size       = new_size
        new._ndim       = d._ndim
        new._fill_value = d._fill_value
        new._hardmask   = d._hardmask
        new._all_axes   = d._all_axes
        new._cyclic     = cyclic_axes
        new._axes       = axes
        new._flip       = flip
        new._dtype      = d.dtype
        new._HDF_chunks = d._HDF_chunks
        new.Units       = d.Units
        new._auxiliary_mask = d._auxiliary_mask

        partitions = d.partitions

        new_partitions = PartitionMatrix(_overlapping_partitions(partitions, 
                                                                 indices, 
                                                                 axes,
                                                                 flip),
                                         partitions.axes)

        if new_size != size:
            new_partitions.set_location_map(axes)

        new.partitions = new_partitions

        # ------------------------------------------------------------
        # Index an existing auxiliary mask. (Note: By now indices are
        # strictly monotonically increasing and don't roll.)
        # ------------------------------------------------------------
        new._auxiliary_mask_subspace(indices)
        
        # --------------------------------------------------------
        # Apply the input auxiliary mask
        # --------------------------------------------------------
        for mask in auxiliary_mask:
            new._auxiliary_mask_add_component(mask)

        # ------------------------------------------------------------
        # Tidy up the auxiliary mask
        # ------------------------------------------------------------
        new._auxiliary_mask_tidy()

        # ------------------------------------------------------------
        # Flip axes
        # ------------------------------------------------------------
        if flip_axes:
            new.flip(flip_axes, i=True)
     
        # ------------------------------------------------------------
        # Mark cyclic axes which have been reduced in size as
        # non-cyclic
        # ------------------------------------------------------------
        if cyclic_axes:
            x = [i
                 for i, (axis, n0, n1) in enumerate(zip(axes, shape, new_shape))
                 if n1 != n0 and axis in cyclic_axes]
            if x:
                new._cyclic = cyclic_axes.difference(x)
        #--- End: if

        #-------------------------------------------------------------
        # Remove size 1 axes from the partition matrix
        #-------------------------------------------------------------
        new_partitions.squeeze(i=True)

        return new
    #--- End: def

    def __setitem__(self, indices, value):
        '''

Implement indexed assignment

x.__setitem__(indices, y) <==> x[indices]=y

Assignment to data array elements defined by indices.

Elements of a data array may be changed by assigning values to a
subspace. See `__getitem__` for details on how to define subspace of
the data array.

**Missing data**

The treatment of missing data elements during assignment to a subspace
depends on the value of the `hardmask` attribute. If it is True then
masked elements will notbe unmasked, otherwise masked elements may be
set to any value.

In either case, unmasked elements may be set, (including missing
data).

Unmasked elements may be set to missing data by assignment to the
`cf.masked` constant or by assignment to a value which contains masked
elements.

.. seealso:: `cf.masked`, `hardmask`, `where`

:Examples:

'''            
        def _mirror_slice(index, size):
            '''

    Return a slice object which creates the reverse of the input
    slice.

    The step of the input slice must have a step of `.
    
    :Parameters:
    
        index : slice
            A slice object with a step of 1.

        size : int
    
    :Returns:
    
        out: slice
    
    :Examples:
    
    >>> s = slice(2, 6)
    >>> t = _mirror_slice(s, 8)
    >>> s, t
    slice(2, 6), slice(5, 1, -1)
    >>> range(8)[s]
    [2, 3, 4, 5]
    >>> range(8)[t]
    [5, 4, 3, 2]
    >>> range(7, -1, -1)[s]
    [5, 4, 3, 2]
    >>> range(7, -1, -1)[t]
    [2, 3, 4, 5]
    
    '''
            start, stop, step = index.indices(size)
            size -= 1
            start = size - start
            stop  = size - stop
            if stop < 0:
                stop = None
                
            return slice(start, stop, -1)
        #--- End: def

        config = self.partition_configuration(readonly=False)

        # ------------------------------------------------------------
        # parse the indices
        # ------------------------------------------------------------
#        indices, roll, flip_axes = _parse_indices(self, indices)
        indices_in = indices
        indices, roll, flip_axes = parse_indices(self._shape, indices_in, True, True)

        if roll:
            for iaxis, shift in roll.iteritems():
                self.roll(iaxis, shift, i=True)
         
        scalar_value = False
        if value is cf_masked:
            scalar_value  = True
        else:
            copied = False
            if not isinstance(value, Data):
                # Convert to the value to a Data object
                value = type(self)(value, self.Units)
            else:
                if value.Units.equivalent(self.Units):
                    if not value.Units.equals(self.Units):                    
                        value = value.copy()                    
                        value.Units = self.Units
                        copied = True
                elif not value.Units:                    
                    value = value.override_units(self.Units)
                    copied = True
                else:
                    raise ValueError(
"Can't assign values with units {!r} to data with units {!r}".format(
     value.Units, self.Units))
            #--- End: if

            if value._size == 1:
                scalar_value = True                

                value = value.datum(0)
        #--- End: if

        if scalar_value:
            # --------------------------------------------------------
            # The value is logically scalar
            # --------------------------------------------------------           
            for partition in self.partitions.matrix.flat:
                p_indices, shape = partition.overlaps(indices)
                if p_indices is None:
                    # This partition does not overlap the indices
                    continue

                partition.open(config)
                array = partition.array

                if value is cf_masked and not partition.masked:
                    # The assignment is masking elements, so turn a
                    # non-masked sub-array into a masked one.
                    array = array.view(numpy_ma_MaskedArray)
                    partition.subarray = array

                set_subspace(array, p_indices, value)
                partition.close()
            #--- End: for

            if roll:
                for iaxis, shift in roll.iteritems():
                    self.roll(iaxis, -shift, i=True)

            return

        # ------------------------------------------------------------
        # Still here? Then the value is not logically scalar.
        # ------------------------------------------------------------
        data0_shape  = self._shape
        value_shape = value._shape
        
        shape0 = map(_size_of_index, indices, data0_shape)
        self_ndim  = self._ndim
        value_ndim = value._ndim
        align_offset = self_ndim - value_ndim
        if align_offset >= 0:
            # self has more dimensions than other
            shape0   = shape0[align_offset:]
            shape1   = value_shape
            ellipsis = None 
            
            flip_axes = [i-align_offset for i in flip_axes
                         if i >= align_offset]                
        else:
            # value has more dimensions than self
            v_align_offset = -align_offset
            if value_shape[:v_align_offset] != [1] * v_align_offset:
                # Can only allow value to have more dimensions then
                # self if the extra dimensions all have size 1.
                raise ValueError("Can't broadcast shape %r across shape %r" %
                                 (value_shape, data0_shape))
            
            shape1       = value_shape[v_align_offset:]
            ellipsis     = Ellipsis
            align_offset = 0

        # Find out which of the dimensions of value are to be
        # broadcast, and those which are not. Note that, as in numpy,
        # it is not allowed for a dimension in value to be larger than
        # a size 1 dimension in self
        base_value_indices       = []
        non_broadcast_dimensions = []

        for i, (a, b) in enumerate(izip(shape0, shape1)):
            if b == 1:
                base_value_indices.append(slice(None))
            elif a == b and b != 1:
                base_value_indices.append(None)
                non_broadcast_dimensions.append(i)
            else:
                raise ValueError("Can't broadcast shape %r across shape %r" %
                                 (shape1, shape0))
        #--- End: for

        previous_location = ((-1,),) * self_ndim
        start             = [0] * value_ndim

#        save = pda_args['save']
#        keep_in_memory = pda_args['keep_in_memory']

        value.to_memory()

        for partition in self.partitions.matrix.flat:
            p_indices, shape = partition.overlaps(indices)        

            if p_indices is None:
                # This partition does not overlap the indices          
                continue

            # --------------------------------------------------------
            # Find which elements of value apply to this partition
            # --------------------------------------------------------
            value_indices = base_value_indices[:]
       
            for i in non_broadcast_dimensions:
                j                  = i + align_offset
                location           = partition.location[j][0]
                reference_location = previous_location[j][0]

                if location > reference_location:
                    stop             = start[i] + shape[j]
                    value_indices[i] = slice(start[i], stop)
                    start[i]         = stop

                elif location == reference_location:
                    value_indices[i] = previous_slice[i]

                elif location < reference_location:
                    stop             = shape[j]
                    value_indices[i] = slice(0, stop)
                    start[i]         = stop
            #--- End: for

            previous_location = partition.location
            previous_slice    = value_indices[:]
          
            for i in flip_axes:
                value_indices[i] = _mirror_slice(value_indices[i], shape1[i])

            if ellipsis:
                value_indices.insert(0, ellipsis)

            # --------------------------------------------------------
            # 
            # --------------------------------------------------------
            v = value[tuple(value_indices)].varray

#            if keep_in_memory: #not save:
#                v = v.copy()

            # Update the partition's data
            partition.open(config)
            array = partition.array

            if not partition.masked and numpy_ma_isMA(v):
                # The sub-array is not masked and the assignment is
                # masking elements, so turn the non-masked sub-array
                # into a masked one.
                array = array.view(numpy_ma_MaskedArray)
                partition.subarray = array

            set_subspace(array, p_indices, v)

            partition.close()
        #--- End: For

        if roll:
            # Unroll
            for iaxis, shift in roll.iteritems():
                self.roll(iaxis, -shift, i=True)
    #--- End: def
    
    def _flag_partitions_for_processing(self, parallelise=True):
        '''
        '''
        if mpi_on and parallelise:
            # Add a flag `_process_partition` to each partition defining
            # whether this partition will be processed on this process
            n_partitions = self.partitions.size
            x = n_partitions / mpi_size
            if n_partitions < mpi_size:
                for i, partition in enumerate(self.partitions.matrix.flat):
                    if i == mpi_rank:
                        partition._process_partition = True
                    else:
                        partition._process_partition = False
                    #--- End: if
                #--- End: for
                self._max_partitions_per_process = 1
            elif n_partitions % mpi_size == 0:
                for i, partition in enumerate(self.partitions.matrix.flat):
                    if i / x == mpi_rank:
                        partition._process_partition = True
                    else:
                        partition._process_partition = False
                    #--- End: if
                #--- End: for
                self._max_partitions_per_process = x
            else:
                for i, partition in enumerate(self.partitions.matrix.flat):
                    if i / (x + 1) == mpi_rank:
                        partition._process_partition = True
                    else:
                        partition._process_partition = False
                    #--- End: if
                #--- End: for
                self._max_partitions_per_process = x + 1
            #--- End: if
        else:
            # Flag all partitions for processing on all processes
            for partition in self.partitions.matrix.flat:
                partition._process_partition = True
            #--- End: for
        #--- End: if

    #--- End: def

    def _share_lock_files(self, parallelise):
        if parallelise:
            # Only gather the lock files if the subarrays have been
            # gathered between procesors, otherwise this will result
            # in incorrect handling of the removal of temporary files
            for partition in self.partitions.matrix.flat:
                if partition.in_temporary_file:
                    # The subarray is in a temporary file
                    lock_file = partition._register_temporary_file()
                    lock_files = mpi_comm.allgather(lock_file)
                    partition._update_lock_files(lock_files)
                #--- End: if
            #--- End: for
        #--- End: if
    #--- End: if

    @classmethod
    def _share_partitions(cls, processed_partitions, parallelise):
        # Share the partitions processed on each rank with every other
        # rank. If parallelise is False then there is nothing to be done
        if parallelise:
            # List to contain sublists of processed partitions from each
            # rank
            partition_list = []

            for rank in range(mpi_size):
                # Get the numper of processed partitions on each rank
                if mpi_rank == rank:
                    n_partitions = len(processed_partitions)
                else:
                    n_partitions = None
                #--- End: if
                n_partitions = mpi_comm.bcast(n_partitions, root=rank)

                # Share each of the processed partitions on each rank with
                # all the other ranks using broadcasting
                if mpi_rank != rank:
                    shared_partitions = []
                #--- End: if

                for i in range(n_partitions):
                    if mpi_rank == rank:
                        partition = processed_partitions[i]
                        if isinstance(partition._subarray, numpy_ndarray):
                            # If the subarray is a numpy array, swap it
                            # out before broadcasting the partition
                            subarray = partition._subarray
                            partition._subarray = None
                            partition._subarray_is_in_memory = True
                            partition._subarray_dtype = subarray.dtype
                            partition._subarray_shape = subarray.shape
                            partition._subarray_isMA = numpy_ma_isMA(subarray)
                            if partition._subarray_isMA:
                                partition._subarray_is_masked = not subarray.mask is numpy_ma_nomask
                            else:
                                partition._subarray_is_masked = False
                            #--- End: if
                        else:
                            partition._subarray_is_in_memory = False
                        #--- End: if
                    else:
                        partition = None
                    #--- End: if
                    partition = mpi_comm.bcast(partition, root=rank)

                    if partition._subarray_is_in_memory:
                        # If the subarray is a numpy array broadcast it
                        # without serialising and swap it back into the
                        # partition
                        if partition._subarray_isMA:
                            # If the subarray is a masked array broadcast
                            # the data and the mask separately
                            if mpi_rank != rank:
                                if partition._subarray_is_masked:
                                    subarray = numpy_ma_masked_all(partition._subarray_shape,
                                                                   dtype=partition._subarray_dtype)
                                else:
                                    subarray = numpy_ma_empty(partition._subarray_shape,
                                                              dtype=partition._subarray_dtype)
                                #--- End: if
                            #--- End: if
                            mpi_comm.Bcast(subarray.data, root=rank)
                            if partition._subarray_is_masked:
                                mpi_comm.Bcast(subarray.mask, root=rank)
                            #--- End: if
                        else:
                            if mpi_rank != rank:
                                subarray = numpy_empty(partition._subarray_shape,
                                                       dtype=partition._subarray_dtype)
                            #--- End: if
                            mpi_comm.Bcast(subarray, root=rank)
                        #--- End: if

                        # Swap the subarray back into the partition
                        partition._subarray = subarray
                        if mpi_rank == rank:
                            # The result of broadcasting an object is
                            # different to the original object even on the
                            # root PE, so the new partition with the numpy
                            # subarray must be put back in the list of
                            # processed partitions
                            processed_partitions[i] = partition
                        #--- End: if

                        # Clean up temporary attributes
                        del partition._subarray_dtype
                        del partition._subarray_shape
                        del partition._subarray_isMA
                        del partition._subarray_is_masked
                    elif mpi_rank == rank:
                        # Remove the subarray from partition so that
                        # when it is deleted it does not delete the
                        # temporary file
                        partition._subarray = None
                    #--- End: if

                    # Clean up temporary attribute
                    del partition._subarray_is_in_memory

                    if mpi_rank != rank:
                        shared_partitions.append(partition)
                    #--- End: if
                #--- End: for

                # Add the sublist of processed partitions from each rank
                # to a list
                if mpi_rank == rank:
                    partition_list.append(processed_partitions)
                else:
                    partition_list.append(shared_partitions)
                #--- End: if
            #--- End: for

            # Flatten the list of lists of processed partitions
            processed_partitions = [item
                                    for sublist in partition_list
                                    for item in sublist]
        #--- End: if
        return processed_partitions
    #--- End: def
    
    def dumps(self):
        '''Return a JSON string serialization of the data array.

        '''
        d = self.dumpd()

        # Change a set to a list
        if '_cyclic' in d:
            d['_cyclic'] = list(d['_cyclic'])

        # Change numpy.dtype object to a data type string
        if 'dtype' in d:
            d['dtype'] = str(d['dtype'])

        # Change a Units object to a units string
        if 'Units' in d:
            d['units'] = str(d.pop('Units'))

        #
        for p in d['Partitions']:
            if 'Units' in p:
                p['units'] = str(p.pop('Units'))
        #--- End: for

        return json_dumps(d, default=_convert_to_builtin_type)
    #--- End: def

    def loads(self, j, chunk=True):
        '''
        '''
        d = json_loads(j)

        # Convert _cyclic to a set
        if '_cyclic' in d:
            d['_cyclic'] = set(d['_cyclic'])

        # Convert dtype to numpy.dtype
        if 'dtype' in d:
            d['dtype'] = numpy_dtype(d['dtype'])

        # Convert units to Units
        if 'units' in d:
            d['Units'] = Units(d.pop('units'))

        # Convert partition location elements to tuples
        for p in d['Partitions']:
            p['location'] = [tuple(x) for x in p['location']]

            if 'units' in p:
                p['Units'] = Units(p.pop('units'))
        #--- End: for

        self.loadd(d, chunk=chunk)
    #--- End: def

    def dumpd(self):
        '''Return a serialization of the data array.

The serialization may be used to reconstruct the data array as it was
at the time of the serialization creation.

.. seealso:: `loadd`

:Examples 1:

>>> s = d.dumpd()

:Returns:

    out: `dict`
        The serialization.

:Examples:

>>> d = cf.Data([[1, 2, 3]], 'm')
>>> d.dumpd()
{'Partitions': [{'location': [(0, 1), (0, 3)],
                 'subarray': array([[1, 2, 3]])}],
 'units': 'm',
 '_axes': ['dim0', 'dim1'],
 '_pmshape': (),
 'dtype': dtype('int64'),
 'shape': (1, 3)}

>>> d.flip(1)
>>> d.transpose()
>>> d.Units *= 1000
>>> d.dumpd()
{'Partitions': [{'units': 'm',
                 'axes': ['dim0', 'dim1'],
                 'location': [(0, 3), (0, 1)],
                 'subarray': array([[1, 2, 3]])}],
` 'units': '1000 m',
 '_axes': ['dim1', 'dim0'],
 '_flip': ['dim1'],
 '_pmshape': (),
 'dtype': dtype('int64'),
 'shape': (3, 1)}

>>> d.dumpd()
{'Partitions': [{'units': 'm',
                 'location': [(0, 1), (0, 3)],
                 'subarray': array([[1, 2, 3]])}],
 'units': '10000 m',
 '_axes': ['dim0', 'dim1'],
 '_flip': ['dim1'],
 '_pmshape': (),
 'dtype': dtype('int64'),
 'shape': (1, 3)}

>>> e = cf.Data(loadd=d.dumpd())
>>> e.equals(d)
True

        ''' 
        axes  = self._axes
        units = self.Units
        dtype = self.dtype

        cfa_data = {
            'dtype'   : dtype,
            'units'   : str(units),
            'shape'   : self._shape,
            '_axes'   : axes[:],
            '_pmshape': self._pmshape,
            }

        pmaxes = self._pmaxes
        if pmaxes:
            cfa_data['_pmaxes'] = pmaxes[:]

        flip = self._flip
        if flip:
            cfa_data['_flip'] =  flip[:]

        fill_value = self._fill_value
        if fill_value is not None:
            cfa_data['fill_value'] = fill_value
           
        cyclic = self._cyclic
        if cyclic:
            cfa_data['_cyclic'] = cyclic.copy()

        HDF_chunks = self._HDF_chunks
        if HDF_chunks:
            cfa_data['_HDF_chunks'] = HDF_chunks.copy()

        partitions = []            
        for index, partition in self.partitions.ndenumerate():

            attrs = {}

            p_subarray = partition.subarray
            p_dtype    = p_subarray.dtype
            
            # Location in partition matrix
            if index:
                attrs['index'] = index

            # Sub-array location
            attrs['location'] = partition.location[:]
            
            # Sub-array part
            p_part = partition.part                       
            if p_part:
                attrs['part'] = p_part[:]

            # Sub-array axes
            p_axes = partition.axes
            if p_axes != axes:
                attrs['axes'] = p_axes[:]

            # Sub-array units
            p_Units = partition.Units
            if p_Units != units:
                attrs['Units'] = str(p_Units)

            # Sub-array flipped axes
            p_flip  = partition.flip
            if p_flip:
                attrs['flip'] = p_flip[:]

            # --------------------------------------------------------
            # File format specific stuff
            # --------------------------------------------------------
            if isinstance(p_subarray, NetCDFFileArray):
#            if isinstance(p_subarray.array, NetCDFFileArray):
                # ----------------------------------------------------
                # NetCDF File Array
                # ----------------------------------------------------
                attrs['format'] = 'netCDF'

                subarray = {}
                for attr in ('file', 'shape'):
                    subarray[attr] = getattr(p_subarray, attr)

                for attr in ('ncvar', 'varid'):
                    value = getattr(p_subarray, attr, None)
#                    value = getattr(p_subarray.array, attr, None)
#                    p_subarray.array.inspect()
                
                    if value is not None:
                        subarray[attr] = value
                #--- End: for

                if p_dtype != dtype:
                    subarray['dtype'] = p_dtype

                attrs['subarray'] = subarray         

            elif isinstance(p_subarray, UMFileArray):
#            elif isinstance(p_subarray.array, UMFileArray):
                # ----------------------------------------------------
                # UM File Array
                # ----------------------------------------------------
                attrs['format'] = 'UM'
            
                subarray = {}
                for attr in ('file', 'shape',
                             'header_offset', 'data_offset', 'disk_length'):
                    subarray[attr] = getattr(p_subarray, attr)
                #--- End: for
                
                if p_dtype != dtype:
                    subarray['dtype'] = p_dtype

                attrs['subarray'] = subarray
            else:
                attrs['subarray'] = p_subarray
#                attrs['subarray'] = p_subarray.array
                 
            partitions.append(attrs)            
        #--- End: for

        cfa_data['Partitions'] = partitions

        # ------------------------------------------------------------
        # Auxiliary mask
        # ------------------------------------------------------------
        if self._auxiliary_mask:
            cfa_data['_auxiliary_mask'] = [m.copy() for m in self._auxiliary_mask]

        return cfa_data
    #--- End:s def
        
    def loadd(self, d, chunk=True):
        '''Reset the data array in place from a data array serialization.

.. seealso:: `dumpd`

:Examples 1:

>>> d.loadd(s)

:Parameters:

    d: `dict`
        A dictionary serialization of a `cf.Data` object, such as one
        as returned by the `dumpd` method.
 
    chunk: `bool`, optional
        If True (the default) then the reset data array will be
        re-partitions according the current chunk size, as defined by
        the `cf.CHUNKSIZE` function.

:Returns:

    `None`

:Examples 2:

>>> d = cf.Data([[1, 2, 3]], 'm')
>>> e = cf.Data([6, 7, 8, 9], 's')
>>> e.loadd(d.dumpd())
>>> e.equals(d)
True
>>> e is d
False

>>> e = cf.Data(loadd=d.dumpd())
>>> e.equals(d)
True

        '''
        axes  = list(d.get('_axes', ()))
        shape = tuple(d.get('shape', ()))

        units = d.get('units', None)
        if units is None:
            units = Units()
        else:
            units = Units(units)
            
        dtype = d['dtype']
        self._dtype = dtype

        self.Units       = units
        self._axes       = axes
        self._flip       = list(d.get('_flip', ()))
        self._fill_value = d.get('fill_value', None)

        self._shape = shape
        self._ndim  = len(shape)
        self._size  = long(reduce(operator_mul, shape, 1))

        cyclic = d.get('_cyclic', None)
        if cyclic:
            self._cyclic = cyclic.copy()
        else:
            self._cyclic = _empty_set

        HDF_chunks = d.get('_HDF_chunks', None)
        if HDF_chunks:
            self._HDF_chunks = HDF_chunks.copy()
        else:
            self._HDF_chunks = None

        filename = d.get('file', None)
#        if filename is not None:
#            filename = abspath(filename)

        base = d.get('base', None)
#        if base is not None:
#            base = abspath(base)

        # ------------------------------------------------------------
        # Initialise an empty partition array
        # ------------------------------------------------------------
        partition_matrix = PartitionMatrix(
            numpy_empty(d.get('_pmshape', ()), dtype=object),
            list(d.get('_pmaxes', ()))
            )
        pmndim = partition_matrix.ndim

        # ------------------------------------------------------------
        # Fill the partition array with partitions
        # ------------------------------------------------------------
        for attrs in d['Partitions']:

            # Find the position of this partition in the partition
            # matrix
            if 'index' in attrs:
                index = attrs['index']
                if len(index) == 1:
                    index = index[0]
                else:
                    index = tuple(index)
            else:
                index = (0,) * pmndim

            location = attrs.get('location', None)
            if location is not None:
                location = location[:]
            else:
                # Default location
                location = [[0, i] for i in shape]

            p_units = attrs.get('p_units', None)
            if p_units is None:
                p_units = units
            else:
                p_units = Units(p_units)
                
            partition = Partition(
                location = location,
                axes     = attrs.get('axes', axes)[:],
                flip     = attrs.get('flip', [])[:],
                Units    = p_units,
                part     = attrs.get('part', [])[:],
                )
            
            fmt = attrs.get('format', None)
            if fmt is None:
                # ----------------------------------------------------
                # Subarray is effectively a numpy array in memory
                # ----------------------------------------------------
                partition.subarray = attrs['subarray']

            else:
                # ----------------------------------------------------
                # Subarray is in a file on disk
                # ----------------------------------------------------
                partition.subarray = attrs['subarray']
                if fmt not in ('netCDF', 'UM'):
                    raise TypeError(
                        "Don't know how to load sub-array from file format %r" %
                        fmt)

                # Set the 'subarray' attribute 
                kwargs = attrs['subarray'].copy()
                kwargs['shape'] = tuple(kwargs['shape'])
                
                kwargs['ndim'] = len(kwargs['shape'])
                kwargs['size'] = long(reduce(operator_mul, kwargs['shape'], 1))
                
                kwargs.setdefault('dtype', dtype)
                
                if 'file' in kwargs:
                    f = kwargs['file']
                    if f == '':
                        kwargs['file'] = filename
                    else:
                        if base is not None:
                            f = pathjoin(base, f)
#                        kwargs['file'] = abspath(f)
                        kwargs['file'] = f
                else:
                    kwargs['file'] = filename
                
                if fmt == 'netCDF':                
                    partition.subarray = NetCDFFileArray(**kwargs)
                elif fmt == 'UM':
                    partition.subarray = UMFileArray(**kwargs)
            #--- End: if

            # Put the partition into the partition array 
            partition_matrix[index] = partition
        #--- End: for

        # Save the partition array
        self.partitions = partition_matrix

        if chunk:
            self.chunk()

        # ------------------------------------------------------------
        # Auxiliary mask
        # ------------------------------------------------------------
        _auxiliary_mask = d.get('_auxiliary_mask', None)
        if _auxiliary_mask:
            self._auxiliary_mask = [m.copy() for m in _auxiliary_mask]
        else:
            self._auxiliary_mask = None
    #--- End: def

    def ceil(self, i=False):
        '''Return the ceiling of the data array.

.. versionadded:: 1.0

.. seealso:: `floor`, `rint`, `trunc`

:Examples 1:

>>> e = d.ceil()

:Parameters:

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: `cf.Data`

:Examples 2:

>>> print d.array
[-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
>>> print d.ceil().array
[-1. -1. -1. -1.  0.  1.  2.  2.  2.]

        '''
        return self.func(numpy_ceil, out=True, i=i)
    #---End: def

    def _chunk_add_partitions(self, d, axes):
        '''
        '''
        for axis in axes[::-1]:
            extra_bounds = d.get(axis)
            
            if not extra_bounds:
                continue
            
            if axis not in self.partitions.axes:
                # Create a new partition axis
                self.partitions.expand_dims(axis, i=True)
                
            # Create the new partitions
            self.add_partitions(sorted(set(extra_bounds)), axis)

            # Update d in-place
            d[axis] = []
    #--- End: def

    def chunk(self, chunksize=None, total=None, omit_axes=None, pmshape=None):
        '''Partition the data array.

:Parameters:

    chunksize: `int`, optional
        The 

    total: sequence of `int`, optional

    omit_axes: sequence of `int`, optional

    pmshape: sequence of `int`, optional

:Returns:

    `None`

:Examples:

>>> d.chunk()
>>> d.chunk(100000)
>>> d.chunk(100000, )
>>> d.chunk(100000, total=[2])
>>> d.chunk(100000, omit_axes=[3, 4])

        '''
        if not chunksize:
            # Set the default chunk size
            chunksize = CHUNKSIZE()

        # Define the factor which, when multiplied by the size of a
        # partition, determines how many chunks are in the partition.
        factor = (self.dtype.itemsize + 1.0)/chunksize

        if not total and self._size*factor <= 1:
            # Don't do any partitioning if the data array is already
            # smaller than the chunk size. Note:
            # self._size*factor=(no. bytes in array)/(no. bytes in a
            # chunk)
            return

        # Initialise the dictionary relating each axis to new
        # partition boundaries for that axis.
        #
        # E.g. {'dim0': [], 'dim1': []}
        axes  = self._axes
        d = {}
        for axis in axes:
            d[axis] = []                   

        shape = self._shape
                        
        if total:
            if omit_axes:
                omit_axes = list(omit_axes)
            else:
                omit_axes = []

            for i in sorted(total):
                if i in omit_axes:
                    raise ValueError("asdasdas 089791728ey bn ")
                omit_axes.append(i)

                d[axes[i]] = range(1, shape[i])
            #--- End: for

            self._chunk_add_partitions(d, axes)                 
        #--- End: if

        if pmshape:
            if len(pmshape) != self._ndim:
                raise ValueError("Bad pmshape {}".format(pmshape))
            if self._pmsize > 1:
                raise ValueError(
"Can't set pmshape when there is more than one partition: {}".format(self._pmsize))

#            shape = self._shape
            for i, n_chunks in enumerate(pmshape):
                axis_size = shape[i] 

                if axis_size == 1:
                    if n_chunks != 1:
                        raise ValueError("Bad shape: {}".format(pmshape))
                    continue

                if n_chunks == 1:
                    continue

                axis = axes[i]
                
                step = int(axis_size/n_chunks)
                if step < 1:
                    raise ValueError("Bad shape: {}".format(pmshape))
                
                
                d[axis] = range(step, axis_size, step)

                if len(d[axis]) + 1 != n_chunks:
                    raise ValueError('asdasdasdasds {} {} : {}'.format( len(d[axis])+1, n_chunks, d[axis]))

                if n_chunks <= 1:
                    break
            #--- End: for

            self._chunk_add_partitions(d, axes)

            return
        #--- End: if
        
        # Still here?
        order = range(self._ndim)

        if omit_axes:
            # Do not chunk particular axes
            order = [i for i in order if i not in omit_axes]

        while order: # Only enter if there are axes to chunk

            (largest_partition_size, largest_partition) = sorted(
                [(partition.size, partition)
                 for partition in self.partitions.matrix.flat])[-1]
            
            # n_chunks = number of equal sized bits that the
            #            partition needs to be split up into so
            #            that each bit's size is less than the
            #            chunk size.
            n_chunks = int(largest_partition_size*factor + 0.5)

            if n_chunks <= 1:
                break

            # Loop round the master array axes in the order
            # specified. This order will be range(0, self.dim)
            # unless the total parameter has been set, in which
            # case the total axes will be looped through first.
            for i in order:
                axis_size = largest_partition.shape[i]
                if axis_size == 1: 
                    continue
                    
                axis = axes[i]
                
                location = largest_partition.location[i]
                
                if axis_size <= n_chunks:
                    d[axis] = range(location[0]+1, location[1])
                    n_chunks = int(math_ceil(float(n_chunks)/axis_size))    
                else:
                    step = int(axis_size/n_chunks)
                    d[axis] = range(location[0]+step, location[1], step)
                    break

                if n_chunks <= 1:
                    break
            #--- End: for

            self._chunk_add_partitions(d, axes)                 
        #--- End: while
        

#        # ------------------------------------------------------------        
#        # Find any new partition boundaries for each axis
#        # ------------------------------------------------------------
#        for indices in x:
#            for partition in self.partitions.matrix[indices].flat:
#                
#                # n_chunks = number of equal sized bits that the
#                #            partition needs to be split up into so
#                #            that each bit's size is less than the
#                #            chunk size.
#                n_chunks = int(partition.size*factor + 0.5)
#                
#                if not total and not pmshape and n_chunks <= 1:
#                    continue
#                
#                # Loop round the master array axes in the order
#                # specified. This order will be range(0, self.dim)
#                # unless the total parameter has been set, in which
#                # case the total axes will be looped through first.
#                for i in order:
#
#                    axis_size = partition.shape[i]
#                    if axis_size == 1: 
#                        if pmshape and pmshape[i] != 1:                          
#                            raise ValueError("Bad pmshape {}".format(pmshape))
#                        continue
#
#                    axis = axes[i]
#
#                    if pmshape:
#                        n_chunks = pmshape[i]
#                    elif total and i in total:
#                        # This axis has been flagged for maximal
#                        # partitioning
#                        if axis_size > n_chunks:
#                            n_chunks = axis_size
#
#                    if n_chunks <= 1:
#                        continue
#                    
#                    location = partition.location[i]
#
#                    if axis_size <= n_chunks:
#                        d[axis].extend(range(location[0]+1, location[1]))
#                        n_chunks = int(math_ceil(float(n_chunks)/axis_size))    
#                    else:
#                        step = int(axis_size/n_chunks)
#                        new_partition_boundaries = range(location[0]+step, location[1], step)
#                        d[axis].extend(new_partition_boundaries)
#
#                        if not pmshape:
#                            break
#                        elif len(new_partition_boundaries) + 1 != n_chunks:
#                            raise ValueError("Bad pmshape {}".format(pmshape))
#                #--- End: for                 
#            #--- End: for
#        #--- End: for
#
#        # ------------------------------------------------------------
#        # Create any new partition boundaries for each axis
#        # ------------------------------------------------------------
#        for axis in axes[::-1]:
#            extra_bounds = d.get(axis)
#
#            if extra_bounds is None:
#                continue
#            
#            if axis not in self.partitions.axes:
#                # Create a new partition axis
#                self.partitions.expand_dims(axis, i=True)
#
#            # Create the new partitions
#            self.add_partitions(sorted(set(extra_bounds)), axis)
#        #--- End: for

    #--- End: def

    def _asdatetime(self, i=False):
        '''

Change the internal representation of data array elements from numeric
reference times to datatime-like objects.

If the calendar has not been set then the default CF calendar will be
used and the units' and the `calendar` attribute will be updated
accordingly.

If the internal representations are already datatime-like objects then
no change occurs.

.. versionadded:: 1.3

.. seealso:: `_asreftime`, `_isdatetime`

:Examples 1:

>>> d._asdatetime()

:Parameters:

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: `cf.Data`

'''
        if i:
            d = self
        else:
            d = self.copy()

        units = self.Units
        
        if not units.isreftime:
            raise ValueError(
"Can't convert {!r} data to date-time objects".format(units))

        if d._isdatetime():
            return d

        config = d.partition_configuration(readonly=False, func=rt2dt, dtype=None)

        for partition in d.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            p_units = partition.Units
            partition.Units = Units(p_units.units, p_units._utime.calendar)
            partition.close()

        d.Units = Units(units.units, units._utime.calendar)
        
        d._dtype = array.dtype

        return d
    #--- End: def

    def _isdatetime(self):
        '''
        '''
        return self.dtype.kind == 'O' and self.Units.isreftime

    def _asreftime(self, i=False):
        '''

Change the internal representation of data array elements from
datatime-like objects to numeric reference times.

If the calendar has not been set then the default CF calendar will be
used and the units' and the `calendar` attribute will be updated
accordingly.

If the internal representations are already numeric reference times
then no change occurs.

.. versionadded:: 1.3

.. seealso:: `_asdatetime`, `_isdatetime`

:Parameters:

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: `cf.Data`

:Examples:

>>> d._asreftime()

'''
        if i:
            d = self
        else:
            d = self.copy()

        units = d.Units

        if not d._isdatetime():
            if units.isreftime:
                return d
            else:
                raise ValueError(
"Can't convert {!r} data to numeric reference times".format(units))
        #--- End: if

        config = d.partition_configuration(readonly=False, func=dt2rt, dtype=None)

        for partition in d.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            p_units = partition.Units
            partition.Units = Units(p_units.units, p_units._utime.calendar)
            partition.close()

        d.Units = Units(units.units, units._utime.calendar)
        
        d._dtype = array.dtype

        return d
    #--- End: def

    def _combined_units(self, data1, method, inplace):
        '''

:Parameters:

    data1 : cf.Data

    method : str
        The 

    inplace : bool

:Returns:

    out: `cf.Data`, `cf.Data`, `cf.Units`

:Examples:

>>> d._combined_units(e, '__sub__')
>>> d._combined_units(e, '__imul__')
>>> d._combined_units(e, '__irdiv__')
>>> d._combined_units(e, '__lt__')
>>> d._combined_units(e, '__rlshift__')
>>> d._combined_units(e, '__iand__')


'''
        method_type = method[-5:-2]

        data0 = self

        units0 = data0.Units
        units1 = data1.Units

        if not units0 and not units1:
            return data0, data1, units0

        if (units0.isreftime and units1.isreftime and
            not units0.equivalent(units1)):
            # Both are reference_time, but have non-equivalent
            # calendars
            if units0._calendar and not units1._calendar:
                data1 = data1._asdatetime()
                data1.override_units(units0, i=True)
                data1._asreftime(i=True)
                units1 = units0
            elif units1._calendar and not units0._calendar:
                if not inplace:
                    inplace = True
                    data0 = data0.copy()
                data0._asdatetime(i=True)
                data0.override_units(units1, i=True)
                data0._asreftime(i=True)
                units0 = units1
        #--- End: if

        if method_type in ('_eq', '_ne', '_lt', '_le', '_gt', '_ge'):
            #---------------------------------------------------------
            # Operator is one of ==, !=, >=, >, <=, <
            #---------------------------------------------------------
            if units0.equivalent(units1):
                # Units are equivalent
                if not units0.equals(units1):
                    data1 = data1.copy()
                    data1.Units = units0
                return data0, data1, _units_None
            elif not units1 or not units0:
                # At least one of the units is undefined
                return data0, data1, _units_None           
            else: 
                raise ValueError(
"Can't compare {0!r} to {1!r}".format(units0, units1))
        #--- End: if

        # still here?
        if method_type in ('and', '_or', 'ior', 'ror', 'xor', 'ift'):
            #---------------------------------------------------------
            # Operation is one of &, |, ^, >>, <<
            #---------------------------------------------------------
            if units0.equivalent(units1):
                # Units are equivalent
                if not units0.equals(units1):
                    data1 = data1.copy()
                    data1.Units = units0
                return data0, data1, units0
            elif not units1:
                # units1 is undefined
                return data0, data1, units0
            elif not units0:
                # units0 is undefined
                return data0, data1, units1
            else:   
                # Both units are defined and not equivalent
                raise ValueError(
"Can't operate with {} on data with {!r} to {!r}".format(method, units0, units1))
        #--- End: if

        # Still here?
        if units0.isreftime:
            #---------------------------------------------------------
            # units0 is reference time
            #---------------------------------------------------------
            if method_type == 'sub':
                if units1.isreftime:
                    if units0.equivalent(units1):
                        # Equivalent reference_times: the output units
                        # are time
                        if not units0.equals(units1):
                            data1 = data1.copy()
                            data1.Units = units0
                        return data0, data1, Units(_ut_unit=units0._ut_unit)
                    else:
                        # Non-equivalent reference_times: raise an
                        # exception
                        getattr(units0, method)(units1)
                elif units1.istime:
                    # reference_time minus time: the output units are
                    # reference_time
                    time0 = Units(_ut_unit=units0._ut_unit)
                    if not units1.equals(time0):
                        data1 = data1.copy()
                        data1.Units = time0
                    return data0, data1, units0
                elif not units1:
                    # reference_time minus no_units: the output units
                    # are reference_time
                    return data0, data1, units0 
#                elif units1.iscalendartime:
#                    # reference_time minus calendar_time: the output
#                    # units are reference_time
#                    return data0, data1, units0
                else:
                    # reference_time minus something not yet accounted
                    # for: raise an exception
                    getattr(units0, method)(units1)

            elif method_type == 'add':
                if units1.istime:
                    # reference_time plus regular_time: the output
                    # units are reference_time
                    time0 = Units(_ut_unit=units0._ut_unit)
                    if not units1.equals(time0):
                        data1 = data1.copy()
                        data1.Units = time0
                    return data0, data1, units0
                elif not units1:
                    # reference_time plus no_units: the output units
                    # are reference_time
                    return data0, data1, units0
#                elif units1.iscalendartime:
#                    # reference_time plus calendar_time: the output
#                    # units are reference_time
#                    return data0, data1, units0
                else:  
                    # reference_time plus something not yet accounted
                    # for: raise an exception
                    getattr(units0, method)(units1)

            else:
                # Raise an exception
                getattr(units0, method)(units1)

        elif units1.isreftime:
            #---------------------------------------------------------
            # units1 is reference time
            #---------------------------------------------------------
            if method_type == 'add':
                if units0.istime:
                    # Time plus reference_time: the output units are
                    # reference_time
                    time1 = Units(_ut_unit=units1._ut_unit)
                    if not units0.equals(time1):
                        if not inplace:
                            data0 = data0.copy()
                        data0.Units = time1
                    return data0, data1, units1
                elif not units0:
                    # No_units plus reference_time: the output units
                    # are reference_time
                    return data0, data1, units1
                else:
                    # Raise an exception
                    getattr(units0, method)(units1)
        #--- End: if

        # Still here?
        if method_type in ('mul', 'div'):
            #---------------------------------------------------------
            # Method is one of *, /, //
            #---------------------------------------------------------
            if not units1:
                # units1 is undefined
                return data0, data1, getattr(units0, method)(_units_1)
            elif not units0:
                # units0 is undefined
                return data0, data1, getattr(_units_1, method)(units1)
#            elif units0.equivalent(units1) and not units0.equals(units1):
#                # Both units are defined and equivalent but not equal
#                data1 = data1.copy()
#                data1.Units = units0
#                return data0, data1, getattr(units0, method)(units0)#  !!!!!!! units0*units0 YOWSER
            else:
                # Both units are defined (note: if the units are
                # noncombinable then this will raise an exception)
                return data0, data1, getattr(units0, method)(units1)
        #--- End: if

        # Still here?
        if method_type in ('sub', 'add', 'mod'):
            #---------------------------------------------------------
            # Operator is one of +, -
            #---------------------------------------------------------
            if units0.equivalent(units1):
                # Units are equivalent
                if not units0.equals(units1):
                    data1 = data1.copy()
                    data1.Units = units0
                return data0, data1, units0
            elif not units1:
                # units1 is undefined
                return data0, data1, units0
            elif not units0:
                # units0 is undefined
                return data0, data1, units1
            else:
                # Both units are defined and not equivalent (note: if
                # the units are noncombinable then this will raise an
                # exception)
                return data0, data1, getattr(units0, method)(units1)
        #--- End: if

        # Still here?
        if method_type == 'pow': 
            if method == '__rpow__':
                #-----------------------------------------------------
                # Operator is __rpow__
                #-----------------------------------------------------
                if not units1:
                    # units1 is undefined
                    if not units0:
                        # units0 is undefined
                        return data0, data1, _units_None
                    elif units0.isdimensionless:
                        # units0 is dimensionless
                        if not units0.equals(_units_1): 
                            if not inplace:
                                data0 = data0.copy()
                            data0.Units = _units_1

                        return data0, data1, _units_None
                elif units1.isdimensionless:
                    # units1 is dimensionless
                    if not units1.equals(_units_1): 
                        data1 = data1.copy()
                        data1.Units = _units_1

                    if not units0:
                        # units0 is undefined
                        return data0, data1, _units_1
                    elif units0.isdimensionless:
                        # units0 is dimensionless
                        if not units0.equals(_units_1): 
                            if not inplace:
                                data0 = data0.copy()
                            data0.Units = _units_1

                        return data0, data1, _units_1
                else:
                    # units1 is defined and is not dimensionless
                    if data0._size > 1:
                        raise ValueError("kkkkkkkkkjjjjjjjjjjjjjjjj")

                    if not units0:
                        # Check that the units are not shifted, as
                        # raising this to a power is a nonlinear
                        # operation
                        p = data0.datum(0)
                        if units0 != (units0**p)**(1.0/p):
                            raise ValueError(
"Can't raise shifted units {!r} to the power {}".format(units0, p))

                        return data0, data1, units1**p
                    elif units0.isdimensionless:
                        # units0 is dimensionless
                        if not units0.equals(_units_1): 
                            if not inplace:
                                data0 = data0.copy()
                            data0.Units = _units_1

                        # Check that the units are not shifted, as
                        # raising this to a power is a nonlinear
                        # operation
                        p = data0.datum(0)
                        if units0 != (units0**p)**(1.0/p):
                            raise ValueError(
"Can't raise shifted units {!r} to the power {}".format(units0, p))

                        return data0, data1, units1**p
                # --- End: if
                # This will deliberately raise an exception
                units1 ** units0
            else:
                #-----------------------------------------------------
                # Operator is __pow__
                #-----------------------------------------------------
                if not units0:
                    # units0 is undefined
                    if not units1:
                        # units0 is undefined
                        return data0, data1, _units_None
                    elif units1.isdimensionless:
                        # units0 is dimensionless
                        if not units1.equals(_units_1): 
                            data1 = data1.copy()
                            data1.Units = _units_1

                        return data0, data1, _units_None
                elif units0.isdimensionless:
                    # units0 is dimensionless
                    if not units0.equals(_units_1): 
                        if not inplace:
                            data0 = data0.copy()
                        data0.Units = _units_1

                    if not units1:
                        # units1 is undefined
                        return data0, data1, _units_1
                    elif units1.isdimensionless:
                        # units1 is dimensionless
                        if not units1.equals(_units_1): 
                            data1 = data1.copy()
                            data1.Units = _units_1

                        return data0, data1, _units_1
                else:
                    # units0 is defined and is not dimensionless
                    if data1._size > 1:
                        raise ValueError("kkkkkkkkkjjjjjjjjjjjjjjjj 8888888888888888")

                    if not units1:
                        # Check that the units are not shifted, as
                        # raising this to a power is a nonlinear
                        # operation
                        p = data1.datum(0)
                        if units0 != (units0**p)**(1.0/p):
                            raise ValueError(
"Can't raise shifted units {!r} to the power {}".format(units0, p))

                        return data0, data1, units0**p
                    elif units1.isdimensionless:
                        # units1 is dimensionless
                        if not units1.equals(_units_1): 
                            data1 = data1.copy()
                            data1.Units = _units_1

                        # Check that the units are not shifted, as
                        # raising this to a power is a nonlinear
                        # operation
                        p = data1.datum(0)
                        if units0 != (units0**p)**(1.0/p):
                            raise ValueError(
"Can't raise shifted units {!r} to the power {}".format(units0, p))
                        
                        return data0, data1, units0**p
                #--- End: if 
                # This will deliberately raise an exception
                units0 ** units1
            #--- End: if
        #--- End: if

        # Still here?
        raise ValueError(
            "Can't operate with {} on data with {!r} to {!r}".format(
                method, units0, units1))
    #--- End: def

    def _binary_operation(self, other, method):
        '''Implement binary arithmetic and comparison operations with the numpy
broadcasting rules.

It is called by the binary arithmetic and comparison
methods, such as `__sub__`, `__imul__`, `__rdiv__`, `__lt__`, etc.

.. seealso:: `_unary_operation`

:Parameters:

    other:
        The object on the right hand side of the operator.

    method: `str`
        The binary arithmetic or comparison method name (such as
        ``'__imul__'`` or ``'__ge__'``).

:Returns:

    new: `cf.Data`
        A new data object, or if the operation was in place, the same
        data object.

:Examples:

>>> d = cf.Data([0, 1, 2, 3])
>>> e = cf.Data([1, 1, 3, 4])

>>> f = d._binary_operation(e, '__add__')
>>> print f.array
[1 2 5 7]

>>> e = d._binary_operation(e, '__lt__')
>>> print e.array
[ True False  True  True]

>>> d._binary_operation(2, '__imul__')
>>> print d.array
[0 2 4 6]

        '''
        inplace      = (method[2] == 'i')
        method_type  = method[-5:-2]

        # ------------------------------------------------------------
        # Ensure that other is an independent Data object
        # ------------------------------------------------------------    
        if getattr(other, '_NotImplemented_RHS_Data_op', False):
            # Make sure that 
            return NotImplemented

        elif not isinstance(other, self.__class__):
            other = type(self).asdata(other)

#            if other._isdt and self.Units.isreftime:
#                # Make sure that an array of date-time objects has the
#                # right calendar.
#                other.override_units(self.Units, i=True)
#            if other._isdt and self.Units.isreftime:
#                # Make sure that an array of date-time objects has the
#                # right calendar.
#                other.override_units(self.Units, i=True)

        data0 = self.copy()

        data0, other, new_Units = data0._combined_units(other, method, True)

#        calendar_arithmetic = data0.Units.isreftime and other.Units.iscalendartime

        # ------------------------------------------------------------
        # Bring other into memory, if appropriate.
        # ------------------------------------------------------------
        other.to_memory()

        # ------------------------------------------------------------
        # Find which dimensions need to be broadcast in one or other
        # of the arrays.
        #
        # Method:
        #
        #   For each common dimension, the 'broadcast_indices' list
        #   will have a value of None if there is no broadcasting
        #   required (i.e. the two arrays have the same size along
        #   that dimension) or a value of slice(None) if broadcasting
        #   is required (i.e. the two arrays have the different sizes
        #   along that dimension and one of the sizes is 1).
        #   
        #   Example:
        #
        #     If c.shape is (7,1,6,1,5) and d.shape is (6,4,1) then
        #     broadcast_indices will be
        #     [None,slice(None),slice(None)].
        #   
        #     The indices to d which correspond to a partition of c,
        #     are the relevant subset of partition.indices updated
        #     with the non None elements of the broadcast_indices
        #     list.
        #   
        #     In this example, if a partition of c were to have a
        #     partition.indices value of (slice(0,3), slice(0,1),
        #     slice(2,4), slice(0,1), slice(0,5)), then the relevant
        #     subset of these is partition.indices[2:] and the
        #     corresponding indices to d are (slice(2,4), slice(None),
        #     slice(None))
        #
        # ------------------------------------------------------------
        data0_shape = data0._shape
        data1_shape = other._shape

        if data0_shape == data1_shape:
            # self and other have the same shapes
            broadcasting = False
            
            align_offset = 0
            ellipsis     = None

            new_shape = data0_shape
            new_ndim  = data0._ndim
            new_axes  = data0._axes
            new_size  = data0._size

        else:
            # self and other have different shapes
            broadcasting = True

            data0_ndim = data0._ndim
            data1_ndim = other._ndim

            align_offset = data0_ndim - data1_ndim
            if align_offset >= 0:
                # self has at least as many axes as other
                shape0 = data0_shape[align_offset:]
                shape1 = data1_shape

                new_shape = data0_shape[:align_offset]
                new_ndim  = data0_ndim
                new_axes  = data0._axes
            else:
                # other has more axes than self
                align_offset = -align_offset
                shape0       = data0_shape
                shape1       = data1_shape[align_offset:]

                new_shape = data1_shape[:align_offset]
                new_ndim  = data1_ndim
                if not data0_ndim:
                    new_axes = other._axes
                else:
                    new_axes = []
                    existing_axes = self._all_axis_names()
                    for n in new_shape:
                        axis = data0._new_axis_identifier(existing_axes)
                        existing_axes.append(axis)
                        new_axes.append(axis)
                    #--- End: for
                    new_axes += data0._axes
                #--- End: for
                     
                align_offset = 0
            #--- End: if

            broadcast_indices = []
            for a, b in izip(shape0, shape1):
                if a == b:
                    new_shape += (a,)
                    broadcast_indices.append(None)
                    continue
                
                # Still here?
                if a > 1 and b == 1:
                    new_shape += (a,)
                elif b > 1 and a == 1:
                    new_shape += (b,)
                else:
                    raise ValueError(
                        "Can't broadcast shape {} against shape {}".format(
                            data1_shape, data0_shape))
                
                broadcast_indices.append(slice(None))
            #--- End: for

            new_size = long(reduce(operator_mul, new_shape, 1))

            dummy_location = [None] * new_ndim
        #---End: if

        new_flip = []

#        if broadcasting:
#            max_size = 0
#            for partition in data0.partitions.matrix.flat:
#                indices0 = partition.indices
#                indices1 = tuple([
#                    (index if not broadcast_index else broadcast_index) 
#                    for index, broadcast_index in izip(
#                            indices0[align_offset:], broadcast_indices)
#                ])
#                indices1 = (Ellipsis,) + indices
#
#                shape0 = partition.shape
#                shape1 = [index.stop - index.start
#                          for index in parse_indices(other, indices1)]
#                
#                broadcast_size = 1
#                for n0, n1 in izip_longest(shape0[::-1], shape1[::-1], fillvalue=1):
#                    if n0 > 1:
#                        broadcast_size *= n0
#                    else:
#                        broadcast_size *= n1
#                #--- End: for
#
#                if broadcast_size > max_size:
#                    max_size = broadcast_size
#            #--- End: for
#
#            chunksize = CHUNKSIZE()
#            ffff = max_size*(new_dtype.itemsize + 1)
#            if ffff > chunksize:
#                data0.chunk(chunksize*(chunksize/ffff))
#        #--- End: if


        # ------------------------------------------------------------
        # Create a Data object which just contains the metadata for
        # the result. If we're doing a binary arithmetic operation
        # then result will get filled with data and returned. If we're
        # an augmented arithmetic assignment then we'll update self
        # with this new metadata.
        # ------------------------------------------------------------

        #if new_shape != data0_shape:
        #    set_location_map = True
        #    new_size = self._size
        #    dummy_location   = [None] * new_ndim
        #else:
        #    set_location_map = False
        #    new_size = long(reduce(mul, new_shape, 1))

#        if not set_location_map:
#            new_size = long(reduce(mul, new_shape, 1))
#        else:
#            new_size = self._size

        result        = data0.copy()
        result._shape = new_shape
        result._ndim  = new_ndim 
        result._size  = new_size 
        result._axes  = new_axes
#        result._flip  = new_flip

        # Is the result an array of date-time objects?
#        new_isdt = data0._isdt and new_Units.isreftime

        # ------------------------------------------------------------
        # Set the data type of the result
        # ------------------------------------------------------------
        if method_type in ('_eq', '_ne', '_lt', '_le', '_gt', '_ge'):
            new_dtype = numpy_dtype(bool)
            rtol = RTOL()
            atol = ATOL()
        else:
            if 'true' in method:
                new_dtype = numpy_dtype(float)
            elif not inplace:
                new_dtype = numpy_result_type(data0.dtype, other.dtype) 
            else:
                new_dtype = data0.dtype

        # ------------------------------------------------------------
        # Set flags to control whether or not the data of result and
        # self should be kept in memory
        # ------------------------------------------------------------
#        keep_result_in_memory = result.fits_in_memory(new_dtype.itemsize)
#        keep_self_in_memory   = data0.fits_in_memory(data0.dtype.itemsize)
#        if not inplace:
#            # When doing a binary arithmetic operation we need to
#            # decide whether or not to keep self's data in memory
#            revert_to_file = True
#            save_self      = not data0.fits_in_memory(data0.dtype.itemsize)
#            keep_self_in_memory = data0.fits_in_memory(data0.dtype.itemsize)
#        else:
#            # When doing an augmented arithmetic assignment we don't
#            # need to keep self's original data in memory
#            revert_to_file      = False
#            save_self           = False
#            keep_self_in_memory = True

#        dimensions     = self._axes
#        direction = self.direction
#        units     = self.Units

    
        config = data0.partition_configuration(readonly=not inplace)

#        print 'config[readonly] =', config['readonly']
        
        #        if calendar_arithmetic:
#            pda_args['func']   = rt2dt
#            pda_args['update'] = False
#            pda_args['dtype']  = None

        original_numpy_seterr = numpy_seterr(**_seterr)

# Think about dtype, here.

            
        for partition_r, partition_s in izip(result.partitions.matrix.flat,
                                             data0.partitions.matrix.flat):

            partition_s.open(config)
            
            indices = partition_s.indices

            array0  = partition_s.array

            if broadcasting:
                indices = tuple([
                        (index if not broadcast_index else broadcast_index) 
                        for index, broadcast_index in izip(
                            indices[align_offset:], broadcast_indices)
                        ])
                indices = (Ellipsis,) + indices

            array1 = other[indices].array
            
            # UNRESOLVED ISSUE: array1 could be much larger than the chunk size.

            if not inplace:
                partition = partition_r
                partition.update_inplace_from(partition_s)
            else:
                partition = partition_s

            # --------------------------------------------------------
            # Do the binary operation on this partition's data
            # --------------------------------------------------------
#            if calendar_arithmetic:
#                pass
#            else:

            try:
                if method == '__eq__': # and data0.Units.isreftime:
#                    array0 = numpy_isclose(array0, array1, rtol=rtol, atol=atol)
                    array0 = _numpy_isclose(array0, array1, rtol=rtol, atol=atol)
                elif method == '__ne__':
#                    array0 = ~numpy_isclose(array0, array1, rtol=rtol, atol=atol)
                    array0 = ~_numpy_isclose(array0, array1, rtol=rtol, atol=atol)
                else:
                    array0 = getattr(array0, method)(array1)    
#            try:
#                array0 = getattr(array0, method)(array1)
            except FloatingPointError as error:
                # Floating point point errors have been trapped
                if _mask_fpe[0]:
                    # Redo the calculation ignoring the errors and
                    # then set invalid numbers to missing data
                    numpy_seterr(**_seterr_raise_to_ignore)
                    array0 = getattr(array0, method)(array1)
                    array0 = numpy_ma_masked_invalid(array0, copy=False)
                    numpy_seterr(**_seterr) 
                else:
                    # Raise the floating point error exception
                    raise FloatingPointError(error)
            except TypeError as error:
                if inplace:
                    raise TypeError(
"Incompatible result data type ({0!r}) for in-place {1!r} arithmetic".format(
    numpy_result_type(array0.dtype, array1.dtype).name, array0.dtype.name))
                else:
                    raise TypeError(error)

            #--- End: try

            if array0 is NotImplemented:
                array0 = numpy_zeros(partition.shape, dtype=bool)
            elif not array0.ndim and not isinstance(array0, numpy_ndarray):
                array0 = numpy_asanyarray(array0)

            if not inplace:
                p_datatype = array0.dtype
                if new_dtype != p_datatype:
                    new_dtype = numpy_result_type(p_datatype, new_dtype)

            partition.subarray = array0
            partition.Units    = new_Units
            partition.axes     = new_axes
            partition.flip     = new_flip
            partition.part     = []

            if broadcasting:
                partition.location = dummy_location
                partition.shape    = list(array0.shape)

            partition._original      = None
            partition._write_to_disk = False
            partition.close()

            if not inplace:
                partition_s.close() 
        #--- End: for

        # Reset numpy.seterr
        numpy_seterr(**original_numpy_seterr)
            
        if not inplace:
            result._Units = new_Units
            result.dtype  = new_dtype
            result._flip  = new_flip

            if broadcasting:
                result.partitions.set_location_map(result._axes)

            return result
        else:
            # Update the metadata for the new master array in place
            data0._shape = new_shape
            data0._ndim  = new_ndim
            data0._size  = new_size
            data0._axes  = new_axes
            data0._flip  = new_flip
            data0._Units = new_Units
            data0.dtype  = new_dtype
   
            if broadcasting:
                data0.partitions.set_location_map(new_axes)

            self.__dict__ = data0.__dict__

            return self
    #--- End: def

    def _query_set(self, values, exact=True):
        '''
'''
        if not exact:
            raise ValueError("Can't, as yet, regex on non string")

        i = iter(values)
        v = i.next()

        out = (self == v)
        for v in i:
            out |= (self == v)
            
        return out

#        new = self.copy()
#        
#        pda_args = new.pda_args(revert_to_file=True)
#        
#        for partition in new.partitions.matrix.flat:
#            array = partition.dataarray(**pda_args)
#
#            i = iter(values)
#            value = i.next()
#            out = (array == value)
#            for value in i:
#                out |= (array == value)
#             
#            partition.subarray = out
#            partition.close()
#        #--- End: for
#
#        new.dtype = bool
#
#        return new
    #--- End: def

    def _query_contain(self, value):
        '''
'''
        return self == value
    #--- End: def 

    def _query_wi(self, value0, value1):
        '''
'''
        return (self >= value0) & (self <= value1)

#        new = self.copy()
#
#        pda_args = new.pda_args(revert_to_file=True)
#
#        for partition in new.partitions.matrix.flat:
#            array = partition.dataarray(**pda_args)                     
#            print array, new.Units, type(value0), value1
#            partition.subarray = (array >= value0) & (array <= value1)
#            partition.close()
#        #--- End: for
#
#        new.dtype = bool
#
#        return new
    #--- End: def

    def _query_wo(self, value0, value1):
        '''
'''
        return (self < value0) | (self > value1)
#        new = self.copy()
#
#        pda_args = new.pda_args(revert_to_file=True)
#
#        for partition in new.partitions.matrix.flat:
#            array = partition.dataarray(**pda_args)
#            partition.subarray = (array < value0) | (array > value1)
#            partition.close()
#        #--- End: for
#
#        new.dtype = bool
#
#        return new
    #--- End: def

    @classmethod
    def concatenate(cls, data, axis=0, _preserve=True):
        '''

Join a sequence of data arrays together.

:Parameters:

    data: sequence of cf.Data
        The data arrays to be concatenated. Concatenation is carried
        out in the order given. Each data array must have equivalent
        units and the same shape, except in the concatenation
        axis. Note that scalar arrays are treated as if they were one
        dimensionsal.

    axis: int, optional
        The axis along which the arrays will be joined. The default is
        0. Note that scalar arrays are treated as if they were one
        dimensionsal.

    _preserve: bool, optional 
        If False then the time taken to do the concatenation is
        reduced at the expense of changing the input data arrays given
        by the *data* parameter in place and **these in place changes
        will render the input data arrays unusable**. Therefore, only
        set to False if it is 100% certain that the input data arrays
        will not be accessed again. By default the input data arrays
        are preserved.

:Returns:

    out: cf.Data
        The concatenated data array.

:Examples:

>>> d = cf.Data([[1, 2], [3, 4]], 'km')
>>> e = cf.Data([[5.0, 6.0]], 'metre')
>>> f = cf.Data.concatenate((d, e))
>>> print f.array
[[ 1.     2.   ]
 [ 3.     4.   ]
 [ 0.005  0.006]]
>>> f.equals(cf.Data.concatenate((d, e), axis=-2))
True

>>> e = cf.Data([[5.0], [6.0]], 'metre')
>>> f = cf.Data.concatenate((d, e), axis=1)
>>> print f.array
[[ 1.     2.     0.005]
 [ 3.     4.     0.006]]

>>> d = cf.Data(1, 'km')
>>> e = cf.Data(50.0, 'metre')
>>> f = cf.Data.concatenate((d, e))
>>> print f.array
[ 1.    0.05]

>>> e = cf.Data([50.0, 75.0], 'metre')
>>> f = cf.Data.concatenate((d, e))
>>> print f.array
[ 1.     0.05   0.075]

'''  
        data = tuple(data)
        if len(data) < 2:
            raise ValueError(
                "Can't concatenate: Must provide at least two data arrays")
        
        data0 = data[0]
        data  = data[1:]

        if _preserve:
            data0 = data0.copy()
        else:
            # If data0 appears more than once in the input data arrays
            # then we need to copy it
            for d in data:
                if d is data0:
                    data0 = data0.copy()
                    break
        #--- End: if

        # Turn a scalar array into a 1-d array
        ndim = data0._ndim
        if not ndim:
            data0.expand_dims(i=True)
            ndim = 1

        # ------------------------------------------------------------
        # Check that the axis, shapes and units of all of the input
        # data arrays are consistent
        # ------------------------------------------------------------
        if axis < 0:
            axis += ndim
        if not 0 <= axis < ndim:
             raise ValueError(
                 "Can't concatenate: Invalid axis (expected %d <= axis < %d)" % 
                 (-ndim, ndim))

        shape0 = data0._shape
        units0 = data0.Units
        axis_p1 = axis + 1
        for data1 in data:
            shape1 = data1._shape
            if (shape0[axis_p1:] != shape1[axis_p1:] or
                shape0[:axis]    != shape1[:axis]):
                raise ValueError(
"Can't concatenate: All the input array axes except for the concatenation axis must have the same size")

            if not units0.equivalent(data1.Units):
                raise ValueError(
"Can't concatenate: All the input arrays must have equivalent units")
        #--- End: for
           
        for i, data1 in enumerate(data):
            if _preserve:
                data1 = data1.copy()
            else:
                # If data1 appears more than once in the input data
                # arrays then we need to copy it
                for d in data[i+1:]:
                    if d is data1:
                        data1 = data1.copy()
                        break
            #--- End: if

            # Turn a scalar array into a 1-d array
            if not data1._ndim:
                data1.expand_dims(i=True)

            shape1 = data1._shape

            # ------------------------------------------------------------
            # 1. Make sure that the internal names of the axes match
            # ------------------------------------------------------------
            axis_map = {}
            if data1._pmsize < data0._pmsize:
                for axis1, axis0 in izip(data1._axes, data0._axes):
                    axis_map[axis1] = axis0
                    
                data1._change_axis_names(axis_map)
            else:
                for axis1, axis0 in izip(data1._axes, data0._axes):
                    axis_map[axis0] = axis1
                    
                data0._change_axis_names(axis_map)
            #--- End: if

            # ------------------------------------------------------------
            # Find the internal name of the concatenation axis
            # ------------------------------------------------------------
            Paxis = data0._axes[axis]
            
            # ------------------------------------------------------------
            # 2. Make sure that the aggregating axis is an axis of the
            #    partition matrix of both arrays and that the partition
            #    matrix axes are the same in both arrays (although, for
            #    now, they may have different orders)
            #
            # Note:
            #
            # a) This may involve adding new partition matrix axes to
            #    either or both of data0 and data1.
            #            
            # b) If the aggregating axis needs to be added it is inserted
            #    as the outer (slowest varying) axis to reduce the
            #    likelihood of having to (expensively) transpose the
            #    partition matrix.
            # ------------------------------------------------------------
            for f, g in izip((data0, data1), 
                             (data1, data0)):
            
                g_pmaxes = g.partitions.axes
                if Paxis in g_pmaxes:
                    g_pmaxes = g_pmaxes[:]
                    g_pmaxes.remove(Paxis)
                    
                f_partitions = f.partitions
                f_pmaxes = f_partitions.axes
                for pmaxis in g_pmaxes[::-1] + [Paxis]:
                    if pmaxis not in f_pmaxes:
                        f_partitions.expand_dims(pmaxis, i=True)
            
#                if Paxis not in f_partitions.axes:
#                    f_partitions.expand_dims(Paxis, i=True)
            #--- End: for

            # ------------------------------------------------------------
            # 3. Make sure that aggregating axis is the outermost (slowest
            #    varying) axis of the partition matrix of data0
            # ------------------------------------------------------------
            ipmaxis = data0.partitions.axes.index(Paxis)
            if ipmaxis:
                data0.partitions.swapaxes(ipmaxis, 0, i=True)
                
            # ------------------------------------------------------------
            # 4. Make sure that the partition matrix axes of data1 are in
            #    the same order as those in data0
            # ------------------------------------------------------------
            pmaxes1 = data1.partitions.axes
            ipmaxes = [pmaxes1.index(pmaxis) for pmaxis in data0.partitions.axes]
            data1.partitions.transpose(ipmaxes, i=True)

            # --------------------------------------------------------
            # 5. Create new partition boundaries in the partition
            #    matrices of data0 and data1 so that their partition
            #    arrays may be considered as different slices of a
            #    common, larger hyperrectangular partition array.
            #
            # Note:
            # 
            # * There is no need to add any boundaries across the
            #   concatenation axis.
            # --------------------------------------------------------
            boundaries0 = data0.partition_boundaries()        
            boundaries1 = data1.partition_boundaries()

            for dim in data0.partitions.axes[1:]:
                
                # Still here? Then see if there are any partition matrix
                # boundaries to be created for this partition dimension
                bounds0 = boundaries0[dim]
                bounds1 = boundaries1[dim]
            
                symmetric_diff = set(bounds0).symmetric_difference(bounds1)
                if not symmetric_diff:
                    # The partition boundaries for this partition
                    # dimension are already the same in data0 and data1
                    continue
                
                # Still here? Then there are some partition boundaries to
                # be created for this partition dimension in data0 and/or
                # data1.
                for f, g, bf, bg in ((data0, data1, bounds0, bounds1), 
                                     (data1, data0, bounds1, bounds0)):
                    extra_bounds = [i for i in bg if i in symmetric_diff]
                    f.add_partitions(extra_bounds, dim)
                #--- End: for
            #--- End: for

            # ------------------------------------------------------------
            # 6. Concatenate data0 and data1 partition matrices
            # ------------------------------------------------------------
            if data0._flip != data1._flip:
                data0._move_flip_to_partitions()
                data1._move_flip_to_partitions()
            
            matrix0 = data0.partitions.matrix
            matrix1 = data1.partitions.matrix

            new_pmshape     = list(matrix0.shape)
            new_pmshape[0] += matrix1.shape[0]
            
            # Initialise an empty partition matrix with the new shape
            new_matrix = numpy_empty(new_pmshape, dtype=object)

            # Insert the data0 partition matrix
            new_matrix[:matrix0.shape[0]] = matrix0       

            # Insert the data1 partition matrix
            new_matrix[matrix0.shape[0]:] = matrix1

            data0.partitions.matrix = new_matrix
            
            # Update the location map of the partition matrix of data0
            data0.partitions.set_location_map((Paxis,), (axis,))

            # ------------------------------------------------------------
            # 7. Update the size, shape and dtype of data0
            # ------------------------------------------------------------
            original_shape0 = data0._shape
            
            data0._size += long(data1._size)
            
            shape0        = list(shape0)
            shape0[axis] += shape1[axis]
            data0._shape  = tuple(shape0)
            
            dtype0 = data0.dtype
            dtype1 = data1.dtype
            if dtype0 != dtype1:
                data0.dtype = numpy_result_type(dtype0, dtype1)

            # --------------------------------------------------------
            # 8. Concatenate the auxiliary mask
            # --------------------------------------------------------
            new_auxiliary_mask = []
            if data0._auxiliary_mask:
                # data0 has an auxiliary mask
                for mask in data0._auxiliary_mask:
                    size = mask.size
                    if ((size > 1 and mask.shape[axis] > 1) or
                        (size == 1 and mask.datum())):
                        new_shape = list(mask.shape)
                        new_shape[axis] = shape0[axis]
                        new_mask = cls.empty(new_shape, dtype=bool)
                        indices = [slice(None)] * new_mask.ndim

                        indices[axis] = slice(0, original_shape0[axis])
                        new_mask[tuple(indices)] = mask
 
                        indices[axis] = slice(original_shape0[axis], None)
                        new_mask[tuple(indices)] = False
                    else:
                        new_auxiliary_mask.append(mask)
                        
                    new_auxiliary_mask.append(new_mask)
                #--- End: for

            if data1._auxiliary_mask:
                # data1 has an auxiliary mask
                for mask in data1._auxiliary_mask:
                    size = mask.size
                    if ((size > 1 and mask.shape[axis] > 1) or
                        (size == 1 and mask.datum())):
                        new_shape = list(mask.shape)
                        new_shape[axis] = shape0[axis]
                        new_mask = cls.empty(new_shape, dtype=bool)
                        
                        indices = [slice(None)] * new_mask.ndim
                        
                        indices[axis] = slice(0, original_shape0[axis])
                        new_mask[tuple(indices)] = False
                        
                        indices[axis] = slice(original_shape0[axis], None)
                        new_mask[tuple(indices)] = mask
                    else:
                        new_auxiliary_mask.append(mask)
                        
                    new_auxiliary_mask.append(new_mask)
                #--- End: for
            #--- End: if
            
            if new_auxiliary_mask:
                data0._auxiliary_mask = new_auxiliary_mask
#                # Set the concatenated auxiliary mask
#                for mask in new_auxiliary_mask:
#                    data0._auxiliary_mask_add_component(mask)
        #--- End: for

        # ------------------------------------------------------------
        # Done
        # ------------------------------------------------------------
        return data0
    #--- End: def

    def concatenate2(self, data, axis=0, i=False, _preserve=True):
        '''

Join a sequence of data arrays together.

:Parameters:

    data : sequence of cf.Data
        The data arrays to be concatenated. Concatenation is carried
        out in the order given. Each data array must have equivalent
        units and the same shape, except in the concatenation
        axis. Note that scalar arrays are treated as if they were one
        dimensionsal.

    axis: `int`, optional
        The axis along which the arrays will be joined. The default is
        0. Note that scalar arrays are treated as if they were one
        dimensionsal.

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

    _preserve : bool, optional 
        If False then the time taken to do the concatenation is
        reduced at the expense of changing the input data arrays given
        by the *data* parameter in place and **these in place changes
        will render the input data arrays unusable**. Therefore, only
        set to False if it is 100% certain that the input data arrays
        will not be accessed again. By default the input data arrays
        are preserved.

:Returns:

    out: cf.Data
        The concatenated data array.

:Examples:

>>> d = cf.Data([[1, 2], [3, 4]], 'km')
>>> e = cf.Data([[5.0, 6.0]], 'metre')
>>> f = cf.Data.concatenate((d, e))
>>> print f.array
[[ 1.     2.   ]
 [ 3.     4.   ]
 [ 0.005  0.006]]
>>> f.equals(cf.Data.concatenate((d, e), axis=-2))
True

>>> e = cf.Data([[5.0], [6.0]], 'metre')
>>> f = cf.Data.concatenate((d, e), axis=1)
>>> print f.array
[[ 1.     2.     0.005]
 [ 3.     4.     0.006]]

>>> d = cf.Data(1, 'km')
>>> e = cf.Data(50.0, 'metre')
>>> f = cf.Data.concatenate((d, e))
>>> print f.array
[ 1.    0.05]

>>> e = cf.Data([50.0, 75.0], 'metre')
>>> f = cf.Data.concatenate((d, e))
>>> print f.array
[ 1.     0.05   0.075]

'''  
        data = tuple(data)
        if len(data) < 1:
            raise ValueError(
                "Can't concatenate: Must provide two or data arrays")
        
        data0 = self

        if _preserve:
            data0 = data0.copy()
        else:
            # If data0 appears more than once in the input data arrays
            # then we need to copy it
            for d in data:
                if d is data0:
                    data0 = data0.copy()
                    break
        #--- End: if

        # Turn a scalar array into a 1-d array
        ndim = data0._ndim
        if not ndim:
            data0.expand_dims(i=True)
            ndim = 1

        # ------------------------------------------------------------
        # Check that the axis, shapes and units of all of the input
        # data arrays are consistent
        # ------------------------------------------------------------
        if axis < 0:
            axis += ndim
        if not 0 <= axis < ndim:
             raise ValueError(
                 "Can't concatenate: Invalid axis (expected %d <= axis < %d)" % 
                 (-ndim, ndim))

        shape0 = data0._shape
        units0 = data0.Units
        axis_p1 = axis + 1
        for data1 in data:
            shape1 = data1._shape
            if (shape0[axis_p1:] != shape1[axis_p1:] or
                shape0[:axis]    != shape1[:axis]):
                raise ValueError(
"Can't concatenate: All the input array axes except for the concatenation axis must have the same size")

            if not units0.equivalent(data1.Units):
                raise ValueError(
"Can't concatenate: All the input arrays must have equivalent units")
        #--- End: for
           
        for i, data1 in enumerate(data):
            if _preserve:
                data1 = data1.copy()
            else:
                # If data1 appears more than once in the input data
                # arrays then we need to copy it
                for d in data[i+1:]:
                    if d is data1:
                        data1 = data1.copy()
                        break
            #--- End: if

            # Turn a scalar array into a 1-d array
            if not data1._ndim:
                data1.expand_dims(i=True)

            shape1 = data1._shape

            # ------------------------------------------------------------
            # 1. Make sure that the internal names of the axes match
            # ------------------------------------------------------------
            axis_map = {}
            if data1._pmsize < data0._pmsize:
                for axis1, axis0 in izip(data1._axes, data0._axes):
                    axis_map[axis1] = axis0
                    
                data1._change_axis_names(axis_map)
            else:
                for axis1, axis0 in izip(data1._axes, data0._axes):
                    axis_map[axis0] = axis1
                    
                data0._change_axis_names(axis_map)
            #--- End: if
            
            # ------------------------------------------------------------
            # Find the internal name of the concatenation axis
            # ------------------------------------------------------------
            Paxis = data0._axes[axis]
            
            # ------------------------------------------------------------
            # 2. Make sure that the aggregating axis is an axis of the
            #    partition matrix of both arrays and that the partition
            #    matrix axes are the same in both arrays (although, for
            #    now, they may have different orders)
            #
            # Note:
            #
            # a) This may involve adding new partition matrix axes to
            #    either or both of data0 and data1.
            #            
            # b) If the aggregating axis needs to be added it is inserted
            #    as the outer (slowest varying) axis to reduce the
            #    likelihood of having to (expensively) transpose the
            #    partition matrix.
            # ------------------------------------------------------------
            for f, g in izip((data0, data1), 
                             (data1, data0)):
            
                g_pmaxes = g.partitions.axes
                if Paxis in g_pmaxes:
                    g_pmaxes = g_pmaxes[:]
                    g_pmaxes.remove(Paxis)
                    
                f_partitions = f.partitions
                f_pmaxes = f_partitions.axes
                for pmaxis in g_pmaxes[::-1] + [Paxis]:
                    if pmaxis not in f_pmaxes:
                        f_partitions.expand_dims(pmaxis, i=True)
            
#                if Paxis not in f_partitions.axes:
#                    f_partitions.expand_dims(Paxis, i=True)
            #--- End: for
            
            # ------------------------------------------------------------
            # 3. Make sure that aggregating axis is the outermost (slowest
            #    varying) axis of the partition matrix of data0
            # ------------------------------------------------------------
            ipmaxis = data0.partitions.axes.index(Paxis)
            if ipmaxis:
                data0.partitions.swapaxes(ipmaxis, 0, i=True)
                
            # ------------------------------------------------------------
            # 4. Make sure that the partition matrix axes of data1 are in
            #    the same order as those in data0
            # ------------------------------------------------------------
            pmaxes1 = data1.partitions.axes
            ipmaxes = [pmaxes1.index(pmaxis) for pmaxis in data0.partitions.axes]
            data1.partitions.transpose(ipmaxes, i=True)
                
            # ------------------------------------------------------------
            # 5. Create new partition boundaries in the partition
            #    matrices of data0 and data1 so that their partition
            #    arrays may be considered as different slices of a common,
            #    larger hyperrectangular partition array.
            #
            # Note:
            # 
            # * There is no need to add any boundaries across the
            #   concatenation axis.
            # ------------------------------------------------------------
            boundaries0 = data0.partition_boundaries()        
            boundaries1 = data1.partition_boundaries()

            for dim in data0.partitions.axes[1:]:
                
                # Still here? Then see if there are any partition matrix
                # boundaries to be created for this partition dimension
                bounds0 = boundaries0[dim]
                bounds1 = boundaries1[dim]
            
                symmetric_diff = set(bounds0).symmetric_difference(bounds1)
                if not symmetric_diff:
                    # The partition boundaries for this partition
                    # dimension are already the same in data0 and data1
                    continue
                
                # Still here? Then there are some partition boundaries to
                # be created for this partition dimension in data0 and/or
                # data1.
                for f, g, bf, bg in ((data0, data1, bounds0, bounds1), 
                                     (data1, data0, bounds1, bounds0)):
                    extra_bounds = [i for i in bg if i in symmetric_diff]
                    f.add_partitions(extra_bounds, dim)
                #--- End: for
            #--- End: for

            # ------------------------------------------------------------
            # 6. Concatenate data0 and data1 partition matrices
            # ------------------------------------------------------------
            if data0._flip != data1._flip:
                data0._move_flip_to_partitions()
                data1._move_flip_to_partitions()
            
            matrix0 = data0.partitions.matrix
            matrix1 = data1.partitions.matrix
            
            new_pmshape     = list(matrix0.shape)
            new_pmshape[0] += matrix1.shape[0]
            
            # Initialise an empty partition matrix with the new shape
            new_matrix = numpy_empty(new_pmshape, dtype=object)
            
            # Insert the data0 partition matrix
            new_matrix[:matrix0.shape[0]] = matrix0       
                
            # Insert the data1 partition matrix
            new_matrix[matrix0.shape[0]:] = matrix1
            
            data0.partitions.matrix = new_matrix
            
            # Update the location map of the partition matrix of data0
            data0.partitions.set_location_map((Paxis,), (axis,))
            
            # ------------------------------------------------------------
            # 7. Update the size, shape and dtype of data0
            # ------------------------------------------------------------
            data0._size += long(data1._size)
            
            shape0        = list(shape0)
            shape0[axis] += shape1[axis]
            data0._shape  = tuple(shape0)
            
            dtype0 = data0.dtype
            dtype1 = data1.dtype
            if dtype0 != dtype1:
                data0.dtype = numpy_result_type(dtype0, dtype1)        
        #--- End: for

        # ------------------------------------------------------------
        # Done
        # ------------------------------------------------------------
        return data0
    #--- End: def

    def _move_flip_to_partitions(self):
        '''

This does not change the master array.

'''
        flip = self._flip
        if not flip:
            return
        
        for partition in self.partitions.matrix.flat:
            p_axes = partition.axes
            p_flip = partition.flip[:]
            for axis in flip:
                if axis in p_flip:
                    p_flip.remove(axis)
                elif axis in p_axes:
                    p_flip.append(axis)
            #--- End: for
            partition.flip = p_flip
        #--- End: for

        self._flip = []
    #--- End: def

    def _parse_axes(self, axes, method):
        '''
        
:Parameters:

    axes : (sequence of) int
        The axes of the data array. May be one of, or a sequence of
        any combination of zero or more of:

            * The integer position of a dimension in the data array
              (negative indices allowed).

    method : str

:Returns:

    out: list

:Examples:

'''
        ndim = self._ndim

        if isinstance(axes, (int, long)):
            axes = (axes,)
            
        axes2 = []
        for axis in axes:
            if 0 <= axis < ndim:
                axes2.append(axis)
            elif -ndim <= axis < 0:
                axes2.append(axis + ndim)
            else:
                raise ValueError(
                    "Can't {}: Invalid axis: {!r}".format(method, axis))
        #--- End: for
            
        # Check for duplicate axes
        n = len(axes2)
        if n > 1 and n > len(set(axes2)):
            raise ValueError("Can't {}: Duplicate axis: {}".format(
                method, axes2))            
        
        return axes2
    #--- End: def

    def _unary_operation(self, operation):
        '''

Implement unary arithmetic operations.

It is called by the unary arithmetic methods, such as
__abs__().

.. seealso:: `_binary_operation`

:Parameters:

    operation : str
        The unary arithmetic method name (such as "__invert__").

:Returns:

    new : Data
        A new Data array.

:Examples:

>>> d = cf.Data([[1, 2, -3, -4, -5]])

>>> e = d._unary_operation('__abs__')
>>> print e.array
[[1 2 3 4 5]]

>>> e = d.__abs__()
>>> print e.array
[[1 2 3 4 5]]

>>> e = abs(d)
>>> print e.array
[[1 2 3 4 5]]

'''
        self.to_memory()

        new = self.copy()

        config = new.partition_configuration(readonly=True)

        for partition in new.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            partition.subarray = getattr(operator, operation)(array)
            partition.close()
        #--- End: for

        return new
    #--- End: def

    def __add__(self, other):
        '''

The binary arithmetic operation ``+``

x.__add__(y) <==> x+y

'''
        return self._binary_operation(other, '__add__')
    #--- End: def

    def __iadd__(self, other):
        '''

The augmented arithmetic assignment ``+=``

x.__iadd__(y) <==> x+=y

'''
        return self._binary_operation(other, '__iadd__')
    #--- End: def

    def __radd__(self, other):
        '''

The binary arithmetic operation ``+`` with reflected operands

x.__radd__(y) <==> y+x

'''
        return self._binary_operation(other, '__radd__')
    #--- End: def

    def __sub__(self, other):
        '''

The binary arithmetic operation ``-``

x.__sub__(y) <==> x-y

'''
        return self._binary_operation(other, '__sub__')
    #--- End: def

    def __isub__(self, other):
        '''

The augmented arithmetic assignment ``-=``

x.__isub__(y) <==> x-=y

'''
        return self._binary_operation(other, '__isub__')
    #--- End: def

    def __rsub__(self, other):
        '''

The binary arithmetic operation ``-`` with reflected operands

x.__rsub__(y) <==> y-x

'''
        return self._binary_operation(other, '__rsub__')
    #--- End: def

    def __mul__(self, other):
        '''

The binary arithmetic operation ``*``

x.__mul__(y) <==> x*y

'''
        return self._binary_operation(other, '__mul__')
    #--- End: def

    def __imul__(self, other):
        '''

The augmented arithmetic assignment ``*=``

x.__imul__(y) <==> x*=y

'''
        return self._binary_operation(other, '__imul__')
    #--- End: def

    def __rmul__(self, other):
        '''

The binary arithmetic operation ``*`` with reflected operands

x.__rmul__(y) <==> y*x

'''
        return self._binary_operation(other, '__rmul__')
    #--- End: def

    def __div__(self, other):
        '''

The binary arithmetic operation ``/``

x.__div__(y) <==> x/y

'''
        return self._binary_operation(other, '__div__')
    #--- End: def

    def __idiv__(self, other):
        '''

The augmented arithmetic assignment ``/=``

x.__idiv__(y) <==> x/=y

'''
        return self._binary_operation(other, '__idiv__')
    #--- End: def

    def __rdiv__(self, other):
        '''

The binary arithmetic operation ``/`` with reflected operands

x.__rdiv__(y) <==> y/x

'''
        return self._binary_operation(other, '__rdiv__')
    #--- End: def

    def __floordiv__(self, other):
        '''

The binary arithmetic operation ``//``

x.__floordiv__(y) <==> x//y

'''
        return self._binary_operation(other, '__floordiv__')
    #--- End: def

    def __ifloordiv__(self, other):
        '''

The augmented arithmetic assignment ``//=``

x.__ifloordiv__(y) <==> x//=y

'''
        return self._binary_operation(other, '__ifloordiv__')
    #--- End: def

    def __rfloordiv__(self, other):
        '''

The binary arithmetic operation ``//`` with reflected operands

x.__rfloordiv__(y) <==> y//x

'''
        return self._binary_operation(other, '__rfloordiv__')
    #--- End: def

    def __truediv__(self, other):
        '''

The binary arithmetic operation ``/`` (true division)

x.__truediv__(y) <==> x/y

'''
        return self._binary_operation(other, '__truediv__')
    #--- End: def

    def __itruediv__(self, other):
        '''

The augmented arithmetic assignment ``/=`` (true division)

x.__itruediv__(y) <==> x/=y

'''
        return self._binary_operation(other, '__itruediv__')
   #--- End: def

    def __rtruediv__(self, other):
        '''

The binary arithmetic operation ``/`` (true division) with reflected
operands

x.__rtruediv__(y) <==> y/x

'''
        return self._binary_operation(other, '__rtruediv__')
    #--- End: def

    def __pow__(self, other, modulo=None):
        '''

The binary arithmetic operations ``**`` and ``pow``

x.__pow__(y) <==> x**y

'''  
        if modulo is not None:
            raise NotImplementedError(
"3-argument power not supported for {!r}".format(self.__class__.__name__))
                
        return self._binary_operation(other, '__pow__')
    #--- End: def

    def __ipow__(self, other, modulo=None):
        '''

The augmented arithmetic assignment ``**=``

x.__ipow__(y) <==> x**=y

'''  
        if modulo is not None:
            raise NotImplementedError(
"3-argument power not supported for {!r}".format(self.__class__.__name__))

        return self._binary_operation(other, '__ipow__')
    #--- End: def

    def __rpow__(self, other, modulo=None):
        '''

The binary arithmetic operations ``**`` and ``pow`` with reflected
operands

x.__rpow__(y) <==> y**x

'''  
        if modulo is not None:
            raise NotImplementedError(
"3-argument power not supported for {!r}".format(self.__class__.__name__))

        return self._binary_operation(other, '__rpow__')
    #--- End: def

    def __mod__(self, other):
        '''

The binary arithmetic operation ``%``

x.__mod__(y) <==> x % y

'''
        return self._binary_operation(other, '__mod__')
    #--- End: def

    def __imod__(self, other):
        '''

The binary arithmetic operation ``%=``

x.__imod__(y) <==> x %= y

'''
        return self._binary_operation(other, '__imod__')
    #--- End: def

    def __rmod__(self, other):
        '''

The binary arithmetic operation ``%`` with reflected operands

x.__rmod__(y) <==> y % x

'''
        return self._binary_operation(other, '__rmod__')
    #--- End: def

    def __eq__(self, other):
        '''

The rich comparison operator ``==``

x.__eq__(y) <==> x==y

'''
        return self._binary_operation(other, '__eq__')
    #--- End: def

    def __ne__(self, other):
        '''

The rich comparison operator ``!=``

x.__ne__(y) <==> x!=y

'''
        return self._binary_operation(other, '__ne__')
    #--- End: def

    def __ge__(self, other):
        '''

The rich comparison operator ``>=``

x.__ge__(y) <==> x>=y

'''
        return self._binary_operation(other, '__ge__')
    #--- End: def

    def __gt__(self, other):
        '''

The rich comparison operator ``>``

x.__gt__(y) <==> x>y

'''
        return self._binary_operation(other, '__gt__')
    #--- End: def

    def __le__(self, other):
        '''

The rich comparison operator ``<=``

x.__le__(y) <==> x<=y

'''
        return self._binary_operation(other, '__le__')
    #--- End: def

    def __lt__(self, other):
        '''

The rich comparison operator ``<``

x.__lt__(y) <==> x<y

'''
        return self._binary_operation(other, '__lt__')
    #--- End: def

    def __and__(self, other):
        '''

The binary bitwise operation ``&``

x.__and__(y) <==> x&y

'''
        return self._binary_operation(other, '__and__')
    #--- End: def

    def __iand__(self, other):
        '''

The augmented bitwise assignment ``&=``

x.__iand__(y) <==> x&=y

'''
        return self._binary_operation(other, '__iand__')
    #--- End: def

    def __rand__(self, other):
        '''

The binary bitwise operation ``&`` with reflected operands

x.__rand__(y) <==> y&x

'''
        return self._binary_operation(other, '__rand__')
    #--- End: def

    def __or__(self, other):
        '''

The binary bitwise operation ``|``

x.__or__(y) <==> x|y

'''
        return self._binary_operation(other, '__or__')
    #--- End: def

    def __ior__(self, other):
        '''

The augmented bitwise assignment ``|=``

x.__ior__(y) <==> x|=y

'''
        return self._binary_operation(other, '__ior__')
    #--- End: def

    def __ror__(self, other):
        '''

The binary bitwise operation ``|`` with reflected operands

x.__ror__(y) <==> y|x

'''
        return self._binary_operation(other, '__ror__')
    #--- End: def

    def __xor__(self, other):
        '''

The binary bitwise operation ``^``

x.__xor__(y) <==> x^y

'''
        return self._binary_operation(other, '__xor__')
    #--- End: def

    def __ixor__(self, other):
        '''

The augmented bitwise assignment ``^=``

x.__ixor__(y) <==> x^=y

'''
        return self._binary_operation(other, '__ixor__')
    #--- End: def

    def __rxor__(self, other):
        '''

The binary bitwise operation ``^`` with reflected operands

x.__rxor__(y) <==> y^x

'''
        return self._binary_operation(other, '__rxor__')
    #--- End: def

    def __lshift__(self, y):
        '''

The binary bitwise operation ``<<``

x.__lshift__(y) <==> x<<y

'''
        return self._binary_operation(y, '__lshift__')
    #--- End: def

    def __ilshift__(self, y):
        '''

The augmented bitwise assignment ``<<=``

x.__ilshift__(y) <==> x<<=y

'''
        return self._binary_operation(y, '__ilshift__')
    #--- End: def

    def __rlshift__(self, y):
        '''

The binary bitwise operation ``<<`` with reflected operands

x.__rlshift__(y) <==> y<<x

'''
        return self._binary_operation(y, '__rlshift__')
    #--- End: def

    def __rshift__(self, y):
        '''

The binary bitwise operation ``>>``

x.__lshift__(y) <==> x>>y

'''
        return self._binary_operation(y, '__rshift__')
    #--- End: def

    def __irshift__(self, y):
        '''

The augmented bitwise assignment ``>>=``

x.__irshift__(y) <==> x>>=y

'''
        return self._binary_operation(y, '__irshift__')
    #--- End: def

    def __rrshift__(self, y):
        '''

The binary bitwise operation ``>>`` with reflected operands

x.__rrshift__(y) <==> y>>x

'''
        return self._binary_operation(y, '__rrshift__')
    #--- End: def

    def __abs__(self):
        '''

The unary arithmetic operation ``abs``

x.__abs__() <==> abs(x)

'''
        return self._unary_operation('__abs__')
    #--- End: def

    def __neg__(self):
        '''

The unary arithmetic operation ``-``

x.__neg__() <==> -x

'''
        return self._unary_operation('__neg__')
    #--- End: def

    def __invert__(self):
        '''

The unary bitwise operation ``~``

x.__invert__() <==> ~x

'''
        return self._unary_operation('__invert__')
    #--- End: def

    def __pos__(self):
        '''

The unary arithmetic operation ``+``

x.__pos__() <==> +x

'''
        return self._unary_operation('__pos__')
    #--- End: def

    def _all_axis_names(self):
        '''

Return a set of all the dimension names in use by the data array.

Note that the output set includes dimensions of individual partitions
which are not dimensions of the master data array.

:Returns:

    out: list of str
        The axis names.

:Examples:

>>> d._axes
['dim1', 'dim0']
>>> d.partitions.info('_dimensions')
[['dim0', 'dim0'],
 ['dim1', 'dim0', 'dim2']]
>>> d._all_axis_names()
set(['dim2', dim0', 'dim1'])

'''
        all_axes = self._all_axes
        if not all_axes:
            return self._axes[:]
        else:
            return list(all_axes)
    #--- End: def

    def _change_axis_names(self, axis_map):
        '''

Change the axis names.

The axis names are arbitrary, so mapping them to another arbitrary
collection does not change the data array values, units, nor axis
order.

:Examples:

'''       
        # Find any axis names which are not mapped. If there are any,
        # then update axis_map.
        all_axes = self._all_axes
        if all_axes:
            d = set(all_axes).difference(axis_map)
            if d:
                axis_map = axis_map.copy()
                existing_axes = all_axes[:] 
                for axis in d:
                    if axis in axis_map.itervalues():
                        axis_map[axis] = self._new_axis_identifier(existing_axes)
                        existing_axes.append(axis)
                    else:
                        axis_map[axis] = axis
                #--- End: for
        #--- End: if

        if all([axis0==axis1 for axis0, axis1 in axis_map.iteritems()]):
            # Return without doing anything if the mapping is null
            return
        
        # Axes
        self._axes = [axis_map[axis] for axis in self._axes]

        # All axes
        if all_axes:
            self._all_axes = tuple([axis_map[axis] for axis in all_axes])
 
        # Flipped axes       
        flip = self._flip
        if flip:
            self._flip = [axis_map[axis] for axis in flip]

        # HDF chunks
        chunks = self._HDF_chunks
        if chunks:
            self._HDF_chunks = dict([(axis_map[axis], size)
                                     for axis, size in chunks.iteritems()])

        # Partitions in the partition matrix
        self.partitions.change_axis_names(axis_map)
    #--- End: def

    def _collapse(self, func, fpartial, ffinalise, axes=None,
                  squeeze=False, weights=None, mtol=1, units=None,
                  i=False, _preserve_partitions=False, **kwargs):
        '''Collapse the data array in place.

:Parameters:

    func: function

    fpartial: function

    ffinalize: function

    axes: (sequence of) `int`, optional
        The axes to be collapsed. By default flattened input is
        used. Each axis is identified by its integer position. No axes
        are collapsed if *axes* is an empty sequence.

    squeeze: `bool`, optional
        If False then the axes which are collapsed are left in the
        result as axes with size 1. In this case the result will
        broadcast correctly against the original array. By default
        collapsed axes are removed.

    weights: *optional*

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.
   
    _preserve_partitions: `bool`, optional
        If True then preserve the shape of the partition matrix of the
        input data, at the expense of a much slower execution. By
        default, the partition matrix may be reduced (using `varray`)
        to considerably speed things up.

    kwargs: *optional*

:Returns:

    out: `cf.Data`

        '''     
        if i:
            d = self
        else:
            d = self.copy()

        ndim = d._ndim
        self_axes  = d._axes
        self_shape = d._shape        

        original_self_axes = self_axes[:]

        if axes is None:
            # Collapse all axes
            axes = range(ndim)
            n_collapse_axes     = ndim
            n_non_collapse_axes = 0
            Nmax = d._size
        elif not axes and axes != 0:
            # Collapse no axes
            return d
        else:
            # Collapse some (maybe all) axes
            axes = sorted(d._parse_axes(axes, '_collapse'))
            n_collapse_axes     = len(axes)
            n_non_collapse_axes = ndim - n_collapse_axes 
            Nmax = 1
            for i in axes:
                Nmax *= self_shape[i]
        #--- End: if
            
        #-------------------------------------------------------------
        # Parse the weights.
        #
        # * Change the keys from dimension names to the integer
        #   positions of the dimensions.
        #
        # * Make sure all non-null weights are Data objects.
        # ------------------------------------------------------------
        if weights is not None:
            if not isinstance(weights, dict):
                # If the shape of the weights is not the same as the
                # shape of the data array then the weights are assumed
                # to span the collapse axes in the order in which they
                # are given
                if numpy_shape(weights) == self_shape:
                    weights = {tuple(self_axes): weights}
                else:
                    weights = {tuple([self_axes[i] for i in axes]): weights}

            else:
                weights = weights.copy()
                weights_axes = set()
                for key, value in weights.items():
                    del weights[key]
                    key = d._parse_axes(key, 'asdasds12983487')
                    if weights_axes.intersection(key):
                        raise ValueError("Duplicate weights axis")
                    
                    weights_axes.update(key)
                    weights[tuple([self_axes[i] for i in key])] = value
                #--- End: for

                if not weights_axes.intersection(axes):
                    # Ignore all of the weights if none of them span
                    # any collapse axes
                    weights = {}
            #--- End: if

            for key, weight in weights.items():
                if weight is None or numpy_size(weight) == 1:
                    # Ignore undefined weights and size 1 weights
                    del weights[key]
                    continue

                weight_ndim = numpy_ndim(weight)
                if weight_ndim != len(key):
                    raise ValueError(
"Can't collapse: Incorrect number of weights axes (%d != %d)" %
(weight.ndim, len(key)))
                
                if weight_ndim > ndim:
                    raise ValueError(
"Can't collapse: Incorrect number of weights axes (%d > %d)" %
(weight.ndim, ndim))
                
                for n, axis in izip(numpy_shape(weight), key):
                    if n != self_shape[self_axes.index(axis)]:
                        raise ValueError(
"Can't collapse: Incorrect weights shape {!r}".format(numpy_shape(weight)))
                #--- End :for

                # Convert weight to a data object, if necessary.
                weight = type(self).asdata(weight)

                if weight.dtype.char == 'S':
                    # Ignore string-valued weights
                    del weights[key]
                    continue

                weights[key] = weight
            #--- End: for
        #--- End: if

        if axes != range(n_non_collapse_axes, ndim):
            transpose_iaxes = [i for i in range(ndim) if i not in axes] + axes
            d.transpose(transpose_iaxes, i=True)

        if weights:
            # Optimize when weights span only non-partitioned axes
            # (do this before permuting the order of the weight
            # axes to be consistent with the order of the data
            # axes)
            weights = d._collapse_optimize_weights(weights)

            # Permute the order of the weight axes to be
            # consistent with the order of the data axes
            self_axes = d._axes              
            for key, w in weights.items():
                key1 = tuple([axis for axis in self_axes if axis in key])
                
                if key1 != key:
                    w = w.transpose([key.index(axis) for axis in key1])

                del weights[key]
                ikey = tuple([self_axes.index(axis) for axis in key1])

                weights[ikey] = w
            #--- End: for
                    
            # Add the weights to kwargs
            kwargs['weights'] = weights
        #--- End: if

        # If the input data array 'fits' in one chunk of memory, then
        # make sure that it has only one partition
        if (not mpi_on and not _preserve_partitions and d._pmndim and
            d.fits_in_one_chunk_in_memory(d.dtype.itemsize)):
            d.varray

        #-------------------------------------------------------------
        # Initialise the output data array
        #-------------------------------------------------------------
        new = d[(Ellipsis,) + (0,)*n_collapse_axes]
        
        new._auxiliary_mask = None
        for partition in new.partitions.matrix.flat:
            # Do this so as not to upset the ref count on the
            # parittion's of d
            del partition.subarray
    
        #d.to_memory()
        
#        save = not new.fits_in_memory(new.dtype.itemsize)
        keep_in_memory = new.fits_in_memory(new.dtype.itemsize)

        datatype = d.dtype
    
        if units is None:
            new_units = new.Units
        else:
            new_units = units

        p_axes  = new._axes[:n_non_collapse_axes]
        p_units = new_units
    
        c_slice = (slice(None),) * n_collapse_axes

        config = new.partition_configuration(readonly=False,
                                             auxiliary_mask=None, # DCH ??x
                                             extra_memory=False)

        if mpi_on:
            mode = COLLAPSE_PARALLEL_MODE()
            if mode == 0:
                # Calculate the number of partitions in each subspace,
                # assuming this will always be the same in each one and
                # compare to the number of partitions in the new partition
                # matrix times the maximum number of partitions per process in
                # each case. The latter is calculated by
                # _flag_partitions_for_processing
                new._flag_partitions_for_processing()
                partition  = new.partitions.matrix.item((0,) * new._pmndim) # "first" partition of new
                indices = partition.indices[:n_non_collapse_axes] + c_slice
                data = d[indices]
                data._flag_partitions_for_processing()
                n_data = data.partitions.matrix.size
                n_new = new.partitions.matrix.size

                if new._max_partitions_per_process*n_data > data._max_partitions_per_process*n_new:
                    # "turn on" parallelism in _collapse_subspace
                    _parallelise_collapse_subspace = True
                    # "turn off" parallelism in _collapse
                    _parallelise_collapse = False
                else:
                    # "turn off" parallelism in _collapse_subspace
                    _parallelise_collapse_subspace = False
                    # "turn on" parallelism in _collapse
                    _parallelise_collapse = True
                #--- End: if
            elif mode == 1:
                # "turn off" parallelism in _collapse_subspace
                _parallelise_collapse_subspace = False
                # "turn on" parallelism in _collapse
                _parallelise_collapse = True
            elif mode == 2:
                # "turn on" parallelism in _collapse_subspace
                _parallelise_collapse_subspace = True
                # "turn off" parallelism in _collapse
                _parallelise_collapse = False
            else:
                raise ValueError('Invalid collapse parallel mode')
            #--- End: if
        else:
            # "turn off" parallelism in both functions
            _parallelise_collapse_subspace = False
            _parallelise_collapse = False
        #--- End: if

        # Flag which partitions will be processed on this rank. If
        # _parallelise_collapse is False then all partitions will be
        # flagged for processing.
        new._flag_partitions_for_processing(_parallelise_collapse)

        processed_partitions = []
        for pmindex, partition in numpy_ndenumerate(new.partitions.matrix):
            if partition._process_partition:
                # Only process the partition if it is flagged
                partition.open(config)

                # Save the position of the partition in the partition
                # matrix
                partition._pmindex = pmindex

                partition.axes  = p_axes
                partition.flip  = []
                partition.part  = []
                partition.Units = p_units
                
                if squeeze:
                    partition.location = partition.location[:n_non_collapse_axes]
                    partition.shape    = partition.shape[:n_non_collapse_axes]
                #--- End: if

                indices = partition.indices[:n_non_collapse_axes] + c_slice
            
                partition.subarray = d._collapse_subspace(
                    func, fpartial, ffinalise,
                    indices, n_non_collapse_axes, n_collapse_axes,
                    Nmax, mtol, _preserve_partitions=_preserve_partitions,
                    _parallelise_collapse_subspace=_parallelise_collapse_subspace,
                    **kwargs)

                partition.close(keep_in_memory=keep_in_memory)

                # Add each partition to a list of processed partitions
                processed_partitions.append(partition)
            #--- End: if
        #--- End: for

        # processed_partitions contains a list of all the partitions
        # that have been processed on this rank. In the serial case
        # this is all of them and this line of code has no
        # effect. Otherwise the processed partitions from each rank
        # are distributed to every rank and processed_partitions now
        # contains all the processed partitions from every rank.
        processed_partitions = self._share_partitions(processed_partitions,
                                                      _parallelise_collapse)

        # Put the processed partitions back in the partition matrix
        # according to each partitions _pmindex attribute set above.
        pm = new.partitions.matrix
        for partition in processed_partitions:
            pm[partition._pmindex] = partition

            p_datatype = partition.subarray.dtype
            if datatype != p_datatype:
                datatype = numpy_result_type(p_datatype, datatype)
        #--- End: for

        # Share the lock files created by each rank for each partition
        # now in a temporary file so that __del__ knows which lock
        # files to check if present
        new._share_lock_files(_parallelise_collapse)
        
        new._all_axes = None
        new._flip     = []
        new._Units    = new_units
        new.dtype     = datatype

        if squeeze:
            new._axes  = p_axes
            new._ndim  = ndim - n_collapse_axes
            new._shape = new._shape[:new._ndim]
        else:
            new_axes = new._axes
            if new_axes != original_self_axes:
                iaxes = [new_axes.index(axis) for axis in original_self_axes]
                new.transpose(iaxes, i=True)
    
        # ------------------------------------------------------------
        # Update d in place
        # ------------------------------------------------------------
        d.__dict__ = new.__dict__
       
        # ------------------------------------------------------------
        # Return
        # ------------------------------------------------------------
        return d
    #--- End: def

    def _collapse_subspace(self, func, fpartial, ffinalise, indices,
                           n_non_collapse_axes, n_collapse_axes, Nmax,
                           mtol, weights=None,
                           _preserve_partitions=False,
                           _parallelise_collapse_subspace=True,
                           **kwargs):
        '''

Collapse a subspace of a data array.

If set, *weights* and *kwargs* are passed to the function call. If
there is a *weights* keyword argument then this should either evaluate
to False or be a dictionary of weights for at least one of the data
dimensions.

:Parameters:

    func : function

    fpartial : function

    ffinalise : function

    indices: tuple
        The indices of the master array which would create the
        subspace.

    n_non_collapse_axes : int
        The number of data array axes which are not being
        collapsed. It is assumed that they are in the slowest moving
        positions.

    n_collapse_axes : int
        The number of data array axes which are being collapsed. It is
        assumed that they are in the fastest moving positions.

    weights : dict, optional

    kwargs : *optional*

:Returns:

    out: list

:Examples:

'''   

        ndim = self._ndim

        master_shape = self.shape

        data = self[indices]

        # If the input data array 'fits' in one chunk of memory, then
        # make sure that it has only one partition
        if (not mpi_on and not _preserve_partitions and data._pmndim
            and data.fits_in_memory(data.dtype.itemsize)):
           data.varray

        # True iff at least two, but not all, axes are to be
        # collapsed.
        reshape = 1 < n_collapse_axes < ndim

        out = None
                    
        if n_collapse_axes == ndim:
            # All axes are to be collapsed
            kwargs.pop('axis', None)
        else:
            # At least one axis, but not all axes, are to be
            # collapsed. It is assumed that the collapse axes are in
            # the last (fastest varying) positions (-1, -2, ...). We
            # set kwargs['axis']=-1 (actually we use the +ve integer
            # equivalent of -1) if there is more then one collapse
            # axis because, in this case (i.e. reshape is True), we
            # will reshape everything.
            kwargs['axis'] = ndim - n_collapse_axes

        masked = False

        sub_samples  = 0

#        pda_args = data.pda_args(revert_to_file=True) #, readonly=True)
        config = data.partition_configuration(readonly=True)

        # Flag which partitions will be processed on this rank. If
        # _parallelise_collapse_subspace is False then all partitions
        # will be flagged for processing.
        data._flag_partitions_for_processing(_parallelise_collapse_subspace)

        for i, partition in enumerate(data.partitions.matrix.flat):
            if partition._process_partition:
                # Only process a partition if flagged
                partition.open(config)
                array = partition.array

                p_masked = partition.masked

                if p_masked:
                    masked = True
                    if array.mask.all():
                        # The array is all missing data
                        partition.close()
                        continue
    
                # Still here? Then there are some non-missing sub-array
                # elements.
                if weights is not None:
                    w = self._collapse_create_weights(array, partition.indices,
                                                      indices,
                                                      master_shape, weights,
                                                      n_non_collapse_axes,
                                                      n_collapse_axes)
                    wmin = w.min()
                    if wmin < 0:
                        raise ValueError("Can't collapse with negative weights")

                    if wmin == 0:
                        # Mask the array where the weights are zero
                        array = numpy_ma_masked_where(w==0, array, copy=True)
                        if array.mask.all():
                            # The array is all missing data
                            partition.close()
                            continue
                    #--- End: if
 
                    kwargs['weights'] = w
                #--- End: if

                partition.close()

                if reshape:
                    # At least two, but not all, axes are to be collapsed
                    # => we need to reshape the array and the weights.
                    shape = array.shape
                    ndim = array.ndim
                    new_shape  = shape[:n_non_collapse_axes]
                    new_shape += (reduce(operator_mul, shape[n_non_collapse_axes:]),)
                    array = numpy_reshape(array.copy(), new_shape)

                    if weights is not None:
                        w = kwargs['weights']
                        if w.ndim < ndim:
                            # The weights span only collapse axes (as
                            # opposed to spanning all axes)
                            new_shape = (w.size,)

                        kwargs['weights'] = numpy_reshape(w, new_shape)
                #--- End: if  

                p_out = func(array, masked=p_masked, **kwargs)

                if out is None:
                    if not _parallelise_collapse_subspace and data.partitions.size == i + 1:
                        # There is exactly one partition so we are done
                        out = p_out
                        break
                    #--- End: if
                    out = fpartial(p_out)
                else:
                    out = fpartial(out, p_out)
                #--- End: if

                sub_samples += 1

            #--- End: if
        #--- End: for

        if _parallelise_collapse_subspace:
            # Aggregate the outputs of each rank using the group=True
            # keyword on fpartial on rank 0 only
            for rank in range(1, mpi_size):
                if mpi_rank == rank:
                    if out is None:
                        out_is_none = True
                        mpi_comm.send(out_is_none, dest=0)
                    else:
                        out_is_none = False
                        mpi_comm.send(out_is_none, dest=0)
                        out_props = []
                        for item in out:
                            item_props = {}
                            if isinstance(item, numpy_ndarray):
                                item_props['is_numpy_array'] = True
                                item_props['isMA'] = numpy_ma_isMA(item)
                                if item_props['isMA']:
                                    item_props['is_masked'] = not item.mask is numpy_ma_nomask
                                else:
                                    item_props['is_masked'] = False
                                #--- End: if
                                item_props['shape'] = item.shape
                                item_props['dtype'] = item.dtype
                            else:
                                item_props['is_numpy_array'] = False
                            #--- End: if
                            out_props.append(item_props)
                        #--- End: for
                        mpi_comm.send(out_props, dest=0)
                        for item, item_props in zip(out, out_props):
                            if item_props['is_numpy_array']:
                                if item_props['is_masked']:
                                    mpi_comm.Send(item.data, dest=0)
                                    mpi_comm.Send(item.mask, dest=0)
                                elif item_props['isMA']:
                                    mpi_comm.Send(item.data, dest=0)
                                else:
                                    mpi_comm.Send(item, dest=0)
                                #--- End: if
                            else:
                                mpi_comm.send(item, dest=0)
                            #--- End: if
                        #--- End: for
                elif mpi_rank == 0:
                    p_out_is_none = mpi_comm.recv(source=rank)
                    if p_out_is_none:
                        continue
                    else:
                        p_out_props = mpi_comm.recv(source=rank)
                        p_out = []
                        for item_props in p_out_props:
                            if item_props['is_numpy_array']:
                                if item_props['is_masked']:
                                    item = numpy_ma_masked_all(item_props['shape'],
                                                               dtype=item_props['dtype'])
                                    mpi_comm.Recv(item.data, source=rank)
                                    mpi_comm.Recv(item.mask, source=rank)
                                elif item_props['isMA']:
                                    item = numpy_ma_empty(item_props['shape'],
                                                          dtype=item_props['dtype'])
                                    mpi_comm.Recv(item.data, source=rank)
                                else:
                                    item = numpy_empty(item_props['shape'],
                                                       dtype=item_props['dtype'])
                                    mpi_comm.Recv(item, source=rank)
                            else:
                                item = mpi_comm.recv(source=rank)
                            #--- End: if
                            p_out.append(item)
                        #--- End: for
                        p_out = tuple(p_out)
                        if out is None:
                            out = p_out
                        else:
                            out = fpartial(out, p_out, group=True)
                        #--- End: if
                    #--- End: if
                #--- End: for
            #--- End: if

            # Finalise
            sub_samples = mpi_comm.gather(sub_samples, root=0)
            if mpi_rank == 0:
                sub_samples = sum(sub_samples)
                out = self._collapse_finalise(ffinalise, out,
                                              sub_samples, masked, Nmax, mtol, data,
                                              n_non_collapse_axes)
            #--- End: if
            if mpi_rank == 0:
                out_props = {}
                out_props['isMA'] = numpy_ma_isMA(out)
                if out_props['isMA']:
                    out_props['is_masked'] = not out.mask is numpy_ma_nomask
                else:
                    out_props['is_masked'] = False
                #--- End: if
                out_props['shape'] = out.shape
                out_props['dtype'] = out.dtype
            else:
                out_props = None
            #--- End: if
            out_props = mpi_comm.bcast(out_props, root=0)
            if out_props['is_masked']:
                if mpi_rank != 0:
                    out = numpy_ma_masked_all(out_props['shape'],
                                              dtype=out_props['dtype'])
                #--- End: if
                mpi_comm.Bcast(out.data, root=0)
                mpi_comm.Bcast(out.mask, root=0)
            elif out_props['isMA']:
                if mpi_rank != 0:
                    out = numpy_ma_empty(out_props['shape'],
                                         dtype=out_props['dtype'])
                #--- End: if
                mpi_comm.Bcast(out.data, root=0)
            else:
                if mpi_rank != 0:
                    out = numpy_empty(out_props['shape'],
                                      dtype=out_props['dtype'])
                #--- End: if
                mpi_comm.Bcast(out, root=0)
            #--- End: if
        else:
            out = self._collapse_finalise(ffinalise, out, sub_samples,
                                          masked, Nmax, mtol, data, n_non_collapse_axes)
        #--- End: if
        return out
    #--- End: def

    @classmethod
    def _collapse_finalise(cls, ffinalise, out, sub_samples, masked,
                           Nmax, mtol, data, n_non_collapse_axes):
        '''
        '''
        if out is not None:
            # Finalise
            N, out = ffinalise(out, sub_samples)
            out = cls._collapse_mask(out, masked, N, Nmax, mtol)
        else:
            # no data - return all masked
            out = numpy_ma_masked_all(data.shape[:n_non_collapse_axes],
                                      data.dtype)
        #--- End: if
        return out
    #--- End: def


    @staticmethod
    def _collapse_mask(array, masked, N, Nmax, mtol):
        '''
 
:Parameters:

    array : numpy array

    masked : bool

    N : numpy array-like

    Nmax : int

    mtol : numpy array-like

:Returns:

   out: numpy array

'''
        if masked and mtol < 1:
            x = N < (1-mtol)*Nmax
            if x.any():
                array = numpy_ma_masked_where(x, array, copy=False)
        #--- End: if

        return array
    #--- End: def


    @staticmethod
    def _collapse_create_weights(array, indices, master_indices, master_shape,
                                 master_weights, n_non_collapse_axes,
                                 n_collapse_axes):
        '''
        
:Parameters:

    array : numpy array

    indices : tuple

    master_indices : tuple

    master_shape : tuple

    master_weights : dict

    n_non_collapse_axes : int
        The number of array axes which are not being collapsed. It is
        assumed that they are in the slowest moving positions.

    n_collapse_axes : int
        The number of array axes which are being collapsed. It is
        assumed that they are in the fastest moving positions.

:Returns:

    out: numpy array or None

:Examples:

'''
        array_shape = array.shape
        array_ndim  = array.ndim
        
        weights_indices = []
        for master_index, index, size in izip(master_indices,
                                              indices,
                                              master_shape):
            start , stop , step = master_index.indices(size)
            
            size1, mod = divmod(stop-start-1, step)            
            
            start1, stop1, step1 = index.indices(size1+1)
            
            size2, mod = divmod(stop1-start1, step1)
            
            if mod != 0:
                size2 += 1
                
            start += start1 * step
            step  *= step1
            stop   = start + (size2-1)*step + 1
    
            weights_indices.append(slice(start, stop, step))
        #--- End: for
    
        base_shape = (1,) * array_ndim
    
        masked       = False
        zero_weights = False

        weights = [] 
        for key, weight in master_weights.iteritems():
            shape = list(base_shape)
            index = []
            for i in key:
                shape[i] = array_shape[i]
                index.append(weights_indices[i])
            #--- End: for
    
            weight = weight[tuple(index)].unsafe_array
                
            zero_weights = zero_weights or (weight.min() <= 0)

            masked = masked or numpy_ma_isMA(weight)

            if weight.ndim != array_ndim:
                # Make sure that the weight has the same number of
                # dimensions as the array
                weight = weight.reshape(shape)
    
            weights.append(weight)
        #--- End: for
    
        weights_out = weights[0]
    
        if len(weights) > 1:
            # There are two or more weights, so create their product
            # (can't do this in-place because of broadcasting woe)
            for w in weights[1:]:
                weights_out = weights_out * w
    
        weights_out_shape = weights_out.shape
    
        if (not masked and 
            weights_out_shape[:n_non_collapse_axes] == base_shape[:n_non_collapse_axes]):
            # The input weights are not masked and only span collapse axes
            weights_out = weights_out.reshape(weights_out_shape[n_non_collapse_axes:])
    
            if weights_out_shape[n_non_collapse_axes:] != array_shape[n_non_collapse_axes:]:
                # The input weights span some, but not all, of the
                # collapse axes, so broadcast the weights over all
                # collapse axes
                weights_out = broadcast_array(weights_out, array_shape[n_non_collapse_axes:])       
        else:
            if weights_out_shape != array_shape:
                # Either a) The input weights span at least one
                # non-collapse axis, so broadcast the weights over all
                # axes or b) The weights contain masked values
                weights_out = broadcast_array(weights_out, array_shape)
    
            if masked and numpy_ma_isMA(array):
                if not (array.mask | weights_out.mask == array.mask).all():
                    raise ValueError("weights mask is duff")
    
        return weights_out
    #--- End: def

    def _collapse_optimize_weights(self, weights):
        '''
    
Optimise when weights span only non-partitioned axes.

    weights : dict

'''
        non_partitioned_axes = set(self._axes).difference(self._pmaxes)
        
        x = []
        new_key = ()
        for key in weights:
            if non_partitioned_axes.issuperset(key):
                x.append(key)
                new_key += key
        #--- End: for
    
        if len(x) > 1:
            reshaped_weights = []
            for key in x:
                w = weights.pop(key)
                w = w.array
                shape = [(w.shape[key.index(axis)] if axis in key else 1) 
                         for axis in new_key]
                w = w.reshape(shape)
                
                reshaped_weights.append(w)
            #--- End: for
                  
            # Create their product
            new_weight = reshaped_weights[0]
            for w in reshaped_weights[1:]:
                new_weight = new_weight * w
       
            weights[new_key] = type(self)(new_weight)
        #--- End: if
    
        return weights
    #--- End: def

    def _new_axis_identifier(self, existing_axes=None):
        '''

Return an axis name not being used by the data array.

The returned axis name will also not be referenced by partitions of
the partition matrix.

:Parameters:

    existing_axes : sequence of str, optional

:Returns:

    out: str
        The new axis name.

:Examples:

>>> d._all_axis_names()   
['dim1', 'dim0']
>>> d._new_axis_identifier()
'dim2'

>>> d._all_axis_names()   
['dim1', 'dim0', 'dim3']
>>> d._new_axis_identifier()
'dim4'

>>> d._all_axis_names()   
['dim5', 'dim6', 'dim7']
>>> d._new_axis_identifier()
'dim3'

'''
        if existing_axes is None:
            existing_axes = self._all_axis_names()

        n = len(existing_axes)
        axis = 'dim%d' % n
        while axis in existing_axes:
            n += 1
            axis = 'dim%d' % n
        #--- End: while

        return axis
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def Units(self):
        '''

The `cf.Units` object containing the units of the data array.

Deleting this attribute is equivalent to setting it to an undefined
units object, so this attribute is guaranteed to always exist.

:Examples:

>>> d.Units = cf.Units('m')
>>> d.Units
<CF Units: m>
>>> del d.Units
>>> d.Units
<CF Units: >

'''
        return self._Units
    #--- End: def

    @Units.setter    
    def Units(self, value):
        units = getattr(self, '_Units', _units_None)
        if units and not self._Units.equivalent(value):
            raise ValueError("Can't set units to non-equivalent units")

        dtype = self.dtype
        if dtype is not None:
            if dtype.kind == 'i':
                char = dtype.char        
                if char == 'i':
                    old_units = getattr(self, '_Units', None)
                    if old_units is not None and not old_units.equals(value):
                        self.dtype = 'float32'
                elif char == 'l':
                    old_units = getattr(self, '_Units', None)
                    if old_units is not None and not old_units.equals(value):
                        self.dtype = float
        #-- End: if

        self._Units = value
    #--- End: def

    @Units.deleter
    def Units(self): self._Units = _units_None

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def data(self):
        '''

The data array object as an object identity.

:Examples:

>>> d.data is d
True

'''
        return self
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def Data(self):
        '''

The data array object as an object identity.

:Examples:

>>> d.Data is d
True

'''
        return self
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def dtype(self):
        '''

The `numpy` data type of the data array.

By default this is the data type with the smallest size and smallest
scalar kind to which all sub-arrays of the master data array may be
safely cast without loss of information. For example, if the
sub-arrays have data types 'int64' and 'float32' then the master data
array's data type will be 'float64'; or if the sub-arrays have data
types 'int64' and 'int32' then the master data array's data type will
be 'int64'.

Setting the data type to a `numpy.dtype` object, or any object
convertible to a `numpy.dtype` object, will cause the master data
array elements to be recast to the specified type at the time that
they are next accessed, and not before. This does not immediately
change the master data array elements, so, for example, reinstating
the original data type prior to data access results in no loss of
information.

Deleting the data type forces the default behaviour. Note that if the
data type of any sub-arrays has changed after `dtype` has been set
(which could occur if the data array is accessed) then the reinstated
default data type may be different to the data type prior to `dtype`
being set.

:Examples:

>>> d = cf.Data([0.5, 1.5, 2.5])
>>> d.dtype
dtype(float64')
>>> type(d.dtype)
<type 'numpy.dtype'>

>>> d = cf.Data([0.5, 1.5, 2.5])
>>> import numpy
>>> d.dtype = numpy.dtype(int)
>>> print d.array
[0 1 2]
>>> d.dtype = bool
>>> print d.array
[False  True  True]
>>> d.dtype = 'float64'
>>> print d.array
[ 0.  1.  1.]

>>> d = cf.Data([0.5, 1.5, 2.5])
>>> d.dtype = int
>>> d.dtype = bool
>>> d.dtype = float
>>> print d.array
[ 0.5  1.5  2.5]

'''
        datatype = self._dtype
        if datatype is None:
            flat = self.partitions.matrix.flat
            datatype = flat.next().subarray.dtype
            for partition in flat:
                datatype = numpy_result_type(datatype, partition.subarray)

            self._dtype = datatype
        #--- End: if

        return datatype
    #--- End: def
    @dtype.setter
    def dtype(self, value):
        self._dtype = numpy_dtype(value)
    #--- End: def
    @dtype.deleter
    def dtype(self):
        self._dtype = None
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def fill_value(self):
        '''

The data array missing data value.

If set to None then the default numpy fill value appropriate to the
data array's data type will be used.

Deleting this attribute is equivalent to setting it to None, so this
attribute is guaranteed to always exist.

:Examples:

>>> d.fill_value = 9999.0
>>> d.fill_value
9999.0
>>> del d.fill_value
>>> d.fill_value
None

'''
        return self._fill_value
    #--- End: def
    @fill_value.setter
    def fill_value(self, value): self._fill_value = value
    @fill_value.deleter
    def fill_value(self)       : self._fill_value = None

    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def hardmask(self):
        '''

Whether the mask is hard (True) or soft (False).

When the mask is hard, masked entries of the data array can not be
unmasked by assignment, but unmasked entries may still be masked.

When the mask is soft, masked entries of the data array may be
unmasked by assignment and unmasked entries may be masked.

By default, the mask is hard.

:Examples:

>>> d.hardmask = False
>>> d.hardmask
False

'''
        return self._hardmask
    @hardmask.setter
    def hardmask(self, value):
        self._hardmask = value
    @hardmask.deleter
    def hardmask(self):
        raise AttributeError(
"Won't delete {} attribute 'hardmask'".format(self.__class__.__name__))
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def ismasked(self):
        '''

True if the data array has any masked values.

:Examples:

>>> d = cf.Data([[1, 2, 3], [4, 5, 6]])
>>> print d.ismasked
False
>>> d[0, ...] = cf.masked
>>> d.ismasked
True

'''
        if self._auxiliary_mask:
            for m in self._auxiliary_mask:
                if m.any():
                    # Found a masked element
                    return True
            #--- End: for

            # Still here? Then remove the auxiliary mask because it
            # must be all False.
            self._auxiliary_mask = None
        #--- End: if

        # Still here?
        config = self.partition_configuration(readonly=True)

        for partition in self.partitions.matrix.flat:
            partition.open(config)
            partition.array
            if partition.masked:
                # Found a masked element
                partition.close()
                return True
            
            partition.close()
        #--- End: for
        
        # There are no masked elements
        return False
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def ispartitioned(self):
        '''

True if the data array is partitioned.

:Examples:

>>> d._pmsize
1        
>>> d.ispartitioned
False

>>> d._pmsize
2
>>> d.ispartitioned
False

'''
        return self._pmsize > 1
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def isscalar(self):
        '''

True if the data array is a 0-d scalar array.

:Examples:

>>> d.ndim
0
>>> d.isscalar
True

>>> d.ndim >= 1
True
>>> d.isscalar
False

'''
        return not self._ndim
    #--- End: def

#    @property
#    def max(self):
#        '''
#
#The maximum of the array.
#
#``d.max`` is equivalent to ``d.max()``.
#
#.. seealso `max`, `min`
#
#:Examples:
#
#>>> d = cf.Data([[4, 5, 6], [1, 2, 3]], 'metre')
#>>> d.max
#<CF Data: 6 metre>
#>> d.max.datum()
#6
#
#'''
#        return self.max(keepdims=False)
#        pda_args = self.pda_args(revert_to_file=True,
#                                         readonly=True)
#        
#        flat = self.partitions.matrix.flat
#
#        partition = flat.next()
#        array = partition.dataarray(**pda_args)
#        m = numpy_amax(array)
#        partition.close()
#
#        for partition in flat:
#            array = partition.dataarray(**pda_args)
#            m = max(m, numpy_amax(array))
#            partition.close()
#        #--- End: for
#
#        if m is numpy_ma_masked:
#            m = numpy_ma_array(0, mask=True, dtype=array.dtype)
#
#        return type(self)(m, self.Units)
    #--- End: def
         
    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def nbytes(self):
        '''

Total number of bytes consumed by the elements of the array.

Does not include bytes consumed by the array mask

:Examples:

>>> d = cf.Data([[1, 1.5, 2]])
>>> d.dtype
dtype('float64')
>>> d.size, d.dtype.itemsize
(3, 8)
>>> d.nbytes
24
>>> d[0] = cf.masked
>>> print d.array
[[-- 1.5 2.0]]
>>> d.nbytes
24

'''
        return self._size * self.dtype.itemsize
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def ndim(self):
        '''

Number of dimensions in the data array.

:Examples:

>>> d.shape
(73, 96)
>>> d.ndim
2

>>> d.shape
()
>>> d.ndim
0

'''
        return self._ndim
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def _pmaxes(self):
        '''
'''
        return self.partitions.axes
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def _pmndim(self):
        '''

Number of dimensions in the partition matrix.

:Examples:

>>> d._pmshape
(4, 7)
>>> d._pmndim
2

>>> d._pmshape
()
>>> d._pmndim
0

'''
        return self.partitions.ndim
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def _pmsize(self):
        '''

Number of partitions in the partition matrix.

:Examples:

>>> d._pmshape
(4, 7)
>>> d._pmsize
28

>>> d._pmndim
0
>>> d._pmsize
1

'''
        return self.partitions.size
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def _pmshape(self):
        '''

Tuple of the partition matrix's dimension sizes.

:Examples:

>>> d._pmshape
(4, 7)

>>> d._pmndim
0
>>> d._pmshape
()

'''
        return self.partitions.shape
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def shape(self):
        '''

Tuple of the data array's dimension sizes.

:Examples:

>>> d.shape
(73, 96)

>>> d.ndim
0
>>> d.shape
()

'''
        return self._shape
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def size(self):
        '''

Number of elements in the data array.

:Examples:

>>> d.shape
(73, 96)
>>> d.size
7008

>>> d.shape
(1, 1, 1)
>>> d.size
1

>>> d.ndim
0
>>> d.shape
()
>>> d.size
1

'''
        return self._size
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def array(self):
        '''A numpy array copy the data array.

.. note:: If the data array is stored as date-time objects then a
          numpy array of numeric reference times will be returned. A
          numpy array of date-time objects may be returned by the
          `dtarray` attribute.

.. seealso:: `dtarray`, `varray`

:Examples:

>>> d = cf.Data([1, 2, 3.0], 'km')
>>> a = d.array
>>> isinstance(a, numpy.ndarray)
True
>>> print a
[ 1.  2.  3.]
>>> d[0] = -99 
>>> print a[0] 
1.0
>>> a[0] = 88
>>> print d[0]
-99.0 km

        '''
        # Set the auxiliary_mask keyword to None because we can apply
        # it later in one go
        config = self.partition_configuration(readonly=True,
                                              auxiliary_mask=None)

        out_data_type = self.dtype
        units = self.Units

        _dtarray = getattr(self, '_dtarray', False)
        
        if _dtarray:
            del self._dtarray            
            out_data_type = _dtype_object
#            if self._isdatetime():
#                pda_args['func'] = None
#        elif self._isdatetime():
#            out_data_type = numpy_dtype(float)
#            pda_args['func']   = dt2rt
#            # Turn off data type checking and partition updating
#            pda_args['dtype']  = None
#            pda_args['update'] = False

        partitions = self.partitions

        # Still here?
        array_out = numpy_empty(self._shape, dtype=out_data_type)

        masked = False

        if not self.ndim:
            # --------------------------------------------------------
            # array_out is a scalar array so index it with Ellipsis
            # (as opposed to the empty tuple which would be returned
            # from partition.indices). This prevents bad behaviour
            # when p_array is a numpy array of objects (e.g. data-time
            # objects).
            # --------------------------------------------------------
            partition = partitions.matrix[()]
            partition.open(config)
            p_array = partition.array

            # copy okect?
                
            if _dtarray:
                if not partition.isdt:
                    # Convert the partition subarray to an array
                    # of date-time objects
                    p_array = rt2dt(p_array, units)
            elif partition.isdt:
                # Convert the partition subarray to an array of
                # reference time floats
                p_array = dt2rt(p_array, None, units)

            if not masked and partition.masked:
                array_out = array_out.view(numpy_ma_MaskedArray)
                array_out.set_fill_value(self._fill_value)
                masked = True

            array_out[...] = p_array
            partition.close()

        else:
            # --------------------------------------------------------
            # array_out is not a scalar array, so it can safely be
            # indexed with partition.indices in all cases.
            # --------------------------------------------------------
            for partition in partitions.matrix.flat:
                partition.open(config)
                p_array = partition.array

                if _dtarray:
                    if not partition.isdt:
                        # Convert the partition subarray to an array
                        # of date-time objects
                        p_array = rt2dt(p_array, units)
                elif partition.isdt:
                    # Convert the partition subarray to an array of
                    # reference time floats
                    p_array = dt2rt(p_array, None, units)

                # copy okect?

                if not masked and partition.masked:
                    array_out = array_out.view(numpy_ma_MaskedArray)
                    array_out.set_fill_value(self._fill_value)
                    masked = True

                array_out[partition.indices] = p_array

                partition.close()
            #--- End: for

        # ------------------------------------------------------------
        # Apply the auxiliary mask
        # ------------------------------------------------------------
        if self._auxiliary_mask:
            if not masked:
                # Convert the output array to a masked array
                array_out = array_out.view(numpy_ma_MaskedArray)
                array_out.set_fill_value(self._fill_value)
                masked = True

            self._auxiliary_mask_tidy()

            for mask in self._auxiliary_mask:
                array_out.mask = array_out.mask | mask.array

            if array_out.mask is numpy_ma_nomask:
                # There are no masked points, so convert the array
                # back to a non-masked array.
                array_out = array_out.data
                masked = False
        #--- End: if

        if masked and self._hardmask:
            # Harden the mask of the output array
            array_out.harden_mask()

        return array_out
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def dtarray(self):
        '''

An independent numpy array of date-time objects.

Only applicable to data arrays with reference time units.

If the calendar has not been set then the CF default calendar will be
used and the units will be updated accordingly.

The data type of the data array is unchanged.

.. seealso:: `array`, `varray`

:Examples:

'''
        if not self.Units.isreftime:
            raise ValueError(
"Can't create date-time array from units {!r}".format(self.Units))

        if getattr(self.Units, 'calendar', None) == 'none':
            raise ValueError(
"Can't create date-time array from units {!r} because calendar is 'none'".format(self.Units))
            
        self._dtarray = True
        return self.array
    #--- End: def

    @property
    def dtvarray(self):
        '''

A numpy array view the data array converted to date-time objects.

Only applicable for reference time units.

If the calendar has not been set then the CF default calendar will be
used and the units will be updated accordingly.

.. seealso:: `array`, `dtarray`, `varray`

'''
        raise NotImplementedError("cf.Data.dtvarray is dead.")
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def unsafe_array(self):
        '''

A numpy array of the data array.

It is unsafe because it might (or might not) be view to the master
data array - you just don't know. So changing the returned array in
place might have dire consequences.

It is useful because if you are 100% certain that you're not going to
change the returned array in place then this method may be much faster
than the `array` method.

Why not just use the `varray` method? Well, you might not want to
destroy the partition matrix.

The data type of the array is as returned by the `dtype` attribute.

:Examples:

>>> a = d.unsafe_array
>>> isinstance(a, numpy.ndarray)
True

'''      
#        partitions = self.partitions
#
#        if partitions.size == 1:
#            # If there is only one partition we can speed things up
#            pda_args = self.pda_args(revert_to_file=True)
#            partition = partitions.matrix.item()
#            array_out = partition.dataarray(readonly=True, **pda_args)
#            partition.close()
#            return array_out
#
#        # Still here?
        return self.array
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def varray(self):
        '''

A numpy array view the data array.

Note that making changes to elements of the returned view changes the
underlying data.

.. seealso:: `array`, `dtarray`

:Examples:

>>> a = d.varray
>>> type(a)
<type 'numpy.ndarray'>
>>> a
array([0, 1, 2, 3, 4])
>>> a[0] = 999
>>> d.varray
array([999, 1, 2, 3, 4])

'''
        config = self.partition_configuration(readonly=False)
       
        data_type = self.dtype

        if getattr(self, '_dtarray', False):
            del self._dtarray
        elif self._isdatetime(): #self._isdt:
            data_type = numpy_dtype(float)
            config['func'] = dt2rt
            # Turn off data type checking and partition updating
            config['dtype']  = None
           
        if self.partitions.size == 1:
            # If there is only one partition, then we can return a
            # view of the partition's data array without having to
            # create an empty array and then filling it up partition
            # by partition.
            partition = self.partitions.matrix.item()
            partition.open(config)
            array = partition.array
            # Note that there is no need to close the partition here.
            self._dtype = data_type

# Flip to []?
            return array

        # Still here?  
        shape = self._shape
        array_out = numpy_empty(shape, dtype=data_type)
        masked = False

        config['readonly'] = True
        
        for partition in self.partitions.matrix.flat:
            partition.open(config)
            p_array = partition.array

            if not masked and partition.masked:
                array_out = array_out.view(numpy_ma_MaskedArray)
                array_out.set_fill_value(self._fill_value)
                masked = True

            array_out[partition.indices] = p_array

            # Note that there is no need to close the partition here
        #--- End: for

        # ------------------------------------------------------------
        # Apply an auxiliary mask
        # ------------------------------------------------------------
        if self._auxiliary_mask:
            if not masked:
                # Convert the output array to a masked array
                array_out = array_out.view(numpy_ma_MaskedArray)
                array_out.set_fill_value(self._fill_value)
                masked = True

            self._auxiliary_mask_tidy()

            for mask in self._auxiliary_mask:
                array_out.mask = array_out.mask | mask

            if array_out.mask is numpy_ma_nomask:
                # There are no masked points, so convert back to a
                # non-masked array.
                array_out = array_out.data
                masked = False

            self._auxiliary_mask = None
        #--- End: if

        if masked and self._hardmask:
            # Harden the mask of the output array
            array_out.harden_mask()

        matrix = _xxx.copy()

        if not array_out.ndim and not isinstance(array_out, numpy_ndarray):
            array_out = numpy_asanyarray(array_out)

        matrix[()] = Partition(subarray = array_out,
                               location = [(0, n) for n in shape],
                               axes     = self._axes,
                               flip     = [],
                               shape    = list(shape),
                               Units    = self.Units,
                               part     = []
                               )

        self.partitions = PartitionMatrix(matrix, [])

        self._dtype = data_type
        self._flip  = []

        return array_out
    #--- End: def

    @property
    def mask(self):
        '''

The boolean missing data mask of the data array.

The boolean mask has True where the data array has missing data and
False otherwise.

:Examples:

>>> d.shape
(12, 73, 96)
>>> m = d.mask
>>> m
<CF Data: >
>>> m.dtype
dtype('bool')
>>> m.shape
(12, 73, 96])

'''
        mask = self.copy()

        config = mask.partition_configuration(readonly=False)
        
        for partition in mask.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            
            if partition.masked:
                # Array is masked                
                partition.subarray = array.mask.copy()
            else:
                # Array is not masked
                partition.subarray = FilledArray(shape=array.shape,
                                                 size=array.size,
                                                 ndim=array.ndim,
                                                 dtype=_dtype_bool,
                                                 fill_value=0)

            partition.Units = _units_None

            partition.close()
        #--- End: for
        
        mask._Units = _units_None
        mask.dtype  = _dtype_bool

        mask._hardmask = True

        return mask
    #--- End: def

    @staticmethod
    def mask_fpe(*arg):
        '''

Masking of floating-point errors in the results of arithmetic
operations.

If masking is allowed then only floating-point errors which would
otherwise be raised as `FloatingPointError` exceptions are
masked. Whether `FloatingPointError` exceptions may be raised is
determined by `cf.Data.seterr`.

If called without an argument then the current behaviour is returned.

Note that if the raising of `FloatingPointError` exceptions has
suppressed then invalid values in the results of arithmetic operations
may be subsequently converted to masked values with the `mask_invalid`
method.

.. seealso:: `cf.Data.seterr`, `mask_invalid`

:Parameters:

    arg : bool, optional
        The new behaviour. True means that `FloatingPointError`
        exceptions are suppressed and replaced with masked
        values. False means that `FloatingPointError` exceptions are
        raised. The default is not to change the current behaviour.

:Returns:

    out: bool
        The behaviour prior to the change, or the current behaviour if
        no new value was specified.

:Examples:

>>> d = cf.Data([0., 1])
>>> e = cf.Data([1., 2])

>>> old = cf.Data.mask_fpe(False)
>>> old = cf.Data.seterr('raise')
>>> e/d
FloatingPointError: divide by zero encountered in divide
>>> e**123456
FloatingPointError: overflow encountered in power

>>> old = cf.Data.mask_fpe(True)
>>> old = cf.Data.seterr('raise')
>>> e/d
<CF Data: [--, 2.0] >
>>> e**123456
<CF Data: [1.0, --] >

>>> old = cf.Data.mask_fpe(True)
>>> old = cf.Data.seterr('ignore')
>>> e/d
<CF Data: [inf, 2.0] >
>>> e**123456
<CF Data: [1.0, inf] >

'''
        old = _mask_fpe[0]

        if arg:
            _mask_fpe[0] = bool(arg[0])

        return old
    #--- End: def

    @staticmethod
    def seterr(all=None, divide=None, over=None, under=None, invalid=None):
        '''

Set how floating-point errors in the results of arithmetic operations
are handled.

The options for handling floating-point errors are:

============  ========================================================
Treatment     Action
============  ========================================================
``'ignore'``  Take no action. Allows invalid values to occur in the
              result data array.

``'warn'``    Print a `RuntimeWarning` (via the Python `warnings`
              module). Allows invalid values to occur in the result
              data array.

``'raise'``   Raise a `FloatingPointError` exception.
============  ========================================================

The different types of floating-point errors are:

=================  =================================  =================
Error              Description                        Default treatment
=================  =================================  =================
Division by zero   Infinite result obtained from      ``'warn'``
                   finite numbers.

Overflow           Result too large to be expressed.  ``'warn'``

Invalid operation  Result is not an expressible       ``'warn'``
                   number, typically indicates that  
                   a NaN was produced.

Underflow          Result so close to zero that some  ``'ignore'``
                   precision was lost.
=================  =================================  =================

Note that operations on integer scalar types (such as int16) are
handled like floating point, and are affected by these settings.

If called without any arguments then the current behaviour is
returned.

.. seealso:: `cf.Data.mask_fpe`, `mask_invalid`

:Parameters:

    all : str, optional
        Set the treatment for all types of floating-point errors at
        once. The default is not to change the current behaviour.

    divide : str, optional
        Set the treatment for division by zero. The default is not to
        change the current behaviour.

    over : str, optional
        Set the treatment for floating-point overflow. The default is
        not to change the current behaviour.

    under : str, optional
        Set the treatment for floating-point underflow. The default is
        not to change the current behaviour.

    invalid : str, optional
        Set the treatment for invalid floating-point operation. The
        default is not to change the current behaviour.

:Returns:

    out: dict
        The behaviour prior to the change, or the current behaviour if
        no new values are specified.

:Examples:

Set treatment for all types of floating-point errors to ``'raise'``
and then reset to the previous behaviours:

>>> cf.Data.seterr()
{'divide': 'warn', 'invalid': 'warn', 'over': 'warn', 'under': 'ignore'}
>>> old = cf.Data.seterr('raise')
>>> cf.Data.seterr(**old)
{'divide': 'raise', 'invalid': 'raise', 'over': 'raise', 'under': 'raise'}
>>> cf.Data.seterr()
{'divide': 'warn', 'invalid': 'warn', 'over': 'warn', 'under': 'ignore'}

Set the treatment of division by zero to ``'ignore'`` and overflow to
``'warn'`` without changing the treatment of underflow and invalid
operation:

>>> cf.Data.seterr(divide='ignore', over='warn')
{'divide': 'warn', 'invalid': 'warn', 'over': 'warn', 'under': 'ignore'}
>>> cf.Data.seterr()
{'divide': 'ignore', 'invalid': 'warn', 'over': 'ignore', 'under': 'ignore'}

Some examples with data arrays:

>>> d = cf.Data([0., 1])
>>> e = cf.Data([1., 2])

>>> old = cf.Data.seterr('ignore')
>>> e/d
<CF Data: [inf, 2.0] >
>>> e**12345
<CF Data: [1.0, inf] >

>>> cf.Data.seterr(divide='warn')
{'divide': 'ignore', 'invalid': 'ignore', 'over': 'ignore', 'under': 'ignore'}
>>> e/d
RuntimeWarning: divide by zero encountered in divide
<CF Data: [inf, 2.0] >
>>> e**12345
<CF Data: [1.0, inf] >

>>> old = cf.Data.mask_fpe(False)
>>> cf.Data.seterr(over='raise')
{'divide': 'warn', 'invalid': 'ignore', 'over': 'ignore', 'under': 'ignore'}
>>> e/d
RuntimeWarning: divide by zero encountered in divide
<CF Data: [inf, 2.0] >
>>> e**12345
FloatingPointError: overflow encountered in power

>>> cf.Data.mask_fpe(True)
False
>>> cf.Data.seterr(divide='ignore')
{'divide': 'warn', 'invalid': 'ignore', 'over': 'raise', 'under': 'ignore'}
>>> e/d
<CF Data: [inf, 2.0] >
>>> e**12345
<CF Data: [1.0, --] >

'''
        old = _seterr.copy()
        
        if all:
            _seterr.update({'divide' : all,
                            'invalid': all,
                            'under'  : all,
                            'over'   : all})
            if all == 'raise':
                _seterr_raise_to_ignore.update({'divide' : 'ignore',
                                                'invalid': 'ignore',
                                                'under'  : 'ignore',
                                                'over'   : 'ignore'})
                                               
        else:
            if divide:
                _seterr['divide'] = divide
                if divide == 'raise':
                     _seterr_raise_to_ignore['divide'] = 'ignore' 

            if over:
                _seterr['over'] = over
                if over == 'raise':
                     _seterr_raise_to_ignore['over'] = 'ignore' 

            if under:
                _seterr['under'] = under
                if under == 'raise':
                     _seterr_raise_to_ignore['under'] = 'ignore' 

            if invalid:
                _seterr['invalid'] = invalid
                if invalid == 'raise':
                     _seterr_raise_to_ignore['invalid'] = 'ignore' 
        #--- End: if
        
        return old
    #--- End: def

    def add_partitions(self,
                       extra_boundaries, 
                       pdim):
        '''

Add partition boundaries.

:Parameters:

    extra_boundaries : list of int
        The boundaries of the new partitions.

    pdim : str
        The name of the axis to have the new partitions.

:Returns:

    None

:Examples:

>>> d.add_partitions(    )

'''            
        self.partitions.add_partitions(self._axes, self._flip,
                                       extra_boundaries, 
                                       pdim)
    #--- End: def

    def all(self):
        '''

Test whether all data array elements evaluate to True.

Performs a logical ``and`` over the data array and returns the
result. Masked values are considered as True during computation.

.. seealso:: `allclose`, `any`, `isclose`

:Returns:

    out: bool
        Whether or not all data array elements evaluate to True.

:Examples:

>>> d = cf.Data([[1, 3, 2]])
>>> print d.array
[[1 3 2]]
>>> d.all()
True
>>> d[0, 2] = cf.masked
>>> print d.array
[[1 3 --]]
>>> d.all()
True
>>> d[0, 0] = 0
>>> print d.array
[[0 3 --]]
>>> d.all()
False
>>> d[...] = cf.masked
>>> print d.array
[[-- -- --]]
>>> d.all()
True

'''
        config = self.partition_configuration(readonly=True)
              
        for partition in self.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            a = array.all()
            if not a and a is not numpy_ma_masked:
                partition.close()
                return False

            partition.close()
        #--- End: for

        return True
    #--- End: def

    def allclose(self, y, rtol=None, atol=None):
        '''Returns True if two broadcastable arrays have equal values, False
otherwise.

For numeric data arrays ``d.allclose(y, rtol, atol)`` is equivalent to
``(abs(d - y) <= atol + rtol*abs(y)).all()``, otherwise it is
equivalent to ``(d == y).all()``.

.. seealso:: `all`, `any`, `isclose`

:Parameters:

    y: data_like

    atol: `float`, optional
        The absolute tolerance for all numerical comparisons. By
        default the value returned by the `ATOL` function is used.

    rtol: `float`, optional
        The relative tolerance for all numerical comparisons. By
        default the value returned by the `RTOL` function is used.

:Returns:

     out: `bool`

:Examples:

>>> d = cf.Data([1000, 2500], 'metre')
>>> e = cf.Data([1, 2.5], 'km')
>>> d.allclose(e)
True

>>> d = cf.Data(['ab', 'cdef'])
>>> d.allclose([[['ab', 'cdef']]])
True

>>> d.allclose(e)
True

>>> d = cf.Data([[1000, 2500], [1000, 2500]], 'metre')
>>> e = cf.Data([1, 2.5], 'km')
>>> d.allclose(e)
True

>>> d = cf.Data([1, 1, 1], 's')
>>> d.allclose(1)
True

        '''     
        return self.isclose(y, rtol=rtol, atol=atol).all()
    #--- End: def

    def any(self):
        '''

Test whether any data array elements evaluate to True.

Performs a logical or over the data array and returns the
result. Masked values are considered as False during computation.

.. seealso:: `all`, `allclose`, `isclose`

:Examples:

>>> d = cf.Data([[0 0 0]])
>>> d.any()
False
>>> d[0, 0] = cf.masked
>>> print d.array
[[-- 0 0]]
>>> d.any()
False
>>> d[0, 1] = 3
>>> print d.array
[[0 3 0]]
>>> d.any()
True

>>> print d.array
[[-- -- --]]
>>> d.any()
False

'''  
        config = self.partition_configuration(readonly=True)

        for partition in self.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            if array.any():
                partition.close()
                return True

            partition.close()
        #--- End: for

        return False
    #--- End: def

    
    @classmethod
    def concatenate_data(cls, data_list, axis):
        """Concatenates a list of Data objects into a single Data object along
the specified access (see cf.Data.concatenate for details). In the
case that the list contains only one element, that element is simply
returned.

:Parameters:

    data_list : list
        The list of data objects to concatenate.

    axis: `int`
        The axis along which to perform the concatenation.

:Returns:

    `Data`
        The resulting single `Data` object.

        """
        if len(data_list) > 1:
            data = cls.concatenate(data_list, axis=axis)         
#            data = Data.concatenate(data_list, axis=axis)
            if data.fits_in_one_chunk_in_memory(data.dtype.itemsize):
                data.varray
            return data
        else:
            assert len(data_list) == 1
            return data_list[0]
    #--- End: def
    
    @classmethod
    def reconstruct_sectioned_data(cls, sections):
        """Expects a dictionary of Data objects with ordering information as
keys, as output by the section method when called with a Data
object. Returns a reconstructed cf.Data object with the sections in
the original order.

:Parameters:

    sections : `dict`
        The dictionary or Data objects with ordering information as
        keys.

:Returns:

    out: `Data`
        The resulting reconstructed Data object.

:Examples 2:

>>> d = cf.Data(numpy.arange(120).reshape(2, 3, 4, 5))
>>> x = d.section([1, 3])
>>> len(x)
8
>>> e = cf.Data.reconstruct_sectioned_data(x)
>>> e.equals(d)
True
        """
        ndims = len(sections.keys()[0])
        for i in range(ndims - 1, -1, -1):
            keys = sorted(sections.keys())
            if i==0:
                if keys[0][i] is None:
                    assert len(keys) == 1
                    return sections.values()[0]
                else:
                    data_list = []
                    for k in keys:
                        data_list.append(sections[k])

                    return cls.concatenate_data(data_list, i)
                #--- End: if
            else:
                if keys[0][i] is None:
                    pass
                else:
                    new_sections = {}
                    new_key = keys[0][:i]
                    data_list = []
                    for k in keys:
                        if k[:i] == new_key:
                            data_list.append(sections[k])
                        else:
                            new_sections[new_key] = cls.concatenate_data(data_list, i)
                            new_key = k[:i]
                            data_list = [sections[k]]
                    #--- End: for
                    new_sections[new_key] = cls.concatenate_data(data_list, i)
                    sections = new_sections
                #--- End: if
            #--- End: if
    #--- End: def

    def argmax(self, axis=None, unravel=False):
        '''Return the indices of the maximum values along an axis.

If no axis is specified then the returned index locates the maximum of
the whole data.

:Examples 1:

>>> d.argmax()

:Parameters:

    axis: `int`, optional
        The specified axis over which to locate te maximum values. By
        default the maximum over the whole data is located.

    unravel: `bool`, optional
        If True, then when locating the maximum over the whole data,
        return the location as a tuple of indices for each axis. By
        default an index to the flattened array is returned in this
        case.

:Returns:

    `Data` or `int` or `tuple`
        The location of the maximum, or maxima.

:Examples 2:

>>> d = cf.Data(numpy.arange(120).reshape(4, 5, 6))
>>> d.argmax()
119
>>> d.argmax(unravel=True)
(3, 4, 5)
>>> d.argmax(axis=1)
<CF Data: [[4, ..., 4]]>

        '''
        if axis is None:
            config = self.partition_configuration(readonly=True)

            out = []
            
            for partition in self.partitions.matrix.flat:
                partition.open(config)
                array = partition.array
                index = numpy_unravel_index(array.argmax(), array.shape)
                mx = array[index]
                index = [x[0] + i for x, i in zip(partition.location, index)]
                out.append((mx, index))
                partition.close()
                
            mx, index = sorted(out)[-1]

            if unravel:
                return tuple(index)

            return numpy_ravel_multi_index(index, self.shape) 
        #--- End: if
                
        # Parse axis
        ndim = self._ndim 
        if -ndim-1 <= axis < 0:
            axis += ndim + 1
        elif not 0 <= axis <= ndim:
            raise ValueError(
                "Invalid axis specification: {}".format(axis))

        sections = self.section([axis], chunks=True)
        for key, d in sections.iteritems():
            array = d.varray.argmax(axis=axis)
            sections[key] = type(self)(array, self.Units,
                                       fill_value=self.fill_value)

        return self.reconstruct_sectioned_data(sections)
    #--- End: def
            
    def max(self, axes=None, squeeze=False, mtol=1, i=False,
            _preserve_partitions=False):
        '''

Collapse axes with their maximum.

Missing data array elements are omitted from the calculation.

:Parameters:

    axes : (sequence of) int, optional

    squeeze : bool, optional

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data
        The collapsed array.

.. seealso:: `min`, `mean`, `mid_range`, `sum`, `sd`, `var`

:Examples:

'''
#        if weights is not None:
#            raise ValueError("can't weight max: %s" % weights)#

        return self._collapse(max_f, max_fpartial, max_ffinalise, axes=axes,
                              squeeze=squeeze, mtol=mtol, i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    def min(self, axes=None, squeeze=False, mtol=1, i=False,
            _preserve_partitions=False):
        '''

Collapse axes with their minimum.

Missing data array elements are omitted from the calculation.

:Parameters:

    axes : (sequence of) int, optional

    squeeze : bool, optional

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data
        The collapsed array.

.. seealso:: `max`, `mean`, `mid_range`, `sum`, `sd`, `var`
 
:Examples:

'''
        return self._collapse(min_f, min_fpartial, min_ffinalise, axes=axes,
                              squeeze=squeeze, mtol=mtol, i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    def mean(self, axes=None, squeeze=False, mtol=1, weights=None,
             i=False, _preserve_partitions=False):
        r'''

Collapse axes with their weighted mean.

The weighted mean, :math:`\mu`, for array elements :math:`x_i` and
corresponding weights elements :math:`w_i` is

.. math:: \mu=\frac{\sum w_i x_i}{\sum w_i}

Missing data array elements and their corresponding weights are
omitted from the calculation.

:Parameters:

    axes : (sequence of) int, optional
        The axes to be collapsed. By default flattened input is
        used. Each axis is identified by its integer position. No axes
        are collapsed if *axes* is an empty sequence.

    squeeze : bool, optional
        If True then collapsed axes are removed. By default the axes
        which are collapsed are left in the result as axes with size
        1, meaning that the result is guaranteed to broadcast
        correctly against the original array.

    weights : data-like or dict, optional
        Weights associated with values of the array. By default all
        non-missing elements of the array are assumed to have a weight
        equal to one. If *weights* is a data-like object then it must
        have either the same shape as the array or, if that is not the
        case, the same shape as the axes being collapsed. If *weights*
        is a dictionary then each key is axes of the array (an int or
        tuple of ints) with a corresponding data-like value of weights
        for those axes. In this case, the implied weights array is the
        outer product of the dictionary's values.

          Example: If ``weights={1: w, (2, 0): x}`` then ``w`` must
          contain 1-dimensionsal weights for axis 1 and ``x`` must
          contain 2-dimensionsal weights for axes 2 and 0. This is
          equivalent, for example, to ``weights={(1, 2, 0), y}``,
          where ``y`` is the outer product of ``w`` and ``x``. If
          ``axes=[1, 2, 0]`` then ``weights={(1, 2, 0), y}`` is
          equivalent to ``weights=y``. If ``axes=None`` and the array
          is 3-dimensionsal then ``weights={(1, 2, 0), y}`` is
          equivalent to ``weights=y.transpose([2, 0, 1])``.

    mtol : number, optional
        For each element in the output data array, the fraction of
        contributing input array elements which is allowed to contain
        missing data. Where this fraction exceeds *mtol*, missing
        data is returned. The default is 1, meaning a missing datum in
        the output array only occurs when its contributing input array
        elements are all missing data. A value of 0 means that a
        missing datum in the output array occurs whenever any of its
        contributing input array elements are missing data. Any
        intermediate value is permitted.

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data
        The collapsed array.

.. seealso:: `max`, `min`, `mid_range`, `range`, `sum`, `sd`, `var`

:Examples:

>>> d = cf.Data([[1, 2, 4], [1, 4, 9]], 'm')
>>> print d.array
[[1 2 4]
 [1 4 9]]

>>> d.mean()
<CF Data: 3.5 m>
>>> d.mean(squeeze=True)
<CF Data: [[3.5]] m>
>>> d.mean(axes=[0, 1])
<CF Data: 3.5 m>
>>> d.mean(axes=[1, 0])
<CF Data: 3.5 m>
>>> print d.mean(axes=0).array
[ 1.   3.   6.5]
>>> print d.mean(axes=1).array
[ 2.33333333  4.66666667]
>>> d.mean(axes=1, squeeze=True)
[[ 2.33333333]
 [ 4.66666667]]

>>> y = cf.Data([1, 3])
>>> x = cf.Data([1, 2, 1])
>>> w = cf.expand_dims(y, 1) * x
>>> print w.array
[[1 2 1]
 [3 6 3]]

>>> d.mean(weights=w)
<CF Data: 3.9375 m>
>>> d.mean(weights={(0, 1): w})
<CF Data: 3.9375 m>
>>> d.mean(axes=[0, 1], weights={(0, 1): w})
<CF Data: 3.9375 m>
>>> d.mean(axes=[1, 0], weights={(0, 1): w})
<CF Data: 3.9375 m>
>>> d.mean(axes=(0, 1), weights={1: x, 0: y})
<CF Data: 3.9375 m>

>>> d.mean(axes=1, weights=w)
<CF Data: [2.25, 4.5] m>
>>> d.mean(axes=1, weights=x)
<CF Data: [2.25, 4.5] m>
>>> d.mean(axes=1, weights={1: x})
<CF Data: [2.25, 4.5] m>
>>> d.mean(axes=1, weights={(0, 1): w})
<CF Data: [2.25, 4.5] m>
>>> d.mean(axes=1, weights={0: y, (1,): x})
<CF Data: [2.25, 4.5] m>

>>> d.mean(axes=1)
<CF Data: [2.33333333333, 4.66666666667] m>
>>> d.mean(axes=1, weights={0: y})
<CF Data: [2.33333333333, 4.66666666667] m>

>>> e = cf.Data(numpy.arange(24).reshape(3, 2, 4))
>>> print e.array
[[[ 0  1  2  3]
  [ 4  5  6  7]]
 [[ 8  9 10 11]
  [12 13 14 15]]
 [[16 17 18 19]
  [20 21 22 23]]]

>>> e.mean(axes=[0, 2])
<CF Data: [9.5, 13.5] >
>>> f = e.mean(axes=[0, 2], squeeze=True)
>>> f
<CF Data: [[[9.5, 13.5]]] >
>>> f.shape
(1, 2, 1)
>>> print e.mean(axes=[0, 1]).array
[ 10.  11.  12.  13.]
>>> print e.mean(axes=[0, 1], weights={(1, 0): w}).array
[ 11.  12.  13.  14.]

>>> e[0, 0] = cf.masked
>>> e[-1, -1] = cf.masked
>>> e[..., 2] = cf.masked
>>> print e.array
[[[-- -- -- --]
  [4 5 -- 7]]
 [[8 9 -- 11]
  [12 13 -- 15]]
 [[16 17 -- 19]
  [-- -- -- --]]]

>>> e.mean()
<CF Data: 11.3333333333 >
>>> print e.mean(axes=[0, 1]).array
[10.0 11.0 -- 13.0]
>>> print e.mean(axes=[0, 1], weights={(1, 0): w}).array
[9.666666666666666 10.666666666666666 -- 12.666666666666666]

'''
        return self._collapse(mean_f, mean_fpartial, mean_ffinalise,
                              axes=axes, squeeze=squeeze, weights=weights,
                              mtol=mtol, i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    def sample_size(self, axes=None, squeeze=False, mtol=1, i=False,
                    _preserve_partitions=False):
        r'''

:Parameters:

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

'''        
        return self._collapse(sample_size_f, sample_size_fpartial,
                              sample_size_ffinalise,
                              axes=axes, squeeze=squeeze, weights=None,
                              mtol=mtol, units=Units('1'), i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    @property
    def binary_mask(self):
        '''A binary (0 and 1) mask of the data array. 

The binary mask's data array comprises dimensionless 8-bit integers
and has 0 where the data array has missing data and 1 otherwise.

.. seealso:: `mask`

:Returns:

    out: Data
        The binary mask.

:Examples:

>>> print d.mask.array
[[ True False  True False]]
>>> b = d.binary_mask.array
>>> print b
[[0 1 0 1]]

        '''
        self.to_memory()

        binary_mask = self.copy()

        config = binary_mask.partition_configuration(readonly=False)   

        for partition in binary_mask.partitions.matrix.flat:            
            partition.open(config)
            array = partition.array

            array = array.astype(bool)
            if partition.masked:
                # data is masked
                partition.subarray = numpy_ma_array(array, 'int32')
            else:
                # data is not masked
                partition.subarray = numpy_array(array, 'int32')


            partition.Units = _units_1

            partition.close()
        #--- End: for

        binary_mask.Units = _units_1
        binary_mask.dtype = 'int32'

        return binary_mask
    #--- End: def

    def clip(self, a_min, a_max, units=None, i=False):
        '''

Clip (limit) the values in the data array in place.

Given an interval, values outside the interval are clipped to the
interval edges. For example, if an interval of [0, 1] is specified
then values smaller than 0 become 0 and values larger than 1 become 1.

Parameters :
 
    a_min: scalar

    a_max: scalar

    units: `str` or `cf.Units`

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns: 

    out: cf.Data

:Examples:

'''
        if i:
            d = self
        else:
            d = self.copy()

        if units is not None:
            # Convert the limits to the same units as the data array
            units = Units(units)

            self_units = d.Units

            if self_units != units:
                a_min = Units.conform(a_min, units, self_units)
                a_max = Units.conform(a_max, units, self_units)
        #--- End: if
            
        config = d.partition_configuration(readonly=False)
        
        for partition in d.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            array.clip(a_min, a_max, out=array)
            partition.close()

        return d
    #--- End: def

    @classmethod
    def asdata(cls, d, copy=False):
        '''Convert the input to a `cf.Data` object.

:Parameters:

    d : data-like
        Input data in any form that can be converted to an cf.Data
        object. This includes `cf.Data` and `cf.Field` objects, numpy
        arrays and any object which may be converted to a numpy array.

:Returns:

    out: cf.Data
        cf.Data interpretation of *d*. No copy is performed on the
        input.

:Examples:

>>> d = cf.Data([1, 2])
>>> cf.Data.asdata(d) is d
True
>>> d.asdata(d) is d
True

>>> cf.Data.asdata([1, 2])
<CF Data: [1, 2]>

>>> cf.Data.asdata(numpy.array([1, 2]))
<CF Data: [1, 2]>

        '''
        data = getattr(d, '__data__', None)
        if data is None:
            return cls(d)

        data = data()
        if copy:
            return data.copy()
        else:
            return data
    #--- End: def

    def close(self):
        '''

Close all files referenced by the data array.

Note that a closed file will be automatically reopened if its contents
are subsequently required.

:Returns:

    None

:Examples:

>>> d.close()

'''    
        for partition in self.partitions.matrix.flat:
            partition.file_close()
    #--- End: def
            
    def copy(self):
        '''

Return a deep copy.

``d.copy()`` is equivalent to ``copy.deepcopy(d)``.

:Returns:

    out: 
        The deep copy.

:Examples:

>>> e = d.copy()

'''
        new = Data.__new__(Data)   ###dch change

        new.__dict__ = self.__dict__.copy()

        new.partitions = self.partitions.copy()

        if new._auxiliary_mask is not None:
            new._auxiliary_mask = [mask.copy() for mask in self._auxiliary_mask]

        return new
    #--- End: def
            
    def cos(self, i=False):
        '''Take the trigonometric cosine of the data array in place.

Units are accounted for in the calculation. If the units are not
equivalent to radians (such as Kelvin) then they are treated as if
they were radians. For example, the the cosine of 90 degrees_east is
0.0, as is the sine of 1.57079632 kg m-2.

The Units are changed to '1' (nondimensionsal).

:Parameters:

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: `cf.Data`

:Examples:

>>> d.Units
<CF Units: degrees_east>
>>> print d.array
[[-90 0 90 --]]
>>> d.cos()
>>> d.Units
<CF Units: 1>
>>> print d.array
[[0.0 1.0 0.0 --]]

>>> d.Units
<CF Units: m s-1>
>>> print d.array
[[1 2 3 --]]
>>> d.cos()
>>> d.Units
<CF Units: 1>
>>> print d.array
[[0.540302305868 -0.416146836547 -0.9899924966 --]]

        '''
        if i:
            d = self
        else:
            d = self.copy()

        if d.Units.equivalent(_units_radians):           
            d.Units = _units_radians

        return d.func(numpy_cos, units=_units_1, i=True)
    #--- End: def

    def _var(self, partition, config):
        partition.open(config)
        v = partition.array
        v = v ** 2
        v = v + 1
        v = v ** 0.5
        v = v ** 2
        v = v + 1
        v = v ** 0.5
        v =  numpy_ma_var(v)
        print ' ', v
        partition.close()
        return v

#    def _var_test(self):
#        '''
#        '''
#        config = self.partition_configuration(readonly=True)
#
#        out = []
#        for partition in self.partitions.matrix.flat:
#            c = self._var(partition, config)
#            out.append(c)
#
#        result = delayed(sum)(out)
#
#        return result.compute(get=dask.threaded.get)
#
#    def _count(partition, config):
#        partition.open(config)
#        n = numpy_ma_count(partition.array)
#        partition.close()
#        return n
#    #--- End: def

    def count(self):
        '''Count the non-masked elements of the array.

:Examples 1:

>>> n = d.count()

:Returns:

    out: `int`

        '''
        config = self.partition_configuration(readonly=True)
        
        n = 0

        for partition in self.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            n += numpy_ma_count(array)  # not this
#            partition.output = numpy_ma_count(array) # but this! or return n?
            partition.close()
        #--- End: for

#if not parallel:    
#    for p in parations:
#        _worker(p)
#        if ?? : break
#else:
#    
#
        
        return n
    #--- End: def

    def count_masked(self):
        '''

'''
        return self._size - self.count()
    #--- End: def

    def cyclic(self, axes=None, iscyclic=True):
        '''

:Parameters:

:Returns:

    out: set

:Examples:

'''
        cyclic_axes = self._cyclic
        data_axes   = self._axes

        old = set([data_axes.index(axis) for axis in cyclic_axes])

        if axes is None:
            return old

        axes = [data_axes[i] for i in self._parse_axes(axes, 'cyclic')]

        if iscyclic:
            self._cyclic = cyclic_axes.union(axes)
        else:
            self._cyclic = cyclic_axes.difference(axes)

        # Make sure that the auxiliary mask has the same cyclicity
        if self._auxiliary_mask:
            for mask in self._auxiliary_mask:
                mask.cyclic(axes_in, iscyclic)

        return old
    #--- End: def

    def _YMDhms(self, attr):
        '''

.. seealso:: `~cf.Data.year`, ~cf.Data.month`, `~cf.Data.day`,
             `~cf.Data.hour`, `~cf.Data.minute`, `~cf.Data.second`

        '''
        def _func(array, units_in, dummy0, dummy1):
            '''

    The returned array is always independent.

    :Parameters:

        array: numpy array
        
        units_in: `cf.Units`
        
        dummy0:
            Ignored.

        dummy1:
            Ignored.

    :Returns: 

        out: numpy array

    '''
            if not self._isdatetime():
                array = rt2dt(array, units_in)

            return _array_getattr(array, attr)
        #--- End: def

        if not self.Units.isreftime:
            raise ValueError(
                "Can't get {}s from data with {!r}".format(attr, self.Units))

        new = self.copy()

        new._Units  = _units_None

        config = new.partition_configuration(readonly=False, func=_func, dtype=None)

        for partition in new.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            new_dtype = array.dtype
            partition.close()
        #--- End: for

        new._dtype = new_dtype

        return new
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def year(self):
        '''

The year of each data array element.

Only applicable for reference time units.

.. seealso:: `~cf.Data.month`, `~cf.Data.day`, `~cf.Data.hour`,
             `~cf.Data.minute`, `~cf.Data.second`

:Examples:

>>> d = cf.Data([[1.93, 5.17]], 'days since 2000-12-29')
>>> d
<CF Data: [[2000-12-30 22:19:12, 2001-01-03 04:04:48]] >
>>> d.year
<CF Data: [[2000, 2001]] >

'''
        return self._YMDhms('year')
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def month(self):
        '''

The month of each data array element.

Only applicable for reference time units.

.. seealso:: `~cf.Data.year`, `~cf.Data.day`, `~cf.Data.hour`,
             `~cf.Data.minute`, `~cf.Data.second`

:Examples:

>>> d = cf.Data([[1.93, 5.17]], 'days since 2000-12-29')
>>> d
<CF Data: [[2000-12-30 22:19:12, 2001-01-03 04:04:48]] >
>>> d.month
<CF Data: [[12, 1]] >

'''
        return self._YMDhms('month')
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def day(self):
        '''

The day of each data array element.

Only applicable for reference time units.

.. seealso:: `~cf.Data.year`, `~cf.Data.month`, `~cf.Data.hour`,
             `~cf.Data.minute`, `~cf.Data.second`

:Examples:

>>> d = cf.Data([[1.93, 5.17]], 'days since 2000-12-29')
>>> d
<CF Data: [[2000-12-30 22:19:12, 2001-01-03 04:04:48]] >
>>> d.day
<CF Data: [[30, 3]] >

'''
        return self._YMDhms('day')
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def hour(self):
        '''

The hour of each data array element.

Only applicable for reference time units.

.. seealso:: `~cf.Data.year`, `~cf.Data.month`, `~cf.Data.day`,
             `~cf.Data.minute`, `~cf.Data.second`

:Examples:

>>> d = cf.Data([[1.93, 5.17]], 'days since 2000-12-29')
>>> d
<CF Data: [[2000-12-30 22:19:12, 2001-01-03 04:04:48]] >
>>> d.hour
<CF Data: [[22, 4]] >

'''
        return self._YMDhms('hour')
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def minute(self):
        '''

The minute of each data array element.

Only applicable for reference time units.

.. seealso:: `~cf.Data.year`, `~cf.Data.month`, `~cf.Data.day`,
             `~cf.Data.hour`, `~cf.Data.second`

:Examples:

>>> d = cf.Data([[1.93, 5.17]], 'days since 2000-12-29')
>>> d
<CF Data: [[2000-12-30 22:19:12, 2001-01-03 04:04:48]] >
>>> d.minute
<CF Data: [[19, 4]] >

'''
        return self._YMDhms('minute')
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def second(self):
        '''

The second of each data array element.

Only applicable for reference time units.

.. seealso:: `~cf.Data.year`, `~cf.Data.month`, `~cf.Data.day`,
             `~cf.Data.hour`, `~cf.Data.minute`

>>> d = cf.Data([[1.93, 5.17]], 'days since 2000-12-29')
>>> d
<CF Data: [[2000-12-30 22:19:12, 2001-01-03 04:04:48]] >
>>> d.second
<CF Data: [[12, 48]] >

'''
        return self._YMDhms('second')
    #--- End: def

    def unique(self):
        '''

The unique elements of the array.

Returns a new object with the sorted unique elements in a one
dimensional array.

:Examples:

>>> d = cf.Data([[4, 2, 1], [1, 2, 3]], 'metre')
>>> d.unique()
<CF Data: [1, 2, 3, 4] metre>
>>> d[1, -1] = cf.masked
>>> d.unique()
<CF Data: [1, 2, 4] metre>

'''
        config = self.partition_configuration(readonly=True)

        u = []
        for partition in self.partitions.matrix.flat:
            partition.open(config)
            array = partition.array
            array = numpy_unique(array)

            if partition.masked:
                # Note that compressing a masked array may result in
                # an array with zero size
                array = array.compressed()

            size = array.size
            if size > 1:
                u.extend(array)
            elif size == 1:
                u.append(array.item())

            partition.close()
        #--- End: for

        u = numpy_unique(numpy_array(u, dtype=self.dtype))

        return type(self)(u, units=self.Units) #, dt=self._isdt)
    #--- End: def

    def dump(self, display=True, prefix=None):
        '''

Return a string containing a full description of the instance.

:Parameters:

    display : bool, optional
        If False then return the description as a string. By default
        the description is printed, i.e. ``d.dump()`` is equivalent to
        ``print d.dump(display=False)``.

    prefix : str, optional
       Set the common prefix of component names. By default the
       instance's class name is used.

:Returns:

    out: None or str
        A string containing the description.

:Examples:

'''
        if prefix is None:
            prefix = self.__class__.__name__
            
        string = ['{0}.shape = {1}'.format(prefix, self._shape)]

        if self._size == 1:
            string.append('{0}.first_datum = {1}'.format(prefix, self.datum(0)))
        else:
            string.append('{0}.first_datum = {1}'.format(prefix, self.datum(0)))
            string.append('{0}.last_datum  = {1}'.format(prefix, self.datum(-1)))
            
        for attr in ('fill_value', 'Units'):
            string.append('{0}.{1} = {2!r}'.format(prefix, attr, getattr(self, attr)))
        #--- End: for

        string = '\n'.join(string)
       
        if display:
            print string
        else:
            return string
    #--- End: def

#    def equivalent(self, other, rtol=None, atol=None, traceback=False,
#                   copy=True):
#        '''
#
#True if and only if two data arrays are logically equivalent.
#
#Equivalence is defined as both data arrays being the same after
#accounting for different but equivalent units.* units
#
#:Parameters:
#
#    other : Data
#
#    atol : float, optional
#        The absolute tolerance for all numerical comparisons. By
#        default the value returned by the `ATOL` function is used.
#
#    rtol : float, optional
#        The relative tolerance for all numerical comparisons. By
#        default the value returned by the `RTOL` function is used.
#
#:Returns:
#
#    out: bool
#        Whether or not the two variables are equivalent.
#
#'''     
#        if self._shape != other._shape:
#            # add traceback
#            return
#
#        if not self.Units.equivalent(other.Units):
#            # add traceback
#            return 
#       
##        if axis_map:
##            axes = [axis_map[axis] for axis in self._axes]
##            if axes == other._axes:
##                axis_map = None
##
##        if not axis_map and self._shape != other._shape:
##            # add traceback
##            return
## 
#        self_Units      = self.Units
##        self_fill_value = self._fill_value
##        if self_Units == other.Units and self_fill_value == other._fill_value:
##            copy = False
#
#        if self_Units != other.Units:
#            if copy:
#                other = other.copy()
#                copy = False
#            other.Units = self_Units
#
#
##        if copy:
##            other = other.copy()
##
##        if axis_map:
##            other.transpose(axes)
##
##        other.Units       = self_Units
##        other._fill_value = self_fill_value
#
#        return self.equals(other, rtol=rtol, atol=atol, ignore_fill_value=True,
#                           traceback=False)
#    #--- End: def

    def ndindex(self):
        '''

Return an iterator over the N-dimensional indices of the data array.

At each iteration a tuple of indices is returned, the last dimension
is iterated over first.

:Returns:

    out: itertools.product
        An iterator over tuples of indices of the data array.

:Examples:

>>> d.shape
(2, 1, 3)
>>> for i in d.ndindex():
...     print i
...
(0, 0, 0)
(0, 0, 1)
(0, 0, 2)
(1, 0, 0)
(1, 0, 1)
(1, 0, 2)

> d.shape
()
>>> for i in d.ndindex():
...     print i
...
()

'''
        return itertools_product(*[xrange(0, r) for r in self._shape])  
    #--- End: def

    def equals(self, other, rtol=None, atol=None, ignore_fill_value=False,
               traceback=False):
        '''

True if two data arrays are logically equal, False otherwise.

:Parameters:

    other : 
        The object to compare for equality.

    atol : float, optional
        The absolute tolerance for all numerical comparisons. By
        default the value returned by the `ATOL` function is used.

    rtol : float, optional
        The relative tolerance for all numerical comparisons. By
        default the value returned by the `RTOL` function is used.

    ignore_fill_value : bool, optional
        If True then data arrays with different fill values are
        considered equal. By default they are considered unequal.

    traceback : bool, optional
        If True then print a traceback highlighting where the two
        instances differ.

:Returns: 

    out: bool
        Whether or not the two instances are equal.

:Examples:

>>> d.equals(d)
True
>>> d.equals(d + 1)
False

'''
        # Check each instance's id
        if self is other:
            return True
 
        # Check that each instance is the same type
        if self.__class__ != other.__class__:
            if traceback:
                print("%s: Different type: %s" %
                      (self.__class__.__name__, other.__class__.__name__))
            return False

        # Check that each instance has the same shape
        if self._shape != other._shape:
            if traceback:
                print("%s: Different shape: %s, %s" %
                      (self.__class__.__name__, self._shape, other._shape))
            return False
        #--- End: if

        # Check that each instance has the same units
        self_Units  = self.Units
        other_Units = other.Units
        if self_Units != other_Units:
            if traceback:
                print("%s: Different Units (%r, %r)" %
                      (self.__class__.__name__, self.Units, other.Units))
            return False
        #--- End: if

        # Check that each instance has the same fill value
        if not ignore_fill_value and self._fill_value != other._fill_value:
            if traceback:
                print("%s: Different fill values (%s, %s)" %
                      (self.__class__.__name__,
                       self._fill_value, other._fill_value))
            return False
        #--- End: if

        # ------------------------------------------------------------
        # Check that each instance has equal array values
        # ------------------------------------------------------------
        # Set default tolerances
        if rtol is None:
            rtol = RTOL()
        if atol is None:
            atol = ATOL()        

        config = self.partition_configuration(readonly=True)

        other.to_memory()
        
        for partition in self.partitions.matrix.flat:
            partition.open(config)
            array0 = partition.array
            array1 = other[partition.indices].varray
            partition.close()

            if not _numpy_allclose(array0, array1, rtol=rtol, atol=atol):
                if traceback:
                    print("{}: Different data array values".format(
                        self.__class__.__name__))
                return False
        #--- End: for

        # ------------------------------------------------------------
        # Still here? Then the two instances are equal.
        # ------------------------------------------------------------
        return True            
    #--- End: def

    def exp(self, i=False):
        '''

Take the exponential of the data array.

:Parameters:

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

'''
        units = self.Units
        if units and not units.isdimensionless:
            raise ValueError(
"Can't take exponential of dimensional quantities: {0!r}".format(units))

        if i:
            d = self
        else:
            d = self.copy()

        if d.Units:
            d.Units = _units_1 

        return d.func(numpy_exp, i=True)
    #--- End: def

    def expand_dims(self, position=0, i=False):
        '''

Expand the shape of the data array in place.

Insert a new size 1 axis, corresponding to a given position in the
data array shape.

.. seealso:: `flip`, `squeeze`, `swapaxes`, `transpose`

:Parameters:

    position : int, optional
        Specify the position that the new axis will have in the data
        array axes. By default the new axis has position 0, the
        slowest varying position.

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

'''

        # Parse position
        ndim = self._ndim 
        if -ndim-1 <= position < 0:
            position += ndim + 1
        elif not 0 <= position <= ndim:
            raise ValueError(
                "Can't expand_dims: Invalid position (%d)" % position)
        #--- End: for

        if i:
            d = self
        else:
            d = self.copy()

        # Expand _axes
        axis = d._new_axis_identifier()
        data_axes = d._axes[:]
        data_axes.insert(position, axis)
        d._axes = data_axes

        # Increment ndim and expand shape
        d._ndim += 1
        shape = list(d._shape)
        shape.insert(position, 1)   
        d._shape = tuple(shape)

        # Expand the location and shape of each partition
        location = (0, 1)
        for partition in d.partitions.matrix.flat:
            partition.location = partition.location[:]
            partition.shape    = partition.shape[:]
            
            partition.location.insert(position, location)
            partition.shape.insert(position, 1)
        #--- End: for
        
        if d._all_axes:
            d._all_axes += (axis,)

        # HDF chunks
        if self._HDF_chunks:
            self._HDF_chunks[axis] = 1

        # Expand dims in the auxiliary mask
        if d._auxiliary_mask:
            for mask in d._auxiliary_mask:
                mask.expand_dims(position, i=True)

        return d
    #--- End: def

    def files(self):
        '''Return the names of files containing parts of the data array.

:Returns:

    out: set
        The file names in normalized, absolute form.

:Examples:

>>> f = cf.read('../file*')
>>> f[0].files()
{'/data/user/file1',
 '/data/user/file2',
 '/data/user/file3'}
>>> a = f[0].array
>>> f[0].files()
set()

        '''
        return set([p.subarray.file
                    for p in self.partitions.matrix.flat if p.in_file])
    #--- End: def

    def flat(self, ignore_masked=True):
        '''

Return a flat iterator over elements of the data array.

:Parameters:

    ignore_masked : bool, optional
        If False then masked and unmasked elements will be returned. By
        default only unmasked elements are returned

:Returns:

    out: generator
        An iterator over elements of the data array.

:Examples:

>>> print d.array
[[1 -- 3]]
>>> for x in d.flat():
...     print x
...
1
3

>>> for x in d.flat(False):
...     print x
...
1
--
3

'''
        self.to_memory()

        mask = self.mask

        if ignore_masked:
            for index in self.ndindex():
                if not mask[index]:
                    yield self[index].unsafe_array.item()
        else:
            for index in self.ndindex():
                if not mask[index]:
                    yield self[index].unsafe_array.item()
                else:
                    yield cf_masked
    #--- End: def

    def floor(self, i=False):
        '''

Return the floor of the data array.

.. versionadded:: 1.0

.. seealso:: `ceil`, `rint`, `trunc`

:Parameters:

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

>>> print d.array
[-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
>>> print d.floor().array
[-2. -2. -2. -1.  0.  1.  1.  1.  1.]

'''
        return self.func(numpy_floor, out=True, i=i)
    #---End: def

    def outerproduct(self, e, i=False):
        '''

Compute the outer product with another data array.

The axes of result will be the combined axes of the two input arrays:

>>> d.outerproduct(e).ndim == d.ndim + e.ndim
True
>>> d.outerproduct(e).shape == d.shape + e.shape
True

:Parameters:

    e : data-like
        The data array with which to form the outer product.

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

>>> d = cf.Data([1, 2, 3], 'metre')
>>> o = d.outerproduct([4, 5, 6, 7])
>>> o
<CF Data: [[4, ..., 21]] m>
>>> print o.array
[[ 4  5  6  7]
 [ 8 10 12 14]
 [12 15 18 21]]

>>> e = cf.Data([[4, 5, 6, 7], [6, 7, 8, 9]], 's-1')
>>> o = d.outerproduct(e)
>>> o
<CF Data: [[[4, ..., 27]]] m.s-1>
>>> print d.shape, e.shape, o.shape
(3,) (2, 4) (3, 2, 4)
>>> print o.array
[[[ 4  5  6  7]
  [ 6  7  8  9]]
 [[ 8 10 12 14]
  [12 14 16 18]]
 [[12 15 18 21]
  [18 21 24 27]]]

'''
        e_ndim = numpy_ndim(e)

        if e_ndim:
            d = self.copy()
            for j in range(e_ndim):
                d.expand_dims(-1, i=True)
        else:
            d = self

        d = d*e

        if i:
            # Update self in place
            self.__dict__ = d.__dict__

        return d
    #--- End: def

    def change_calendar(self, calendar, i=False):
        '''Change the calendar of the data array elements.

Changing the calendar could result in a change of reference time data
array values.

Not to be confused with using the `override_calendar` method or
resetting `d.Units`. `override_calendar` is different because the new
calendar need not be equivalent to the original ones and the data
array elements will not be changed to reflect the new units. Resetting
`d.Units` will 

        '''
        if not self.Units.isreftime:
            raise ValueError(
"Can't change calendar of non-reference time units: {!r}".format(self.Units))

        if i:
            d = self
        else:
            d = self.copy()

        d._asdatetime(i=True)
        d.override_units(Units(self.Units.units, calendar), i=True)
        d._asreftime(i=True)

        return d
    #--- End: def

    def override_units(self, units, i=False):
        '''

Override the data array units.

Not to be confused with setting the `Units` attribute to units which
are equivalent to the original units. This is different because in
this case the new units need not be equivalent to the original ones
and the data array elements will not be changed to reflect the new
units.

:Parameters:

    units: `str` or `cf.Units`
        The new units for the data array.

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: `cf.Data`

:Examples:

>>> d = cf.Data(1012.0, 'hPa')
>>> d.override_units('km')
>>> d.Units
<CF Units: km>
>>> d.datum(0)
1012.0
>>> d.override_units(cf.Units('watts'))
>>> d.Units
<CF Units: watts>
>>> d.datum(0)
1012.0

'''
        if i:
            d = self
        else:
            d = self.copy()

        units = Units(units)
 
        config = self.partition_configuration(readonly=False)

        for partition in d.partitions.matrix.flat:
            p_units = partition.Units
            if not p_units or p_units == units:
                # No need to create the data array if the sub-array
                # units are the same as the master data array units or
                # the partition units are not set
                partition.Units = units
                continue

            partition.open(config)
            partition.array
            partition.Units = units
            partition.close()
        #--- End: for

        d._Units = units

        return d
    #--- End: def

    def override_calendar(self, calendar, i=False):
        '''Override the calendar of the data array elements.

Not to be confused with using the `change_calendar` method or setting
the `d.Units.calendar`. `override_calendar` is different because the
new calendar need not be equivalent to the original ones and the data
array elements will not be changed to reflect the new units.

:Parameters:

    calendar : str
        The new calendar.

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

        '''
        if not self.Units.isreftime:
            raise ValueError(
"Can't override the calender of non-reference-time units: {0!r}".format(
    self.Units))

        if i:
            d = self
        else:
            d = self.copy()

        for partition in d.partitions.matrix.flat:            
            partition.Units = Units(partition.Units._units, calendar)
            partition.close()
        #--- End: for

        d._Units = Units(d.Units._units, calendar)

        return d
    #--- End: def

    def to_disk(self):
        '''Store the data array on disk.

There is no change to partition's whose sub-arrays are already on
disk.

:Returns:

    None

:Examples:

>>> d.to_disk()

        '''
        config = self.partition_configuration(readonly=True, to_disk=True)

        for partition in self.partitions.matrix.flat:
            if partition.in_memory:
                partition.open(config)
                partition.array
                partition.close()
    #--- End: def

    def to_memory(self, regardless=False, parallelise=False):
        '''Store each partition's data in memory in place if the master array is
smaller than the chunk size.

There is no change to partitions with data that are already in memory.

:Parameters:
    
    regardless : bool, optional
        If True then store all partitions' data in memory regardless
        of the size of the master array. By default only store all
        partitions' data in memory if the master array is smaller than
        the chunk size.

    parallelise : bool, optional If True than only move those
        partitions to memory that are flagged for processing on this
        rank

:Returns:

    None

:Examples:

>>> d.to_memory()
>>> d.to_memory(regardless=True)

        '''
        config = self.partition_configuration(readonly=True)
        fm_threshold = FM_THRESHOLD()

        # If parallelise is False then all partitions are flagged for
        # processing on this rank, otherwise only a subset are
        self._flag_partitions_for_processing(parallelise)

        for partition in self.partitions.matrix.flat:
            if partition._process_partition:
                # Only move the partition to memory if it is flagged
                # for processing
                partition.open(config)
                if partition.on_disk and partition.nbytes <= FREE_MEMORY()-fm_threshold:
                    partition.array
                    
                partition.close()
            #--- End: if
        #--- End: for
    #--- End: def

    # ----------------------------------------------------------------
    # Attribute (read only)
    # ----------------------------------------------------------------
    @property
    def in_memory(self):
        '''

:Returns:

:Examples:

>>> d.in_memory

'''
        for partition in self.partitions.matrix.flat:
            if not partition.in_memory:
                return False
        #--- End: for

        return True
    #--- End: def

    def partition_boundaries(self):
        '''

Return the partition boundaries for each partition matrix dimension.

:Returns:

    out: dict

:Examples:

'''            
        return self.partitions.partition_boundaries(self._axes)
    #--- End: def

    def partition_configuration(self, readonly, **kwargs):
        '''Return parameters for opening and closing array partitions.

If dtype=None then data type checking is disabled.

        '''
        config = {'readonly'       : readonly,
                  'axes'           : self._axes,
                  'flip'           : self._flip,
                  'hardmask'       : self._hardmask,
                  'auxiliary_mask' : self._auxiliary_mask,
                  'units'          : self.Units,
                  'dtype'          : self.dtype,
                  'func'           : None,
                  'update'         : True,
                  'serial'         : True,
              }
          
        if kwargs:
            config.update(kwargs)

        return config
    #--- End: def

    def datum(self, *index):
        '''

Return an element of the data array as a standard Python scalar.

The first and last elements are always returned with ``d.datum(0)``
and ``d.datum(-1)`` respectively, even if the data array is a scalar
array or has two or more dimensions.

The returned object is of the same type as is stored internally.

.. seealso:: `array`, `dtarray`

:Parameters:

    index : *optional*
        Specify which element to return. When no positional arguments
        are provided, the method only works for data arrays with one
        element (but any number of dimensions), and the single element
        is returned. If positional arguments are given then they must
        be one of the following:

          * An integer. This argument is interpreted as a flat index
            into the array, specifying which element to copy and
            return.
         
              Example: If the data aray shape is ``(2, 3, 6)`` then:
                * ``d.datum(0)`` is equivalent to ``d.datum(0, 0, 0)``.
                * ``d.datum(-1)`` is equivalent to ``d.datum(1, 2, 5)``.
                * ``d.datum(16)`` is equivalent to ``d.datum(0, 2, 4)``.

            If *index* is ``0`` or ``-1`` then the first or last data
            array element respecitively will be returned, even if the
            data array is a scalar array.
        ..
         
          * Two or more integers. These arguments are interpreted as a
            multidimensionsal index to the array. There must be the
            same number of integers as data array dimensions.
        ..
         
          * A tuple of integers. This argument is interpreted as a
            multidimensionsal index to the array. There must be the
            same number of integers as data array dimensions.
         
              Example: ``d.datum((0, 2, 4))`` is equivalent to
              ``d.datum(0, 2, 4)``; and ``d.datum(())`` is equivalent
              to ``d.datum()``.

:Returns:

    out :
        A copy of the specified element of the array as a suitable
        Python scalar.

:Examples:

>>> d = cf.Data(2)
>>> d.datum()
2
>>> 2 == d.datum(0) == d.datum(-1) == d.datum(())
True

>>> d = cf.Data([[2]])
>>> 2 == d.datum() == d.datum(0) == d.datum(-1)
True
>>> 2 == d.datum(0, 0) == d.datum((-1, -1)) == d.datum(-1, 0)
True

>>> d = cf.Data([[4, 5, 6], [1, 2, 3]], 'metre')
>>> d[0, 1] = cf.masked
>>> print d
[[4 -- 6]
 [1 2 3]]
>>> d.datum(0)
4
>>> d.datum(-1)
3
>>> d.datum(1)
masked
>>> d.datum(4)
2
>>> d.datum(-2)
2
>>> d.datum(0, 0)
4
>>> d.datum(-2, -1)
6
>>> d.datum(1, 2)
3
>>> d.datum((0, 2))
6


'''
        if index:
            n_index = len(index)
            if n_index == 1:
                index = index[0]
                if index == 0:
                    # This also works for scalar arrays
                    index = (slice(0, 1),) * self._ndim
                elif index == -1:
                    # This also works for scalar arrays
                    index = (slice(-1, None),) * self._ndim
                elif isinstance(index, (int, long)):
                    if index < 0:
                        index += self._size

                    index = numpy_unravel_index(index, self._shape)
                elif len(index) != self._ndim:
                    raise ValueError(
                        "Incorrect number of indices for %s array" %
                        self.__class__.__name__)
                #--- End: if
            elif n_index != self._ndim:
                raise ValueError(
                    "Incorrect number of indices for %s array" %
                    self.__class__.__name__)

            array = self[index].array

        elif self._size == 1:
            array = self.array

        else:
            raise ValueError(
                "Can only convert a {} array of size 1 to a Python scalar".format(
    self.__class__.__name__))

        if not numpy_ma_isMA(array):
            return array.item()
        
        mask = array.mask
        if mask is numpy_ma_nomask or not mask.item():
            return array.item()

        return cf_masked
    #--- End: def
  
    def mask_invalid(self, i=False):
        '''Mask the array where invalid values occur (NaN or inf).

Note that:

* Invalid values in the results of arithmetic operations may only
  occur if the raising of `FloatingPointError` exceptions has been
  suppressed by `cf.Data.seterr`.

* If the raising of `FloatingPointError` exceptions has been allowed
  then invalid values in the results of arithmetic operations it is
  possible for them to be automatically converted to masked values,
  depending on the setting of `cf.Data.mask_fpe`. In this case, such
  automatic conversion might be faster than calling `mask_invalid`.

.. seealso:: `cf.Data.mask_fpe`, `cf.Data.seterr`

:Parameters:

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples 2:

>>> d = cf.Data([0., 1])
>>> e = cf.Data([1., 2])
>>> old = cf.Data.seterr('ignore')

>>> f = e/d
>>> f
<CF Data: [inf, 2.0] >
>>> f.mask_invalid()
<CF Data: [--, 2.0] >

>>> f=e**12345
>>> f
<CF Data: [1.0, inf] >
>>> f.mask_invalid()
<CF Data: [1.0, --] >

>>> old = cf.Data.seterr('raise')
>>> old = cf.Data.mask_fpe(True)
>>> e/d
<CF Data: [--, 2.0] >
>>> e**12345
<CF Data: [1.0, --] >

        '''
        if i:
            d = self
        else:
            d = self.copy()

        config = d.partition_configuration(readonly=False)
                                           
        for partition in d.partitions.matrix.flat:
            partition.open(config)
            array = partition.array

            array = numpy_ma_masked_invalid(array, copy=False)
            array.shrink_mask()
            if array.mask is numpy_ma_nomask:
                array = array.data

            partition.subarray = array
            
            partition.close()
        #--- End: for

        return d
    #--- End: def

    def mid_range(self, axes=None, squeeze=True, mtol=1, i=False,
                  _preserve_partitions=False):
        '''

Collapse axes with the unweighted average of their maximum and minimum
values.

Missing data array elements are omitted from the calculation.

.. seealso:: `max`, `min`, `mean`, `range`, `sum`, `sd`, `var`

:Parameters:

    axes : (sequence of) int, optional

    squeeze : bool, optional

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data
        The collapsed array.

:Examples:

        '''
        return self._collapse(mid_range_f, mid_range_fpartial, mid_range_ffinalise,
                              axes=axes, squeeze=squeeze, mtol=mtol, i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    def flip(self, axes=None, i=False):
        '''Reverse the direction of axes of the data array.

.. seealso:: `expand_dims`, `squeeze`, `swapaxes`, `transpose`

:Parameters:

    axes: (sequence of) `int`
        Select the axes. By default all axes are flipped. Each axis is
        identified by its integer position. No axes are flipped if
        *axes* is an empty sequence.

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: `cf.Data`

:Examples:

>>> d.flip()
>>> d.flip(1)
>>> d.flip([0, 1])
>>> d.flip([])

>>> e = d[::-1, :, ::-1]
>>> d.flip((2, 0)).equals(e)
True

        '''
        if i:
            d = self
        else:
            d = self.copy()
            
        if axes is not None and not axes and axes != 0:
            # Null flip
            return d

        if axes is None:
            iaxes = range(d._ndim)
        else:
            iaxes = d._parse_axes(axes, 'flip')

        reverse    = d._flip[:]
        data_axes  = d._axes       
        partitions = d.partitions
        _pmaxes    = partitions.axes

        flip_partition_matrix = False
        if _pmaxes:
            indices = [slice(None)] * partitions.ndim

        for i in iaxes:
            axis = data_axes[i]

            if axis in reverse:
                reverse.remove(axis)
            else:
                reverse.append(axis)

            if axis in _pmaxes:
                # This flip axis is also an axis of the partition
                # matrix
                indices[_pmaxes.index(axis)] = slice(None, None, -1)
                flip_partition_matrix = True
        #--- End: for
                
        d._flip = reverse

        if flip_partition_matrix:
            # At least one of the flip axes is also an axis of the
            # partition matrix
            partitions = partitions[tuple(indices)]
            partitions.set_location_map(data_axes)
            d.partitions = partitions

        # Flip the auxiliary mask
        if d._auxiliary_mask:
            for mask in d._auxiliary_mask:
                mask.flip(iaxes, i=True)
        #--- End: if
        
        return d
    #--- End: def
    
    def HDF_chunks(self, *chunks):
        '''
        '''
        _HDF_chunks = self._HDF_chunks

        if _HDF_chunks is None:
            _HDF_chunks = {}
        else:
            _HDF_chunks = _HDF_chunks.copy()

        org_HDF_chunks = dict([(i, _HDF_chunks.get(axis))
                               for i, axis in enumerate(self._axes)])

        if not chunks:
            return org_HDF_chunks

        chunks = chunks[0]
        
        if chunks is None:
            # Clear all chunking
            self._HDF_chunks = None
            return org_HDF_chunks

        axes = self._axes
        for axis, size in chunks.iteritems():
            _HDF_chunks[axes[axis]] = size

        if _HDF_chunks.values() == [None] * self._ndim:
            _HDF_chunks = None

        self._HDF_chunks = _HDF_chunks
            
        return org_HDF_chunks
    #--- End: def

    def inspect(self):
        '''

Inspect the object for debugging.

.. seealso:: `cf.inspect`

:Returns: 

    None

'''
        print cf_inspect(self)
    #--- End: def

    def isclose(self, y, rtol=None, atol=None):
        '''Return a boolean data array showing where two broadcastable arrays
have equal values within a tolerance.

For numeric data arrays, ``d.isclose(y, rtol, atol)`` is equivalent to
``abs(d - y) <= ``atol + rtol*abs(y)``, otherwise it is equivalent to
``d == y``.

:Parameters:

    y: data_like

    atol: `float`, optional
        The absolute tolerance for all numerical comparisons. By
        default the value returned by the `ATOL` function is used.

    rtol: `float`, optional
        The relative tolerance for all numerical comparisons. By
        default the value returned by the `RTOL` function is used.

:Returns:

     out: `bool`

:Examples:

>>> d = cf.Data([1000, 2500], 'metre')
>>> e = cf.Data([1, 2.5], 'km')
>>> print d.isclose(e).array
[ True  True]

>>> d = cf.Data(['ab', 'cdef'])
>>> print d.isclose([[['ab', 'cdef']]]).array
[[[ True  True]]]

>>> d = cf.Data([[1000, 2500], [1000, 2500]], 'metre')
>>> e = cf.Data([1, 2.5], 'km')
>>> print d.isclose(e).array
[[ True  True]
 [ True  True]]

>>> d = cf.Data([1, 1, 1], 's')
>>> print d.isclose(1).array
[ True  True  True]

        '''     
        if atol is None:
            atol = ATOL()        
        if rtol is None:
            rtol = RTOL()

        units0 = self.Units
        units1 = getattr(y, 'Units', _units_None)
        if units0.isreftime and units1.isreftime:
            if not units0.equals(units1):
                if not units0.equivalent(units1):
                    pass

            x = self.override_units(_units_1)
            y = y.copy()
            y.Units = units0
            y.override_units(_units_1, i=True)
        else:
            x = self

        try:
            return abs(x - y) <= atol + rtol*abs(y)
        except (TypeError, NotImplementedError, IndexError):
            return self == y
    #--- End: def

    def rint(self, i=False):
        '''

Round elements of the data array to the nearest integer.

.. versionadded:: 1.0

.. seealso:: `ceil`, `floor`, `trunc`

:Parameters:

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

    >>> print d.array
    [-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
    >>> print d.rint().array
    [-2. -2. -1. -1.  0.  1.  1.  2.  2.]

'''
        return self.func(numpy_rint, out=True, i=i)
    #---End: def

    def round(self, decimals=0, i=False):
        '''Evenly round elements of the data array to the given number of
decimals.


.. note:: Values exactly halfway between rounded decimal values are
          rounded to the nearest even value. Thus 1.5 and 2.5 round to
          2.0, -0.5 and 0.5 round to 0.0, etc. Results may also be
          surprising due to the inexact representation of decimal
          fractions in the IEEE floating point standard and errors
          introduced when scaling by powers of ten.

.. versionadded:: 1.1.4

.. seealso:: `ceil`, `floor`, `rint`, `trunc`

:Parameters:
	
    decimals : `int`, optional
        Number of decimal places to round to (default: 0). If decimals
        is negative, it specifies the number of positions to the left
        of the decimal point.

    i : `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out : `cf.Data`

:Examples:

>>> print d.array
[-1.81, -1.41, -1.01, -0.91,  0.09,  1.09,  1.19,  1.59,  1.99])
>>> print d.round().array
[-2., -1., -1., -1.,  0.,  1.,  1.,  2.,  2.]
>>> print d.round(1).array
[-1.8, -1.4, -1. , -0.9,  0.1,  1.1,  1.2,  1.6,  2. ]
>>> print d.round(-1).array
[-0., -0., -0., -0.,  0.,  0.,  0.,  0.,  0.]

        '''
        return self.func(numpy_round, out=True, i=i, decimals=decimals)
    #---End: def

    def swapaxes(self, axis0, axis1, i=False):
        '''

Interchange two axes of an array.

.. seealso:: `expand_dims`, `flip`, `squeeze`, `transpose`

:Parameters:

    axis0, axis1 : ints
        Select the axes to swap. Each axis is identified by its
        original integer position.

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

>>> d=cf.Data([[[1, 2, 3], [4, 5, 6]]])
>>> d.shape
(1, 2, 3)
>>> d.swapaxes(1, 0).shape

>>> d.swapaxes(2, 1).shape

>>> d.swapaxes(0, -1).shape

>>> d.swapaxes(1, 1).shape


'''
        if i:
            d = self
        else:
            d = self.copy()

        axis0 = d._parse_axes((axis0,), 'swapaxes')[0]
        axis1 = d._parse_axes((axis1,), 'swapaxes')[0]

        if axis0 != axis1:
            iaxes = range(d._ndim)
            iaxes[axis1], iaxes[axis0] = axis0, axis1
            d.transpose(iaxes, i=True)

        # Swap axes in the auxiliary mask
        if d._auxiliary_mask:
            for mask in d._auxiliary_mask:
                mask.swapaxes(axis0, axis1, i=True)

        return d
    #--- End: def

    def save_to_disk(self, itemsize=None):
        raise NotImplementedError(
"cf.Data.save_to_disk is dead. Use not cf.Data.fits_in_memory instead.")
#        '''
#
#Return True if the master array is large enough to be saved to disk.
#
#:Parameters:
#
#    itemsize : int, optional
#        The number of bytes per word of the master data array. By
#        default it taken from the array's data type.
#
#:Returns:
#
#    out: bool
#
#:Examples:
#
#>>> print d.save_to_disk()
#True
#
#>>> print d.save_to_disk(8)
#False
#
#'''
#        if not itemsize:            
#            try:
#                itemsize = self.dtype.itemsize
#            except AttributeError:
#                raise ValueError(
#                    "save_to_disk: Must set itemsize if there is no dtype")
#        #--- End: if
#
#        # ------------------------------------------------------------
#        # Note that self._size*(itemsize+1) is the array size in bytes
#        # including space for a full boolean mask
#        # ------------------------------------------------------------
#        return self._size*(itemsize+1) > FREE_MEMORY() - FM_THRESHOLD()
#    #--- End: def

    def fits_in_memory(self, itemsize):
        '''

Return True if the master array is small enough to be retained in
memory.

:Parameters:

    itemsize : int
        The number of bytes per word of the master data array.

:Returns:

    out: bool

:Examples:

>>> print d.fits_in_memory(8)
False

'''
        # ------------------------------------------------------------
        # Note that self._size*(itemsize+1) is the array size in bytes
        # including space for a full boolean mask
        # ------------------------------------------------------------
        return self._size*(itemsize+1) <= FREE_MEMORY() - FM_THRESHOLD()
    #--- End: def

    def fits_in_one_chunk_in_memory(self, itemsize):
        '''

Return True if the master array is small enough to be retained in
memory.

:Parameters:

    itemsize: `int`
        The number of bytes per word of the master data array.

:Returns:

    out: `bool`

:Examples:

>>> print d.fits_one_chunk_in_memory(8)
False

'''
        # ------------------------------------------------------------
        # Note that self._size*(itemsize+1) is the array size in bytes
        # including space for a full boolean mask
        # ------------------------------------------------------------
        return CHUNKSIZE() >= self._size*(itemsize+1) <= FREE_MEMORY() - FM_THRESHOLD()
    #--- End: def

    def where(self, condition, x=None, y=None, i=False, _debug=False):
        '''

Set data array elements depending on a condition.

Elements are set differently depending on where the condition is True
or False. Two assignment values are given. From one of them, the data
array is set where the condition is True and where the condition is
False, the data array is set from the other.

Each assignment value may either contain a single datum, or is an
array-like object which is broadcastable shape of the data array.

**Missing data**

The treatment of missing data elements depends on the value of the
`hardmask` attribute. If it is True then masked elements will not
unmasked, otherwise masked elements may be set to any value.

In either case, unmasked elements may be set to any value (including
missing data).

Unmasked elements may be set to missing data by assignment to the
`cf.masked` constant or by assignment to a value which contains masked
elements.

.. seealso:: `cf.masked`, `hardmask`, `__setitem__`

:Parameters:

    condition : *optional*
        Define the condition which determines how to set the data
        array. The condition is any object which is broadcastable to
        the data array shape. The condition is True where the object
        broadcast to the data array shape is True. If *condition* is
        unset then it defaults to a condition of True everywhere.

    x, y :

        Specify the assignment value. Where the condition defined by
        the *arg* and *kwargs* arguments is True, set the data array
        from *x* and where the condition is False, set the data array
        from *y*. Arguments *x* and *y* are each one of:

          * ``None``. The appropriate elements of the data array are
            unchanged.
        ..

          * Any object which is broadcastable to the data array's
            shape. The appropriate elements of the data array are set
            to the corresponding values from the object broadcast to
            the data array shape.
                
    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.
 
:Returns:

    out: cf.Data

:Examples:

'''     
        def _slice_to_partition(data, indices):           
            '''Return a numpy array for the part of the input data which spans the
given indices.

:Parameters:
    
    data: `cf.Data`
            
    indices: `tuple`
           
:Returns:
        
    out: `numpy.ndarray`

            '''
            indices2 = [(slice(0, 1) if n == 1 else i)
                        for n, i in zip(data.shape[::-1], indices[::-1])]

            return data[tuple(indices2)[::-1]].unsafe_array
        #--- End: def

        def _is_broadcastable(data0, data1, do_not_broadcast, is_scalar):
            '''Check that the data1 is broadcastable to data0 and return data1, as
a python scalar if possible.

.. note:: The input lists are updated inplace.

:Parameters:

    data0: `cf.Data`

    data1: `cf.Data`

    do_not_broadcast: `list`

    is_scalar: `list`

:Returns:

    out: `cf.Data` or scalar
        Return *data1* or, if possible, ``data1.datum(0)``.

            '''
            shape0 = data0._shape
            shape1 = data1._shape
            size1  = data1._size

            if shape1 == shape0:
                do_not_broadcast.append(True)
                is_scalar.append(False)

            elif size1 == 1:
                do_not_broadcast.append(False)
                is_scalar.append(True)
                # Replace data1 with its scalar value
                data1 = data1.datum(0)
                
            elif data1._ndim <= data0._ndim and size1 < data0._size:
                do_not_broadcast.append(False)
                is_scalar.append(False)
                for n, m in zip(shape1[::-1], shape0[::-1]):
                    if n != m and n != 1:
                        raise ValueError(
"where: Can't broadcast data with shape {} to shape {}".format(
    shape1, shape0))
            else:
                raise ValueError(
"where: Can't broadcast data with shape {} to shape {}".format(
    shape1, shape0))

            return data1
        #--- End: def
        
        if i:
            d = self
        else:
            d = self.copy()

        if x is None and y is None:
            # The data is unchanged regardless of condition
            return d

        do_not_broadcast = []
        is_scalar        = []

#        # ------------------------------------------------------------
#        # Make sure that the condition is a cf.Data object
#        # ------------------------------------------------------------
#
#        if not isinstance(condition, d.__class__):
#            condition = type(d)(condition)

        # ------------------------------------------------------------
        # Check that the input condition is broadcastable
        # ------------------------------------------------------------
        condition = Data.asdata(condition, copy=False)
        condition = _is_broadcastable(d, condition, do_not_broadcast, is_scalar)

#        if isinstance(condition, Query):
#        condition = condition.evaluate(f).Data
        # ------------------------------------------------------------
        # Parse inputs x and y so that each is one of A) None, B) a
        # scalar or C) a data array with the same shape as the master
        # array
        # ------------------------------------------------------------
        xy = []
        for value in (x, y):
            if value is None or value is cf_masked:
                do_not_broadcast.append(False)
                is_scalar.append(True)

            else:
                # Make sure that the value is a cf.Data object and has
                # compatible units
                if not isinstance(value, d.__class__):
                    value = type(d)(value)
                else:
                    if value.Units.equivalent(d.Units):
                        if not value.Units.equals(d.Units):                    
                            value = value.copy()                    
                            value.Units = d.Units
                    elif value.Units:
                        raise ValueError(
"where: Can't assign values with units {!r} to data with units {!r}".format(
    value.Units, d.Units))
                #--- End: if

                # Check that the value is broadcastable
                value = _is_broadcastable(d, value, do_not_broadcast, is_scalar)
            #--- End: if

            xy.append(value)
        #--- End: for
        (x, y) = xy
        (condition_is_scalar, x_is_scalar, y_is_scalar) = is_scalar
        broadcast = not any(do_not_broadcast)

        if _debug:
            print '    x =', repr(x)
            print '    y =', repr(y)
            print '    condition_is_scalar =', repr(condition_is_scalar)
            print '    x_is_scalar         =', repr(x_is_scalar)
            print '    y_is_scalar         =', repr(y_is_scalar)
            print '    broadcast           =', repr(broadcast)
            
        #-------------------------------------------------------------
        # Try some shortcuts if the condition is a scalar
        #-------------------------------------------------------------
        if condition_is_scalar and not getattr(condition, 'isquery', False):
            if _debug:
                print '    Condition is a scalar:', repr(condition), type(condition)
            if condition:
                if x is not None:
                    d[...] = x

                return d
            else:
                if y is not None:
                    d[...] = y
                    
                return d
        #--- End: if

        # Still here?
 
        hardmask = d._hardmask
        config = d.partition_configuration(readonly=False) # or True?

        for partition in d.partitions.matrix.flat:
            partition.open(config)
            array = partition.array

            # --------------------------------------------------------
            # Find the master array indices for this partition
            # --------------------------------------------------------
            shape = array.shape
            indices = partition.indices

            # --------------------------------------------------------
            # Find the condition for this partition
            # --------------------------------------------------------
            if getattr(condition, 'isquery', False):
                c = condition.evaluate(array)
            elif condition_is_scalar:
                c = condition
            else:
                c = _slice_to_partition(condition, indices)

            # --------------------------------------------------------
            # Find value to use where condition is True for this
            # partition
            # --------------------------------------------------------
            if x_is_scalar:  
                if x is None:
                    # Use d
                    T = array
                    T_masked = partition.masked
                else:
                    T = x
                    T_masked = (x is cf_masked)
            else:
                T = _slice_to_partition(x, indices)
                T_masked = numpy_ma_isMA(T) and numpy_ma_is_masked(T)

            # --------------------------------------------------------
            # Find value to use where condition is False for this
            # partition
            # --------------------------------------------------------
            if y_is_scalar:  
                if y is None:
                    # Use d
                    F = array
                    F_masked = partition.masked
                else:
                    F = y
                    F_masked = (y is cf_masked)
            else:
                F = _slice_to_partition(y, indices)
                F_masked = numpy_ma_isMA(F) and numpy_ma_is_masked(F)

            # --------------------------------------------------------
            # Make sure that at least one of the arrays is the same
            # shape as the partition
            # --------------------------------------------------------
            if broadcast:
                if x is cf_masked or y is cf_masked:
                    c = _broadcast(c, shape)
                else:
                    max_sizes = max((numpy_size(c), numpy_size(T), numpy_size(F)))
                    if numpy_size(c) == max_sizes:
                        c = _broadcast(c, shape)
                    elif numpy_size(T) == max_sizes:
                        T = _broadcast(T, shape)
                    else:
                        F = _broadcast(F, shape)
            #--- End: if

            # --------------------------------------------------------
            # Create a numpy array which takes vales from T where c
            # is True and from F where c is False
            # --------------------------------------------------------
            if T_masked or F_masked:
                # T and/or F have missing data
                new = numpy_ma_where(c, T, F)
                if partition.masked:
                    if hardmask:
                        # The original partition has missing data and
                        # a hardmask, so apply the original
                        # partition's mask to the new array.
                        new.mask |= array.mask
                    elif not numpy_ma_is_masked(new):
                        # The original partition has missing data and
                        # a softmask and the new array doesn't have
                        # missing data, so turn the new array into an
                        # unmasked array.
                        new = new.data[...]  

                elif not numpy_ma_is_masked(new):
                    # The original partition doesn't have missing data
                    # and neither does the new array
                    new = new.data[...]
           
            else:
                # Neither T nor F have missing data
                new = numpy_where(c, T, F)

                if partition.masked and hardmask:
                    # The original partition has missing data and a
                    # hardmask, so apply the original partition's mask
                    # to the new array.
                    new = numpy_ma_masked_where(array.mask, new, copy=False)
            #--- End: if
                            
            # --------------------------------------------------------
            # Replace the partition's subarray with the new numpy
            # array
            # --------------------------------------------------------
            partition.subarray = new

            partition.close()
        #--- End: for

        return d
    #--- End: def

    def sin(self, i=False):
        '''

Take the trigonometric sine of the data array in place.

Units are accounted for in the calculation. If the units are not
equivalent to radians (such as Kelvin) then they are treated as if
they were radians. For example, the the cosine of 90 degrees_east is
1.0, as is the sine of 1.57079632 radians.

The Units are changed to '1' (nondimensionsal).

:Parameters:

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

>>> d.Units
<CF Units: degrees_north>
>>> print d.array
[[-90 0 90 --]]
>>> d.sin()
>>> d.Units
<CF Units: 1>
>>> print d.array
[[-1.0 0.0 1.0 --]]

>>> d.Units
<CF Units: m s-1>
>>> print d.array
[[1 2 3 --]]
>>> d.sin()
>>> d.Units
<CF Units: 1>
>>> print d.array
[[0.841470984808 0.909297426826 0.14112000806 --]]

'''
        if i:
            d = self
        else:
            d = self.copy()

        if d.Units.equivalent(_units_radians):           
            d.Units = _units_radians

        return d.func(numpy_sin, units=_units_1, i=True)
    #--- End: def

    def log(self, base=None, i=False):
        '''

:Parameters:

    base : 

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

'''
        if i:
            d = self
        else:
            d = self.copy()
        
        if base is None:
            d.func(numpy_log, units=d.Units.log(numpy_e), i=True)
        elif base == 10:
            d.func(numpy_log10, units=d.Units.log(10), i=True)
        elif base == 2:
            d.func(numpy_log2, units=d.Units.log(2), i=True)
        else:
            d.func(numpy_log, units=d.Units.log(base), i=True)
            d /= numpy_log(base)
            
        return d
    #--- End: def

    def squeeze(self, axes=None, i=False):
        '''

Remove size 1 axes from the data array.

By default all size 1 axes are removed, but particular axes may be
selected with the keyword arguments.

.. seealso:: `expand_dims`, `flip`, `swapaxes`, `transpose`

:Parameters:

    axes : (sequence of) int or str, optional
        Select the axes.  By default all size 1 axes are removed. The
        *axes* argument may be one, or a sequence, of:

          * An internal axis identifier. Selects this axis.
        ..

          * An integer. Selects the axis coresponding to the given
            position in the list of axes of the data array.

        No axes are removed if *axes* is an empty sequence.

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data
        The squeezed data array.

:Examples:

>>> v.shape
(1,)
>>> v.squeeze()
>>> v.shape
()

>>> v.shape
(1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1)
>>> v.squeeze((0,))
>>> v.shape
(2, 1, 3, 1, 4, 1, 5, 1, 6, 1)
>>> v.squeeze(1)
>>> v.shape
(2, 3, 1, 4, 1, 5, 1, 6, 1)
>>> v.squeeze([2, 4])
>>> v.shape
(2, 3, 4, 5, 1, 6, 1)
>>> v.squeeze([])
>>> v.shape
(2, 3, 4, 5, 1, 6, 1)
>>> v.squeeze()
>>> v.shape
(2, 3, 4, 5, 6)

'''
        if i:
            d = self
        else:
            d = self.copy()

        ndim = d._ndim
        if not ndim:
            if axes or axes == 0:
                raise ValueError(
"Can't squeeze: Can't remove an axis from scalar {}".format(d.__class__.__name__))
            return d
        #--- End: if

        shape = list(d._shape)

        if axes is None:
            axes = [i for i, n in enumerate(shape) if n == 1]
        else:
            axes = d._parse_axes(axes, 'squeeze')
            
            # Check the squeeze axes
            for i in axes:
                if shape[i] > 1:
                    raise ValueError(
"Can't squeeze {}: Can't remove axis of size {}".format(d.__class__.__name__, shape[i]))
        #--- End: if

        if not axes:
            return d

        # Still here? Then the data array is not scalar and at least
        # one size 1 axis needs squeezing.
        data_axes = d._axes[:]
        flip      = d._flip[:]

        if not d._all_axes:
            d._all_axes = tuple(data_axes)            

        i_axis = []
        for axis in [data_axes[i] for i in axes]:  
            if axis in flip:
                flip.remove(axis)

            i = data_axes.index(axis)              
            shape.pop(i)
            data_axes.pop(i)

            i_axis.append((i, axis))
        #--- End: for

        for partition in d.partitions.matrix.flat:
            p_location = partition.location[:]
            p_shape    = partition.shape[:]
            p_flip     = partition.flip[:]
          
            for i, axis in i_axis:
                p_location.pop(i)
                p_shape.pop(i)                
                if axis in p_flip:
                    p_flip.remove(axis)
            #--- End: for

            partition.location = p_location
            partition.shape    = p_shape            
            partition.flip     = p_flip
        #--- End: for

        d._ndim  = len(shape)
        d._shape = tuple(shape)

        d._axes = data_axes
        d._flip = flip

        # Remove size 1 partition dimensions       
        d.partitions.squeeze(i=True)

        # Squeeze the auxiliary mask
        if d._auxiliary_mask:
            for mask in d._auxiliary_mask:
                mask.squeeze(axes, i=True)

        return d
    #--- End: def

    def tan(self, i=False):
        '''

Take the trigonometric tangent of the data array element-wise.

Units are accounted for in the calculation. If the units are not
equivalent to radians (such as Kelvin) then they are treated as if
they were radians. For example, the the tangent of 45 degrees_east is
1.0, as is the tangent of 0.78539816 radians.

The Units are changed to ``'1'`` (nondimensionsal).

.. seealso:: `cos`, `sin`

:Parmaeters:

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

>>> d.Units
<CF Units: degrees_north>
>>> print d.array
[[-45 0 45 --]]
>>> d.tan()
>>> d.Units
<CF Units: 1>
>>> print d.array
[[-1.0 0.0 1.0 --]]

>>> d.Units
<CF Units: m s-1>
>>> print d.array
[[1 2 3 --]]
>>> d.tan()
>>> d.Units
<CF Units: 1>
>>> print d.array
[[1.55740772465 -2.18503986326 -0.142546543074 --]]

'''
        if i:
            d = self
        else:
            d = self.copy()

        if d.Units.equivalent(_units_radians):           
            d.Units = _units_radians

        return d.func(numpy_tan, units=_units_1, i=True)
    #--- End: def

    def tolist(self):
        '''
Return the array as a (possibly nested) list.

Return a copy of the array data as a (nested) Python list. Data items
are converted to the nearest compatible Python type.

:Returns:	

    out: list
        The possibly nested list of array elements.

:Examples:

>>> d = cf.Data([1, 2])
>>> d.tolist()
[1, 2]

>>> d = cf.Data(([[1, 2], [3, 4]])
>>> list(d)
[array([1, 2]), array([3, 4])]      # DCH CHECK
>>> d.tolist()
[[1, 2], [3, 4]]

>>> d.equals(cf.Data(d.tolist()))
True


'''
        return self.array.tolist()
    #--- End: def

    def transpose(self, axes=None, i=False):
        '''
        
Permute the axes of the data array.

.. seealso:: `expand_dims`, `flip`, `squeeze`, `swapaxes`

:Parameters:

    axes : (sequence of) int
        The new axis order of the data array. By default the order is
        reversed. Each axis of the new order is identified by its
        original integer position.

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

>>> d.shape
(19, 73, 96)
>>> d.transpose()
>>> d.shape
(96, 73, 19)
>>> d.transpose([1, 0, 2])
>>> d.shape
(73, 96, 19)
>>> d.transpose((-1, 0, 1))
>>> d.shape
(19, 73, 96)

'''
        if i:
            d = self
        else:
            d = self.copy()

        ndim = d._ndim    
        
        # Parse the axes. By default, reverse the order of the axes.
        if axes is None:
            if ndim <= 1:
                return d

            iaxes = range(ndim-1, -1, -1)
        else:
            iaxes = d._parse_axes(axes, 'transpose')

            # Return unchanged if axes are in the same order as the data
            if iaxes == range(ndim):
                return d

            if len(iaxes) != ndim:
                raise ValueError(
                    "Can't tranpose: Axes don't match array: {}".format(iaxes))
        #--- End: if

        # Permute the axes
        data_axes = d._axes
        d._axes = [data_axes[i] for i in iaxes]

        # Permute the shape
        shape = d._shape
        d._shape = tuple([shape[i] for i in iaxes])

        # Permute the locations map
        for partition in d.partitions.matrix.flat:
            location = partition.location
            shape    = partition.shape

            partition.location = [location[i] for i in iaxes]
            partition.shape    = [shape[i]    for i in iaxes]
        #--- End: for

        # Transpose the auxiliary mask
        if d._auxiliary_mask:
            for mask in d._auxiliary_mask:
                mask.transpose(iaxes, i=True)

        return d
    #--- End: def

    def trunc(self, i=False):
        '''

Return the truncated values of the data array.

The truncated value of the number, ``x``, is the nearest integer which
is closer to zero than ``x`` is. In short, the fractional part of the
signed number ``x`` is discarded.

.. versionadded:: 1.0

.. seealso:: `ceil`, `floor`, `rint`

:Parameters:

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

>>> print d.array
[-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
>>> print d.trunc().array
[-1. -1. -1. -1.  0.  1.  1.  1.  1.]

'''
        return self.func(numpy_trunc, out=True, i=i)
    #---End: def

    @classmethod
    def empty(cls, shape, dtype=None, units=None, chunk=True):
        ''' Create a new data array without initializing the elements.

.. seealso:: `full`, `ones`, `zeros`

:Examples 1:

>>> d = cf.Data.empty((96, 73))

:Parameters:

    shape: `int` or `tuple` of `int`
        The shape of the new array.

    dtype: `numpy.dtype` or any object convertible to `numpy.dtype`
        The data type of the new array. By default the data type is
        numpy.float64.

    units: `str` or `cf.Units`
        The units for the new data array.

:Returns:

    out: `cf.Data`

:Examples 2:

'''
        return cls.full(shape, None, dtype=dtype, units=units,
                        chunk=chunk)
    #--- End: def

    @classmethod
    def full(cls, shape, fill_value, dtype=None, units=None,
             chunk=True):
        '''Return a new data array of given shape and type, filled with
`fill_value`.

.. seealso:: `empty`, `ones`, `zeros`

:Examples 1:

>>> d = cf.Data.full((96, 73), -99)

:Parameters:

    shape: `int` or `tuple` of `int`
        The shape of the new array.

    fill_value: scalar
        Fill value.

    dtype: data-type
        The data type of the new array. By default the data type is
        `numpy.float64`.

    units: `str` or `cf.Units`
        The units for the new data array.

:Returns:

    out: `cf.Data`

:Examples 2:

        '''
        array = FilledArray(shape=tuple(shape),
                            size=long(reduce(operator_mul, shape, 1)),
                            ndim=len(shape),
                            dtype=numpy_dtype(dtype),
                            fill_value=fill_value)
        
        return cls(array, units=units, chunk=chunk)
    #--- End: def

    @classmethod
    def ones(cls, shape, dtype=None, units=None, chunk=True):
        '''
        '''
        return cls.full(shape, 1, dtype=dtype, units=units, chunk=chunk)
    #--- End: def
    
    @classmethod
    def zeros(cls, shape, dtype=None, units=None, chunk=True):
        '''
        '''
        return cls.full(shape, 0, dtype=dtype, units=units, chunk=chunk)
    #--- End: def

    def func(self, f, units=None, out=False, i=False, **kwargs):
        '''Apply an element-wise array operation to the data array.

:Parameters:

    f: `function`
        The function to be applied.
        
    units: `cf.Units`, optional
        
    out: `bool`, optional

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: `cf.Data`

:Examples:

>>> d.Units
<CF Units: radians>
>>> print d.array
[[ 0.          1.57079633]
 [ 3.14159265  4.71238898]]
>>> import numpy
>>> e = d.func(numpy.cos)
>>> e.Units
<CF Units: 1>
>>> print e.array
[[ 1.0  0.0]
 [-1.0  0.0]]
>>> d.func(numpy.sin, i=True)
>>> print d.array
[[0.0   1.0]
 [0.0  -1.0]]

        '''      
        if i:
            d = self
        else:
            d = self.copy()

        config = d.partition_configuration(readonly=False)
            
        datatype = d.dtype

        for partition in d.partitions.matrix.flat:
            partition.open(config)
            array = partition.array

            if out:
                f(array, out=array, **kwargs)
            else:
                array = f(array, **kwargs)

            p_datatype = array.dtype
            if datatype != p_datatype:
                datatype = numpy_result_type(p_datatype, datatype)
                
            partition.subarray = array

            if units is not None:
                partition.Units = units

            partition.close()
        #--- End: for
            
        d.dtype = datatype

        if units is not None:
            d.Units = units

        return d
    #--- End: def

    def range(self, axes=None, squeeze=True, mtol=1, i=False,
              _preserve_partitions=False):
        '''Collapse axes with the absolute difference between their maximum
and minimum values.

Missing data array elements are omitted from the calculation.

.. seealso:: `max`, `min`, `mean`, `mid_range`, `sample_size`,
             `sd`, `sum`, `sum_of_weights`, `sum_of_weights2`, `var`

:Parameters:

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data
        The collapsed array.

:Examples:

        '''   
        return self._collapse(range_f, range_fpartial,
                              range_ffinalise, axes=axes,
                              squeeze=squeeze, weights=None,
                              mtol=mtol, i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    def roll(self, axis, shift, i=False):
        '''A lot like `numpy.roll`

:Parameters:

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

        '''
        if not shift:
            # Null roll
            if i:
                return self
            else:
                return self.copy()

        iaxes = self._parse_axes(axis, 'roll')
        if len(iaxes) != 1:
            raise ValueError("987345 9087345 ^^ roll ^")

        axis = iaxes[0]

        n = self._shape[axis]

        shift %= n
      
        if not shift:
            # Null roll
            if i:
                return self
            else:
                return self.copy()

        shift = n - shift

        indices0 = [slice(None)] * self._ndim
        indices0[axis] = slice(None, shift)

        indices1 = indices0[:]
        indices1[axis] = slice(shift, None)

        indices0 = tuple(indices0)
        indices1 = tuple(indices1)

        d = type(self).concatenate((self[indices1], self[indices0]),
                                   axis=axis)
        
        if i:
            self.__dict__ = d.__dict__
            return self
        else:
            return d
    #--- End: def

    def sum(self, axes=None, squeeze=False, mtol=1, i=False,
            _preserve_partitions=False):
        '''Collapse axes with their sum.

Missing data array elements are omitted from the calculation.

.. seealso:: `max`, `min`, `mean`, `mid_range`, `range`,
             `sample_size`, `sd`, `sum_of_weights`, `sum_of_weights2`,
             `var`

:Parameters:

    axes : (sequence of) int, optional

    squeeze : bool, optional

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data
        The collapsed array.

:Examples:

        '''   
        return self._collapse(sum_f, sum_fpartial, sum_ffinalise, axes=axes,
                              squeeze=squeeze, weights=None, mtol=mtol, i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    def sum_of_weights(self, axes=None, squeeze=False, mtol=1, weights=None,
                       i=False, _preserve_partitions=False):
        '''

Missing data array elements are omitted from the calculation.

.. seealso:: `max`, `mean`, `mid_range`, `min`, `range`,
             `sample_size`, `sd`, `sum`, `sum_of_weights2`, `var`

:Parameters:

    axes : (sequence of) int, optional

    squeeze : bool, optional

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data
        The collapsed array.

:Examples:

        '''   
        return self._collapse(sw_f, sw_fpartial, sw_ffinalise, axes=axes,
                              squeeze=squeeze, weights=weights, mtol=mtol,
                              i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    def sum_of_weights2(self, axes=None, squeeze=False, mtol=1, weights=None,
                        i=False, _preserve_partitions=False):
        '''

Missing data array elements are omitted from the calculation.

.. seealso:: `max`, `mean`, `mid_range`, `min`, `range`,
             `sample_size`, `sd`, `sum`, `sum_of_weights`, `var`

:Parameters:

    axes : (sequence of) int, optional

    squeeze : bool, optional

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data
        The collapsed array.

:Examples:

        '''   
        return self._collapse(sw2_f, sw2_fpartial, sw2_ffinalise, axes=axes,
                              squeeze=squeeze, weights=weights, mtol=mtol,
                              i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    def sd(self, axes=None, squeeze=False, mtol=1, weights=None,
           ddof=0, i=False, _preserve_partitions=False):
        r'''

Collapse axes by calculating their standard deviation.

The standard deviation may be adjusted for the number of degrees of
freedom and may be calculated with weighted values.

Missing data array elements and those with zero weight are omitted
from the calculation.

The unweighted standard deviation, :math:`s`, of :math:`N` values
:math:`x_i` with mean :math:`m` and with :math:`N-ddof` degrees of
freedom (:math:`ddof\ge0`) is

.. math:: s=\sqrt{\frac{1}{N-ddof} \sum_{i=1}^{N} (x_i - m)^2}

The weighted standard deviation, :math:`\tilde{s}_N`, of :math:`N`
values :math:`x_i` with corresponding weights :math:`w_i`, weighted
mean :math:`\tilde{m}` and with :math:`N` degrees of freedom is

.. math:: \tilde{s}_N=\sqrt{\frac{1}{\sum_{i=1}^{N} w_i}
                      \sum_{i=1}^{N} w_i(x_i - \tilde{m})^2}

The weighted standard deviation, :math:`\tilde{s}`, of :math:`N`
values :math:`x_i` with corresponding weights :math:`w_i` and with
:math:`N-ddof` degrees of freedom (:math:`ddof>0`) is

.. math:: \tilde{s} = \sqrt{\frac{f \sum_{i=1}^{N} w_i}{f
                      \sum_{i=1}^{N} w_i - ddof}} \tilde{s}_N

where :math:`f` is the smallest positive number whose product with
each weight is an integer. :math:`f \sum_{i=1}^{N} w_i` is the size of
a new sample created by each :math:`x_i` having :math:`fw_i`
repeats. In practice, :math:`f` may not exist or may be difficult to
calculate, so :math:`f` is either set to a predetermined value or an
approximate value is calculated. The approximation is the smallest
positive number whose products with the smallest and largest weights
and the sum of the weights are all integers, where a positive number
is considered to be an integer if its decimal part is sufficiently
small (no greater than :math:`10^{-8}` plus :math:`10^{-5}` times its
integer part). This approximation will never overestimate :math:`f`,
so :math:`\tilde{s}` will never be underestimated when the
approximation is used. If the weights are all integers which are
collectively coprime then setting :math:`f=1` will guarantee that
:math:`\tilde{s}` is exact.

:Parameters:

    axes : (sequence of) int, optional
        The axes to be collapsed. By default flattened input is
        used. Each axis is identified by its integer position. No axes
        are collapsed if *axes* is an empty sequence.

    squeeze : bool, optional
        If True then collapsed axes are removed. By default the axes
        which are collapsed are left in the result as axes with size
        1. When the collapsed axes are retained, the result is
        guaranteed to broadcast correctly against the original array.

          **Example:** Suppose that an array, ``d``, has shape (2, 3,
          4) and ``e = d.sd(axis=1)``. Then ``e`` has shape (2, 1, 4)
          and, for example, ``d/e`` is allowed. If ``e = d.sd(axis=1,
          squeeze=True)`` then ``e`` will have shape (2, 4) and
          ``d/e`` is an illegal operation.

    weights : data-like or dict, optional
        Weights associated with values of the array. By default all
        non-missing elements of the array are assumed to have equal
        weights of 1. If *weights* is a data-like object then it must
        have either the same shape as the array or, if that is not the
        case, the same shape as the axes being collapsed. If *weights*
        is a dictionary then each key is axes of the array (an int or
        tuple of ints) with a corresponding data-like value of weights
        for those axes. In this case, the implied weights array is the
        outer product of the dictionary's values it may be used in
        conjunction wih any value of *axes*, because the axes to which
        the weights apply are given explicitly.

          **Example:** Suppose that the original array being collapsed
          has shape (2, 3, 4) and *weights* is set to a data-like
          object, ``w``. If ``axes=None`` then ``w`` must have shape
          (2, 3, 4). If ``axes=(0, 1, 2)`` then ``w`` must have shape
          (2, 3, 4). If ``axes=(2, 0, 1)`` then ``w`` must either have
          shape (2, 3, 4) or else (4, 2, 3). If ``axes=1`` then ``w``
          must either have shape (2, 3, 4) or else (3,). If ``axes=(2,
          0)`` then ``w`` must either have shape (2, 3, 4) or else (4,
          2). Suppose *weights* is a dictionary. If ``weights={1: x}``
          then ``x`` must have shape (3,). If ``weights={1: x, (2, 0):
          y}`` then ``x`` must have shape (3,) and ``y`` must have
          shape (4, 2). The last example is equivalent to
          ``weights={(1, 2, 0): x.outerproduct(y)}`` (see
          `outerproduct` for details).

    mtol : number, optional
        For each element in the output data array, the fraction of
        contributing input array elements which is allowed to contain
        missing data. Where this fraction exceeds *mtol*, missing
        data is returned. The default is 1, meaning a missing datum in
        the output array only occurs when its contributing input array
        elements are all missing data. A value of 0 means that a
        missing datum in the output array occurs whenever any of its
        contributing input array elements are missing data. Any
        intermediate value is permitted.

    ddof : number, *optional*
        The delta degrees of freedom. The number of degrees of freedom
        used in the calculation is (N-*ddof*) where N represents the
        number of elements. By default *ddof* is 1, meaning the
        standard deviation of the population is estimated according to
        the usual formula with (N-1) in the denominator to avoid the
        bias caused by the use of the sample mean (Bessel's
        correction).

    i : bool, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: cf.Data

:Examples:

Some, not wholly comprehensive, examples:

>>> d = cf.Data([1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4])
>>> e = cf.Data([1, 2, 3, 4])
>>> d.sd(squeeze=False)
<CF Data: [1.06262254195] >
>>> d.sd()
<CF Data: 1.06262254195 >
>>> e.sd(weights=[2, 3, 5, 6])
<CF Data: 1.09991882817 >
>>> e.sd(weights=[2, 3, 5, 6], f=1)
<CF Data: 1.06262254195 >
>>> d.sd(ddof=0)
<CF Data: 1.02887985207 >
>>> e.sd(ddof=0, weights=[2, 3, 5, 6])
<CF Data: 1.02887985207 >

'''        
        return self._collapse(sd_f, sd_fpartial, sd_ffinalise,
                              axes=axes, squeeze=squeeze,
                              weights=weights, mtol=mtol, ddof=ddof,
                              i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def

    def var(self, axes=None, squeeze=False, weights=None, mtol=1,
            ddof=0, i=False, _preserve_partitions=False):
        r'''

Collapse axes with their weighted variance.

The units of the returned array are the square of the units of the
array.

.. seealso:: `max`, `min`, `mean`, `mid_range`, `range`, `sum`, `sd`

:Parameters:

    axes : (sequence of) int, optional

    squeeze : bool, optional

    weights :

    i: `bool`, optional
        If True then update the data array in place. By default a new
        data array is created.

:Returns:

    out: `cf.Data`
        The collapsed array.

:Examples:

'''
        units = self.Units
        if units:
            units = units ** 2

        return self._collapse(var_f, var_fpartial, var_ffinalise,
                              axes=axes, squeeze=squeeze,
                              weights=weights, mtol=mtol, units=units,
                              ddof=ddof, i=i,
                              _preserve_partitions=_preserve_partitions)
    #--- End: def
    
    def section(self, axes, stop=None, chunks=False, min_step=1,
                mode='dictionary'):
        """

Return a dictionary of Data objects, which are the m dimensional
sections of this n dimensional Data object, where m <= n. The keys
of the dictionary are the indicies of the sections in the original
Data object. The m dimensions that are not sliced are marked with
None as a placeholder making it possible to reconstruct the original
data object. The corresponding values are the resulting sections of
type cf.Data.

:Parameters:

    axes : *optional*
        This is should be a tuple or a list of the m indices of the
        m axes that define the sections of the Data object. If axes
        is None (the default) all axes are selected.

    stop : int, optional
        Stop after this number of sections and return. If stop is
        None all sections are taken.

    chunks : bool, optional
        If True return sections that are of the maximum possible size
        that will fit in one chunk of memory instead of sectioning
        into slices of size 1 along the dimensions that are being
        sectioned.
    
    min_step : int, optional
        The minimum step size when making chunks. By default this is
        1. Can be set higher to avoid size 1 dimensions, which are
        problematic for bilinear regridding.

:Returns:

    out: dict
        The dictionary of m dimensional sections of the Data object.

:Examples:

Section a Data object into 2D slices:

>>> d.section((0,1))

        """
#        dictionary = (mode == 'dictionary')
#        if dictionary:
#            out = {}
#        else:
#            out = []
#
#        empty_data = self.empty(self.shape, chunk=False)
#        
#        empty_data.chunk(omit_axes=axes, min_step=[])
#        
#        for n, partition in enumerate(empty_data.partitions.flat):
#            if stop is not None and n >= stop:
#                break
#            
#            e = self[partition.indices]
#            if dictionary:
#                out[indices] = e
#            else:
#                out.append(e)
#        #--- End: for
#            
#        return out
#
        return _section(self, axes, data=True, stop=stop, chunks=chunks,
                        min_step=min_step)
    #--- End: def

#--- End: class
   

## ====================================================================
##
## SubspaceData object
##
## ====================================================================
#
#class SubspaceData(object):
#
#    __slots__ = ('data',)
#
#    def __init__(self, data):
#        '''
#
#Set the contained data object.
#
#'''
#        self.data = data
#    #--- End: def
#
#
#    def __getitem__(self, indices):
#        '''
#
#Implement indexing
#
#x.__getitem__(indices) <==> x[indices]
#
#'''
#        return self.data[indices]
#    #--- End: def
#
#    def __setitem__(self, indices, value):
#        '''
#
#Implement indexed assignment
#
#x.__setitem__(indices, value) <==> x[indices]=value
#
#'''
#        self.data[indices] = value
#    #--- End: def
#
##--- End: class

def _size_of_index(index, size=None):
    '''

Return the number of elements resulting in applying an index to a
sequence.

:Parameters:

    index : slice or list of ints
        The index being applied to the sequence.

    size : int, optional
        The number of elements in the sequence being indexed. Only
        required if *index* is a slice object.

:Returns:

    out: int
        The length of the sequence resulting from applying the index.

:Examples:

>>> _size_of_index(slice(None, None, -2), 10)
5
>>> _size_of_index([1, 4, 9])
3

'''
    if isinstance(index, slice):
        # Index is a slice object
        start, stop, step = index.indices(size)
        div, mod = divmod(stop-start, step)
        if mod != 0:
            div += 1
        return div
    else:
        # Index is a list of integers
        return len(index)
#--- End: def

#def _parse_indices(data, indices):
#    '''
#
#:Parameters:
#
#   data : 
#
#   indices : sequence of indices
#
#:Returns:
#
#    parsed_indices, flip_axes : {list, list} 
#
#:Examples:
#
#'''
#    parsed_indices, roll = parse_indices(data, indices, True)
#
#    parsed_indices = list(parsed_indices)
#    
#    flip_axes = []
#
#    for i, index in enumerate(parsed_indices):      
#
#        if isinstance(index, slice):
#            size = data.shape[i]
#            if index.step < 0:              
#                # If the slice step is negative, then transform the
#                # original slice to a new slice with a positive step
#                # such that the result of the new slice is the reverse
#                # of the result of the original slice.
#                #
#                # For example, if the original slice is slice(6,0,-2)
#                # then the new slice will be slice(2,7,2):
#                #
#                # >>> a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#                # >>> a[slice(6, 0, -2)]
#                # [6, 4, 2]
#                # >>> a[slice(2, 7, 2)]
#                # [2, 4, 6]
#                # a[slice(6, 0, -2)] == list(reversed(a[slice(2, 7, 2)]))
#                # True
#                start, stop, step = index.indices(size)
#                step    *= -1
#                div, mod = divmod(start-stop-1, step)
#                div_step = div*step
#                start   -= div_step
#                stop     = start + div_step + 1
#                
#                index = slice(start, stop, step)
#                flip_axes.append(i)         
#            #--- End: if      
#
#            # If step is greater than one, make sure that index.stop isn't
#            # bigger than it needs to be.
#            if index.step > 1:
#                start, stop, step = index.indices(size)
#                div, mod = divmod(stop-start-1, step)
#                stop     = start + div*step + 1
#                index    = slice(start, stop, step)
#            #--- End: if
#
#            parsed_indices[i] = index    
#
#        else:
#            # --------------------------------------------------------
#            # Check that an integer list is strictly monotonic and if
#            # it's descending then flip it so that it's ascending
#            # --------------------------------------------------------
#            step = index[1] - index[0]
#
#            if step > 0:
#                for j in xrange(len(index)-1):
#                    if index[j] >= index[j+1]:
#                        raise ValueError("Bad slice (not strictly monotonic): %s" % index)
#            elif step < 0:
#                for j in xrange(len(index)-1):
#                    if index[j] <= index[j+1]:
#                        raise ValueError("Bad slice (not strictly monotonic): %s" % index)
#                
#                # Reverse the list so that it's strictly monotonically
#                # increasing and make a note that this dimension will
#                # need flipping later
#                index.reverse()
#                flip_axes.append(i)
#            else:
#                # Step is 0
#                raise ValueError("Bad slice (not strictly monotonic): %s" % index)
#        #--- End: if
#    #--- End: for
#    
##    return parsed_indices, roll, flip_axes
#    return tuple(parsed_indices), roll, flip_axes
##--- End: def

def _overlapping_partitions(partitions, indices, axes, master_flip):
    '''

Return the nested list of (modified) partitions which overlap the
given indices to the master array.

:Parameters:

    partitions : cf.PartitionMatrix

    indices : tuple

    axes : sequence of str

    master_flip : list

:Returns:

    out: numpy array
        A numpy array of cf.Partition objects.

:Examples:

>>> type f.Data
<class 'cf.data.Data'>
>>> d._axes
['dim1', 'dim2', 'dim0']
>>> axis_to_position = {'dim0': 2, 'dim1': 0, 'dim2' : 1}
>>> indices = (slice(None), slice(5, 1, -2), [1,3,4,8])
>>> x = _overlapping_partitions(d.partitions, indices, axis_to_position, master_flip)

'''

    axis_to_position = {}
    for i, axis in enumerate(axes):
        axis_to_position[axis] = i

    if partitions.size == 1:
        partition = partitions.matrix.item()

        # Find out if this partition overlaps the original slice
        p_indices, shape = partition.overlaps(indices)

        if p_indices is None:
            # This partition is not in the slice out of bounds - raise
            # error?
            return
        
        # Still here? Create a new partition                      
        partition = partition.copy()
        partition.new_part(p_indices, axis_to_position, master_flip)
        partition.shape = shape
        
        new_partition_matrix      = numpy_empty(partitions.shape, dtype=object)
        new_partition_matrix[...] = partition
        
        return new_partition_matrix
    #--- End: if

    # Still here? Then there are 2 or more partitions.

    partitions_list        = []
    partitions_list_append = partitions_list.append

    flat_pm_indices        = []
    flat_pm_indices_append = flat_pm_indices.append

    partitions_flat = partitions.matrix.flat

    i = partitions_flat.index

    for partition in partitions_flat:
        # Find out if this partition overlaps the original slice
        p_indices, shape = partition.overlaps(indices)
        
        if p_indices is None:
            # This partition is not in the slice 
            i = partitions_flat.index
            continue

        # Still here? Then this partition overlaps the slice, so
        # create a new partition.
        partition = partition.copy()
        partition.new_part(p_indices, axis_to_position, master_flip)
        partition.shape = shape
        
        partitions_list_append(partition)

        flat_pm_indices_append(i)

        i = partitions_flat.index 
    #--- End: for

    new_shape = [len(set(s)) 
                 for s in numpy_unravel_index(flat_pm_indices, partitions.shape)]

    new_partition_matrix = numpy_empty((len(flat_pm_indices),), dtype=object)
    new_partition_matrix[...] = partitions_list
    new_partition_matrix.resize(new_shape)

    return new_partition_matrix
#--- End: def

# --------------------------------------------------------------------
#
# --------------------------------------------------------------------
def _getattr(x, attr):
    if not x:
        return False
    return getattr(x, attr)
_array_getattr = numpy_vectorize(_getattr)

def _broadcast(a, shape):
    '''

Broadcast an array to a given shape.
    
It is assumed that ``len(array.shape) <= len(shape)`` and that the
array is broadcastable to the shape by the normal numpy boradcasting
rules, but neither of these things are checked.
    
For example, ``d[...] = d._broadcast(e, d.shape)`` gives the same
result as ``d[...] = e``
    
:Parameters:

    a: numpy array-like

    shape: `tuple`

:Returns:

    out: `numpy.ndarray`

'''
# Replace with numpy.broadcast_to v1.10 ??/

    a_shape = numpy_shape(a)
    if a_shape == shape:
        return a
    
    tile = [(m if n == 1 else 1)
            for n, m in zip(a_shape[::-1], shape[::-1])]
    tile = shape[0:len(shape)-len(a_shape)] + tuple(tile[::-1])
    
    return numpy_tile(a, tile)
#--- End: def

class AuxiliaryMask(object):
    '''
'''
    def __init__(self):
        '''
        '''
        self._mask = []
    #--- End: def

    def __getitem__(self, indices):
        '''
        '''
        new = type(self)()

        for mask in self._mask:
            mask_indices = [(slice(None) if n == 1 else index)
                            for n, index in zip(mask.shape, indices)]
            new._mask.append(mask[tuple(mask_indices)])
            
        return new
    #--- End: def

#    # ----------------------------------------------------------------
#    # Attributes
#    # ----------------------------------------------------------------
#    @property
#    def mask(self):
#        '''
#'''
#        _auxiliary_mask = self._mask
#        if not _auxiliary_mask:
#            return None
#
#        mask = _auxiliary_mask[0]
#        for m in _auxiliary_mask[1:]:
#            mask = mask | m
#
#        return mask
#    #-- End: def
#
#    @auxiliary_mask.setter
#    def mask(self, value):
#        if value is None:
#            return
#
#        if numpy_ndim(value) != self._ndim:
#            raise ValueError(
#"Auxiliary mask must have same number of axes as the data array ({0}!={1})".format(
#    numpy_ndim(value), self._ndim))
#
#        for i, j in zip(numpy_shape(value), self._shape):
#            if not (i == j or i == 1):
#                raise ValueError(
#"Auxiliary mask shape {0} is not broadcastable to data array shape {1}".format(
#    numpy_shape(value), self._shape))
#
#        if not self._auxiliary_mask:
#            value = self.asdata(value)
#        
#            # Make sure that the same axes are cyclic for the data
#            # array and the auxiliary mask
#            indices = [self._axes.index(axis) for axis in self._cyclic]
#            value._cyclic = set([value._axes[i] for i in indices])
#
#            self._auxiliary_mask = [value]
#        else:
#            self._auxiliary_mask.append(value)
#    #--- End: def

    @property
    def dtype(self):
        '''
'''
        return self._mask[0].dtype
    #--- End: def

    @property
    def ndim(self):
        '''
'''
        return self._mask[0].ndim
    #--- End: def
            
    @property
    def dtype(self):
        '''
'''
        return self._mask[0].dtype
    #--- End: def

    # ----------------------------------------------------------------
    # Methods
    # ----------------------------------------------------------------
    def append(self, mask):
        '''
        '''
        self._mask.append(mask)
    #--- End: def
