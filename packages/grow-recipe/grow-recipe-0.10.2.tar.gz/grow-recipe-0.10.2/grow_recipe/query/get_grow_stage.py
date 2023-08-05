from datetime import datetime

from xml.etree import ElementTree

from grow_recipe import constants, check_for_error


def get_grow_stage(xml, start_time, query_time=None):
    """
    Takes in a buffer, xml, and attempts to find a stage based on the how much
    time has elapsed since the beginning of the grow
    """
    # put the buffer back to the beginning
    xml.seek(0)

    # raise schema errors if they exist
    check_for_error(xml)

    xml.seek(0)

    tree = ElementTree.parse(xml)

    if not query_time:
        query_time = datetime.utcnow()

    if start_time > query_time:
        raise ValueError('start_time is after query_time')

    seconds_diff = (query_time - start_time).seconds

    root = tree.getroot()

    # keeps track of the cumulative amount of seconds while checking
    # each stage
    time_counter = 0

    for stage in root.getchildren():

        if stage.tag == constants.DEFAULT:
            continue

        duration_str = stage.attrib.get('duration')
        if duration_str is None:
            continue
        duration = int(duration_str)

        if seconds_diff < time_counter + duration:
            return stage.tag

        time_counter += duration
