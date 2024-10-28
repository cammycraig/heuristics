import operator

# Foreign Key, Auth Code, Number, Primary Key, Heuristic Number, Heuristic, Description
DATA_FILE = "C:/Users/camer/OneDrive/Desktop/data.txt"
OUTPUT_FILE = "C:/Users/camer/OneDrive/Desktop/output.csv"

data = {}

with open(DATA_FILE, "r", encoding="utf8") as data_input:
    
    lines = data_input.readlines()
    reference_line = lines[0].strip().split("   ")

    for line_index in range(1, len(lines)):
        line = lines[line_index]
        items = line.strip().split("   ")
        
        data[items[3]] = {
            "Auth Code": items[1],
            "User Heuristic Number": items[2],
            "Heuristic Number": items[4],
            "Heuristic": items[5],
            "Description": items[6],
            "Foreign Key": items[0]
        }

'''
ex:
1: ["CC", "MD"] 
'''
heuristics = {}

for primary_key, entry_dictionary in data.items():
    foreign_key = entry_dictionary["Foreign Key"]
    if foreign_key in heuristics:
        auth_code = entry_dictionary["Auth Code"]
        if auth_code not in heuristics[foreign_key]:
            heuristics[foreign_key].append(auth_code)
    else:
        heuristics[foreign_key] = [entry_dictionary["Auth Code"]]

reviewer_success = {}

for heuristic_key, reviewers in heuristics.items():
    for reviewer in reviewers:
        if reviewer in heuristics[heuristic_key]:
            if reviewer in reviewer_success:
                reviewer_success[reviewer]["count"] += 1
                reviewer_success[reviewer]["heuristics"].append(heuristic_key)
            else:
                reviewer_success[reviewer] = {
                    "count": 1,
                    "heuristics": [heuristic_key]
                }

# find an array of unique reviewers, the numbers of successes each has, and their corresponding row
reviewers = []
successes = []
lines = []

for reviewer, reviewer_data in reviewer_success.items():
    line_data = []
    for heuristic_key in heuristics.keys():
        if heuristic_key in reviewer_data["heuristics"]:
            line_data.append("T")
        else:
            line_data.append("F")
    lines.append(line_data)
    if reviewer not in reviewers:
        reviewers.append(reviewer)
        successes.append(reviewer_data["count"])

# ALL GOOD

# sort each row by increasing corresponding reviewer count
lines_sorted = []

heuristic_numbers = heuristics.keys()
heuristic_successes_original = [len(reviewers) for heuristic_nums, reviewers in heuristics.items()]

heuristic_numbers_sorted = [k for k, v in sorted(zip(
    heuristic_numbers,
    heuristic_successes_original
), key=operator.itemgetter(1))]

# heuristic_successes_sorted, heuristic_numbers_sorted = zip(*sorted(zip(heuristic_successes_original,
#                                                                        heuristic_numbers)))

for line in lines:
    line_sorted = [k for k, v in sorted(zip(
        line,
        heuristic_successes_original
    ), key=operator.itemgetter(1))]
    # heuristic_successes_sorted, line_sorted = zip(*sorted(zip(heuristic_successes_original, line)))
    lines_sorted.append(",".join(line_sorted))

lines = lines_sorted

successes, reviewers, lines = zip(*sorted(zip(successes, reviewers, lines), reverse=False))

lines_labeled = []
for line_index in range(len(lines)):
    lines_labeled.append(lines[line_index] + "," + reviewers[line_index])

for number_index in range(len(heuristic_numbers_sorted)):
    if len(heuristic_numbers_sorted[number_index]) == 1:
        heuristic_numbers_sorted[number_index] = "0" + heuristic_numbers_sorted[number_index]
lines_labeled.append(",".join(heuristic_numbers_sorted))
lines_labeled.append("Hard Easy")
lines_labeled[0] += ",Successful Unsuccessful"

chart = "\n".join(lines_labeled)

with open(OUTPUT_FILE, "w") as output_file:
    output_file.write(chart)
    



    
