import csv

file_name = 'sensortag_debug_20160110101356_1000lines'

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
            type1_ = row[1]
            type2_ = row[2]

            if type1_ in output_files:
                if type2_ in output_files[type1_]:
                    output = output_files[type1_][type2_][0]
                else:
                    output_fp = open(file_name+' %s %s.csv' % (type1_.replace(":",""), type2_.replace(":","")), 'wb')
                    output = csv.writer(output_fp)
                    output_files[type1_][type2_] = output, output_fp
            else:
                output_files[type1_] = {}
                output_fp = open(file_name+' %s %s.csv' % (type1_.replace(":",""), type2_.replace(":","")), 'wb')
                output = csv.writer(output_fp)
                output_files[type1_][type2_] = output, output_fp

            # Right the row in that file
            output.writerow(row)

            # Report progress
            nb += 1
            if nb % 10000 == 0:
                print("Processed %d lines, %.1f%%" % (
                      nb,
                      mixed_fp.tell() * 100 / filelen))

    # for _, output_fp in output_files.itervalues():
    #     output_fp.close()