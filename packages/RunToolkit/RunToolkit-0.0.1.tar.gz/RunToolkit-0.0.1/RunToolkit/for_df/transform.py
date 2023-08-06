# -*- coding: utf-8 -*-
# @Time     : 2019/5/13 13:55
# @Author   : Run 
# @File     : transform.py
# @Software : PyCharm

"""
Notes:
    1. experiments about nan
        >>> set([float('nan'), float('nan')])
        {nan, nan}

        >>> set([np.nan, np.nan])
        {nan}

        >>> df = pd.DataFrame({'a': [np.nan, np.nan, float('nan'), float('nan')]})
        >>> df
            a
        0 NaN
        1 NaN
        2 NaN
        3 NaN
        >>> set(df.a)
        {nan, nan, nan, nan}
        >>> df.a.unique()
        array([nan])
    2.
        1. {key: y, ...} 注意：如果key中有重复项的话，后面的y值会覆盖之前的
        2. {key: set(y), ...} 建议去除y中的NaN后再进行该操作，具体原因详见Notes1
        3. {key: unique(y), ...}
                当y中不存在NaN时，效果等同于set(y)，但是得到的并不是集合，而是np.array
                当y中存在NaN时，得到的结果中含有nan
        4. {key: nunique(y), ...} 效果相当于去除y中nan后，再进行len(set(y))
        5. {key: count(y), ...} 效果相当于去除y中nan后，再进行len(list())
        6. {key: f(y), ...} 其中f可以为: max, min, mean, median, sum。效果相当于去除y中nan后，再进行这些运算
        7. {key: len(set(y)), ...} 通常想要的结果是nunique(y)，该操作没什么意义，具体原因详见Notes1
        8. {key: len(list(y)), ...}
                通常想要的结果是count(y)，统计y中非nan值的数目，和y是有关系的
                len(list(y))实际上和y并没有关系，统计的是同一个key重复出现的次数，推荐使用count()
    3. 关于warnings.warn()的使用有些疑问, 在console中重复运行同一句代码，只有第一次会输出相应警告，后续不再会重复输出。使用logging模块进行替代。
"""

import pandas as pd
from collections import defaultdict, Counter
# import warnings
import re
from RunToolkit.for_list import flatten_iterable
from RunToolkit.utils import gen_logger


