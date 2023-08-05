import numbers

def is_scalar(x):
    return isinstance(x, (numbers.Number, str))


def is_vector(x):
    return hasattr(x, "__len__") and all(is_scalar(i) for i in x)


def is_number(x):
    return isinstance(x, numbers.Number)


def is_vector_of_type(x):
    

def is_numeric_vector(x):
    return hasattr(x, "__len__") and all(is_number(i) for i in x)

def assert_is_numeric_array(x):
    if not hasattr(x, "__len__"):
        raise TypeError("Attempted operation that is only defined "
                        "for array-like objects, but got %s, "
                        "which is a %s." % (x, type(x).__name__))
    for i in x:
        if not is_number(i):
            raise TypeError("Attempted operation that is only "
                            "defined for array-like objects "
                            "containing all numbers, but got an "
                            "array containing %s, which is a %s." %
                            (i, type(i).__name__))
    return
