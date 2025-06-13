import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

df = pd.read_csv("basel_weather.csv")
df['datetime'] = pd.to_datetime(df['hourly__time'])
df = df.rename(columns={
    'hourly__temperature_2m': 'temp2m',
    'hourly__windspeed_10m': 'windspeed',
    'hourly__relative_humidity_2m': 'humidity'
})
df = df[['datetime', 'temp2m', 'windspeed', 'humidity']].dropna()

engine = create_engine("sqlite:///weather.db")
df.to_sql("weather_data", con=engine, if_exists="replace", index=False)

df['day_of_year'] = df['datetime'].dt.dayofyear
df['hour'] = df['datetime'].dt.hour

X = df[['day_of_year', 'hour', 'windspeed']]
y = df['temp2m']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
print(f"MAE: {mae:.2f} °C")

day_features = pd.DataFrame({
    'day_of_year': [75],
    'hour': [14],
    'windspeed': [5]
})
forecast = model.predict(day_features)[0]
print(f"Прогноз на 15 березня о 14:00 = {forecast:.2f} °C")

plt.figure(figsize=(10, 5))
plt.scatter(X_test['day_of_year'], y_test, alpha=0.3, label='Факт')
plt.scatter(X_test['day_of_year'], y_pred, alpha=0.3, label='Прогноз')
plt.axvline(75, color='red', linestyle='--', label='15 березня')
plt.scatter(75, forecast, color='black', s=100, label='Прогноз 15.03')
plt.xlabel("День року")
plt.ylabel("Температура (°C)")
plt.title("Передбачення температури")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()