class Cube:
    """mainly used for transforming df to dict"""
    __info_dict = {}
    df2dict_logger = gen_logger('df2dict')

    @classmethod
    def df2dict(cls, df, format_str=None, keys=None, value=None, func=None, dropna=False,
                with_warnings=True, print_codes=False, store_info=True):
        """
        Converts DataFrame to dict according to specific format.
        e.g.1. {(a1, a2, a3): {b: {(c1, c2): set(d), ...}, ...}, ...}
            method1：df2dict(df, "{(a1, a2, a3): {b: {(c1, c2): set(d), ...}, ...}, ...}")
            method2：df2dict(df, keys=[('a1', 'a2', 'a3'), 'b', ('c1', 'c2')], value='d', func='set')
        :param df:
        :param format_str: 数据格式字符串。
            Notes:
                1. 在一些情况下，解析字符串可能会出错，比如字段名称中含有英文冒号`:`、逗号`,`、各种括号或者`set()`等函数。
                   此时推荐采用第二种传参方式，明确地规定keys, value和func。
                2. 该有省略号"..."的地方必须有，以指示这是一个复杂数据类型。
            Examples:
                single-layer dict: key和y均为单个字段x或多个字段组成的元组(x1, ..., xn)，格式允许的情况下y也可以为列表[x1, ..., xn]
                    1_1:  {key: y, ...}
                    1_2:  {key: {y, ...}, ...} or {key: set(y), ...}
                    1_3:  {key: [y, ...], ...} or {key: list(y), ...}
                    1_4:  {key: count(), ...}
                    1_5:  {key: f(y), ...} 其中f可以为: unique, nunique, count, max, min, mean, median, sum
                    1_6:  {key: f(...g(y)...), ...}  其中函数嵌套可以为: len(set(y)), len(list(y)), list(set(y))
                multi-layer dict: 任意多层嵌套
                    multi: {key1: {key2: {key3: y, ...}, ...}, ...}
                           {key1: {key2: {key3: f(y), ...}, ...}, ...}
        :param keys: list
        :param value: single field or tuple/list of multi field
        :param func:
        :param dropna: 默认为False todo
            False: 1_4中对key的count计数包含key的NaN在内；1_5中对y的nunique计数包含y中的NaN在内
            True:
        :param with_warnings: 对数据进行有些操作时可能会存在隐患，默认为True，检测这些隐患是否存在，若存在则屏显警告信息
        :param print_codes: todo
        :param store_info:
        :return:
        """
        if df.empty:
            # warnings.warn("DataFrame is empty, return {} directly.")
            cls.df2dict_logger.warning("DataFrame is empty, return {} directly.")
            return {}
        cols_set = set(df.columns)
        df_len = len(df)

        # parse keys, value, func
        if format_str is not None:  # method1
            assert isinstance(format_str, str)
            if ':' not in format_str:
                raise Exception("too simple, please do this directly")
            format_str = format_str.strip()
            count = _check_brackets(format_str)  # num of layers
            keys, value, func = _parse_format_str(format_str, count, cols_set)
        else:  # method2
            count = len(keys)

        if store_info:  # todo merge to bottom
            format_str = _gen_format_str(keys, value, func)
            # print("format_str:", format_str)

        # todo change parameter value to value_ser for functions value_x_y, more elegant to solve tuple(list) value
        vtype = value.__class__
        if vtype == str:
            delete_flag = False
        else:
            delete_flag = True
            tmp_col = 'tmp'
            while tmp_col in cols_set:  # avoid tmp_col in df.columns
                tmp_col *= 2
            if vtype == tuple:
                df[tmp_col] = list(zip(*[df[k] for k in value]))
            else:  # list
                df[tmp_col] = df[value].values.tolist()
            value = tmp_col

        if count == 1:  # single layer
            keys = keys[0]
            if func is None:  # 1_1
                res = _match_1_1(df, df_len, keys, value, with_warnings, print_codes, cls.df2dict_logger)
            else:
                if isinstance(func, str):  # single function
                    if func == 'set':  # 1_2
                        res = _match_1_2(df, keys, value, with_warnings, print_codes, cls.df2dict_logger)
                    elif func == 'list':  # 1_3
                        res = _match_1_3(df, keys, value, with_warnings, print_codes, cls.df2dict_logger)
                    elif func == 'count':  # 1_4
                        res = _match_1_4(df, keys, value, dropna, with_warnings, print_codes, cls.df2dict_logger)
                    elif func in {'unique', 'nunique', 'max', 'min', 'median', 'sum', 'mean'}:
                        res = _match_1_common(df, keys, value, func, dropna, with_warnings, print_codes, cls.df2dict_logger)
                    else:
                        raise Exception("invalid func: {}".format(func))
                else:  # nested functions
                    if func == ['len', 'set']:
                        raise Exception("meaningless, please use nunique(y)")
                    elif func == ['len', 'list']:
                        raise Exception("meaningless, you might need count(y) or len()")
                    elif func == ['list', 'set']:
                        res = _match_1_nested_func_list_set(df, keys, value, with_warnings, print_codes, cls.df2dict_logger)
                    else:
                        raise Exception("invalid func combination: {}".format(func))
        else:  # multi layer
            if func is None:  # multi_1
                res = _match_multi_1(df, df_len, keys, value, with_warnings, print_codes, cls.df2dict_logger)
            else:
                if isinstance(func, str):  # single function
                    if func == 'set':  # multi_2
                        res = _match_multi_2(df, keys, value, with_warnings, print_codes, cls.df2dict_logger)
                    elif func == 'list':  # multi_3
                        res = _match_multi_3(df, keys, value, with_warnings, print_codes, cls.df2dict_logger)
                    elif func == 'count':  # multi_4
                        res = _match_multi_4(df, keys, value, with_warnings, print_codes, cls.df2dict_logger)
                    elif func in {'unique', 'nunique', 'count', 'max', 'min', 'median', 'sum', 'mean'}:
                        res = _match_multi_common(df, keys, value, func, with_warnings, print_codes, cls.df2dict_logger)
                    else:
                        raise Exception("invalid func: {}".format(func))
                else:  # functions list
                    if func == ['len', 'set']:
                        raise Exception("meaningless, please use nunique(y)")
                    elif func == ['len', 'list']:
                        raise Exception("meaningless, you might need count(y) or len()")
                    elif func == ['list', 'set']:
                        res = _match_multi_nested_func_list_set(df, keys, value, with_warnings, print_codes)
                    else:
                        raise Exception("invalid func combination: {}".format(func))

        if store_info:
            cls.__info_dict[id(res)] = format_str

        # delete tmp_col to recover df
        if delete_flag:
            df.drop(value, axis=1, inplace=True)

        return res

    @classmethod
    def get_info(cls, target):
        return cls.__info_dict[id(target)]


