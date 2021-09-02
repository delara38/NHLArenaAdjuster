from statsmodels.distributions.empirical_distribution import ECDF
from copy import copy
from Venue import Venue
import pandas as pd
import numpy as np

class CoordinateAdjuster:


    totalXCords = None
    totalYCords = None
    venues = {}
    passed_data = None



    def fit(self,data):
        '''
        Builds Venue objects for each venue in data as well as creating total CDFs

        :param data: pandas dataframe with following columns:
                 *   [x coordinate, y coordinate, arena, away team name, away shot boolean]
        :return: 2xN array where N is the length of the input dataframe with columns: [ adjusted x coordinate, adjusted y coordinate ]
        '''

        #setting to dataframe if not already
        if(type(data) != pd.DataFrame):
            data = pd.DataFrame(data)
        df = copy(data)
        #setting columns
        df.columns = ['xCord','yCord','arenaId','awayTeam','isAway']


        #set passed data to df
        self.passed_data = df

        #set x cord and y cord total lists to be all the x and y values
        # ordered in their own respective lists
        self.totalXCords = df[['xCord']].sort_values(ascending=True,by='xCord').values.reshape(-1)
        self.totalYCords = df[['yCord']].sort_values(ascending=True,by='yCord').values.reshape(-1)

        #create total x and y df for all shots and away shots
        self.totalXCDF = ECDF(df['xCord'].values.reshape(-1))
        self.totalYCDF = ECDF(df['yCord'].values.reshape(-1))
        self.aTotalXCDF = ECDF(df[df['isAway'] == 1]['xCord'].values.reshape(-1))
        self.aTotalYCDF = ECDF(df[df['isAway'] == 1]['yCord'].values.reshape(-1))

        #go through each venue in df
        for venue in df['arenaId'].unique().tolist():
            #get shots taken at venue
            arenaData = df[df['arenaId'] == venue]
            #make venue object
            vn = Venue(venue)
            #make shot models
            vn.makeShotsModel(arenaData[arenaData['isAway'] == 0].values,arenaData[arenaData['isAway'] == 1].values)
            #put object in venues dict
            self.venues[venue] = vn

    def transform(self, data):
        """
        Applies arena adjustments according to method described by Shuckers & Curro
            in "Total Hockey Rating (THoR): A comprehensive statistical rating
            of National Hockey League forwards and defensemen based upon all on-ice events"

            x’= FX-1( FR(x) – (FRA(x)-FA(x) )
            y’= GX-1( GR(y) – (GRA(y)-GA(y) )

        :param data: pandas dataframe with following columns:
                 *   [x coordinate, y coordinate, arena, away team name, away shot boolean]
        :return: 2xN array where N is the length of the input dataframe with columns: [ adjusted x coordinate, adjusted y coordinate ]



       """


        #set data to dataframe
        if(type(data) != pd.DataFrame):
            data = pd.DataFrame(data)
        df = copy(data)
        #set columns so it can be used without risk of misnamed columns
        df.columns = ['xCord', 'yCord', 'arenaId', 'awayTeam', 'isAway']

        #iterate through each row in dataframe
        for i in range(len(df)):

            #set venue object to be picked later
            vnObj = None

            #get correct venue object or raise error
            try:
                vnObj = self.venues[df.iloc[i]['arenaId']]
            except:
                raise ValueError("arenaId column (3rd column) has id that did not exist in data that was originally passed to CoordinateAdjuster")

            #get x and y coordinate of row iterating on
            x = df.iloc[i]['xCord']
            y = df.iloc[i]['yCord']

            #get values to be fit to "inverse ecdf"
            x = vnObj.shotsCDFX(x) - (vnObj.awayShotsCDFX(x) - self.aTotalXCDF(x))
            y = vnObj.shotsCDFY(y) - (vnObj.awayShotsCDFY(y) - self.aTotalYCDF(y))

            '''
            these values gotten above will be like 0.77 or 0.2 on [0,1] representing the percentile of data
            to which it should belong so for 0.77 it should be the x value bigger than 77% of all x values
            as such we multiply by those values by the lengths of their respective /ordered/ coordinate lists 
            '''


            if x == 1:
                df.iloc[i]['xCord'] = self.totalXCords[int(len(self.totalXCords) * x )-1]
                df.iloc[i]['yCord'] = self.totalYCords[int(len(self.totalYCords) * y)-1]

            else:
                df.iloc[i]['xCord'] = self.totalXCords[int(len(self.totalXCords)*x)]
                df.iloc[i]['yCord'] = self.totalYCords[int(len(self.totalYCords)*y)]

        return df

    def fit_transform(self,data):
        self.fit(data)
        return self.transform(data)




