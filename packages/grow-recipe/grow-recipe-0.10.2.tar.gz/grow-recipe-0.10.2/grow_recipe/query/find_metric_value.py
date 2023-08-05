from xml.etree import ElementTree

from grow_recipe import constants, check_for_error


class Metric:

    def __init__(self, min_value=None, max_value=None):
        self.min = min_value
        if self.min:
            self.min = float(self.min)

        self.max = max_value
        if self.max:
            self.max = float(self.max)


def find_metric_value(xml, stage, topic, metric):
    """
    Takes in a buffer, xml,  and finds the specified metric in the
    given stage. If the metric is not present in the given stage,
    the metric is taken from the default stage
    """

    # put the buffer back to the beginning
    xml.seek(0)

    # raise schema errors if they exist
    check_for_error(xml)

    xml.seek(0)

    tree = ElementTree.parse(xml)
    root = tree.getroot()

    if not stage:
        stage = constants.DEFAULT

    value = root.find('{stage}/{topic}/{metric}'
                       .format(root=constants.ROOT_NODE, stage=stage,
                               topic=topic, metric=metric))

    if value is None:
        value = root.find('{stage}/{topic}/{metric}'.format(
            root=constants.ROOT_NODE,
            stage=constants.DEFAULT,
            topic=topic,
            metric=metric
        ))

    if value is None:
        return None

    return Metric(value.attrib.get('min'),
                  value.attrib.get('max'))
