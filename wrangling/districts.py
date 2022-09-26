from collections import defaultdict
from csv import DictReader, DictWriter
import heapq

kHEADER = ["DISTRICT", "MARGIN"]

def compute_margin(scores_list):
    """
    return the margin (the larges number - the second larges number)
    """
    scores_list.sort() # sorting the list 

    if len(scores_list) <= 1 :
        return 100.0

    return scores_list[-1] - scores_list[-2]


def district_margins(state_lines):
    """
    Return a dictionary with districts as keys, and the difference in
    percentage between the winner and the second-place as values.

    @lines The csv rows that correspond to the districts of a single state
    """

    scores_list = []
    state_dict = {}
    last_d  = None
    for line in state_lines:
        if not (line["D"] == "H" or " - " in line["D"] or line['GENERAL %'] ==''):
            if last_d != line['D']:
                #save the last one
                if last_d != None:
                    state_dict[int(last_d)] = compute_margin(scores_list)
                last_d = line['D']
                scores_list = []

            scores_list.append(float(line['GENERAL %'][:-1].replace(',', '.')))

    #save the last one
    if last_d != None:
        state_dict[int(last_d)] = compute_margin(scores_list)



    # Complete this function
    # return dict((int(x["D"]), 25.0) for x in state_lines if x["D"] and
                # not (x["D"] == "H" or " - " in x["D"]))
    return state_dict

def all_states(lines):
    """
    Return all of the states (column "STATE") in list created from a
    CsvReader object.  Don't think too hard on this; it can be written
    in one line of Python.
    """

    states_list = []
    last_state = None
    for line in lines:
        if last_state != line['STATE']:
            last_state = line['STATE']
            states_list.append(last_state)

    # states_list = []
    # last_state = None
    # jumb = 20
    # steps= 0
    # i = 0
    # while i < len(lines):
    #     if last_state == lines[i]['STATE']:

    #     if last_state != lines[i]['STATE']:
    #         last_state = lines[i]['
    #         states_list.append(last_state)

    #     i =+ jumb

    # Complete this function
    return set(states_list)

def all_state_rows(lines, state):
    """
    Given a list of output from DictReader, filter to the rows from a single state.

    @state Only return lines from this state
    @lines Only return lines from this larger list
    """

    # Complete/correct this function
    for line in lines:
        if line['STATE'] == state:
            yield line

if __name__ == "__main__":
    # You shouldn't need to modify this part of the code
    lines = list(DictReader(open("../data/2014_election_results.csv")))
    output = DictWriter(open("district_margins.csv", 'w'), fieldnames=kHEADER)
    output.writeheader()

    summary = {}
    with open("train.csv", 'w') as train_file, \
         open("sub.csv", 'w') as sub_file:
      train = DictWriter(train_file, fieldnames=kHEADER)
      key = DictWriter(sub_file, fieldnames=kHEADER)
    
      train.writeheader()
      key.writeheader()

      for state in all_states(lines):
        state_districts = list(all_state_rows(lines, state))
        margins = district_margins(state_districts)

        for ii in margins:
            summary[(state, ii)] = margins[ii]

      for ii, mm in sorted(summary.items(), key=lambda x: x[1]):
        if ii[0] in ["Texas", "Arizona", "Maryland"]:
            train.writerow({"DISTRICT": "%s %i" % (ii[0], ii[1]), "MARGIN": mm})
        else:
            key.writerow({"DISTRICT": "%s %i" % (ii[0], ii[1]), "MARGIN": mm})
