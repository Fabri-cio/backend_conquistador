# views.py
from django.http import JsonResponse
import pandas as pd
from prophet import Prophet

def forecast_view(request):
    # Cargar los datos de ejemplo o datos relevantes para la predicción
    df = pd.read_csv('https://raw.githubusercontent.com/facebook/prophet/main/examples/example_wp_log_peyton_manning.csv')

    # Crear y ajustar el modelo Prophet
    model = Prophet()
    model.fit(df)

    # Crear las predicciones
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    # Convertir las predicciones a JSON
    forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')

    # Retornar los datos en formato JSON
    return JsonResponse(forecast_data, safe=False)
