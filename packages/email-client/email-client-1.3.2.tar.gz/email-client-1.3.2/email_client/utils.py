import warnings


def deprecated(message=''):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used.

    :param message: message for user
    """
    def wrapper_args(func):
        def wrapper(*args, **kwargs):
            warnings.warn(f'Call to object function {func.__name__}. {message}', category=DeprecationWarning)
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__dict__.update(func.__dict__)
        return wrapper
    return wrapper_args
