import csv

# Merges two files together
# File 1 is the first 1 in chronological order

#file1 = 'rm env sensortag_output_20160113234009 Humidity(rH) rm env sensortag_output_20160114201706 Humidity(rH) rm env sensortag_output_20160116124758 Humidity(rH)'
#file2 = "rm env sensortag_output_20160117180352 Humidity(rH)"
directory = 'New data/Bathroom/'
list_files = ["sensortag_datacapture_20160405233159", "sensortag_datacapture_20160406113249", "sensortag_datacapture_20160406233325",
              "sensortag_datacapture_20160407113407", "sensortag_datacapture_20160407233459", "sensortag_datacapture_20160408113530",
              "sensortag_datacapture_20160408233627", "sensortag_datacapture_20160409113645"]

list_ = [directory + file for file in list_files]

file_out = 'New data/merged/bathroom/20160405233159 to 20160409113645'

if __name__ == '__main__':
    output_fp = open(file_out + ".csv", 'wb')
    output = csv.writer(output_fp)

    for file in list_:
        print file
        input_fp = open(file + ".csv", 'rb')
        input = csv.reader(input_fp)

        for row in input:
                output.writerow(row)


print "File " + file_out + ".csv created"