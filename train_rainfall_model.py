import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib
os.makedirs("models", exist_ok=True)

# ----------- CONFIG -----------
DATA_FOLDER = "data/weather"
TARGET_COL = "precipitation_sum"
LAG_DAYS = 2

# ----------- LOAD & MERGE DATA -----------
def load_weather_data(folder):
    dfs = []
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            city_name = filename.replace(".csv", "")
            df = pd.read_csv(os.path.join(folder, filename))
            df["city"] = city_name
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# ----------- ADD LAG FEATURES -----------
def add_lag_features(df, target_col, lag_days):
    df = df.sort_values(by=["city", "time"]).reset_index(drop=True)
    for lag in range(1, lag_days + 1):
        df[f"{target_col}_lag{lag}"] = df.groupby("city")[target_col].shift(lag)
    return df

# ----------- PREPROCESS -----------
def preprocess(df):
    df["time"] = pd.to_datetime(df["time"])
    df = add_lag_features(df, TARGET_COL, LAG_DAYS)
    df = df.dropna().reset_index(drop=True)  # Drop rows with NaN from lag

    X = df[[
        "temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
        "wind_speed_10m_max", "wind_gusts_10m_max",
        "sunshine_duration", "daylight_duration",
    ] + [f"{TARGET_COL}_lag{i}" for i in range(1, LAG_DAYS+1)]]

    y = df[TARGET_COL]
    return train_test_split(X, y, test_size=0.2, random_state=42)

# ----------- MAIN TRAINING -----------
if __name__ == "__main__":
    print("Loading data...")
    df = load_weather_data(DATA_FOLDER)

    print("Preprocessing data...")
    X_train, X_test, y_train, y_test = preprocess(df)

    print("Running grid search for XGBoost...")
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5],
        'learning_rate': [0.05, 0.1],
    }

    xgb = XGBRegressor(random_state=42, verbosity=0)
    grid = GridSearchCV(xgb, param_grid, cv=3, scoring='r2', n_jobs=-1)
    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_
    print("Best Params:", grid.best_params_)

    y_pred = best_model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("Model trained with XGBoost.")
    print(f"R² Score: {r2:.4f}")
    print(f"RMSE: {rmse:.4f}")

    # Optional: Save model
   
    joblib.dump(best_model, "models/xgboost_rainfall_model.pkl")
    print("Model saved to models/xgboost_rainfall_model.pkl")
