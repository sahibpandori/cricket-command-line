from xml.etree import ElementTree
import requests
import time
import curses
from match import TestMatch, ODIMatch, Match


live_matches_url = 'http://synd.cricbuzz.com/j2me/1.0/livematches.xml'
ODI_NUM_OVERS_PER_INNINGS = 50
ODI_NUM_INNINGS = 2
TEST_MAX_NUM_DAYS = 5
TEST_MAX_NUM_OVERS_PER_DAY = 90
TEST_MAX_NUM_INNINGS = 4
SCORE_UPDATE_INTERVAL_IN_SECONDS = 15


def display_choices(matches):
    print("Choose a match:-")
    i = 1
    for match in matches:
        print(str(i) + ". " + match.get_header())
        i += 1


def get_selected_match_id():
    response = requests.get(url=live_matches_url)
    root = ElementTree.fromstring(response.content)
    matches = []
    for match in root:
        if match.tag == 'match':
            m = Match.get_instance(match)
            if m is not None:
                matches.append(m)
    display_choices(matches)
    idx = int(input("Enter your choice: ")) - 1
    return matches[idx].get_id()


def main():
    # Get the match to be followed
    match_id = get_selected_match_id()

    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    try:
        # Create a new window to display the score
        win = curses.newwin(20, 75, 0, 0)
        # Display the score until user exits
        while True:
            response = requests.get(url=live_matches_url)
            root = ElementTree.fromstring(response.content)
            for match in root:
                if match.tag == 'match' and match.attrib['id'] == match_id:
                    m = Match.get_instance(match)
                    m.render_score_summary(win)
            time.sleep(SCORE_UPDATE_INTERVAL_IN_SECONDS)
    except KeyboardInterrupt:
        pass
    except ValueError:
        pass
    finally:
        # Close the window and terminate curses
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()


main()
