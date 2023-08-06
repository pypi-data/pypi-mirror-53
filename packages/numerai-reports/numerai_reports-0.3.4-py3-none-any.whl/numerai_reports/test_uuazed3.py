import tabulate
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


import data
import reports
import leaderboard



mails = {
         151: {'nmr_total': 0.12, 'usd_total': 2.22},
         152: {'nmr_total': 1.97, 'usd_total': 5.87},
         153: {'nmr_total': -0.05, 'usd_total': 0.0,
               'nmr_staked': 1.3, 'nmr_rep_bonus': 0.2,
               'nmr_burned': 0.25},
         154: {'nmr_total': -0.42, 'usd_total': 0.28,
               'nmr_rep_bonus': 0.1, 'nmr_staked': 2.6,
               'nmr_burned': 0.59},
         155: {'nmr_total': -0.21, 'usd_total': 1.1},
         156: {'nmr_total': -0.62, 'usd_total': 0.89},
         157: {'nmr_total': -1.17, 'usd_total': 0.37,
               'nmr_burned': 1.36, 'nmr_rep_bonus': 0.1},
         158: {'nmr_total': -0.68, 'usd_total': 0},
         159: {'nmr_total': -1.16, 'usd_total': 0},
         160: {'nmr_total': -0.23, 'usd_total': 0.28},
         161: {'nmr_total': 0.66, 'usd_total': 2.32},
         162: {'nmr_total': 0.93, 'usd_total': 3.95},
         163: {'nmr_total': 0.8, 'usd_total': 3.38},
         164: {'nmr_total': 0.48, 'usd_total': 2.15}
        }

for round_num, values in mails.items():
    df = reports.payments('uuazed3', round_num)
    results = []
    count = 0

    for metric, value in values.items():
        report_val = df.loc[round_num][metric]
        count += report_val != value
        results.append([metric, value, report_val, report_val == value])

    if count > 0:
        print(f"======== {round_num} =======")
        print(df)
        print(tabulate.tabulate(results, headers=['metric', 'target', 'numerai_reports', 'same']))


df = leaderboard.Leaderboard()[157]
print(df[df.username=="uuazed3"])
