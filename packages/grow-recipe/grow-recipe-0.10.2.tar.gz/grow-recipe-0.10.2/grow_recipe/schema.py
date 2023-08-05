import logging
import os

LXML_INSTALLED = True
try:
    from lxml import etree
except ImportError:
    LXML_INSTALLED = False

DEFAULT_SCHEMA = os.path.join(os.path.dirname(__file__), 'grow-recipe.xsd')

logger = logging.getLogger('grow-recipe')


def check_for_error(xml, schema=None, raise_exception=True):
    """
    Returns or raises the schema error message. If there is no errors it
    returns None. If there are multiple errors, only returns or raises the
    first error.
    """

    if not LXML_INSTALLED:
        logger.warning('Cannot validate grow recipe against schema without '
                       'lxml package installed. If you would like to perform '
                       'schema validation without lxml, please refer to the '
                       'documentation on how to do so.')
        return None

    if not schema:
        with open(DEFAULT_SCHEMA, 'r') as schema_file:
            schema_tree = etree.parse(schema_file)
            schema = etree.XMLSchema(schema_tree)

    xml_str = xml.read().replace('\n', '').encode('utf-8')
    parser = etree.XMLParser(schema=schema)

    try:
        etree.fromstring(xml_str, parser)
    except etree.XMLSyntaxError as e:
        if raise_exception:
            raise

        if e.msg:
            return e.msg
        else:
            return 'Error parsing XML'

    return None
