import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained model
try:
    with open('random.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# HTML Template with Embedded Modern CSS Styling
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Prediction Portal</title>
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
            --text-color: #1f2937;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background: var(--card-bg);
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            width: 100%;
            max-width: 600px;
        }
        h2 {
            margin-bottom: 20px;
            color: var(--primary);
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            font-size: 14px;
        }
        input, select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            box-sizing: border-box;
            transition: border-color 0.2s;
        }
        input:focus, select:focus {
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        button {
            width: 100%;
            background-color: var(--primary);
            color: white;
            padding: 12px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
            transition: background-color 0.2s;
        }
        button:hover {
            background-color: var(--primary-hover);
        }
        .result-card {
            margin-top: 25px;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            background-color: #e0e7ff;
            color: #3730a3;
        }
        .error {
            background-color: #fee2e2;
            color: #991b1b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Customer Prediction System</h2>
        <form method="POST" action="/">
            
            <div class="form-group">
                <label for="age">Age</label>
                <input type="number" id="age" name="age" required min="1" max="120" value="{{ request.form.get('age', '') }}">
            </div>

            <div class="form-group">
                <label for="gender">Gender</label>
                <select id="gender" name="gender" required>
                    <option value="" disabled {% if not request.form.get('gender') %}selected{% endif %}>Select Gender</option>
                    <option value="Male" {% if request.form.get('gender') == 'Male' %}selected{% endif %}>Male</option>
                    <option value="Female" {% if request.form.get('gender') == 'Female' %}selected{% endif %}>Female</option>
                    <option value="Other" {% if request.form.get('gender') == 'Other' %}selected{% endif %}>Other</option>
                </select>
            </div>

            <div class="form-group">
                <label for="marital_status">Marital Status</label>
                <select id="marital_status" name="marital_status" required>
                    <option value="" disabled {% if not request.form.get('marital_status') %}selected{% endif %}>Select Marital Status</option>
                    <option value="Single" {% if request.form.get('marital_status') == 'Single' %}selected{% endif %}>Single</option>
                    <option value="Married" {% if request.form.get('marital_status') == 'Married' %}selected{% endif %}>Married</option>
                    <option value="Divorced" {% if request.form.get('marital_status') == 'Divorced' %}selected{% endif %}>Divorced</option>
                </select>
            </div>

            <div class="form-group">
                <label for="occupation">Occupation</label>
                <select id="occupation" name="occupation" required>
                    <option value="" disabled {% if not request.form.get('occupation') %}selected{% endif %}>Select Occupation</option>
                    <option value="Salaried" {% if request.form.get('occupation') == 'Salaried' %}selected{% endif %}>Salaried</option>
                    <option value="Self-Employed" {% if request.form.get('occupation') == 'Self-Employed' %}selected{% endif %}>Self-Employed</option>
                    <option value="Business" {% if request.form.get('occupation') == 'Business' %}selected{% endif %}>Business</option>
                    <option value="Student" {% if request.form.get('occupation') == 'Student' %}selected{% endif %}>Student</option>
                    <option value="Other" {% if request.form.get('occupation') == 'Other' %}selected{% endif %}>Other</option>
                </select>
            </div>

            <div class="form-group">
                <label for="monthly_income">Monthly Income</label>
                <input type="number" id="monthly_income" name="monthly_income" required min="0" step="any" value="{{ request.form.get('monthly_income', '') }}">
            </div>

            <div class="form-group">
                <label for="educational_qualifications">Educational Qualifications</label>
                <select id="educational_qualifications" name="educational_qualifications" required>
                    <option value="" disabled {% if not request.form.get('educational_qualifications') %}selected{% endif %}>Select Qualification</option>
                    <option value="High School" {% if request.form.get('educational_qualifications') == 'High School' %}selected{% endif %}>High School</option>
                    <option value="Graduate" {% if request.form.get('educational_qualifications') == 'Graduate' %}selected{% endif %}>Graduate</option>
                    <option value="Post Graduate" {% if request.form.get('educational_qualifications') == 'Post Graduate' %}selected{% endif %}>Post Graduate</option>
                    <option value="Doctorate" {% if request.form.get('educational_qualifications') == 'Doctorate' %}selected{% endif %}>Doctorate</option>
                </select>
            </div>

            <div class="form-group">
                <label for="family_size">Family Size</label>
                <input type="number" id="family_size" name="family_size" required min="1" max="20" value="{{ request.form.get('family_size', '') }}">
            </div>

            <div class="form-group">
                <label for="customer_type">Customer Type</label>
                <select id="customer_type" name="customer_type" required>
                    <option value="" disabled {% if not request.form.get('customer_type') %}selected{% endif %}>Select Customer Type</option>
                    <option value="Regular" {% if request.form.get('customer_type') == 'Regular' %}selected{% endif %}>Regular</option>
                    <option value="Premium" {% if request.form.get('customer_type') == 'Premium' %}selected{% endif %}>Premium</option>
                    <option value="New" {% if request.form.get('customer_type') == 'New' %}selected{% endif %}>New</option>
                </select>
            </div>

            <button type="submit">Predict</button>
        </form>

        {% if prediction %}
            <div class="result-card">
                Prediction Result: {{ prediction }}
            </div>
        {% endif %}
        
        {% if error %}
            <div class="result-card error">
                {{ error }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    error = None

    if request.method == 'POST':
        if model is None:
            error = "Model could not be loaded on the server."
            return render_template_string(HTML_PAGE, error=error)

        try:
            # Extract features matching the model's expected input feature order:
            # ['Age', 'Gender', 'Marital Status', 'Occupation', 'Monthly Income', 'Educational Qualifications', 'Family size', 'Customer Type']
            age = float(request.form['age'])
            gender = request.form['gender']
            marital_status = request.form['marital_status']
            occupation = request.form['occupation']
            monthly_income = float(request.form['monthly_income'])
            educational_qualifications = request.form['educational_qualifications']
            family_size = float(request.form['family_size'])
            customer_type = request.form['customer_type']

            # Note: If your training pipeline used a preprocessor/Encoder (like OneHotEncoder/OrdinalEncoder) 
            # embedded inside the pickle object, pass raw values. If it expects numerical encoding, 
            # you will need to map strings to the exact indices your training script used.
            # Below is structured for standard pipelines or direct inference arrays.
            
            # Example feature array construction (adjust if your pipeline includes a preprocessor):
            features = np.array([[
                age, 
                gender, 
                marital_status, 
                occupation, 
                monthly_income, 
                educational_qualifications, 
                family_size, 
                customer_type
            ],], dtype=object)

            # Perform prediction
            pred_result = model.predict(features)[0]
            
            # Map output if target classes are ['No', 'Yes']
            prediction = str(pred_result)

        except Exception as e:
            error = f"An error occurred during prediction: {str(e)}"

    return render_template_string(HTML_PAGE, prediction=prediction, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
