import numpy as np
import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler, RobustScaler

from sklearn.linear_model import LinearRegression


from sklearn.metrics import mean_squared_error

#----------------------------------Expl

columns_to_absolutely_ignore = ['Street', 'PoolQC', 'FireplaceQu']
columns_to_probably_ignore = ['Fence', 'LotFrontage']
columns_to_ignore = list(dict.fromkeys(columns_to_absolutely_ignore + columns_to_probably_ignore))

original_df = pd.read_csv('data/train (1).csv')
df = pd.read_csv('data/train (1).csv').drop(columns=columns_to_ignore)
df.drop_duplicates(inplace = True)

#----------------------------------Feat

# filtering one big time outlier for consistency.
df = df[df['GrLivArea']<5000].reset_index(drop=True)

# w/o o w Shed is the only relevant data to extract from MiscFeature
df['MiscFeature'] = df['MiscFeature'].apply(lambda x: 0 if x != 'Shed' else 1)


#----------------------------------Model

# All Columns to preprocess
to_classify = ['HouseStyle']
to_robust = ['LotArea', 'YearBuilt', 'GrLivArea']
to_min_max = ['OverallQual', 'OverallCond', 'Fireplaces', 'GarageCars', 'FullBath']
already_fine = []
# Bench : 'MiscFeature'
select_features = to_classify + to_robust + to_min_max + already_fine


X = df[select_features]
y = df['SalePrice']  # Target

r2list = []
rmse_list = []

for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, \
        random_state=np.random.randint(1, 20001) )


    # Building Pipeline
    preprocessor = ColumnTransformer([
        ('onehot', OneHotEncoder(), to_classify),
        ('std_scaler', RobustScaler(), to_robust), # RobustScaler/StandardScaler
        ('minmax', MinMaxScaler(), to_min_max),
    ], remainder='passthrough')  # passthrough/drop

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())  # Linear Regression model
    ])
    pipeline.fit(X_train, y_train)

    # R^2 Score, not RMSE
    # train_score = pipeline.score(X_train, y_train)
    # test_score = pipeline.score(X_test, y_test)
    r2list.append(pipeline.score(X_test, y_test))
    # print(f"Training_Score: {train_score:.5f}")

    predicted_prices = pipeline.predict(X_test)
    rmse_list.append(np.sqrt(mean_squared_error(y_test, predicted_prices)))

print(f"# Used features count : {len(select_features)}") #/len(df.columns)
print(f"# Mean Test_Score: {np.mean(r2list):.5f}")
# Display RMSE
print(f"# Average prediction error: ~{np.mean(rmse_list):.4f} (RMSE)")
