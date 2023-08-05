class QueryFilter(object):
    """
    add filter condition on specific QuerySet
    Usage::
      >>> query_set, allow_fields, query_params = User.objects.all(), ["name"], ["name=ethan"]
      >>> q = QueryFilter(query_set, allow_fields, query_params)
      >>> query_set = q.get_filter_queryset()
    """

    def __init__(self, query_set, allow_fields, query_params):
        """
        :param query_set: :class:`Request <QuerySet>`.
        :param allow_fields: allow filter fields 
        :param query_params: eg ["name=ethan", "age=12"]
        """
        self.query_set = query_set
        self.query_params = query_params
        self.allow_fields = allow_fields

    def get_filter_queryset(self):
        raise NotImplemented


class SimpleQueryFilter(QueryFilter):
    list_operation = "in",

    def is_list_operation(self, param):
        return param.split("__")[-1] in self.list_operation

    @classmethod
    def get_query_kwargs(cls, param):
        """
        >>>"id__get=3"
        >>>{"id_get": 3}
        """
        left, right = param.split("=")
        return {left: right}

    def is_valid_param(self, param):
        field = param.split("_")[0].strip("^")
        return field in self.allow_fields

    def get_filter_queryset(self):
        query = self.query_set
        query_params = self.query_params

        filter_fields = {field: value for field, value in query_params.items() if not str(field).startswith("^") if
                         self.is_valid_param(field)}
        exclude_fields = {field.strip("^"): value for field, value in query_params.items() if str(field).startswith("^")
                          if
                          self.is_valid_param(field)}

        order_by = query_params.get("order_by", "-id")
        order_bys = order_by.split(",")

        # filter
        for field, value in filter_fields.items():
            if self.is_list_operation(field):
                value = value.split(",")
            query = query.filter(**{field: value})

        # exclude filter
        for field, value in exclude_fields.items():
            if self.is_list_operation(field):
                value = value.split(",")
            query = query.exclude(**{field: value})

        # order_by
        query = query.order_by(*order_bys)
        return query
