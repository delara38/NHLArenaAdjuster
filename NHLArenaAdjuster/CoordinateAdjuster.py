from statsmodels.distributions.empirical_distribution import ECDF
from copy import copy
import pandas as pd


class CoordinateAdjuster:
    totalXCords = None
    totalYCords = None
    rinkCDFS = {}
    aTeamCDFS = {}
    raCDFS = {}
    passed_data = None

    def fit(self, data):
        '''
        Builds Venue objects for each venue in data as well as creating total CDFs

        :param data: pandas dataframe with following columns:
                 *   [x coordinate, y coordinate, arena, away team name, away shot boolean]
        :return: None
        '''

        # setting to dataframe if not already
        if (type(data) != pd.DataFrame):
            data = pd.DataFrame(data)
        df = copy(data)
        # setting columns
        df.columns = ['xCord', 'yCord', 'arenaId', 'awayTeam', 'isAway']

        # set passed data to df
        self.passed_data = df

        # set x cord and y cord total lists to be all the x and y values
        # ordered in their own respective lists
        self.totalXCords = df[['xCord']].sort_values(ascending=True, by='xCord').values.reshape(-1)
        self.totalYCords = df[['yCord']].sort_values(ascending=True, by='yCord').values.reshape(-1)

        # create total x and y df for all shots and away shots
        self.totalXCDF = ECDF(df['xCord'].values.reshape(-1))
        self.totalYCDF = ECDF(df['yCord'].values.reshape(-1))

        for arena in df['arenaId'].unique().tolist():
            self.rinkCDFS[arena] = {}
            self.rinkCDFS[arena]['y'] = ECDF(df[df['arenaId'] == arena]['yCord'].values.reshape(-1))
            self.rinkCDFS[arena]['x'] = ECDF(df[df['arenaId'] == arena]['xCord'].values.reshape(-1))

            for team in df['awayTeam'].unique().tolist():
                print(arena, team, len(df[(df['arenaId'] == arena) & (df['awayTeam'] == team) & (df['isAway'] == 1)][
                        'yCord'].values.reshape(-1)))
                if team not in self.aTeamCDFS.keys():

                    self.aTeamCDFS[team] = {}
                    self.aTeamCDFS[team]['y'] = ECDF(
                        df[(df['awayTeam'] == team) & (df['isAway'] == 1)]['yCord'].values.reshape(-1))
                    self.aTeamCDFS[team]['x'] = ECDF(
                        df[(df['awayTeam'] == team) & (df['isAway'] == 1)]['xCord'].values.reshape(-1))

                if len(df[(df['arenaId'] == arena) & (df['awayTeam'] == team) & (df['isAway'] == 1)][
                        'yCord'].values.reshape(-1)) == 0:
                    continue

                self.raCDFS[f"{team}{arena}"] = {}
                self.raCDFS[f"{team}{arena}"]['y'] = ECDF(
                    df[(df['arenaId'] == arena) & (df['awayTeam'] == team) & (df['isAway'] == 1)][
                        'yCord'].values.reshape(-1))
                self.raCDFS[f"{team}{arena}"]['x'] = ECDF(
                    df[(df['arenaId'] == arena) & (df['awayTeam'] == team) & (df['isAway'] == 1)][
                        'xCord'].values.reshape(-1))
            self.raCDFS[f"{arena}"] = {}
            self.raCDFS[f"{arena}"]['y'] = ECDF(
                df[(df['arenaId'] == arena) & (df['isAway'] == 0)]['yCord'].values.reshape(-1))
            self.raCDFS[f"{arena}"]['x'] = ECDF(
                df[(df['arenaId'] == arena) & (df['isAway'] == 0)]['xCord'].values.reshape(-1))

    def upd_row(self, r):
        # set venue object to be picked later
        aTeamCDF = None
        rCDF = None
        arCDF = None

        # get correct venue object or raise error

        if r['awayTeam'] in self.aTeamCDFS.keys():
            aTeamCDF = self.aTeamCDFS[r['awayTeam']]
        else:
            raise ValueError(
                "arenaId column (3rd column) has id that did not exist in data that was originally passed to CoordinateAdjuster")
        if r['arenaId'] in self.rinkCDFS.keys():
            rCDF = self.rinkCDFS[r['arenaId']]
        else:
            raise ValueError(
                "arenaId column (3rd column) has id that did not exist in data that was originally passed to CoordinateAdjuster")
        if r['isAway'] == 1:
            arCDF = self.raCDFS[f"{r['awayTeam']}{r['arenaId']}"]
        else:
            arCDF = self.raCDFS[f"{r['arenaId']}"]

        # get x and y coordinate of row iterating on
        x = r['xCord']
        y = r['yCord']

        # get values to be fit to "inverse ecdf"
        xp = rCDF['x'](x) - (arCDF['x'](x) - aTeamCDF['x'](x))
        yp = rCDF['y'](y) - (arCDF['y'](y) - aTeamCDF['y'](y))

        '''
        these values gotten above will be like 0.77 or 0.2 on [0,1] representing the percentile of data
        to which it should belong so for 0.77 it should be the x value bigger than 77% of all x values
        as such we multiply by those values by the lengths of their respective /ordered/ coordinate lists 
        '''

        xp = self.totalXCords[int(len(self.totalXCords) * xp)] if xp < 1 else self.totalXCords[
            len(self.totalXCords) - 1]
        yp = self.totalYCords[int(len(self.totalYCords) * yp)] if yp < 1 else self.totalYCords[
            len(self.totalYCords) - 1]

        return xp, yp

    def transform(self, data):
        """
        Applies arena adjustments according to method described by Shuckers & Curro
            in "Total Hockey Rating (THoR): A comprehensive statistical rating
            of National Hockey League forwards and defensemen based upon all on-ice events"

            x’= FX-1( FR(x) – (FRA(x)-FA(x) )
            y’= GX-1( GR(y) – (GRA(y)-GA(y) )

        :param data: pandas dataframe with following columns:
                 *   [x coordinate, y coordinate, arena, away team name, away shot boolean]
        :return: 5xN array where N is the length of the input dataframe with 'xCord' and 'yCord' being adjusted values: [ adjusted x coordinate, adjusted y coordinate ]



       """

        # set data to dataframe
        if (type(data) != pd.DataFrame):
            data = pd.DataFrame(data)
        df = copy(data)
        # set columns so it can be used without risk of misnamed columns
        df.columns = ['xCord', 'yCord', 'arenaId', 'awayTeam', 'isAway']

        df[['xCord', 'yCord']] = df.apply(self.upd_row, axis=1, result_type='expand')
        return df

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)