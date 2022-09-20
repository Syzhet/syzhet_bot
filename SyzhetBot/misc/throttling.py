def rate_limit(limit: int, key=None):
    '''Функция установки лимита для тротлинга.'''
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator
