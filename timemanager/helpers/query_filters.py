# from sqlalchemy import or_, func


# RESOURCE http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters


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




# ADD CUSTOM FILTERS TO LIST


FILTERS_LIST = {

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
