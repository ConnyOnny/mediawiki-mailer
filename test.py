import table

with table.openWriter("test.csv") as writer:
	writer.writerow({"name":"Mensch Meyer","email":"mensch@meyer.com"})
	writer.writerow({"name":"Mänßch Diéter","email":"mensch@dieter.com"})

with table.openAppender("test.csv") as appender:
	appender.writerow({"name":"Mensch Dreyer","email":"dreyer@meyer.com"})

for entry in table.MailTable("test.csv"):
	print(entry)