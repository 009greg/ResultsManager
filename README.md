# ResultsManager
Imports a SUIS formatted CSV results file from SUIS Electronic Scoring Systems into a SQLite Database.

Process results dependant on competition type and add these to a master dataframe using Pandas. Once details are extracted from CSV, i.e Name, x654 score and x109 series, save the master dataframe to a SQLite database for future reference and lookups of competitors averages and handicap scores.  

# Current Features

CSV results processing for ISSF 50m Prone 60 shot competitions. 
Creation of 'your competition name' tables in SQLite Database.
Competition name duplicate checking
Basic GUI for CSV Import

# Future Features

Average and Handicap Calculation
More extensive error handling
Results processing for ISSF 50m 3P and 10m Air Rifle.
GUI Results Lookup 


