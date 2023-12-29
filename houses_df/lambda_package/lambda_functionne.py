import pandas as pd
import joblib


if __name__ == "__main__":
   user_input = pd.DataFrame(sample_data).transpose().reset_index(drop=True)
   model = joblib.load('aws_houses_df/model.pkl')
   predicted_prices = model.predict(user_input)[0]
   print(predicted_prices)
