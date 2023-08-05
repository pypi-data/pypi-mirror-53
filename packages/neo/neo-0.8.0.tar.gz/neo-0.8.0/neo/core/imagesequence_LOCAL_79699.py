from neo.core.regionofinterest import RegionOfInterest
from neo.core.analogsignal import AnalogSignal, _get_sampling_rate
from neo.core.dataobject import ArrayDict
import quantities as pq
import numpy as np
from neo.core.basesignal import BaseSignal


class ImageSequence(BaseSignal):
    # format ImageSequence subclass dataobject
    # should be a 3d numerical array
    # format data[image_index][y][x]
    # meta data sampling interval/frame rate , spatia scale
    #
    # should contain a method  which take one or more regionofinterest as argument
    # and returns an analogicsignal
    #
    # exemples c2_avg  1 px =25ym  1 frame 2ms

    _single_parent_objects = ('Segment')
    _single_parent_attrs = ('segment')
    _quantity_attr = 'image_data'
    _necessary_attrs = (('image_data', pq.Quantity, 3),
                        ('sampling_rate', pq.Quantity, 0),
                        ('spatial_scale', pq.Quantity, 0))
    _recommended_attrs = BaseSignal._recommended_attrs

    def __new__(cls, image_data=None, units=None, dtype=None, copy=True, spatial_scale=None, sampling_period=None,
                sampling_rate=None, name=None, description=None, file_origin=None, array_annotations=None,
                **annotations):

        if spatial_scale is None:
            raise ValueError('spatial_scale is required')

        image_data = np.stack(image_data)

        if len(image_data.shape) != 3:
            raise ValueError('list doesn\'t have the good number of dimension')

        obj = pq.Quantity(image_data, units=units, dtype=dtype, copy=copy).view(cls)

        # function from analogsignal.py in neo/core directory
        obj.sampling_rate = _get_sampling_rate(sampling_rate, sampling_period)
        obj.spatial_scale = spatial_scale
        print("sampling rate in __new__: " + str(obj.sampling_rate))
        return obj

    def __init__(self, image_data=None, units=None, sampling_rate=None, sampling_period=None, spatial_scale=None,
                 name=None, description=None, file_origin=None, array_annotations=None, **annotations):
        BaseSignal.__init__(self, name=name, description=description, file_origin=file_origin,
                            array_annotations=array_annotations, **annotations)

    def __array_finalize__(self, obj):
        '''
        This is called every time a new image sequence is created.

        It is the appropriate place to set default values for attributes
        for an image sequence constructed by slicing or viewing.

        User-specified values are only relevant for construction from
        constructor, and these are set in __new__ in the child object.
        Then they are just copied over here.
        '''
        # print('In array_finalize:')
        # print('   self type is %s' % type(self))
        # print('   obj type is %s' % type(obj))

        super(ImageSequence, self).__array_finalize__(obj)

        # The additional arguments
        self.annotations = getattr(obj, 'annotations', {})
        # Add empty array annotations, because they cannot always be copied,
        # but do not overwrite existing ones from slicing etc.
        # This ensures the attribute exists
        if not hasattr(self, 'array_annotations'):
            self.array_annotations = ArrayDict(self._get_arr_ann_length())

        # Globally recommended attributes
        self.name = getattr(obj, 'name', None)
        self.file_origin = getattr(obj, 'file_origin', None)
        self.description = getattr(obj, 'description', None)

        # Parent objects
        self.segment = getattr(obj, 'segment', None)
        self.channel_index = getattr(obj, 'channel_index', None)

        # Specific attributes
        self.sampling_rate = getattr(obj, 'sampling_rate', None)
        self.spatial_scale = getattr(obj, 'spatial_scale', None)
        #raise Exception()

        print("obj.sampling rate in __array_finalize__: " + str(getattr(obj, 'sampling_rate', None)))

    def _check_consistency(self, other):
        '''
        Check if the attributes of another :class:`ImageSequence`
        are compatible with this one.
        '''
        if isinstance(other, ImageSequence):
            for attr in ("sampling_rate", "spatial_scale"):
                if getattr(self, attr) != getattr(other, attr):
                    raise ValueError(
                        "Inconsistent values of %s" % attr)  # how to handle name and annotations?

    def signal_from_region(self, *region):

        if len(region) == 0:
            raise ValueError('no region of interest have been given')

        region_pixel = []
        for i in range(len(region)):
            region_pixel.append(region[i].pixels_in_region())

        analogsignal_list = []
        for i in region_pixel:
            data = []
            for frame in range(len(self)):
                picture_data = 0
                count = 0
                for v in i:
                    picture_data += self.view(pq.Quantity)[frame][v[0]][v[1]]
                    count += 1
                data.append((picture_data * 1.0) / count)
            analogsignal_list.append(AnalogSignal(data, self.units, sampling_rate=self.sampling_rate))

        return analogsignal_list
