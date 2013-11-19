#!/usr/bin/env python
# -*- coding: utf-8
import argparse
import datetime

# Assign environment libraries
import sys
env='.\\BusBud\\Lib\\site-packages'
if env not in sys.path:
    sys.path.append(env)

#--------------------------------------------------------------
#File begins
	
import mechanize
from BeautifulSoup import BeautifulSoup 
import HTMLParser

class findForm:
	def __init__(self, url, fname):
		
		self.br.set_handle_robots(False) # ignore robots if allowed
		self.br.open(url)
		self.br.select_form(name=fname)
		
	def ini(self,url,fname):
		return self.__init__(url,fname)
	
	br = mechanize.Browser()
	
	def listf(self):
		a=""
		#List all form of the page
		for form in br.forms():
			a= a,"Form name:", form.name, "\n"
			a=a, form, "\n"
	
	def listc(self):
		a=""
		#List all controls of the form	
		for control in self.br.form.controls:
			if not(control.readonly):
				t="type=%s, name=%s value=%s \n" % (control.type, control.name, control.value)
				a=a+t
		return a
		
	def submit(self, fields):
		#Submit query to form		
		for q in fields:
			for control in self.br.form.controls:
				if not(control.readonly):
					if control.name==q:
						control.value = fields[q]
			
		res = self.br.submit()
		
		
		#Get URL
		self.newUrl=self.br.geturl()
		
		#Get content
		self.content = res.read()
		#with open("mechanize_results.html", "w") as f:
		#	f.write(content)
		return
	
def getPrice(url):
	#Visit page
	br = mechanize.Browser()
	br.set_handle_robots(False) # ignore robots if allowed
	brOpen=br.open(url)

	#Read page and parse
	brSoup = BeautifulSoup(brOpen.read())
	
	#Find form-specific HTML tags
	trs = brSoup.findAll(attrs={"class":"pickme"})
	
	price=[]
	
	#Find price tags (both refundable and non-refundable)
	for tr in trs:
		td=tr.find(attrs={'headers':'fare_noinsurance'})
		
		#prices are given in Pounds (and Euro available) --> need interpreter
		h = HTMLParser.HTMLParser()
		p=h.unescape(td.find(text=True))
		#u"\u20AC" (EURO)
		#u"\xA3" (Pound) also: &#163;
		
		price.append(p)

	return price
	



def parse_date(s):
    """Parse a date string

    Arguments:
    s -- Date as string in format: YYYY-MM-DD
    """
    return datetime.datetime.strptime(s, '%Y-%m-%d')


def today(offset=0):
    """Get today's date, with an optional offset

    Keyword arguments:
    offset -- offset the number of days to offset from today (default 0)
    """
    return datetime.date.today() + datetime.timedelta(days=offset)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Crawl web site.')
	parser.add_argument('--extract', required=True, choices=['stops', 'departures'],
                        help='the type of extraction to perform')
	parser.add_argument('--output', required=True, type=argparse.FileType('w'),
                        help='the path of the output file to generate')
	parser.add_argument('--startdate', required=False, type=parse_date, default=today(),
                        help='the beginning of the departure date range')
	parser.add_argument('--enddate', required=False, type=parse_date, default=today(7),
                        help='the end of the departure date range')

	args = parser.parse_args()
	
	content=[]

	if args.extract == 'stops':
		print 'Downloading stops to {}'.format(args.output)
		""" I ran into trouble trying to crawl pages returning value via javascript on the same page.  I didn't do this part and I had to do the departures in "accessible version" for the same reason. """
		
		#Fetch stops by inserting Zip Codes in the StopFinder
		# UK zipcodes: http://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting
		#postcodes area: http://en.wikipedia.org/wiki/List_of_postcode_areas_in_the_United_Kingdom
		
		#Elements can be fetched on the page http://coach.nationalexpress.com/nxbooking/stop-finder through the form 'stopfinderForm' by inserting areacodes of UK in the text input 'zipCode'
		#Fetch is executed on this element of the HTML tree: div id='stopListContainer'
		#All info (Long, Lat, Name, address(and indirectly the zipcode since we used it originally) can be found in the li class="contain"
		#Position and name: in the <a> onclick attribute (in the javascript code)
		#name and address : in the div class="address" (name in <h4>, address is <span>)
		
		#write to stops.json
		args.output.write('%s' % content)

		

	elif args.extract == 'departures':
		print 'Downloading departures to {0} for dates {1} through {2}'.format(
			args.output, args.startdate, args.enddate)
		
		#with open("stops.json", "r") as f:
		#	stops = f.read()
		
		#for all date inputs between .startdate and .enddate
		"""
		k=0
		while args.startdate+datetime.timedelta(days=k) <= args.enddate:
			k=k+1
			dd=datetime.date.day
			dm=datetime.date.month
			dy=datetime.date.year
			
			for d in stops
				for a in stops
				
				form1Args = {"fromc":[d[stop_name]],"toc":[a[stop_name]],"od":[dd],"om":[dm],"oy":[dy]} 
			...
		"""
		
		#Hard-Coded to have a functional code. The pseudo-code above shows how the code would work with inputs from stops.json
		#Bournemouth to Durham on Jan 1, 2013 (it's actually 2014, but the form has a typo online)
		form1Args = {"fromc":["65026"],"toc":["70022"],"od":["1"],"om":["01"],"oy":["2013"]} 
			
		#First form of Accessible View
		form1 = findForm('http://www.nationalexpress.com/home.aspx','staticBookingForm')
		form1.submit(form1Args)
		
		#Second form of Accessible View
		form2=findForm(form1.newUrl,'bookingForm')
		mainSoup = BeautifulSoup(form1.content)
		table=mainSoup.findAll(attrs={"class":'pickme'})
		
		#Select on of the itineraries
		for tr in table:
			tds=tr.findAll('td')
			#print tds[6:7]
			dt=tds[0].find(text=True)
			at=tds[1].find(text=True)
			dur=tds[2].find(text=True).split("\n")[0]
			connexions=tds[3].find(text=True)
			
			o=tds[8].find(attrs={"name":'oj'})
			oval= o.get('value')
			form2Args = {"oj":[oval], "uk_ad":["1"]} 
			form2.submit(form2Args)

			#fetch tickets price array 
			tpr = getPrice(form2.newUrl)
			form2.ini(form1.newUrl,'bookingForm') #reset browser to previous page
			
			#origin and destinations are hard-coded because stops.json doesn't exist
			content.append({'origin_stop':'Bournemouth','destination_stop':'Durham','departure_time':dt,'arrival_time':at,'duration':dur,'price':tpr})
			
		#write to departures.json
		args.output.write('%s' % content)
