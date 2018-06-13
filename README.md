# Stock-Recommendations-App
From a mac on the terminal, navigate to the directory to which this repository has been cloned.
\nTo install the requirements, type 'pip3 install -r requirements.txt'
\nAdd a file called '.env' to the repository and enter the text 'ALPHAVANTAGE_API_KEY = your_api_key'. 
\nSave the file, as it will be necessary to request data from the server.
From the terminal, type 'python3 stock-guru.py'. This will initialize the program.
You will be prompted to input a stock symbol.
The script will output:
  The run time and date
  The latest close price for the stock
  The recent average high price for the stock
  The recent average low price for the stock
  A recommendation to buy or sell the stock based on its last close compared to its 100 day simple moving average, and
  When the latest data is from.