def _check_brackets(strs):
    """

    :param strs:
    :return: number of colons
    """
    s = {'(', ')', '[', ']', '{', '}'}
    d = {'(': ')', '[': ']', '{': '}'}
    l = []
    count = 0
    for i, c in enumerate(strs):
        if c == ":":
            if not l or l[-1][1] != '{':
                raise Exception("Invalid colon, position {}.".format(i))
            count += 1
        elif c in s:
            if c in d:
                l.append((i, c))
            else:
                if not l:
                    raise Exception("Redundant '{}', position {}".format(c, i))
                i0, c0 = l.pop()
                if d[c0] != c:
                    raise Exception("Unmatched '{}, with '{}'! position {} and {}".format(c0, c, i0, i))
    if l:
        raise Exception("Redundant parentheses: {}".format(l))
    return count


def _parse_format_str(strs, colon_num, fields):
    """

    :param strs: format_str
    :param colon_num: number of colons
    :param fields: set(columns of df)
    :return:
    """
    keys, value, func = [], None, None

    while colon_num > 0:
        tmp = re.match('{(.*?):(.*),\s*\.{3,}\s*}$', strs)
        if tmp is None:
            raise Exception("invalid format_str: {}".format(strs))
        key, strs = tmp.groups()
        key, strs = key.strip(), strs.strip()
        # keys
        if key in fields:
            keys.append(key)
        elif key.startswith('(') and key.endswith(')'):
            key_tuple = tuple(x.strip() for x in key[1: -1].split(','))
            temp = set(key_tuple) - fields
            if temp:
                raise Exception("invalid fileds: {}".format(temp))
            keys.append(key_tuple)
        else:
            raise Exception("invalid sub_str for dict's key: '{}'".format(key))

        colon_num -= 1

    # value and func
    if strs in fields:  # {key: y, ...}
        value = strs
    elif '...' in strs:
        if strs.startswith('{') and strs.endswith('}'):
            tmp2 = re.match('{(.*),\s*\.{3,}\s*}$', strs)
            if tmp2 is not None:
                value, func = tmp2.groups()[0].strip(), 'set'
                if value in fields:  # {key: {y, ...}, ...}
                    pass
                elif value.startswith('(') and value.endswith(')'):  # {key: {(y1, y2), ...}, ...}
                    value = tuple(x.strip() for x in value[1: -1].split(','))
                    temp = set(value) - fields
                    if temp:
                        raise Exception("invalid fileds: {}".format(temp))
                elif value.startswith('[') and value.endswith(']'):  # {key: {[y1, y2], ...}, ...}
                    raise TypeError("unhashable type: 'list'")
                else:
                    raise Exception("can't parse: {}".format(value))
            else:
                raise Exception("can't parse: {}".format(strs))
        elif strs.startswith('[') and strs.endswith(']'):
            tmp2 = re.match('\[(.*),\s*\.{3,}\s*\]$', strs)
            if tmp2 is not None:
                value, func = tmp2.groups()[0].strip(), 'list'
                if value in fields:  # {key: [y, ...], ...}
                    pass
                elif value.startswith('(') and value.endswith(')'):  # {key: [(y1, y2), ...], ...}
                    value = tuple(x.strip() for x in value[1: -1].split(','))
                    temp = set(value) - fields
                    if temp:
                        raise Exception("invalid fileds: {}".format(temp))
                elif value.startswith('[') and value.endswith(']'):  # {key: [[y1, y2], ...], ...}
                    value = [x.strip() for x in value[1: -1].split(',')]
                    temp = set(value) - fields
                    if temp:
                        raise Exception("invalid fileds: {}".format(temp))
                else:
                    raise Exception("can't parse: {}".format(value))
            else:
                raise Exception("can't parse: {}".format(strs))
        else:
            raise Exception("can't parse: {}".format(strs))
    else:
        if strs.startswith('(') and strs.endswith(')'):  # {key: (y1, y2), ...}
            value = tuple(x.strip() for x in strs[1: -1].split(','))
            if len(value) == 1:
                raise Exception("rewrite {} correctly".format(strs))
            temp = set(value) - fields
            if temp:
                raise Exception("invalid fileds: {}".format(temp))
        elif strs.startswith('[') and strs.endswith(']'):  # {key: [y1, y2], ...}
            value = [x.strip() for x in strs[1: -1].split(',')]
            if len(value) == 1:
                raise Exception("rewrite {} correctly".format(strs))
            temp = set(value) - fields
            if temp:
                raise Exception("invalid fileds: {}".format(temp))
        else:  # contains func
            if '[' in strs:  # {key: f([y1, y2]), ...}
                tmp = re.match('(.+)\(\[(.*?)\]\)+$', strs)
                if tmp is not None:
                    func, value = tmp.groups()
                    func = func.strip() if '(' not in func else [x.strip() for x in func.split('(')]
                    value = [x.strip() for x in value.split(',')]
                    if len(value) == 1:
                        raise Exception("please rewrite {} correctly".format(tmp))
                    temp = set(value) - fields
                    if temp:
                        raise Exception("invalid fileds: {}".format(temp))
                else:
                    raise Exception("can't parse: {}".format(strs))
            else:
                tmp = re.match('(.+)\((.*?)\)+$', strs)
                if tmp is not None:
                    func, value = tmp.groups()
                    func, value = func.strip(), value.strip()
                    if func.endswith('('):  # {key: f((y1, y2)), ...}
                        value = tuple(x.strip() for x in value.split(','))
                        if len(value) == 1:
                            raise Exception("please rewrite {} correctly".format(tmp))
                        temp = set(value) - fields
                        if temp:
                            raise Exception("invalid fileds: {}".format(temp))
                        func = func[:-1]
                        func = func.strip() if '(' not in func else [x.strip() for x in func.split('(')]
                    else:  # {key: f(y), ...}
                        value = value.strip()
                        func = func.strip() if '(' not in func else [x.strip() for x in func.split('(')]
                else:
                    raise Exception("can't parse {}".format(strs))

    return keys, value, func


