def basic_formatter(routes):
    output = []
    output.append("\n==============  Routes  ==============")

    for (rule, methods) in routes:
        output.extend([format_route(method, rule) for method in methods])

    output.append("======================================\n")
    output.append("\n")
    return "\n".join(output)


def format_route(method, rule):
    return method.ljust(10) + str(rule)
