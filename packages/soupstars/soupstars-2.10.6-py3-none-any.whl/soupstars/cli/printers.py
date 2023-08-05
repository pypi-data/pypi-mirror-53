import json
from pygments import highlight, lexers, formatters

pygments_style = "native"


def jsonify(data):
    formatted_json = json.dumps(data, sort_keys=True, indent=2)
    colorful_json = highlight(
        formatted_json,
        lexers.JsonLexer(),
        formatters.Terminal256Formatter(style=pygments_style)
    )
    print(colorful_json)


def pythonify(module):
    result = highlight(
        module,
        lexers.PythonLexer(),
        formatters.Terminal256Formatter(style=pygments_style)
    )
    print(result)
