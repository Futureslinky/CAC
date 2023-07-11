import json
from flask import Flask, render_template, request
from helpers.functions import get_image_by_zip, get_all_information

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        response = get_all_information(zipcode)
        data = json.loads(response)
        results = []
        for result in data['results']:
            division_id = result['current_role'].get('division_id', '')
            if division_id.startswith('ocd-division/country:us/state:') and '/cd:' in division_id:
                image_url, district = get_image_by_zip(zipcode)
                result['image'] = image_url
                result['current_role']['district'] = district
                results.append(result)
        return render_template('result.html', results=results)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
