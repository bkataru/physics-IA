import csv

with open('hip2.dat') as input_file:
    newLines = []
    for line in input_file:
        newLine = [x.strip() for x in line.split('  ')]
        fixedNewLine = []
        for elem in newLine:
            if elem != '':
                for i in elem.split(' '):
                    fixedNewLine.append(i)
        newLines.append(fixedNewLine)

print(len(newLines))
with open('hip2.csv', 'w') as output_file:
    file_writer = csv.writer(output_file)
    file_writer.writerows(newLines)