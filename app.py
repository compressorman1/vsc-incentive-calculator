from flask import Flask, render_template, request

app = Flask(__name__)

# Constants
PRESCRIPTIVE_RATE = 200       # $ per HP
KW_PER_HP = 0.7               # kW per HP
ELECTRICITY_RATE = 0.14       # $ per kWh
PRESCRIPTIVE_HP_CAP = 300     # HP cap for prescriptive incentive

@app.route('/', methods=['GET', 'POST'])
def index():
    prescriptive_incentive = None
    energy_use = None
    custom_incentive = None

    if request.method == 'POST':
        total_hp = float(request.form.get('total_hp', 0))
        percent_loaded = float(request.form.get('percent_loaded', 0))
        annual_hours = float(request.form.get('annual_hours', 0))

        # Prescriptive incentive capped at PRESCRIPTIVE_HP_CAP
        capped_hp = min(total_hp, PRESCRIPTIVE_HP_CAP)
        prescriptive_incentive = capped_hp * PRESCRIPTIVE_RATE

        # Baseline energy use (kWh)
        baseline_kw = total_hp * KW_PER_HP
        energy_use = baseline_kw * annual_hours  # annual energy consumption

        # Custom incentive based on energy savings from variable speed
        reduced_kw = baseline_kw * percent_loaded
        reduced_energy_use = reduced_kw * annual_hours
        energy_savings = energy_use - reduced_energy_use
        custom_incentive = energy_savings * ELECTRICITY_RATE

    return render_template(
        'index.html',
        prescriptive=prescriptive_incentive,
        energy_use=energy_use,
        custom=custom_incentive
    )

if __name__ == '__main__':
    app.run(debug=True)
