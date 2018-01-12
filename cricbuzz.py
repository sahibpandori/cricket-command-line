from xml.etree import ElementTree
import requests
import time
import curses
from match import TestMatch, ODIMatch


live_matches_url = 'http://synd.cricbuzz.com/j2me/1.0/livematches.xml'
ODI_NUM_OVERS_PER_INNINGS = 50
ODI_NUM_INNINGS = 2
TEST_MAX_NUM_DAYS = 5
TEST_MAX_NUM_OVERS_PER_DAY = 90
TEST_MAX_NUM_INNINGS = 4
SCORE_UPDATE_INTERVAL_IN_SECONDS = 15


def main():
    stdscr = curses.initscr()
    try:
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)
        while True:
            response = requests.get(url=live_matches_url)
            root = ElementTree.fromstring(response.content)
            win = curses.newwin(20, 75, 0, 0)
            for match in root:
                if match.tag != 'match':
                    continue
                elif match.attrib['type'] == 'TEST':
                    tm = TestMatch(match)
                    tm.render_score_summary(win)
                elif match.attrib['type'] == 'ODI':
                    om = ODIMatch(match)
                    om.render_score_summary(win)
                else:
                    pass
            time.sleep(SCORE_UPDATE_INTERVAL_IN_SECONDS)
    except KeyboardInterrupt:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
    except ValueError:
        pass


main()
