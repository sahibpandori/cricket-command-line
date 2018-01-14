import abc
from datetime import datetime
from inning import Inning


class Match:
    """
    Abstract Match class from which ODIs and Tests will be derived
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, match):
        """
        Constructs a Match object given an XML format of the object
        :param match: the XML format for the match object
        """
        self.id = match.attrib['id']
        self.series = match.attrib['srs']
        self.match_desc = match.attrib['mchDesc']
        self.match_num = match.attrib['mnum']
        self.type = None
        try:
            self.city = match.attrib['vcity']
            self.country = match.attrib['vcountry']
            self.ground = match.attrib['grnd']
        except KeyError:
            pass
        self.inning_num = match.attrib['inngCnt']
        self.teams = list()
        self.innings = list()
        for child in match:
            if child.tag == 'state':
                self.match_state = child.attrib['mchState']
                self.curr_status = child.attrib['status']
                try:
                    self.toss_winner = child.attrib['TW']
                    self.toss_decision = child.attrib['decisn']
                    self.addn_status = child.attrib['addnStatus']
                except KeyError:
                    pass
            elif child.tag == 'Tm':
                self.teams.append(child.attrib['sName'])
            elif child.tag == 'Tme':
                self.start_date = child.attrib['Dt']
                self.start_time = child.attrib['stTme']
                self.end_date = child.attrib['enddt']
            elif child.tag == 'mscr':
                for attr in child:
                    if attr.tag == 'inngsdetail':
                        self.num_overs_completed = attr.attrib['noofovers']
                        self.req_run_rate = attr.attrib['rrr']
                        self.curr_run_rate = attr.attrib['crr']
                        self.curr_partnership = attr.attrib['cprtshp']
                    elif attr.tag == 'btTm':
                        batting_team_name = attr.attrib['sName']
                        bowling_team_name = self.teams[0] if self.teams[1] == batting_team_name else self.teams[1]
                        for ing in attr:
                            inning = Inning(ing.attrib, batting_team_name, bowling_team_name)
                            self.innings.append(inning)
                    elif attr.tag == 'blgTm':
                        batting_team_name = attr.attrib['sName']
                        bowling_team_name = self.teams[0] if self.teams[1] == batting_team_name else self.teams[1]
                        for ing in attr:
                            inning = Inning(ing.attrib, batting_team_name, bowling_team_name)
                            self.innings.append(inning)
        self.innings.sort(key=self.get_inning_rank)

    def get_inning_rank(self, inning):
        """
        Returns the rank of an innings in order to sort them in chronological order
        :param inning: The inning whose rank is to be returned
        :return: Rank of inning
        """
        if inning.desc == '1st Inns':
            if (self.toss_decision == 'Batting') == (inning.batting_team == self.toss_winner):
                return 1
            else:
                return 2
        elif inning.following_on:
            return 2.5
        else:
            if (self.toss_decision == 'Batting') == (inning.batting_team == self.toss_winner):
                return 3
            else:
                return 4

    def get_score_summary(self):
        """
        Return the string representation of the score summary
        :return: Score summary
        """
        score_summary = "\n"
        dt = datetime.now()
        if len(self.innings) > 0:
            for inning in self.innings:
                score_summary += str(inning)
        else:
            score_summary += "Match has not started yet..."

        def pad_0(x):
            return str(x) if x > 10 else '0'+str(x)

        score_summary += "\n(Last updated at {hr}:{min}:{sec})\n".format(hr=pad_0(dt.hour),
                                                                         min=pad_0(dt.minute),
                                                                         sec=pad_0(dt.second))
        return score_summary

    def render_score_summary(self, win):
        """
        Render the score summary and update it at each update interval
        :param: The window to render the score in
        """
        if win is None:
            raise ValueError('No window provided to render the score summary')
        win.addstr(0, 0, self.get_score_summary())
        win.addstr("\nPress 'q' to Quit")
        win.refresh()

    def get_header(self):
        """
        :return: The title of the match
        """
        return self.teams[0] + ' vs. ' + self.teams[1]

    @staticmethod
    def get_instance(match):
        """
        Factory method to get the relevant match object
        :param match: XML form of the match
        :return: An instance of the relevant match class
        """
        if match.attrib['type'] == 'TEST':
            return TestMatch(match)
        elif match.attrib['type'] == 'ODI':
            return ODIMatch(match)
        else:
            return None

    def __str__(self):
        return self.get_score_summary()


class ODIMatch(Match):
    """
    Represents a 50-over One Day International match
    """
    def __init__(self, match):
        super().__init__(match)
        self.type = 'ODI'


class TestMatch(Match):
    """
    Represents a 5-day Test match
    """
    def __init__(self, match):
        super().__init__(match)
        self.type = 'TEST'
