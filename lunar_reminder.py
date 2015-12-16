#!/usr/bin/env python
# encoding: utf8

import getopt,sys,re,datetime
import lunar

def main():
	try:
		optlist, args = getopt.getopt(sys.argv[1:], "hd:n:p:s:D:", ["help", "date=", "number=", "location=", "summary=", "description="])
	except getopt.GetoptError as err:
		print >> sys.stderr, str(err)
		usage()
		sys.exit(2)
	
	date, number, location, summary, description, output = None, 1, "", "", "", None
	for o, a in optlist:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-d", "--date"):
			m = re.match(r"(\d{4})([-/.])(\d{1,2})\2(\d{1,2})", a)
			if not m:
				print >> sys.stderr, "错误的日期格式"
				sys.exit(1)
			else:
				date = (int(m.group(1)), int(m.group(3)), int(m.group(4)))
		elif o in ("-n", "--number"):
			number = int(a)
		elif o in ("-p", "--location"):
			location = a
		elif o in ("-s", "--summary"):
			summary = a
		elif o in ("-D", "--description"):
			description = a
	
	if not date:
		print >> sys.stderr, "必须指定起始农历日期，参数-d, --date=DATE"
		usage()
		sys.exit(1)
	if not summary:
		print >> sys.stderr, "必须指定概要信息，参数-s, --summary"
		usage()
		sys.exit(1)
	if len(args) > 0:
		try:
			output = open(args[0], "w")
		except IOError:
			print >> sys.stderr, "不能打开文件%s" % args[0]
	else:
		output = sys.stdout
			
	try:
		iCal(output, date, number, location, summary, description)
	finally:
		output.close()

def	iCal(output, date, number, location, summary, description):
	print >> output, "BEGIN:VCALENDAR"
	print >> output, "PRODID:-//Google Inc//Google Calendar 70.9054//EN"
	print >> output, "VERSION:2.0"
	
	for i in range(0, number):
		d = (date[0]+i, date[1], date[2])
		try:
			solar_dates = lunar.get_solar_date(*d)
			for solar_date in solar_dates:
				print >> output, "BEGIN:VEVENT"
				print >> output, "DTSTART;VALUE=DATE:" + solar_date.strftime("%Y%m%d")
				print >> output, "DTEND;VALUE=DATE:" + (solar_date+datetime.timedelta(1)).strftime("%Y%m%d")
				print >> output, "CLASS:PRIVATE"
				print >> output, "DESCRIPTION:" + format_text(description)
				print >> output, "LOCATION:" + format_text(location)
				print >> output, "SEQUENCE:0"
				print >> output, "STATUS:CONFIRMED"
				print >> output, "SUMMARY:" + format_text(summary)
				print >> output, "TRANSP:TRANSPARENT"
				print >> output, "END:VEVENT"
		except Exception as err:
			print >> sys.stderr, str(err)
	print >> output, "END:VCALENDAR"

def format_text(text):
	return text.replace("\n", "\\n")

def usage():
	print >> sys.stderr, """\
Usage: python lunar_reminder.py -d[npm] [output-file]
以iCal格式输出按年重复农历提醒信息，不指定输出文件时输出到标准输出

 -h, --help             输出此帮助信息
 -d, --date=DATE        指定起始农历信息，可以使用如下格式：
                          1980/2/25，1980-2-25，1980.2.25
 -n, --number=N         指定重复的年数，默认只重复一年
 -p, --location=LOC     指定事件的地点
 -s, --summary=MESG     指定事件概要信息
 -D, --description=DESC 指定事件描述信息
"""

if __name__ == "__main__":
	main()
