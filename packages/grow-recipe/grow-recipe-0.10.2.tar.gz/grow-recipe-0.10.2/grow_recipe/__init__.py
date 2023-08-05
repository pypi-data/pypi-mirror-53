from grow_recipe.schema import check_for_error
from grow_recipe.query.get_grow_stage import get_grow_stage
from grow_recipe.query.find_metric_value import find_metric_value


def get_metric(xml, topic, metric, start_time, query_time=None):

    stage = get_grow_stage(xml, start_time, query_time)

    return find_metric_value(xml, stage, topic, metric)
