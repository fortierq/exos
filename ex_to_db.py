from pathlib import Path

import yaml

dir_ex = Path(__file__).parents.resolve() / "exos"
file_output = Path("cpge-exos-app/db/exos.sql")

attributes = { s: set() for s in ["subject", "ds", "language", "algorithm", "classe"] }

with file_output.open("w") as f:
    f.write(f"CREATE TABLE IF NOT EXISTS exercise (\n"
        "\tname VARCHAR(255) NOT NULL,\n"
        "\tpath VARCHAR(255) NOT NULL PRIMARY KEY);\n")
    for k in attributes:
        f.write(f"CREATE TABLE IF NOT EXISTS {k} (\n"
            "\tname VARCHAR(255) NOT NULL PRIMARY KEY);\n")
        f.write(f"CREATE TABLE IF NOT EXISTS exercise_{k} (\n"
            "\tid SERIAL PRIMARY KEY,\n"
            "\texercise_path VARCHAR(255) NOT NULL REFERENCES exercise,\n"
            f"\t{k}_name VARCHAR(255) NOT NULL REFERENCES {k});\n")

    for file_yaml in dir_ex.rglob("*.yml"):
        with file_yaml.open("r") as f_yaml:
            path = file_yaml.parent.relative_to(dir_ex)
            try:
                d = yaml.load(f_yaml, Loader=yaml.FullLoader)
                name = d["name"]
                f.write(f"INSERT INTO exercise(name, path) VALUES ('{name}', '{path}');\n")
                for k in attributes:
                    if k in d:
                        for v in d[k]: 
                            if v not in attributes[k]:
                                attributes[k].add(v)
                                f.write(f"INSERT INTO {k} (name) VALUES ('{v}');\n")
                            f.write(f"INSERT INTO exercise_{k} (exercise_path, {k}_name) VALUES ('{path}', '{v}');\n")
                print(f"OK: {file_yaml}")
            except Exception as e:
                print(f"ERROR: {file_yaml} {e}")
