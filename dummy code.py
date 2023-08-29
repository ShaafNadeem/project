from flask import Flask, render_template, request

app = Flask(__name__)

# Sample diagnosis data for demonstration
diagnosis_data = {
    "patient1": {
        "diagnosis1": "Common Cold",
        "diagnosis2": "Flu"
    },
    "patient2": {
        "diagnosis1": "Migraine",
        "diagnosis2": "Tension Headache"
    }
}

@app.route('/', methods=['GET', 'POST'])
def diagnosis_page():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        if patient_id in diagnosis_data:
            patient_diagnoses = diagnosis_data[patient_id]
            diagnosis1 = patient_diagnoses['diagnosis1']
            diagnosis2 = patient_diagnoses['diagnosis2']
            return render_template('index.html', patient_id=patient_id, diagnosis1=diagnosis1, diagnosis2=diagnosis2)
        else:
            return render_template('index.html', patient_id=patient_id, diagnosis1=None, diagnosis2=None)
    return render_template('index.html', patient_id=None, diagnosis1=None, diagnosis2=None)

if __name__ == '__main__':
    app.run(debug=True)
