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


# Separating in three eras: 1996 until 2004, 2005 until 2013, and 2014 until 2022
df_merge_before = df_merge[(df_merge['SEASON_1'] >= 1996) & (df_merge['SEASON_1'] <= 2004)].copy()
df_merge_mid = df_merge[(df_merge['SEASON_1'] >= 2005) & (df_merge['SEASON_1'] <= 2013)].copy()
df_merge_after = df_merge[(df_merge['SEASON_1'] >= 2014) & (df_merge['SEASON_1'] <= 2022)].copy()

winpcb_lm = smf.ols(formula = 'W_PCT ~ FG3_PCT + OPP_FG3_PCT + FG2_PCT + OPP_FG2_PCT', data=df_merge_before).fit()
winpcm_lm = smf.ols(formula = 'W_PCT ~ FG3_PCT + OPP_FG3_PCT + FG2_PCT + OPP_FG2_PCT', data=df_merge_mid).fit()
winpca_lm = smf.ols(formula = 'W_PCT ~ FG3_PCT + OPP_FG3_PCT + FG2_PCT + OPP_FG2_PCT', data=df_merge_after).fit()

table = summary_col([winpcb_lm, winpcm_lm, winpca_lm], stars=True, float_format='%.4f',
                     model_names=['1996-2004', '2005-2013', '2014-2022'], info_dict={'N': lambda x: "{0:d}".format(int(x.nobs))})
print(table)
