import csv
import datetime
ATT_STRING = "\n@ATTRIBUTE"
NUMER = "NUMERIC"
T_F_String = "{True, False}"
ATTENTION_LEVEL_THRESHOLD = 51

with open("sample_blinking_data.arff", 'w') as blinking_data:
    blinking_data.write('@RELATION blinking\n')
    blinking_data.write(f'{ATT_STRING} frames_since_experiment_started {NUMER}')
    blinking_data.write(f'{ATT_STRING} frames_since_the_last_blink {NUMER}')
    blinking_data.write(f'{ATT_STRING} is_blink {NUMER}')
    blinking_data.write(f'{ATT_STRING} attention_level {T_F_String}')
    blinking_data.write("\n@DATA")
    for student_index in range(1, 12):
        with open(
                f"../mEBAL_database/Webcams-EEG (User 1-11)/Webcams-EEG (User 1-11)/User {str(student_index)}/StudentData/StudentData.csv") as stud_data:
            stud_reader = csv.DictReader(stud_data, delimiter=' ')
            for row in stud_reader:
                start = row["Start_the_exam"].split(':')
                end = row["End_of_exam"].split(':')
                date = row["Exam_day_is"].split('-')
                start_day_time = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(start[0]),
                                                   int(start[1]),
                                                   int(start[2].split('.')[0]), int(start[2].split('.')[1][:-3]))
                end_day_time = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(end[0]), int(end[1]),
                                                 int(end[2].split('.')[0]), int(end[2].split('.')[1][:-3]))
                duration = end_day_time - start_day_time
                #  read attention data
                with open(
                        f"C:/Users/Polina/Documents/Studies/Final Project/Alert Fatigue/mEBAL_database/Webcams-EEG (User 1-11)/Webcams-EEG (User 1-11)/User {str(student_index)}/MindWave/file_ATT.csv") as attention_file:
                    att_reader = csv.DictReader(attention_file, delimiter=' ')
                    attention_dictionary = {}
                    for row in att_reader:
                        date = row['Date'].split('/')
                        hour = row['Hour'].split(':')
                        attention_level = int(row['ATT'])
                        time_diff = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(hour[0]),
                                                      int(hour[1]),
                                                      int(hour[2]), int(hour[3])) - start_day_time
                        seconds_diff = time_diff.total_seconds()
                        frame = int(seconds_diff // 0.033)
                        #  print(frame)
                        attention_dictionary[frame] = attention_level
                # print(attention_dictionary)
        #  read blinks data
        with open(
                f"C:/Users/Polina/Documents/Studies/Final Project/Alert Fatigue/mEBAL_database/Eye Blinks/Eye Blinks/User {str(student_index)}/Blink/Right_Blink.csv") as blink_db:
            blink_reader = csv.reader(blink_db, delimiter=' ')
            blinks_list = []
            last_blink_frame = 0
            # print(blink_reader)
            for row in blink_reader:
                if row[0] != 'Start_Blink' and len(row) == 3:
                    print(row)
                    if row[2] == '1':
                        last_blink_frame = int(((int(row[1]) + int(row[0])) / 2) - last_blink_frame)
                    blinks_list.append([int(row[0]), int(row[1]), int(row[2]), last_blink_frame])
                    # start_frame = int(row[0])
                    # end_frame = int(row[0])
                    # blink = row([2])
            #print(blinks_list)
            last_blink = 0
        for key in attention_dictionary:
            curr_str = "\n"
            found = False

            for bl_data in blinks_list:
                if (bl_data[0] <= key <= bl_data[1]):
                    curr_str = f'\n{str(key)},{bl_data[3]},{bl_data[2]},{attention_dictionary[key]>=ATTENTION_LEVEL_THRESHOLD}'
                    found = True
                    blinking_data.write(curr_str)
                    last_blink = bl_data[3]
                    # print(last_blink)
                    break
            if not found:
                curr_str = f'\n{str(key)},{last_blink+key},0,{attention_dictionary[key]>=ATTENTION_LEVEL_THRESHOLD}'
                blinking_data.write(curr_str)


