from flask import Flask, render_template, request
import pandas as pd
import json
import os

app = Flask(__name__)
file_name = ''

# Load the JSON files
data_folder = 'clusters_data'
json_files = [f for f in os.listdir(data_folder) if f.endswith('.json')]
data = []
for file in json_files:
    with open(os.path.join(data_folder, file), 'r') as f:
        # file_name = file
        data.append(json.load(f))


@app.route('/')
@app.route('/<int:entry_index>')
def view_entry(entry_index=0):
    if entry_index < 0:
        entry_index = 0
    if entry_index >= len(data):
        entry_index = len(data) - 1
    entry = data[entry_index]

    prompt = entry['prompt']
    response = entry['response']
    checked_statements = entry['checked_statements']
    supported = entry['Supported']
    not_supported = entry['Not Supported']
    irrelevant = entry['Irrelevant']
    dataset_length = len(data)
    file_name = entry_index

    return render_template('index.html', entry_index=entry_index, prompt=prompt,
                           response=response, checked_statements=checked_statements,
                           supported=supported, not_supported=not_supported,
                           irrelevant=irrelevant, dataset_length=dataset_length, file_name=file_name)


@app.route('/navigate', methods=['POST'])
def navigate():
    action = request.form['action']
    entry_index = int(request.form['entry_index'])
    if action == 'forward':
        entry_index += 1
    elif action == 'backward':
        entry_index -= 1
    elif action == 'go':
        entry_index = int(request.form['entry_index_input'])
    return view_entry(entry_index)


if __name__ == '__main__':
    app.run(debug=True)
