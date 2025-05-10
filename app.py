from flask import Flask, render_template, request

app = Flask(__name__)

# Constants
PRESCRIPTIVE_RATE = 200       # $ per HP
KW_PER_HP = 0.7               # kW per HP
CUSTOM_INCENTIVE_RATE = 1200  # $ per kW of reduced capacity
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

        # Annual energy use (kWh)
        baseline_kw = total_hp * KW_PER_HP
        energy_use = baseline_kw * annual_hours

        # Custom incentive: reduction in kW capacity times incentive rate
        reduction_hp = total_hp * (1 - percent_loaded)
        reduction_kw = reduction_hp * KW_PER_HP
        custom_incentive = reduction_kw * CUSTOM_INCENTIVE_RATE

    return render_template(
        'index.html',
        prescriptive=prescriptive_incentive,
        energy_use=energy_use,
        custom=custom_incentive
    )

if __name__ == '__main__':
    app.run(debug=True)
