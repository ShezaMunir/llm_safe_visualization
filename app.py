from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('data/dataset.csv')


@app.route('/')
@app.route('/<int:entry_index>')
def view_entry(entry_index=0):
    if entry_index < 0:
        entry_index = 0
    if entry_index >= len(df):
        entry_index = len(df) - 1
    entry = df.iloc[entry_index]
    cluster_name = entry['name_of_cluster']
    prompt = entry['representative_prompt']
    answer = entry['representative_answer']
    safe_dict = json.loads(entry['safe_dict'])
    table_data = [[d['split'], d['revise'], d['relevance'],
                   d['rate_google_search']] for d in safe_dict]
    dataset_length = len(df)
    output_dict = json.loads(entry['output_dict'])
    return render_template('index.html', entry_index=entry_index, cluster_name=cluster_name,
                           prompt=prompt, answer=answer, table_data=table_data, output_dict=output_dict, dataset_length=dataset_length)


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
