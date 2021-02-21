import pandas
import sqlite3
from PyQt5 import QtWidgets

# Create dataframes for each results parameter, i.e decimal score x654, inner tens etc
# Then once all these dataframes are generated, merge them into one frame
# This master frame becomes the competition frame and includes all details from the match
# This frame is then imported into the database under a new SQLite table. (E.g Table = Competition1)

global names, SN


def importname(path):
    df = pandas.read_csv(path, sep=';', names=['1', 'SN', 'LastName', 'FirstName', 'FirstAndLast',
                                               '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'])
    df.to_csv('nametest.csv')

    # Remove non useful information
    f = pandas.read_csv('nametest.csv', sep=',')
    f.set_index('SN')
    keep_cols = ['SN', 'FirstName', 'LastName']
    new_f = f[keep_cols]
    new_f.set_index('SN')
    new_f.to_csv("nameuseful.csv", index=False)


def uploadtodatabase_50m():
    # Import database #fixme for when start numbers don't begin 0

    data = pandas.read_csv('sinclairformatprocessed.csv', sep=',')


    # Define dataframes per result parameter
    decscoreframe = pandas.DataFrame(columns=['x654Series'])
    intscoreframe = pandas.DataFrame(columns=['x600Series'])
    innertensframe = pandas.DataFrame(columns=['IT'])
    x109Seriesframe = pandas.DataFrame(columns=['x109Series1','x109Series2','x109Series3','x109Series4',
                                           'x109Series5','x109Series6'])
    x436frame = pandas.DataFrame(columns=['x436Series'])
    x400frame = pandas.DataFrame(columns=['x400Series'])



    def getdecimalscorefromsn(SN):
        # Decimal Score from Start Number
        # Need to do this only for match = 1
        if SN in data.StartN.array:
            condition1 = data.SightorMatch.array == 1
            filtereddf = data[condition1]
            condition3 = filtereddf.StartN.array == SN
            combined = filtereddf[condition3]

            sumdecscore = str(combined.PrimaryScore.array.sum())
            sumdecscoreISSF = '{0:.1f}'.format(float(sumdecscore))
            # Create individual decimal score dataframe with index based on start number
            decscoreframe.loc[SN] = [sumdecscoreISSF]
        return

    def getintegerscorefromsn(SN):
        #fixme In 50m match, Secondary score is blank, so int score can't be calculated this way -
        if SN in data.StartN.array:
            condition1 = data.SightorMatch.array == 1
            filtereddf = data[condition1]
            condition3 = filtereddf.StartN.array == SN
            combined = filtereddf[condition3]
            sumintscore = str(combined.SS.array.sum())
            # Create individual decimal score dataframe with index based on start number
            intscoreframe.loc[SN] = [sumintscore]
        return

    def getx436(SN):
        if SN in data.StartN.array:
            condition1 = data.SightorMatch.array == 1
            filtereddf = data[condition1]
            condition3 = filtereddf.StartN.array == SN
            combined = filtereddf[condition3]
            x436 = str(combined.iloc[0:40, 4].sum())
            x436ISSF = '{0:.1f}'.format(float(x436))
            x436frame.loc[SN] = [x436ISSF]

    def getx400(SN):
        if SN in data.StartN.array:
            condition1 = data.SightorMatch.array == 1
            filtereddf = data[condition1]
            condition3 = filtereddf.StartN.array == SN
            combined = filtereddf[condition3]
            x400 = str(combined.iloc[0:40, 1].sum())
            x400frame.loc[SN] = [x400]

    def get109series(SN):
        # Get x109 Series 1 to 6
        if SN in data.StartN.array:
            condition1 = data.SightorMatch.array == 1
            filtereddf = data[condition1]
            condition3 = filtereddf.StartN.array == SN
            combined = filtereddf[condition3]
            # x109Series
            x109Series1 = str(combined.iloc[0:10, 1].sum())
            x109SeriesISSF1 = '{0:.1f}'.format(float(x109Series1))
            x109Series2 = str(combined.iloc[10:20, 1].sum())
            x109SeriesISSF2 = '{0:.1f}'.format(float(x109Series2))
            x109Series3 = str(combined.iloc[20:30, 1].sum())
            x109SeriesISSF3 = '{0:.1f}'.format(float(x109Series3))
            x109Series4 = str(combined.iloc[30:40, 1].sum())
            x109SeriesISSF4 = '{0:.1f}'.format(float(x109Series4))
            x109Series5 = str(combined.iloc[40:50, 1].sum())
            x109SeriesISSF5 = '{0:.1f}'.format(float(x109Series5))
            x109Series6 = str(combined.iloc[50:60, 1].sum())
            x109SeriesISSF6 = '{0:.1f}'.format(float(x109Series6))


            # Stitch together
            x109Seriesframe.loc[SN, 'x109Series1'] = x109SeriesISSF1
            x109Seriesframe.loc[SN, 'x109Series2'] = x109SeriesISSF2
            x109Seriesframe.loc[SN, 'x109Series3'] = x109SeriesISSF3
            x109Seriesframe.loc[SN, 'x109Series4'] = x109SeriesISSF4
            x109Seriesframe.loc[SN, 'x109Series5'] = x109SeriesISSF5
            x109Seriesframe.loc[SN, 'x109Series6'] = x109SeriesISSF6

    def getinnertensfromsn(SN):
        # Get number of inner tens from a firing point
        if SN in data.StartN.array:
            condition1 = data.SightorMatch.array == 1
            filtereddf = data[condition1]
            condition3 = filtereddf.StartN.array == SN
            combined = filtereddf[condition3]
            innertensstr = str(combined.IT.array.sum())
            innertensframe.loc[SN] = [innertensstr]


    # def getfiringpoint():
    #     # Get Active Firing Points
    #     firingpoints = data.FP.array
    #     firingpoints = data.FP.drop_duplicates()
    #     print(firingpoints)

    # Need start numbers processed without dupes
    startnumbersnodupes = data.StartN.drop_duplicates()

    # New results frame
    for SN in startnumbersnodupes:
        getdecimalscorefromsn(SN)
        getinnertensfromsn(SN)
        get109series(SN)
        getintegerscorefromsn(SN)
        getx400(SN)
        getx436(SN)

    global masterframe

    # fixme - data puts 'shooter0' with no score, remove all shooter 0s

    names = pandas.read_csv('nameuseful.csv', sep=',', index_col='SN')

    masterframe = pandas.concat([names,x109Seriesframe, decscoreframe, intscoreframe, innertensframe, x436frame, x400frame], axis=1)


