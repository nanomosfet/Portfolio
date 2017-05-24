import xml.etree.ElementTree as ET

tree = ET.parse('CEN_D_THIRDPARTY_12345_CONSUMPTION_20151029_20151029131558_ESPI2-1_01-01.xml')
root = tree.getroot()

f = open('data_electric_usage.tsv', 'w')

f.write('TimeStamp	Usage\n')
for i in range(1, len(root[14][5][0])):
	f.write(root[14][5][0][i][1][1].text + '	' + root[14][5][0][i][2].text + '\n')

f.close()




