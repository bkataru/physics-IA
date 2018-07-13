import csv

with open('HIP_star.dat') as input_file:
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
with open('HIP_star.csv', 'w') as output_file:
    file_writer = csv.writer(output_file)
    file_writer.writerows(newLines)