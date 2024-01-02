import pandas as pd
import joblib
import boto3
import io

# Define your sample_data here
sample_data = {
    'HouseStyle': '1Story',
    'LotArea': 9937,
    'YearBuilt': 1965,
    'GrLivArea': 1256,
    'OverallQual': 5,
    'OverallCond': 6,
    'Fireplaces': 0,
    'GarageCars': 1,
    'FullBath': 1,
    'sin_MoSold': 0.0,
    'cos_MoSold': -1.0,
    'CentralAir': 1.0
}

def load_model_from_s3(bucket_name, key):
    # Create a S3 client
    s3 = boto3.client('s3')

    # Load model file from S3
    response = s3.get_object(Bucket=bucket_name, Key=key)
    model_content = response['Body'].read()

    # Load the model from the content
    model = joblib.load(io.BytesIO(model_content))
    return model


def lambda_handler(event, context):
    if 'HouseStyle' in event:
        # User has provided input, use the provided data
        user_input_df = pd.DataFrame(event, index=[0])
    else:
        # Use predefined sample_data if no additional input is provided
        user_input_df = pd.DataFrame(sample_data, index=[0])

    # Load the model from S3
    model_bucket_name = 'your-s3-bucket-name'  # Replace with your S3 bucket name
    model_key = 'aws_houses_df/model.pkl'  # Replace with your model's S3 key
    model = load_model_from_s3(model_bucket_name, model_key)

    # Make predictions
    predicted_prices = model.predict(user_input_df)
    print(predicted_prices)

    # Optionally, return the predicted value (for API Gateway or other uses)
    return {
        'predicted_price': predicted_prices[0]  # Return the first predicted price if it's an array
    }
