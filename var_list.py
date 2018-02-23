from sys import getsizeof
from IPython import get_ipython
import json
_Jupyter = get_ipython()
_hidden = _Jupyter.user_ns_hidden.keys()


def _getsizeof(x):
    # return the size of variable x. Amended version of sys.getsizeof
    # which also supports ndarray, Series and DataFrame
    if type(x).__name__ in ['ndarray', 'Series']:
        return x.nbytes
    elif type(x).__name__ == 'DataFrame':
        return x.memory_usage().sum()
    else:
        return getsizeof(x)


def var_dic_list():
    types_to_exclude = ['module', 'function', 'builtin_function_or_method',
                        'instance', '_Feature', 'type', 'ufunc']
    values = [k for k in _Jupyter.ns_table['user_local'] if k not in _hidden]
    vardic = [{'varName': v, 'varType': type(eval(v)).__name__, 'varSize': _getsizeof(eval(v)), 'varContent': str(eval(v))[:200]} # noqa
    for v in values if (v not in ['_html', '_Jupyter', '_hidden']) & (type(eval(v)).__name__ not in types_to_exclude)] # noqa 
    return json.dumps(vardic)


# command to refresh the list of variables
print(var_dic_list())