def _gen_format_str(keys, value, func):
    # value
    vtype = value.__class__
    if vtype == str:
        pass
    elif vtype == tuple:
        value = '(' + ', '.join(value) + ')'
    else:  # list
        value = '[' + ', '.join(value) + ']'

    # func
    if func is None:
        pass
    elif isinstance(func, str):
        value = "{}({})".format(func, value)
    else:  # functions list
        value = '('.join(func) + '(' + value + ')' * len(func)

    res = '{' + ': {'.join(item if isinstance(item, str) else '(' + ', '.join(item) + ')' for item in keys) + \
        ': ' + value + ', ...}' * len(keys)

    return res


def _match_1_1(df, df_len, keys, value, with_warnings, print_codes, logger):
    if isinstance(keys, str):  # single column as key
        res = dict(zip(df[keys], df[value]))
        if with_warnings:
            if len(res) < df_len:
                # warnings.warn("column '{}' exists duplicates.".format(keys))
                logger.warning("column '{}' exists duplicates.".format(keys))
            if df[keys].isnull().any():
                # warnings.warn("column '{}' exists NaN".format(keys))
                logger.warning("column '{}' exists NaN".format(keys))
        # if print_codes:
        #     codes_str = "dict(zip(df['{}'], df['{}']))".format(keys, value)
        #     print("codes_str:", codes_str)
    else:  # tuple, multi columns as key
        res = dict(zip(zip(*[df[k] for k in keys]), df[value]))
        if with_warnings:
            if len(res) < df_len:
                # warnings.warn("columns tuple {} exists duplicates.".format(keys))
                logger.warning("columns tuple {} exists duplicates.".format(keys))
        # if print_codes:
        #     codes_str = "dict(zip(zip({}), df['{}']))".format(', '.join(["df['{}']".format(k) for k in keys]), value)
        #     print("codes_str:", codes_str)

    return res


