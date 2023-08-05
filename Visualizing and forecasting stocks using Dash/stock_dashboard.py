import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Step 3: Get stock data
def get_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    return stock_data

# Step 5: Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='stock-input', value='AAPL', type='text'),
    dcc.Graph(id='stock-graph'),
    dcc.Graph(id='forecast-graph')
])

# Step 5: Define the callback functions
@app.callback(
    [Output('stock-graph', 'figure'),
     Output('forecast-graph', 'figure')],
    [Input('stock-input', 'value')]
)
def update_graph(stock_symbol):
    # Get stock data for the last year
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.DateOffset(years=1)
    stock_data = get_stock_data(stock_symbol, start_date, end_date)

    # Create the stock graph
    stock_fig = go.Figure()
    stock_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close Price'))
    stock_fig.update_layout(title=f'{stock_symbol} Stock Price',
                            xaxis_title='Date',
                            yaxis_title='Price',
                            showlegend=True)

    # Forecasting (you can use your desired forecasting method here)
    # For simplicity, we'll use a simple moving average
    forecast_data = stock_data.copy()
    forecast_data['Forecast'] = stock_data['Close'].rolling(window=5).mean()

    # Create the forecast graph
    forecast_fig = go.Figure()
    forecast_fig.add_trace(go.Scatter(x=forecast_data.index, y=forecast_data['Close'], mode='lines', name='Close Price'))
    forecast_fig.add_trace(go.Scatter(x=forecast_data.index, y=forecast_data['Forecast'], mode='lines', name='Forecast'))
    forecast_fig.update_layout(title=f'{stock_symbol} Stock Forecast',
                               xaxis_title='Date',
                               yaxis_title='Price',
                               showlegend=True)

    return stock_fig, forecast_fig


if __name__ == '__main__':
    app.run_server(debug=True)
