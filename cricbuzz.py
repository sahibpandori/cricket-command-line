from xml.etree import ElementTree
import requests
import time
import curses
from threading import Thread
from match import Match


live_matches_url = 'http://synd.cricbuzz.com/j2me/1.0/livematches.xml'


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
    return matches[idx].id


def update_score(win, match_id, update_interval):
    while True:
        # Get the current live score in XML form
        response = requests.get(url=live_matches_url)
        root = ElementTree.fromstring(response.content)
        # Render the score summary for the selected match
        for match in root:
            if match.tag == 'match' and match.attrib['id'] == match_id:
                m = Match.get_instance(match)
                m.render_score_summary(win)
        time.sleep(update_interval)


def main():
    score_update_interval_sec = 15

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

        # Create a thread to periodically update scores
        score_updater = Thread(target=update_score, args=(win, match_id, score_update_interval_sec))
        score_updater.daemon = True
        score_updater.start()

        key = ''
        # Wait for the user to quit
        while key != ord('q'):
            key = win.getch()

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
