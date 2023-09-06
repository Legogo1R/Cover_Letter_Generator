def get_dir_of_obj(object, filter='__', include=False):
    """
    Returns methods and atributes of object with filtering
    """
    method_list = [method for method in dir(object) if method.startswith(filter) is include]
    return method_list
