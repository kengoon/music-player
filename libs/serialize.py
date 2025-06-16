from jnius import autoclass


def serialize_map_to_dict(hash_map):
    """
    Serializes a nested map-like structure into a Python dictionary by recursively
    converting nested maps and arrays to equivalent Python data structures. The
    function processes each key-value pair, checking if the value is another map,
    an iterable, or a primitive type, and converts it accordingly.

    :param hash_map: The input map-like structure to be serialized. It is expected
        that this parameter supports iteration over its items and has attributes
        indicating if its value is a map (via "put" attribute) or an array/list
        (via "iterator" attribute).
    :type hash_map: Any compatible map-like object

    :return: A dictionary representation of the input map-like structure.
    :rtype: dict
    """
    map_to_dict_data = {}

    for key, value in zip(hash_map, hash_map.values()):
        if hasattr(value, "put"):
            map_to_dict_data[key] = serialize_map_to_dict(value)
        elif hasattr(value, "iterator"):
            map_to_dict_data[key] = serialize_array_to_list(value)
        else:
            map_to_dict_data[key] = value
    return map_to_dict_data


def serialize_array_to_list(array):
    """
    Converts an array structure to a serialized list structure by processing its
    elements. Elements are recursively serialized if they are arrays or maps
    that can be further processed. For non-iterable, non-mappable elements, it
    adds them directly to the serialized list.

    :param array: Input array containing various serializable or non-serializable
        elements. Each element might be iterable or might represent mappings.
        It may be nested and will be traversed recursively.
    :type array: Any iterable supporting nested objects like arrays or maps.
    :return: Serialized list containing processed elements from the input array.
        Iterables are recursively converted into lists, mappings into
        dictionaries, and all other elements are added directly.
    :rtype: list
    """
    array_to_list_data = []

    for value in array:
        if hasattr(value, "iterator"):
            data = serialize_array_to_list(value)
            array_to_list_data.append(data)
        elif hasattr(value, "put"):
            data = serialize_map_to_dict(value)
            array_to_list_data.append(data)
        else:
            array_to_list_data.append(value)
    return array_to_list_data


def serialize_dict_to_map(dictionary):
    """
    Transforms a Python dictionary into a Java `HashMap`, converting nested structures
    recursively where necessary. This function supports handling nested dictionaries, lists,
    boolean values, and other standard types, ensuring compatibility with Java data structures.

    :param dictionary: A Python dictionary to be serialized into a Java `HashMap`. Keys must be strings,
        and values can be of types: dict, list, bool, or other serializable Java-compatible types.
    :type dictionary: dict
    :return: A Java `HashMap` object representing the serialized structure of the input Python dictionary.
    :rtype: java.util.HashMap
    """
    dict_to_map_data = autoclass("java.util.HashMap")()

    for key, value in dictionary.items():
        if isinstance(value, dict):
            data = serialize_dict_to_map(value)
            dict_to_map_data.put(key, data)
        elif isinstance(value, list):
            data = serialize_list_to_array(value)
            dict_to_map_data.put(key, data)
        elif isinstance(value, bool):
            Boolean = autoclass("java.lang.Boolean")
            dict_to_map_data.put(key, Boolean(value))
        else:
            dict_to_map_data.put(key, value)
    return dict_to_map_data


