
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


import data
import reports



df = reports.retroactive_stake_bonus()
print(df)
exit


reports.all_star_club(162)
reports.out_of_n(160, 162)
reports.summary(162, 163)
reports.dominance("uuazed", 162)
reports.friends("uuazed", 162)
reports.reputation_bonus(162)
reports.reputation("uuazed", 162)
reports.pass_rate(162)


#print(reports.all_star_club(160))

#exit()

#lb = data.fetch_leaderboard(142, 161)
#print(reports.friends(lb, "uuazed"))

#exit(

start = 150
end = 163


print("uuazed")
print(reports.payments(['uuazed'], start, end))
print("uuazed2")
print(reports.payments(['uuazed2'], start, end))
print("uuazed3")
print(reports.payments(['uuazed3'], start, end))
print("uuazed account")
print(reports.payments(['uuazed', 'uuazed2', 'uuazed3'], start, end))
print("anna accounts")
print(reports.payments(['anna1', 'anna2', 'anna3'], start, end))
print("all")
print(reports.payments(['uuazed', 'uuazed2', 'uuazed3', 'anna1', 'anna2', 'anna3'], start, end))


reports.reputation_bonus(end).to_csv("rep.csv")
