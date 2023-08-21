import statsmodels.formula.api as smf
import pandas as pd
from statsmodels.iolib.summary2 import summary_col

# Importing
df = pd.read_csv('teamdata.csv')
dfa = pd.read_csv('teamagainstdata.csv')

df.columns
dfa.columns

# Merging both tables
df_merge = pd.merge(df, dfa, on=['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'PLUS_MINUS_RANK', 'SEASON'], how='left')
df_merge.head()

# Creating an integer number for each season
df_merge['SEASON_1'] = df_merge['SEASON'].str[:4].astype(int)
df_merge.head()

# Creating metrics
df_merge['FG3PERCTOTAL'] = df_merge['FG3M']/df_merge['FGM']
df_merge['OPPFG3PERCTOTAL'] = df_merge['OPP_FG3M']/df_merge['OPP_FGM']
df_merge['FG2M'] = df_merge['FGM'] - df_merge['FG3M']
df_merge['OPP_FG2M'] = df_merge['OPP_FGM'] - df_merge['OPP_FG3M']
df_merge['FG2A'] = df_merge['FGA'] - df_merge['FG3A']
df_merge['OPP_FG2A'] = df_merge['OPP_FGA'] - df_merge['OPP_FG3A']
df_merge['FG2_PCT'] = df_merge['FG2M']/df_merge['FG2A'] 
df_merge['OPP_FG2_PCT'] = df_merge['OPP_FG2M']/df_merge['OPP_FG2A']
df_merge.head()

# Separating in two eras: 1996 until 2011 and 2012 until 2022
df_merge_before = df_merge[(df_merge['SEASON_1'] >= 1996) & (df_merge['SEASON_1'] <= 2011)].copy()
df_merge_after = df_merge[(df_merge['SEASON_1'] >= 2012) & (df_merge['SEASON_1'] <= 2022)].copy()

## Regression calculation for 3 pts
# 1996-97 to 2011-12
winpcbef_lm = smf.ols(formula = 'W_PCT ~ FG3_PCT + OPP_FG3_PCT', data=df_merge_before).fit()
winpcbef_lm.summary()
# 2012-13 to 2022-23
winpc_lm = smf.ols(formula = 'W_PCT ~ FG3_PCT + OPP_FG3_PCT', data=df_merge_after).fit()
winpc_lm.summary()

# Table with regressions
table3pt = summary_col([winpcbef_lm, winpc_lm], stars=True, float_format='%.4f',
                     model_names=['Before 2011', 'After 2012'], info_dict={'N': lambda x: "{0:d}".format(int(x.nobs))})
print(table3pt)

## Regression calculation for 2 pts
# 1996-97 to 2011-12
winpc2bef_lm = smf.ols(formula = 'W_PCT ~ FG2_PCT + OPP_FG2_PCT', data=df_merge_before).fit()
winpc2bef_lm.summary()
# 2012-13 to 2022-23
winpc2_lm = smf.ols(formula = 'W_PCT ~ FG2_PCT + OPP_FG2_PCT', data=df_merge_after).fit()
winpc2_lm.summary()

# Table with regressions
table2pt = summary_col([winpc2_lm, winpc2bef_lm], stars=True, float_format='%.4f',
                     model_names=['Before 2011', 'After 2012'], info_dict={'N': lambda x: "{0:d}".format(int(x.nobs))})
print(table2pt)

## Comparing 2 pts and 3 pts influence over the seasons
print(f"2 points",table2pt, f"\n\n\n3 points", table3pt)
