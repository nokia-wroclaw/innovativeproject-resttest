def transform_nested_array(array, transform):
    for i in range(0, len(array)):
        if isinstance(array[i], (list, tuple)):
            array[i] = transform_nested_array(array[i], transform)
        else:
            array[i] = transform(array[i])
    return array