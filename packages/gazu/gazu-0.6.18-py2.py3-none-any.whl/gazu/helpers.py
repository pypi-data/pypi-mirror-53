def normalize_model_parameter(model_parameter):
    """
    Args:
        model_parameter (str / dict): The parameter to convert.

    Returns:
        dict: If `model_parameter` is an ID (a string), it turns it into a model
        dict. If it's already a dict, the `model_parameter` is returned as it
        is. It returns None if the paramater is None.
    """
    if model_parameter is None:
        return None
    elif isinstance(model_parameter, str):
        return {"id": model_parameter}
    elif isinstance(model_parameter, dict):
        return model_parameter
    else:
        raise ValueError("Wrong format: expected ID string or Data dict")
