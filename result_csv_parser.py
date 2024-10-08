import csv

statistic_list = []
files_endings_list = ['bayes', 'functions', 'lazy', 'meta', 'misc', 'rules', 'trees']
for file in files_endings_list:
    with open(f"learning_results_{file}.csv") as results_csv:
        results_dict = csv.DictReader(results_csv)
        for entry in results_dict:
            statistic_list.append([entry['Percent_incorrect'], entry['Key_Scheme']])

statistic_list.sort(key=lambda x: x[0])
no_duplicates_list = []
additional_list = []
for line in statistic_list:
        #  print(line[1])
    if line[1] not in additional_list:
        no_duplicates_list.append(line)
        additional_list.append(line[1])
with open('best_algorithms.csv', 'w') as res:
    for any in no_duplicates_list:
        print(f'{any[0]} {any[1]}')


