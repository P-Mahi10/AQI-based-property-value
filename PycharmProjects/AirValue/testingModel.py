# Load size mapping CSV (generated during training)
size_mapping = pd.read_csv('size_mapping.csv').set_index('size')['encoded'].to_dict()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # ✅ Location encoding
        location_name = data.get('location')
        location_encoded = location_price.get(location_name, np.mean(list(location_price.values())))

        # ✅ Size encoding
        size_str = data.get('size')  # Example: '2 BHK'
        size_encoded = size_mapping.get(size_str, np.mean(list(size_mapping.values())))  # Default to mean if not found

        # ✅ Other features
        total_sqft = data.get('total_sqft', 0)
        bath = data.get('bath', 0)
        balcony = data.get('balcony', 0)
        price_per_sqft = data.get('price_per_sqft', 0)

        # ✅ Prepare input
        input_data = np.array([[total_sqft, bath, balcony, location_encoded, size_encoded, price_per_sqft]])

        # ✅ Predict and convert back from log scale
        log_price = model.predict(input_data)
        predicted_price = np.expm1(log_price)[0]

        return jsonify({
            'predicted_price_lakhs': round(predicted_price, 2)
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'trace': traceback.format_exc()
        })
