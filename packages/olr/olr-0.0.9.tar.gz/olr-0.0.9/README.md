The olr function runs all the possible combinations of linear regressions with all of the
dependent variables against the independent variable and returns the statistical summary
of either the greatest adjusted R-squared or R-squared term.



datasetname = pd.read_csv('C:\Rstuff\olr\inst\extdata\oildata.csv')
resvarname = datasetname[['OilPrices']]
expvarnames = datasetname[['SP500', 'RigCount', 'API', 'Field_Production', 'RefinerNetInput', 'OperableCapacity', 'Imports', 'StocksExcludingSPR']]

The TRUE or FALSE in the olr function, specifies either the adjusted R-squared or the R-squared regression summary, respectfully.

Adjusted R-squared <br />
olr(datasetname, resvarname, expvarnames, adjr2 = "True")

R-squared <br />
olr(datasetname, resvarname, expvarnames, adjr2 = "False")

list of summaries <br />
olrmodels(datasetname, resvarname, expvarnames)

list of formulas <br />
olrformulas(datasetname, resvarname, expvarnames)

list of forumlas with the dependant variables in ascending order <br />
olrformulasorder(datasetname, resvarname, expvarnames)

the list of adjusted R-squared terms <br />
adjr2list(datasetname, resvarname, expvarnames)

the list of R-squared terms <br />
r2list(datasetname, resvarname, expvarnames)

There is an R version of this package.