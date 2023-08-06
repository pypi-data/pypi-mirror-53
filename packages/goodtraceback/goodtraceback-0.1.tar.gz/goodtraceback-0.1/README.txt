# goodtraceback
Simple module to extend the usefullnes of python stacktrace for unattended scripts.
To use it just import it and generate an exception.


import goodtraceback

def func(param):
    inner_variable = {'this': 'is', 'the': 'inner val'}
    # This generates an exception
    return param * None


func(5)

