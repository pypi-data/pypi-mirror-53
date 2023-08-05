"""
Reference these constants in your application code to avoid using
magic strings. There are also sets for each type of constant for
convenience to check if a string is valid. For example:

valid_stage = 'foo' in stages
valid_topic = 'bar' in topics
valid_metric = 'baz' in metrics
"""


# the root node in the XML structure
ROOT_NODE = 'recipe'

DEFAULT = 'default'
GERMINATION = 'germination'
VEGETATIVE = 'vegetative'
FLOWERING = 'flowering'
FRUITING = 'fruiting'
stages = {DEFAULT, GERMINATION, VEGETATIVE, FLOWERING, FRUITING}


AIR = 'air'
WATER = 'water'
LIGHT = 'light'
topics = {AIR, WATER, LIGHT}


T9E = 'temperature'
HUMIDITY = 'relative-humidity'
EC = 'electro-conductivity'
OXYGEN = 'dissolved-oxygen'
OXIDIZING_REDUCTION_POTENTIAL = 'oxidizing-reduction-potential'
HARDNESS = 'hardness'
PH = 'ph'
VPD = 'vpd'
BICARBONATE = 'bicarbonate'
NITROGEN = 'nitrogen'
POTASSIUM = 'potassium'
CALCIUM = 'calcium'
MAGNESIUM = 'magnesium'
SULFER = 'sulfer'
IRON = 'iron'
COPPER = 'copper'
ZINC = 'zinc'
MANGANESE = 'manganese'
SODIUM = 'sodium'
BORON = 'boron'
CHLORINE = 'chlorine'
SILICON = 'silicon'
IRON_CHELATES = 'iron-chelates'
SODIUM_CHLORIDE = 'sodium-chloride'
metrics = {T9E, HUMIDITY, EC, OXYGEN, OXIDIZING_REDUCTION_POTENTIAL, HARDNESS,
           PH, VPD, BICARBONATE, NITROGEN, POTASSIUM, CALCIUM, MAGNESIUM,
           SULFER, IRON, COPPER, ZINC, MANGANESE, SODIUM, BORON, CHLORINE,
           SILICON, IRON_CHELATES, SODIUM_CHLORIDE}
