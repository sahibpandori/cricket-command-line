from xml.etree import ElementTree
from threading import Thread
from match import Match
import requests
import curses
import time

live_matches_url = 'http://synd.cricbuzz.com/j2me/1.0/livematches.xml'


def display_choices(matches):
    """
    Display possible matches for which live scores are available
    :param matches: All match objects
    """
    print("Choose a match:-")
    i = 1
    for match in matches:
        print(str(i) + ". " + match.get_header())
        i += 1


def get_selected_match_id():
    """
    Get all current live matches and make user select the match they're most interested in following
    :return: The match id of the respective match
    """
    response = requests.get(url=live_matches_url)
    root = ElementTree.fromstring(response.content)
    matches = []
    for match in root:
        if match.tag == 'match':
            m = Match.get_instance(match)
            if m is not None:
                matches.append(m)
    while True:
        display_choices(matches)
        idx = int(input("Enter your choice: ")) - 1
        if idx < 0 or idx >= len(matches):
            print("Invalid choice, choose again.\n")
        else:
            break
    return matches[idx].id


def update_score(win, match_id, update_interval):
    """
    Method to update the score with the most recent score received from the Cricbuzz API
    :param win: The window to display the score in
    :param match_id: The id of the match we're displaying the score for
    :param update_interval: The frequency at which to poll the Cricbuzz API for the live score
    """
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
    """
    main controller function that creates a window to render the scores, starts the update thread and waits until the
    user quits
    """
    score_update_interval_sec = 15
    window_width = 75
    window_height = 20

    # Get the match to be followed
    match_id = get_selected_match_id()

    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    try:
        # Create a new window to display the score
        win = curses.newwin(window_height, window_width, 0, 0)

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
