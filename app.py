from flask import Flask, render_template, request
import requests
import json
import math

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

        print(report)

        # check for error message
        for key in report:
            if key == 'error':
                error_message = report['error']
                return render_template('error.html', 
                                       stake_address=stake_key, error_message=error_message)

        # format results for UI template
        rewards_dict = {}
        cumulative_epoch_rewards = 0
        for item in report['rewards']:
            active_stake = item['active_stake']
            epoch = int(item['epoch'])
            epoch_rewards = item['base_rewards']
            epoch_bonus = item['bonus']
            epoch_total = item['adjusted_rewards']
            epoch_total = epoch_total.replace(',','')            
            cumulative_epoch_rewards += float(epoch_total)
            truncated_epoch_rewards = truncate(cumulative_epoch_rewards, 4)
            rewards_dict[epoch] = [active_stake, 
                                   epoch_rewards, epoch_bonus, truncated_epoch_rewards]
            
        return render_template('rewards.html',
                               latest_epoch = report['latest_epoch'],
                               total_ispo_stake = report['live_stake'],
                               total_ispo_rewards = report['ispo_total_adjusted_rewards'],
                               total_ispo_rewards_percent = report['total_ispo_rewards_percent'],
                               total_ispo_bonus = report['ispo_total_bonus'],
                               stake_address=report['stake_address'], total_rewards=report['total_adjusted_rewards'],
                               rewards_share = report['rewards_percentage_from_total'],rewards=rewards_dict)


    return render_template('index.html')


def truncate(number, digits) -> float:
    # trim decimal points
    nbDecimals = len(str(number).split('.')[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')