import csv

# open the file in the write mode
def addToCSV(meetings):
    with open('./csvTest', 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerows(meetings)
