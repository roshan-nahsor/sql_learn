import toml
output_file = ".streamlit/secrets.toml"
with open("sql-learn-fa3e6-0f8947c48904.json") as json_file:
    json_text = json_file.read()
config = {"textkey": json_text}
toml_config = toml.dumps(config)
with open(output_file, "w") as target:
    target.write(toml_config)