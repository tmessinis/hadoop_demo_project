import sys

def mapper():
    for line in sys.stdin:
        data = line.strip().split('\t')
        Vehicle, yr1999, yr2000, yr2001, yr2002, yr2003, yr2004, yr2005, yr2006, yr2007, yr2008, yr2009, yr2010, yr2011, yr2012, yr2013, yr2014, yr2015 = data
        print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\t{14}\t{15}\t{16}\t{17}'.format(Vehicle, yr1999, yr2000, yr2001, yr2002, yr2003, yr2004, yr2005, yr2006, yr2007, yr2008, yr2009, yr2010, yr2011, yr2012, yr2013, yr2014, yr2015))
        
mapper()