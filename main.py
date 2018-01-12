import requests
import time
import xml.etree.ElementTree


TOP_TEAMS = [
    'India',
    'Pak',
]
API_KEY = 'XcYqxucnQ0N3MfPLsfgnYO73pjj2'


def get_top_matches_ids():
    url = 'http://cricapi.com/api/matches'
    data = {
        'apikey': API_KEY
    }
    response = requests.get(url, data=data)
    # Get the set of match IDs of the top teams playing
    matches_ids = set()
    for match in response.json()['matches']:
        for team in TOP_TEAMS:
            if team == match['team-1'] or team == match['team-2']:
                matches_ids.add(match['unique_id'])
    return matches_ids


def get_match_scores(matches_ids):
    url = 'http://cricapi.com/api/cricketScore'
    params = {
        'unique_id': None
    }
    data = {
        'apikey': API_KEY
    }
    match_scores = []
    for match_id in matches_ids:
        params['unique_id'] = match_id
        response = requests.get(url, data=data, params=params)
        match_scores.append(response.json())
    return match_scores


def print_match_score(matches_ids):
    match_scores = get_match_scores(matches_ids)
    while True:
        for match in match_scores:
            print(match['score'], end='\r')
        time.sleep(60)


def main():
    matches_ids = get_top_matches_ids()
    print_match_score(matches_ids)


main()
