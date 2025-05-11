from flask import Flask, render_template, request

app = Flask(__name__)

# Constants
PRESCRIPTIVE_RATE = 200       # $ per HP
KW_PER_HP = 0.7               # kW per HP
ELECTRICITY_RATE = 0.14       # $ per kWh
PRESCRIPTIVE_HP_CAP = 300     # HP cap for prescriptive incentive

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize results and form defaults
    prescriptive_incentive = None
    energy_use = None
    custom_incentive = None
    total_hp_input = ''
    percent_loaded_input = ''
    annual_hours_input = ''

    if request.method == 'POST':
        # Retrieve raw inputs
        total_hp_input = request.form.get('total_hp', '')
        percent_loaded_input = request.form.get('percent_loaded', '')
        annual_hours_input = request.form.get('annual_hours', '')

        # Parse inputs safely
        try:
            total_hp = float(total_hp_input)
        except (ValueError, TypeError):
            total_hp = 0.0
        try:
            percent_loaded_fraction = float(percent_loaded_input) / 100.0
        except (ValueError, TypeError):
            percent_loaded_fraction = 0.0
        try:
            annual_hours = float(annual_hours_input)
        except (ValueError, TypeError):
            annual_hours = 0.0

        # Prescriptive incentive calculation with cap
        capped_hp = min(total_hp, PRESCRIPTIVE_HP_CAP)
        prescriptive_incentive = capped_hp * PRESCRIPTIVE_RATE

        # Baseline energy use in kWh/year
        baseline_kw = total_hp * KW_PER_HP
        energy_use = baseline_kw * annual_hours

        # New energy use at loaded capacity
        new_kw = baseline_kw * percent_loaded_fraction
        new_energy_use = new_kw * annual_hours

        # Energy savings
        energy_savings = energy_use - new_energy_use

        # Custom incentive based on energy savings
        custom_incentive = energy_savings * ELECTRICITY_RATE

    # Render template with results and raw input values
    return render_template(
        'index.html',
        prescriptive=prescriptive_incentive,
        energy_use=energy_use,
        custom=custom_incentive,
        total_hp=total_hp_input,
        percent_loaded=percent_loaded_input,
        annual_hours=annual_hours_input
    )

if __name__ == '__main__':
    app.run(debug=True)
