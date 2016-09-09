# coding=utf-8
from . import const

# "+" Ascending, "-" for the descending order.
const.SEARCH_SORT_ASC = '+'
const.SEARCH_SORT_DESC = '-'


class Search(object):

    """
    This class provides get search api and scan api response result
    """

    def __init__(self, client):
        self.client = client
        self.path = '/search'

        self.query = ''
        self.indexes = []
        self.qp = None
        self.disable = None
        self.summaries = []
        self.fetch_fields = None
        self.formula_name = None
        self.first_formula_name = None

        # config args
        self.start = 0
        self.hits = 50
        self.format = 'json'
        self.rerank_size = 200

        self.sort = []      # ['-price']
        self.filter = ''    # fieldName>=1 AND fieldName>=1 OR fieldName>=1
        self.distinct = {}
        self.aggregate = {}
        self.kvpairs = ''

    def addIndex(self, index_name):
        '''
        add query index
        '''
        self.indexes.append(index_name)

    def addSort(self, field_name, sort_mode=const.SEARCH_SORT_DESC):
        """
        table field sort mode
        Args:
            field_name (str): table field name
            sort_mode (str): sort mode, options: const.SEARCH_SORT_ASC, const.SEARCH_SORT_DESC
        """
        self.sort.append('%s%s' % (sort_mode, field_name))

    def addDistinct(self, key, dist_count=1, dist_times=1, reserved=True, dist_filter=None, update_total_hit=False, grade=None):
        """
        Args:
            key (str): dist_key
            dist_count (int): default value: 1
            dist_times (int): default value: 1
            reserved (bool): default value: True
            update_total_hit (bool): default value: False
            dist_filter (str): dist_filter
            grade (list[float]): grade
        """
        _distinct = {}
        _distinct['dist_key'] = key
        _distinct['dist_count'] = dist_count
        _distinct['dist_times'] = dist_times

        if reserved:
            _distinct['reserved'] = 'true'
        else:
            _distinct['reserved'] = 'false'

        if update_total_hit:
            _distinct['update_total_hit'] = 'true'
        else:
            _distinct['update_total_hit'] = 'false'

        if dist_filter:
            _distinct['dist_filter'] = dist_filter

        if grade:
            _distinct['grade'] = '|'.join([str(i) for i in grade])

        self.distinct[key] = _distinct

    def addSummary(self, field_name, length=None, element=None, ellipsis=None, snipped=0, element_prefix=None, element_postfix=None):
        """
        Args:
            field_name (str): summary_field
            length (int): summary_len
            element (str): summary_element
            ellipsis (str): summary_ellipsis
            snipped (int): summary_snipped
            element_prefix (str): summary_element_prefix
            element_postfix (str): summary_element_postfix
        """
        if not field_name:
            return
        _summary = {}
        _summary['summary_field'] = field_name
        if length:
            _summary['summary_len'] = str(length)
        if element:
            _summary['summary_element'] = element
        if ellipsis:
            _summary['summary_ellipsis'] = ellipsis
        if snipped:
            _summary['summary_snipped'] = snipped
        if element_prefix:
            _summary['summary_element_prefix'] = element_prefix
        if element_postfix:
            _summary['summary_element_postfix'] = element_postfix
        self.summaries.append(_summary)

    def addFilter(self, expr_filter, operator='AND'):
        if not self.filter:
            self.filter = expr_filter
        else:
            self.filter = '%s %s %s' % (self.filter, operator, expr_filter)

    def addAggregate(self, group_key, agg_fun, agg_range=None, max_group=None, agg_filter=None, agg_sampler_threshold=None, agg_sampler_step=None):
        """
        Args:
            group_key (str): group_key
            agg_fun (str): agg_fun: count()、sum(id)、max(id)、min(id)
            agg_range (list[str]): range : ['0~100', '100~500']
            max_group (int): return max group number
            agg_filter (str): agg_filter
            agg_sampler_threshold (int): agg_sampler_threshold
            agg_sampler_step (int): agg_sampler_step
        """

        if not group_key or not agg_fun:
            return
        _aggregate = {}
        _aggregate['group_key'] = group_key
        _aggregate['agg_fun'] = agg_fun

        if agg_range and isinstance(agg_range, list):
            _aggregate['range'] = agg_range
        if max_group:
            _aggregate['max_group'] = max_group
        if agg_filter:
            _aggregate['agg_filter'] = agg_filter
        if agg_sampler_threshold:
            _aggregate['agg_sampler_threshold'] = agg_sampler_threshold
        if agg_sampler_step:
            _aggregate['agg_sampler_step'] = agg_sampler_step

        self.aggregate[group_key] = _aggregate

    def call(self):
        _query = []

        config = []
        config.append('format:%s' % self.format)
        config.append('start:%s' % self.start)
        config.append('hit:%s' % self.hits)
        config.append('rerank_size:%s' % self.rerank_size)
        _query.append('config=%s' % ','.join(config))

        _query.append('query=%s' % self.query)

        if self.sort:
            _query.append('sort=%s' % ';'.join(self.sort))

        if self.filter:
            _query.append('filter=%s' % self.filter)

        if self.distinct:
            _distinct = []
            for key, val in self.distinct.items():
                item = []
                for k, v in val.items():
                    item.append('%s:%s' % (k, v))
                _distinct.append(','.join(item))
            _query.append('distinct=%s' % ';'.join(_distinct))

        if self.aggregate:
            _aggregate = []
            for key, val in self.aggregate.items():
                item = []
                for k, v in val.items():
                    if k == 'range':
                        # range:0~100,range:100~200
                        _ranges = []
                        for _ in v:
                            _ranges.append('%s:%s' % (k, _))
                        item.append(','.join(_ranges))
                    else:
                        item.append('%s:%s' % (k, v))
                _aggregate.append(','.join(item))
            _query.append('aggregate=%s' % ';'.join(_aggregate))

        if self.kvpairs:
            _query.append('kvpairs=%s' % self.kvpairs)

        params = {}
        params['format'] = self.format
        params['index_name'] = ';'.join(self.indexes)
        params['query'] = '&&'.join(_query)

        if self.qp:
            params['qp'] = self.qp

        if self.disable:
            params['disable'] = self.disable

        if self.summaries:
            _summaries = []
            for summary in self.summaries:
                _summary = []
                for key, val in summary.items():
                    _summary.append('%s:%s' % (key, val))
                _summaries.append(','.join(_summary))
            params['summary'] = ';'.join(_summaries)

        if self.fetch_fields:
            params['fetch_fields'] = ';'.join(self.fetch_fields)

        if self.formula_name:
            params['formula_name'] = self.formula_name

        if self.first_formula_name:
            params['first_formula_name'] = self.first_formula_name

        result = self.client.getResponse(self.path, params)
        return result

    def scroll(self, scroll, search_type=None, scroll_id=None):
        """
        Args:
            scroll (int or str): int value of time in milliseconds,
                                 str value : time units include：w=Week, d=Day, h=Hour, m=minute, s=second
            search_type (str): options: scan
            scroll_id (str): scroll_id
        """
        _query = []
        _query.append('query=%s' % self.query)

        if self.filter:
            _query.append('filter=%s' % self.filter)

        params = {}
        params['scroll'] = scroll
        if search_type:
            params['search_type'] = search_type
        if scroll_id:
            params['scroll_id'] = scroll_id

        params['index_name'] = ';'.join(self.indexes)
        params['query'] = '&&'.join(_query)

        if self.qp:
            params['qp'] = self.qp

        if self.disable:
            params['disable'] = self.disable

        if self.summaries:
            _summaries = []
            for summary in self.summaries:
                _summary = []
                for key, val in summary.items():
                    _summary.append('%s:%s' % (key, val))
                _summaries.append(','.join(_summary))
            params['summary'] = ';'.join(_summaries)

        if self.fetch_fields:
            params['fetch_fields'] = ';'.join(self.fetch_fields)

        if self.formula_name:
            params['formula_name'] = self.formula_name

        if self.first_formula_name:
            params['first_formula_name'] = self.first_formula_name

        result = self.client.getResponse(self.path, params)
        return result
