from flask import Flask, render_template, request

app = Flask(__name__)

# Constants
PRESCRIPTIVE_RATE = 200       # $ per HP
KW_PER_HP = 0.7               # kW per HP
ELECTRICITY_RATE = 0.14       # $ per kWh
PRESCRIPTIVE_HP_CAP = 300     # HP cap for prescriptive incentive

@app.route('/', methods=['GET','POST'])
def index():
    # initialize
    prescriptive_incentive = energy_use = custom_incentive = None
    # default form values (so template always sees something)
    form_vals = {
      'total_hp': '',
      'percent_loaded': '',
      'annual_hours': ''
    }

    if request.method == 'POST':
        # pull raw strings first
        form_vals['total_hp']      = request.form.get('total_hp','')
        form_vals['percent_loaded']= request.form.get('percent_loaded','')
        form_vals['annual_hours']  = request.form.get('annual_hours','')

        total_hp       = float(form_vals['total_hp'])
        percent_loaded = float(form_vals['percent_loaded'])/100
        annual_hours   = float(form_vals['annual_hours'])

        # … your existing calculations here …

    return render_template(
      'index.html',
      prescriptive=prescriptive_incentive,
      energy_use=energy_use,
      custom=custom_incentive,
      **form_vals            # <-- pass the raw values through
    )


if __name__ == '__main__':
    app.run(debug=True)
