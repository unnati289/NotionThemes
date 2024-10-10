import requests
import matplotlib.pyplot as plt

# Function to query Google Ngram Viewer for word data
def query_ngram(word, start_year, end_year):
    url = f'https://books.google.com/ngrams/graph?content={word}&year_start={start_year}&year_end={end_year}&corpus=15&smoothing=3'
    response = requests.get(url)
    return response.url  # The response URL can be used to directly view the graph

# Example query for the word "computer"
word = "computer"
start_year = 1960
end_year = 2023
result_url = query_ngram(word, start_year, end_year)

print("View the trend graph at:", result_url)
