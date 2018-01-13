class Inning:
    """
    Represents information about a Innings
    """

    def __init__(self, attr, batting_team_name, bowling_team_name):
        self.batting_team = batting_team_name
        self.bowling_team = bowling_team_name
        self.runs = attr['r']
        self.wickets = attr['wkts']
        self.declared = False if attr['Decl'] == '0' else True
        self.following_on = False if attr['FollowOn'] == '0' else True
        self.overs = attr['ovrs']
        self.desc = attr['desc']

    def __str__(self):
        header = "{batting_team:<30}\t\t{runs:>4}/{wkts:<2}{decl:<1}\t{overs:>5} overs\n".format(
            batting_team=self.batting_team,
            runs=self.runs,
            wkts=self.wickets,
            decl="d" if self.declared else "",
            overs=self.overs,
        )
        return header
