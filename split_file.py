import csv

file_name = 'trial bathroom 12 hours sensortag_output_20160106230013'

if __name__ == '__main__':
    output_files = {}

    with open(file_name+'.csv', 'rb') as mixed_fp:
        # Measure the file
        mixed_fp.seek(0, 2)
        filelen = mixed_fp.tell()
        mixed_fp.seek(0, 0)

        # Read as CSV
        mixed = csv.reader(mixed_fp)
        for nb, row in enumerate(mixed):
            # Find the right output file for type type (second column)
            type_ = row[1]
            if type_ == 'Pressure()':
                row[2] = row[2].split(" ")[0]
            if type_ in output_files:
                output = output_files[type_][0]
            else:
                output_fp = open(file_name+' %s.csv' % type_, 'wb')
                output = csv.writer(output_fp)
                output_files[type_] = output, output_fp

            # Right the row in that file
            output.writerow(row)

            # Report progress
            nb += 1
            if nb % 100000 == 0:
                print("Processed %d lines, %.1f%%" % (
                      nb,
                      mixed_fp.tell() * 100 / filelen))

    for _, output_fp in output_files.itervalues():
        output_fp.close()