def _match_1_2(df, keys, value, with_warnings, print_codes, logger):
    if with_warnings and df[value].isnull().any():
        # warnings.warn("column '{}' exists NaN, please drop or fill it".format(value))
        logger.warning("column '{}' exists NaN, please drop or fill it".format(value))

    def _f(ser, arr):
        d = defaultdict(set)
        for i, k in enumerate(ser):
            d[k].add(arr[i])
        return dict(d)

    if isinstance(keys, str):  # single column as key
        if with_warnings and df[keys].isnull().any():
            # warnings.warn("column '{}' exists NaN, please drop or fill it".format(keys))
            logger.warning("column '{}' exists NaN, please drop or fill it".format(keys))
        res = _f(df[keys], df[value].values)
    else:  # tuple, multi columns as key
        res = _f(zip(*[df[k] for k in keys]), df[value].values)

    return res


def _match_1_3(df, keys, value, with_warnings, print_codes, logger):
    if with_warnings:
        # warnings.warn("you might need set('{0}') or list(set('{0}')) instead".format(value))
        logger.warning("you might need set('{0}') or list(set('{0}')) instead".format(value))

    def _f(ser, arr):
        d = defaultdict(list)
        for i, k in enumerate(ser):
            d[k].append(arr[i])
        return dict(d)

    if isinstance(keys, str):  # single column as key
        res = _f(df[keys], df[value].values)
    else:  # tuple, multi columns as key
        res = _f(zip(*[df[k] for k in keys]), df[value].values)

    return res


def _match_1_4(df, keys, value, dropna, with_warnings, print_codes, logger):
    if value == '':
        if isinstance(keys, str):  # single column as key
            # if print_codes:
            #     codes_str = "df['{}'].value_counts().to_dict()".format(keys)
            #     print("codes_str:", codes_str)
            res = df[keys].value_counts(dropna=dropna).to_dict()
        else:  # tuple, multi columns as key
            # if print_codes:  # todo
            #     codes_str = "dict(Counter(zip(*{})))".format(', '.join(["df['{}']".format(k) for k in keys]))
            #     print("codes_str:", codes_str)
            res = dict(Counter(zip(*[df[k] for k in keys])))
    else:
        keys = [keys] if isinstance(keys, str) else list(keys)
        if with_warnings and df[value].isnull().any():
            # warnings.warn("column '{}' exists NaN, count doesn't contain number of NaNs in this column.".format(value))
            logger.warning("column '{}' exists NaN, count doesn't contain number of NaNs in this column.".format(value))
        res = df.groupby(keys)[value].count().to_dict()

    return res


def _match_1_common(df, keys, value, func, dropna, with_warnings, print_codes, logger):
    keys = [keys] if isinstance(keys, str) else list(keys)
    if print_codes:
        codes_str = "df.groupby({})['{}'].{}().to_dict()".format(keys, value, func)
        print("codes_str:", codes_str)
    #
    if func == 'unique':
        if with_warnings and df[value].isnull().any():
            # warnings.warn("column '{}' exists NaN, please drop or fill it".format(value))
            logger.warning("column '{}' exists NaN, please drop or fill it".format(value))
        res = df.groupby(keys)[value].unique().to_dict()
    elif func == 'nunique':
        # if with_warnings and df[value].isnull().any():
        #     warnings.warn("column '{}' exists NaN, nunique doesn't contain number of NaNs".format(value))
        res = df.groupby(keys)[value].nunique(dropna=dropna).to_dict()
    elif func == "max":
        res = df.groupby(keys)[value].max().to_dict()
    elif func == "min":
        res = df.groupby(keys)[value].min().to_dict()
    elif func == "median":
        res = df.groupby(keys)[value].median().to_dict()
    elif func == "sum":
        res = df.groupby(keys)[value].sum().to_dict()
    elif func == "mean":
        if with_warnings and df[value].isnull().any():
            # warnings.warn("column '{}' exists NaN, mean = sum/count, count doesn't contain number of NaNs".format(value))
            logger.warning("column '{}' exists NaN, mean = sum/count, count doesn't contain number of NaNs".format(value))
        res = df.groupby(keys)[value].mean().to_dict()
    else:
        res = None

    return res


