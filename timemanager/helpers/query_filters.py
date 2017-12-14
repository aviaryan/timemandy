from timemanager.models.task_model import Task
from .custom_fields import DateTime


def extract_special_queries(queries):
    """
   Separate special queries from normal queries
   """
    specials = {}
    dc = queries.copy()
    for i in queries:
        if i.startswith('__') and i in FILTERS_LIST:
            specials[i] = queries[i]
            del dc[i]
    return (dc, specials)


def apply_special_queries(query, specials):
    """
   Apply all special queries on the current
   existing :query (set)
   """
    for i in specials:
        query = FILTERS_LIST[i](specials[i], query)
    return query


# DEFINE CUSTOM FILTERS BELOW

def task_from(value, query):
    return query.filter(Task.date >= DateTime().from_str_query(value))


def task_to(value, query):
    return query.filter(Task.date <= DateTime().from_str_query(value, True))


# ADD CUSTOM FILTERS TO LIST


FILTERS_LIST = {
    '__task_to': task_to,
    '__task_from': task_from,
}


# UTIL FUNCTIONS

def parse_args(parser, keep_none=False):
    """
    Abstraction over flask_restplus.reqparse.parser.parse_args
    It returned None value if a value was not set
    This completely removes that value from the returned dict
    """
    args = parser.parse_args()
    if not keep_none:
        args = {k: v for k, v in args.items() if v is not None}
    return args
