from flask import Flask, render_template, request

app = Flask(__name__)

# Constants from your spreadsheet
PRESCRIPTIVE_RATE = 200        # $ per HP
KW_PER_HP = 0.7                # kW per HP
ELECTRICITY_RATE = 0.14        # $ per kWh

@app.route('/', methods=['GET', 'POST'])
def index():
    prescriptive_incentive = None
    custom_incentive = None
    energy_use = None

    if request.method == 'POST':
        # Gather inputs
        total_hp = float(request.form.get('total_hp', 0))
        percent_loaded = float(request.form.get('percent_loaded', 0))
        annual_hours = float(request.form.get('annual_hours', 0))

        # Calculations
        prescriptive_incentive = total_hp * PRESCRIPTIVE_RATE
        energy_use = total_hp * KW_PER_HP * percent_loaded * annual_hours
        custom_incentive = energy_use * ELECTRICITY_RATE

    return render_template(
        'index.html',
        prescriptive=prescriptive_incentive,
        energy_use=energy_use,
        custom=custom_incentive
    )

if __name__ == '__main__':
    app.run(debug=True)
"Add Flask app"
