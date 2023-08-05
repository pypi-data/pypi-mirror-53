import re


def load(filename):
    queries = {}

    with open(filename) as f:
        lines = f.readlines()

        current_query = None

        for line in lines:
            name = re.match(r"--\s?(.*)\n", line)

            if name:
                current_query = name.group(1)
            else:
                queries[current_query] = queries.get(current_query,'') + line.strip(" \t").replace("\n", " ")

    for key, value in queries.items():
        queries[key] = value.strip()

    return queries