from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    """
    Simulates a db query where a part of the result set is
    retrieved from the db table by providing a limit and offset.

    @params

        -limit: constrains the maximum rows returned
        -offset: reps the starting position of the rows with reference
                to complete size of data returned.
    """

    max_limit = 10
    default_limit = 5
    limit_query_param = "limit"
    offset_query_param = "offset"
