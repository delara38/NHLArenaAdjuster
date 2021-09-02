from statsmodels.distributions.empirical_distribution import ECDF
import numpy as np

class Venue:

    Shotsx = None
    aShotsx = None
    Shotsy = None
    aShotsy = None
    ShotsModelx = None
    ShotsModely = None
    awayShotsModelx = None
    awayShotsModely = None
    name = None
    venueId = None

    def __init__(self, venueId, name=None):
        self.name = name
        self.venueId = venueId

    def makeShotsModel(self,hShots,aShots):
        self.Shotsx = np.concatenate((hShots[:,0], aShots[:,0]),axis=0)
        self.aShotsx = aShots[:,0]
        self.Shotsy = np.concatenate((hShots[:,1], aShots[:,0]),axis=0)
        self.aShotsy = aShots[:,1]



        self.ShotsModelx = ECDF(self.Shotsx)
        self.ShotsModely = ECDF(self.Shotsy)
        self.awayShotsModelx = ECDF(self.aShotsx)
        self.awayShotsModely = ECDF(self.aShotsy)

    def awayShotsCDFX(self,x):
        return self.awayShotsModelx(x)

    def shotsCDFX(self,x):
        return self.ShotsModelx(x)

    def awayShotsCDFY(self,y):
        return self.awayShotsModely(y)
    def shotsCDFY(self,y):
        return self.ShotsModely(y)

    def aShotsInvCDFX(self,x):
        return self.aShotsX[int(x*len(self.aShotsx))]
    def ShotsInvCDFX(self,x):
        return self.ShotsX[int(x*len(self.Shotsx))]

    def aShotsInvCDFY(self,y):
        return self.aShotsy[int(y*len(self.aShotsy))]
    def ShotsInvCDFY(self,y):
        return self.Shotsy[int(y*len(self.Shotsy))]

    def adjustShotsX(self,xCords, awayCDF):

        n = self.ShotsModelx(xCords) - (self.awayShotsModelx(xCords) - awayCDF(xCords))
        for i in len(xCords):
            xCords[i]= self.ShotsInvCDFX(xCords[i])

        return xCords

    def adjustShotsY(self,yCords,awayCDF):
        n = self.ShotsModely(yCords) - (self.awayShotsModely(yCords) - awayCDF(yCords))
        for i in len(yCords):
            yCords[i] = self.ShotsInvCDFY(yCords[i])

        return yCords


    def get_name(self):
        return self.name

    def getId(self):
        return self.venueId