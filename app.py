from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)
api_address = "https://orcfax.apexpool.info/api/v0/"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stake_key = request.form['stake_address']

        # connect to API for stake address data
        api_url = api_address + "/get_rewards/" + stake_key
        response = requests.get(api_url)
        report = json.loads(response.text)

        # check for error message
        for key in report:
            if key == 'error':
                error_message = report['error']
                return render_template('error.html', stake_address=stake_key, error_message=error_message)

        # format results for UI template
        rewards_dict = {}
        for item in report['rewards']:
            active_stake = int(item['active_stake'])
            epoch = int(item['epoch'])
            rewards = float(item['rewards'])
            rewards_dict[epoch] = [active_stake, rewards]

        return render_template('rewards.html', stake_address=report['stake_address'], total_rewards=report['total_rewards'], rewards=rewards_dict)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)