def _match_1_nested_func_list_set(df, keys, value, with_warnings, print_codes, logger):
    # todo too slow
    keys = [keys] if isinstance(keys, str) else list(keys)
    if with_warnings and df[value].isnull().any():
        # warnings.warn("column '{}' exists NaN, please drop or fill it".format(value))
        logger.warning("column '{}' exists NaN, please drop or fill it".format(value))
    if print_codes:
        codes_str = "df.groupby({})['{}'].apply(lambda x: list(set(x))).to_dict()".format(keys, value)
        print("codes_str:", codes_str)
    return df.groupby(keys)[value].apply(lambda x: list(set(x))).to_dict()


def _match_multi_1(df, df_len, keys, value, with_warnings, print_codes, logger):
    if with_warnings:
        keys_list = flatten_iterable(keys)
        df = df.drop_duplicates(keys_list, keep='last')
        if len(df) < df_len:
            # warnings.warn("columns combination {} exists duplicates.".format(keys_list))
            logger.warning("columns combination {} exists duplicates.".format(keys_list))
        for item in keys:
            if isinstance(item, str) and df[item].isnull().any():
                # warnings.warn("column '{}' exists NaN".format(item))
                logger.warning("column '{}' exists NaN".format(item))

    return _nested_dict_set_value_from_df(df, keys, value)


def _match_multi_2(df, keys, value, with_warnings, print_codes, logger):
    if with_warnings:
        if df[value].isnull().any():
            # warnings.warn("column '{}' exists NaN, please drop or fill it".format(value))
            logger.warning("column '{}' exists NaN, please drop or fill it".format(value))
        for item in keys:
            if isinstance(item, str) and df[item].isnull().any():
                # warnings.warn("column '{}' exists NaN".format(item))
                logger.warning("column '{}' exists NaN".format(item))

    return _nested_dict_gen_set_from_df(df, keys, value)


def _match_multi_3(df, keys, value, with_warnings, print_codes, logger):
    if with_warnings:
        # warnings.warn("you might need set('{0}') or list(set('{0}')) instead".format(value))
        # logger.warning("you might need set('{0}') or list(set('{0}')) instead".format(value))
        logger.warning("you might need set('{0}') instead".format(value))
        #
        if df[value].isnull().any():
            # warnings.warn("column '{}' exists NaN, please drop or fill it".format(value))
            logger.warning("column '{}' exists NaN, please drop or fill it".format(value))
        #
        for item in keys:
            if isinstance(item, str) and df[item].isnull().any():
                # warnings.warn("column '{}' exists NaN".format(item))
                logger.warning("column '{}' exists NaN".format(item))

    return _nested_dict_gen_list_from_df(df, keys, value)


def _match_multi_4(df, keys, value, with_warnings, print_codes, logger):
    if value != '':
        raise Exception("invalid sub_str for dict's value, please change len({}) to len()".format(value))
    if with_warnings:
        for item in keys:
            if isinstance(item, str) and df[item].isnull().any():
                # warnings.warn("column '{}' exists NaN".format(item))
                logger.warning("column '{}' exists NaN".format(item))

    return _nested_dict_counter_from_df(df, keys)


