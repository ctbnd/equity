from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {
        'names': ['Mark', 'Mat', 'Ollie', 'Dave', 'Seva'],
        'weights': [0.5, 0.3, 0.2],
        'scores': [[10, 10, 10], [1, 1, 3], [0, 5, 0], [10, 10, 0], [5, 1, 0]],
        'equities': [0, 0, 0, 0, 0]
    }

    if request.method == 'POST':
        for i, name in enumerate(data['names']):
            for j in range(3):
                data['scores'][i][j] = int(request.form[f'score-{name}-{j}'])

        for i, weight in enumerate(data['weights']):
            data['weights'][i] = float(request.form[f'weight-{i}'])

        total_score = sum(sum(score * weight for score, weight in zip(scores_row, data['weights'])) for scores_row in data['scores'])

        # Check for zero total score
        if total_score == 0:
            return "Total score is zero. Please provide valid inputs.", 400

        for i, scores_row in enumerate(data['scores']):
            data['equities'][i] = round(sum(score * weight for score, weight in zip(scores_row, data['weights'])) / total_score * 100, 2)

    zipped_data = zip(data['names'], data['scores'], data['equities'])
    return render_template('index.html', zipped_data=zipped_data, names=data['names'], equities=data['equities'], weights=data['weights'], enumerate=enumerate)

if __name__ == '__main__':
    app.run(debug=True)
