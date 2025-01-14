# Python
import pandas as pd
from prophet import Prophet

# Python
df = pd.read_csv('https://raw.githubusercontent.com/facebook/prophet/main/examples/example_wp_log_peyton_manning.csv')
df.head()

# Python
m = Prophet()
m.fit(df)

# Python
future = m.make_future_dataframe(periods=365)
future.tail()

# Python
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

# Python
fig1 = m.plot(forecast)

# Python
fig2 = m.plot_components(forecast)

# Python
from prophet.plot import plot_plotly, plot_components_plotly

plot_plotly(m, forecast)

# Python
plot_components_plotly(m, forecast)


