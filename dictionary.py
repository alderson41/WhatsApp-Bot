import requests

def definition(query):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{query}/definitions"

    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "cd45b26e6bmsh4f478493bc8c6bap1978bejsn235dbc6e119d"
        }

    response = requests.request("GET", url, headers=headers)

    return response.json()['definitions']


def synonym(query):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{query}/synonyms"

    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "cd45b26e6bmsh4f478493bc8c6bap1978bejsn235dbc6e119d"
        }

    response = requests.request("GET", url, headers=headers)
    return response.json()['synonyms']
