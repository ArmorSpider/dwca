import terminaltables
from src.dwca_log.log import get_log

LOG = get_log(__name__)


def print_table(table_data, title, headers=True):
    table = terminaltables.AsciiTable(table_data, title)
    table.inner_heading_row_border = headers
    LOG.info(table.table)


def print_entity_dict(entity, stat_key):
    char_table = []
    stat_dict = entity.get_stat(stat_key, {})
    for modifier_name, value in stat_dict.items():
        char_row = [modifier_name, value]
        char_table.append(char_row)
    print_table(char_table, entity.name, headers=False)
