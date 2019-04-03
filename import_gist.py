import urllib.request
import json


def import_gist(gist_id, file_names=None):
    """Execute gist python file.

    Keyword arguments:
    gist_id     -- Gist id
    file_names  -- File names of gist to execute (default: None)

    If the file_names is None, executes every python files in the gist.
    """

    response = urllib.request.urlopen("https://api.github.com/gists/{}".format(gist_id))
    if str(response.status).startswith("2"):
        body = response.read()
        body = body.decode(encoding="utf-8")
        body = json.loads(body)
        files = body["files"]

        if file_names is None:
            file_names = files.keys()

        for file_name in file_names or files.keys():
            if file_name not in files:
                raise ModuleNotFoundError("{}/{}".format(gist_id, file_name))

            code = files[file_name]["content"]
            ast = compile(code, file_name, "exec")
            exec(ast, globals())
    else:
        raise ImportError(response.status, response.msg)
