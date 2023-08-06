import xlrd
from pylab import *

def readExcel(file_name):
    ''' it reads excel files
    '''
    workbook=xlrd.open_workbook(file_name)

    sheet1=workbook.sheets()[0]

    data=[]

    for i in xrange(sheet1.nrows):
        data.append(sheet1.row_values(i))
    
        return data


def get_column(data,col):
    result=[]
    for row in data:
        result.append(row[col])
    return result

def plotData(data):
    yield_data=[]

    process=get_column(data,2)[4:20]

    yield_data=get_column(data,6)[4:20]



    plot(yield_data,'ro-')
    ylim(0.7, 1.1)
    show()
	
	
def plotBarData(data1,data2,ylabel,title):
	# cakemix.plotBarData(['Python','C+',"java","Perl","scala","lisp"],[10,8,6,4,5,1],'Usage','programming language')
	import numpy as np
	import matplotlib .pyplot as plt

	#data1=['Python','C+',"java","Perl","scala","lisp"]

	#data2=[10,8,6,4,2,1]

	plt.bar(data1,data2,alpha=0.5)
	#plt.ylabel('Usage')
	plt.ylabel(ylabel)
	#plt.title('programming language usage')
	plt.title(title)
	plt.show()

def plotLineData(data1,xlabel,ylabel,title):
	# cakemix.plotLineData([1, 2, 4, 8, 16, 32, 64, 128, 256],'model','xlabel','variance')
	from matplotlib import pyplot as plt
	data = [i for i, _ in enumerate(data1)]
	plt.plot(data, data1,     'g-',  label='variance') 
	plt.xlabel(xlabel)
	plt.ylabel(ylabel) 	
	plt.title(title) 
	plt.show()

def plotScatterData(data1,data2,labels,xlabel,ylabel,title):
	# cakemix.plotScatterData([70,65,72, 63, 71, 64, 60, 64, 67],[175,170,205,120,220,130,105,145,190],['a','b','c','d','e','f','g','h','i'],'# of Friends','daily minutes spent on the site','Daily Minutes vs Number of Friends')
	from matplotlib import pyplot as plt

	friends = [70,65,72, 63, 71, 64, 60, 64, 67]
	minutes = [175,170,205,120,220,130,105,145,190]

	labels = ['a','b','c','d','e','f','g','h','i']

	plt.scatter(data1,data2)
	for label, data1_count, data2_count in zip(labels, data1, data2):
		plt.annotate(label,xy=(data1_count,data2_count),xytext = (5,-5),textcoords='offset points')

	plt.title('Daily Minutes vs Number of Friends')
	plt.xlabel('# of Friends')
	plt.ylabel('daily minutes spent on the site')
	
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.show()
	
def plotHistData(data,label,title):
	import matplotlib.pyplot as plt
	plt.hist(data,10, histtype='bar', align='mid',color='c',label=label,edgecolor='black')
	plt.legend()
	plt.title(title)
	plt.show()

	