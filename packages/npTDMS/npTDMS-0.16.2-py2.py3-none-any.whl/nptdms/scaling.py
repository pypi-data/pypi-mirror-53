import logging
import numpy as np
import re


log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


class LinearScaling(object):
    def __init__(self, intercept, slope):
        self.intercept = intercept
        self.slope = slope

    def scale(self, data):
        return data * self.slope + self.intercept


class PolynomialScaling(object):
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def scale(self, data):
        return np.polynomial.polynomial.polyval(data, self.coefficients)


class MultiScaling(object):
    def __init__(self, scalings):
        self.scalings = scalings

    def scale(self, data):
        for scaling in self.scalings:
            data = scaling.scale(data)
        return data


def get_scaling(channel):
    scalings = (_get_object_scaling(o) for o in _tdms_hierarchy(channel))
    try:
        return next(s for s in scalings if s is not None)
    except StopIteration:
        return None


def _get_object_scaling(obj):
    num_scalings = _get_number_of_scalings(obj.properties)
    if num_scalings is None or num_scalings == 0:
        return None

    try:
        scaling_status = obj.properties["NI_Scaling_Status"]
    except KeyError:
        scaling_status = "unscaled"

    # NI documentation doesn't describe how the scaling status
    # should be used, but based on the behaviour observed from the Excel
    # plugin, when the scaling status is unscaled, all scalings are applied,
    # but if it is scaled, only the last scale is used.
    # See https://github.com/adamreeve/npTDMS/issues/64 and
    # https://github.com/adamreeve/npTDMS/issues/120
    if scaling_status == "scaled":
        scale_indices = [num_scalings - 1]
    else:
        scale_indices = range(num_scalings)

    scalings = []
    for scale_index in scale_indices:
        type_property = 'NI_Scale[%d]_Scale_Type' % scale_index
        try:
            scale_type = obj.properties[type_property]
        except KeyError:
            # Sometimes num scalings is > 1 but some scalings are not provided
            continue
        if scale_type == 'Polynomial':
            scalings.append(_read_polynomial_scaling(obj, scale_index))
        elif scale_type == 'Linear':
            scalings.append(_read_linear_scaling(obj, scale_index))
        else:
            log.warning("Unsupported scale type: %s", scale_type)
            return None

    if not scalings:
        return None
    if len(scalings) > 1:
        return MultiScaling(scalings)
    return scalings[0]


def _read_linear_scaling(obj, scale_index):
    return LinearScaling(
        obj.properties["NI_Scale[%d]_Linear_Y_Intercept" % scale_index],
        obj.properties["NI_Scale[%d]_Linear_Slope" % scale_index])


def _read_polynomial_scaling(obj, scale_index):
    try:
        number_of_coefficients = obj.properties[
            'NI_Scale[%d]_Polynomial_Coefficients_Size' % (scale_index)]
    except KeyError:
        number_of_coefficients = 4
    coefficients = [
        obj.properties[
            'NI_Scale[%d]_Polynomial_Coefficients[%d]' % (scale_index, i)]
        for i in range(number_of_coefficients)]
    return PolynomialScaling(coefficients)


def _tdms_hierarchy(tdms_channel):
    yield tdms_channel

    tdms_file = tdms_channel.tdms_file
    if tdms_file is None:
        return

    group_name = tdms_channel.group
    if group_name is not None:
        try:
            yield tdms_file.object(group_name)
        except KeyError:
            pass

    try:
        yield tdms_file.object()
    except KeyError:
        pass


_scale_regex = re.compile(r"NI_Scale\[(\d+)\]_Scale_Type")


def _get_number_of_scalings(properties):
    num_scalings_property = "NI_Number_Of_Scales"
    if num_scalings_property in properties:
        return int(properties[num_scalings_property])

    matches = (_scale_regex.match(key) for key in properties.keys())
    try:
        return max(int(m.group(1)) for m in matches if m is not None) + 1
    except ValueError:
        return None