def serialize_list_to_array(list_):
    """
    Converts a Python list to a Java ArrayList and handles nested structures
    and data type conversions. Elements in the input list are recursively
    converted into Java-compatible types depending on their original types,
    ensuring Java utilities and operations can effectively manage the data.

    :param list_: The input list containing elements of various types,
                  including integers, floats, booleans, strings, nested lists,
                  and dictionaries.
    :type list_: list
    :returns: A Java ArrayList containing the converted elements suitable
              for Java interoperability.
    :rtype: java.util.ArrayList
    """
    list_to_array_data = autoclass("java.util.ArrayList")()

    for value in list_:
        if isinstance(value, list):
            data = serialize_list_to_array(value)
            list_to_array_data.add(data)
        elif isinstance(value, dict):
            data = serialize_dict_to_map(value)
            list_to_array_data.add(data)
        elif isinstance(value, bool):
            Boolean = autoclass("java.lang.Boolean")
            list_to_array_data.add(Boolean(value))
        elif isinstance(value, int):
            Long = autoclass("java.lang.Long")
            list_to_array_data.add(Long(value))
        elif isinstance(value, float):
            Double = autoclass("java.lang.Double")
            list_to_array_data.add(Double(value))
        elif isinstance(value, str):
            String = autoclass("java.lang.String")
            list_to_array_data.add(String(value))
        else:
            list_to_array_data.add(value)
    return list_to_array_data


def serialize(data, raw_python=False):
    """
    Serializes Python data structures into formats compatible with specific Java objects
    or back. Handles lists, dictionaries, iterables with Java-compatible attributes,
    and raw serialization for supported types.

    :param data: The input data to serialize. Accepts various types including
        lists, dictionaries, iterables, and objects with specific attributes such
        as `iterator` and `put`.
    :type data: Any
    :param raw_python: A boolean flag indicating whether to perform raw Python
        serialization. Supported only for lists and their compatible elements.
    :type raw_python: bool
    :return: The serialized Java-compatible representation of the input data,
        or the original data when no serialization is applicable.
    :rtype: Any

    :raises Exception: If `raw_python` is set to True and the input data is not
        a list, or if a data type within the list is not supported.
    """
    if raw_python:
        if not isinstance(data, list):
            raise Exception(f"raw `{type(data)}` serialization not supported")
        raw_data = []
        for value in data:
            if isinstance(value, list):
                data = serialize_list_to_array(value)
                raw_data.append(data)
            elif isinstance(value, dict):
                data = serialize_dict_to_map(value)
                raw_data.append(data)
            elif isinstance(value, bool):
                Boolean = autoclass("java.lang.Boolean")
                raw_data.append(Boolean(value))
            elif isinstance(value, int):
                Long = autoclass("java.lang.Long")
                raw_data.append(Long(value))
            elif isinstance(value, float):
                Double = autoclass("java.lang.Double")
                raw_data.append(Double(value))
            elif isinstance(value, str):
                String = autoclass("java.lang.String")
                raw_data.append(String(value))
            else:
                raw_data.append(value)
        return raw_data
    if isinstance(data, dict):
        return serialize_dict_to_map(data)
    if isinstance(data, list):
        return serialize_list_to_array(data)
    if hasattr(data, "iterator"):
        return serialize_array_to_list(data)
    if hasattr(data, "put"):
        return serialize_map_to_dict(data)
    return data


if __name__ == "__main__":
    # Serialize Java map to Python dictionary
    hm = autoclass("java.util.HashMap")()
    hm.put("ada", "kene")
    hm.put("kene", "ada")

    bm = autoclass("java.util.HashMap")()
    bm.put("ken", 1)
    bm.put(2, 3)

    cm = autoclass("java.util.HashMap")()

    ar = autoclass("java.util.ArrayList")()
    ar.add(1)
    ar.add(2)
    ar.add(bm)
    # cm.put("hj", ar)
    #
    # bm.put("extras", cm)
    hm.put("extra", ar)
    print(serialize_map_to_dict(hm))

    # Serialize Java array to Python list
    al = autoclass("java.util.ArrayList")()
    al.add(1)
    al.add("ada")

    dm = autoclass("java.util.HashMap")()
    dm.put("ada", "kene")

    al.add(dm)
    print(serialize_array_to_list(al))

    # Serialize Python dictionary to Java map
    dt = {"ada": "kene", 1: [{"1": "ada"}]}
    print(serialize_dict_to_map(dt).get(1).get(0).get("1"))

    # Serialize Python list to Java Array
    lt = [1, 2, 3, {"ada": "kene"}]
    print(serialize_list_to_array(lt))
