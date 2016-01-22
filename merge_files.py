import csv

# Merges two files together
# File 1 is the first 1 in chronological order

file1 = 'rm env sensortag_output_20160113234009 Humidity(rH) rm env sensortag_output_20160114201706 Humidity(rH) rm env sensortag_output_20160116124758 Humidity(rH)'
file2 = "rm env sensortag_output_20160117180352 Humidity(rH)"


if __name__ == '__main__':

    output_fp = open(file1 + " " + file2 + ".csv", 'wb')
    input1_fp = open(file1 + ".csv", 'rb')
    input2_fp = open(file2 + ".csv", 'rb')

    output = csv.writer(output_fp)
    input1 = csv.reader(input1_fp)
    input2 = csv.reader(input2_fp)

    for row1 in input1:
        output.writerow(row1)

    for row2 in input2:
        output.writerow(row2)

print "File " + file1 + " " + file2 + ".csv created"