def convert_constant(node, params, layers, node_name, keras_name):
    """
    Convert Constant layer
    :param node: current operation node
    :param params: operation attributes
    :param layers: available keras layers
    :param node_name: internal converter name
    :param keras_name: resulting layer name
    :return: None
    """
    if node_name['change_ordering']:
        print(params['value'].shape)
        exit(0)
        if len(params['value'].shape) == 4:
            pass
    else:
        layers[node_name] = params['value']