def _match_multi_common(df, keys, value, func, with_warnings, print_codes, logger):
    if with_warnings:
        for item in keys:
            if isinstance(item, str) and df[item].isnull().any():
                # warnings.warn("column '{}' exists NaN".format(item))
                logger.warning("column '{}' exists NaN".format(item))
    #
    if func == 'unique':
        if with_warnings and df[value].isnull().any():
            # warnings.warn("column '{}' exists NaN, please drop or fill it".format(value))
            logger.warning("column '{}' exists NaN, please drop or fill it".format(value))
        df = df.groupby(flatten_iterable(keys))[value].unique().reset_index()
    elif func == 'nunique':
        if with_warnings and df[value].isnull().any():
            # warnings.warn("column '{}' exists NaN, nunique doesn't contain number of NaNs".format(value))
            logger.warning("column '{}' exists NaN, nunique doesn't contain number of NaNs".format(value))
        df = df.groupby(flatten_iterable(keys))[value].nunique().reset_index()
    elif func == 'count':
        if with_warnings and df[value].isnull().any():
            # warnings.warn("column '{}' exists NaN, count doesn't contain number of NaNs".format(value))
            logger.warning("column '{}' exists NaN, count doesn't contain number of NaNs".format(value))
        df = df.groupby(flatten_iterable(keys))[value].count().reset_index()
    elif func == "max":
        df = df.groupby(flatten_iterable(keys))[value].max().reset_index()
    elif func == "min":
        df = df.groupby(flatten_iterable(keys))[value].min().reset_index()
    elif func == "median":
        df = df.groupby(flatten_iterable(keys))[value].median().reset_index()
    elif func == "sum":
        df = df.groupby(flatten_iterable(keys))[value].sum().reset_index()
    elif func == "mean":
        if with_warnings and df[value].isnull().any():
            # warnings.warn("column '{}' exists NaN, mean = sum/count, count doesn't contain number of NaNs".format(value))
            logger.warning("column '{}' exists NaN, mean = sum/count, count doesn't contain number of NaNs".format(value))
        df = df.groupby(flatten_iterable(keys))[value].mean().reset_index()

    return _nested_dict_set_value_from_df(df, keys, value)


def _match_multi_nested_func_list_set(df, keys, value, with_warnings, print_codes):
    # todo too slow
    return


def _nested_dict_set_value(d, lists):
    k = lists[0]
    if len(lists) == 2:
        d[k] = lists[1]
    else:
        if k not in d:
            d[k] = {}
        _nested_dict_set_value(d[k], lists[1:])


def _nested_dict_set_value_from_df(df, keys, value):
    d = {}
    tmp = zip(*[df[item] if isinstance(item, str) else zip(*[df[k] for k in item]) for item in keys], df[value])
    for lists in tmp:
        _nested_dict_set_value(d, lists)

    return d


def _nested_dict_gen_set(d, lists):
    k = lists[0]
    if len(lists) == 2:
        if k not in d:
            d[k] = {lists[1]}
        else:
            d[k].add(lists[1])
    else:
        if k not in d:
            d[k] = {}
        _nested_dict_gen_set(d[k], lists[1:])


def _nested_dict_gen_set_from_df(df, keys, value):
    d = {}
    tmp = zip(*[df[item] if isinstance(item, str) else zip(*[df[k] for k in item]) for item in keys], df[value])
    for lists in tmp:
        _nested_dict_gen_set(d, lists)

    return d


def _nested_dict_gen_list(d, lists):
    k = lists[0]
    if len(lists) == 2:
        if k not in d:
            d[k] = [lists[1]]
        else:
            d[k].append(lists[1])
    else:
        if k not in d:
            d[k] = {}
        _nested_dict_gen_list(d[k], lists[1:])


def _nested_dict_gen_list_from_df(df, keys, value):
    d = {}
    tmp = zip(*[df[item] if isinstance(item, str) else zip(*[df[k] for k in item]) for item in keys], df[value])
    for lists in tmp:
        _nested_dict_gen_list(d, lists)

    return d


def _nested_dict_counter(d, lists):
    k = lists[0]
    if len(lists) == 1:
        if k not in d:
            d[k] = 1
        else:
            d[k] += 1
    else:
        if k not in d:
            d[k] = {}
        _nested_dict_counter(d[k], lists[1:])


def _nested_dict_counter_from_df(df, keys):
    d = {}
    tmp = zip(*[df[item] if isinstance(item, str) else zip(*[df[k] for k in item]) for item in keys])
    for lists in tmp:
        _nested_dict_counter(d, lists)

    return d