def masterframetodb_50m(namecomp):

        # Upload to Database
        conn = sqlite3.connect('IOMSC_Results.db')
        try:
            masterframe.to_sql(namecomp, conn, if_exists="fail")
            pass
        except ValueError:
            error = QtWidgets.QMessageBox()
            error.setIcon(QtWidgets.QMessageBox.Warning)
            error.setWindowTitle('Warning')
            error.setText("Duplicate Name")
            error.setInformativeText("The competition already exists, please choose another name.")
            error.exec_()
            pass
        except sqlite3.OperationalError:
            error = QtWidgets.QMessageBox()
            error.setIcon(QtWidgets.QMessageBox.Warning)
            error.setWindowTitle('Warning')
            error.setText("SQLite Operational Error")
            error.setInformativeText("The competition already exists, please choose another name.")
            error.exec_()
            pass
        conn.close()


def uploadtodatabase_3P():
    # Import database #fixme for when start numbers don't begin 0

    data = pandas.read_csv('useful.csv', sep=',')


    # Define dataframes per result parameter
    decscoreframe = pandas.DataFrame(columns=['x654Series'])
    intscoreframe = pandas.DataFrame(columns=['x600Series'])
    innertensframe = pandas.DataFrame(columns=['IT'])
    x109Seriesframe = pandas.DataFrame(columns=['x109Series1','x109Series2','x109Series3','x109Series4',
                                           'x109Series5','x109Series6'])
    x436frame = pandas.DataFrame(columns=['x436Series'])
    x400frame = pandas.DataFrame(columns=['x400Series'])



    def getdecimalscorefromsn(SN):
        # Decimal Score from Start Number
        if SN in data.StartN.array:
            condition = data.StartN.array == SN
            filtereddf = data[condition]
            sumdecscore = str(filtereddf.SS.array.sum())
            sumdecscoreISSF = '{0:.1f}'.format(float(sumdecscore))
            # Create individual decimal score dataframe with index based on start number
            decscoreframe.loc[SN] = [sumdecscoreISSF]
        return

    def getintegerscorefromsn(SN):
        if SN in data.StartN.array:
            condition = data.StartN.array == SN
            filtereddf = data[condition]
            sumintscore = str(filtereddf.PrimaryScore.array.sum())
            # Create individual decimal score dataframe with index based on start number
            intscoreframe.loc[SN] = [sumintscore]
        return

    def getx436(SN):
        if SN in data.StartN.array:
            condition = data.StartN.array == SN
            filtereddf = data[condition]
            x436 = str(filtereddf.iloc[0:40, 4].sum())
            x436ISSF = '{0:.1f}'.format(float(x436))
            x436frame.loc[SN] = [x436ISSF]

    def getx400(SN):
        if SN in data.StartN.array:
            condition = data.StartN.array == SN
            filtereddf = data[condition]
            x400 = str(filtereddf.iloc[0:40, 1].sum())
            x400frame.loc[SN] = [x400]

    def get109series(SN):
        # Get x109 Series 1 to 6
        if SN in data.StartN.array:
            condition = data.StartN.array == SN
            filtereddf = data[condition]
            # x109Series
            x109Series1 = str(filtereddf.iloc[0:10, 4].sum())
            x109SeriesISSF1 = '{0:.1f}'.format(float(x109Series1))
            x109Series2 = str(filtereddf.iloc[10:20, 4].sum())
            x109SeriesISSF2 = '{0:.1f}'.format(float(x109Series2))
            x109Series3 = str(filtereddf.iloc[20:30, 4].sum())
            x109SeriesISSF3 = '{0:.1f}'.format(float(x109Series3))
            x109Series4 = str(filtereddf.iloc[30:40, 4].sum())
            x109SeriesISSF4 = '{0:.1f}'.format(float(x109Series4))
            x109Series5 = str(filtereddf.iloc[40:50, 4].sum())
            x109SeriesISSF5 = '{0:.1f}'.format(float(x109Series5))
            x109Series6 = str(filtereddf.iloc[50:60, 4].sum())
            x109SeriesISSF6 = '{0:.1f}'.format(float(x109Series6))


            # Stitch together
            x109Seriesframe.loc[SN, 'x109Series1'] = x109SeriesISSF1
            x109Seriesframe.loc[SN, 'x109Series2'] = x109SeriesISSF2
            x109Seriesframe.loc[SN, 'x109Series3'] = x109SeriesISSF3
            x109Seriesframe.loc[SN, 'x109Series4'] = x109SeriesISSF4
            x109Seriesframe.loc[SN, 'x109Series5'] = x109SeriesISSF5
            x109Seriesframe.loc[SN, 'x109Series6'] = x109SeriesISSF6

    def getinnertensfromsn(SN):
        # Get number of inner tens from a firing point
        if SN in data.StartN.array:
            condition = data.StartN.array == SN
            filtereddf = data[condition]
            innertensstr = str(filtereddf.IT.array.sum())
            innertensframe.loc[SN] = [innertensstr]


    # def getfiringpoint():
    #     # Get Active Firing Points
    #     firingpoints = data.FP.array
    #     firingpoints = data.FP.drop_duplicates()
    #     print(firingpoints)

    # Need start numbers processed without dupes
    startnumbersnodupes = data.StartN.drop_duplicates()

    # New results frame
    for SN in startnumbersnodupes:
        getdecimalscorefromsn(SN)
        getinnertensfromsn(SN)
        get109series(SN)
        getintegerscorefromsn(SN)
        getx400(SN)
        getx436(SN)

    global masterframe

    # fixme - data puts 'shooter0' with no score, remove all shooter 0s

    names = pandas.read_csv('nameuseful.csv', sep=',')
    names.index = names.index + SN
    # Split Names into First Name and Last Name
    names.dropna(inplace=True)
    new = names["Name"].str.split(" ", n=1, expand=True)
    names["FirstName"] = new[0]
    names["LastName"] = new[1]
    names.drop(columns=["Name"], inplace=True)

    masterframe = pandas.concat([names,x109Seriesframe, decscoreframe, intscoreframe, innertensframe, x436frame, x400frame], axis=1)


def masterframetodb_3P(namecomp):

        # Upload to Database
        conn = sqlite3.connect('IOMSC_Results.db')
        try:
            masterframe.to_sql(namecomp, conn, if_exists="fail")
            pass
        except ValueError:
            error = QtWidgets.QMessageBox()
            error.setIcon(QtWidgets.QMessageBox.Warning)
            error.setWindowTitle('Warning')
            error.setText("Duplicate Name")
            error.setInformativeText("The competition already exists, please choose another name.")
            error.exec_()
            pass
        except sqlite3.OperationalError:
            error = QtWidgets.QMessageBox()
            error.setIcon(QtWidgets.QMessageBox.Warning)
            error.setWindowTitle('Warning')
            error.setText("SQLite Operational Error")
            error.setInformativeText("The competition already exists, please choose another name.")
            error.exec_()
            pass
        conn.close()



