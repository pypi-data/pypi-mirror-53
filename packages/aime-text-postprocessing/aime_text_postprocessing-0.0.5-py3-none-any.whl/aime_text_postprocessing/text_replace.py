from . import dictionary_db


def replace_str_with_dic(text, replace_dic):
    keys = replace_dic.keys()
    arr = sorted(keys, key=lambda element: (element[1], element[0]))  # sort coors ascending order
    leng = len(arr)
    result = text
    for i in range(leng):
        index = leng - 1 - i
        start, end = arr[index]
        r_val = replace_dic[(start, end)]
        result = result[:start] + r_val + result[end + 1:]
    return result


def find_nearest_interval_index(current_index, intervals):
    index = current_index - 1
    if index == -1:
        return -1
    start = intervals[current_index][0]
    while index >= 0:
        if intervals[index][1] < start:
            return index
        index -= 1
    return -1


def get_score_of_interval(interval, score_dic):
    if score_dic is None:
        return interval[1] - interval[0] + 1
    return score_dic[interval]


def get_longest_non_overlaping_intervals(intervals, score_dic=None):
    arr = sorted(intervals, key=lambda element: (element[1], element[0]))
    s = {}
    trace = {}
    trace[-1] = []
    s[-1] = 0
    arr_len = len(arr)
    for i in range(0, arr_len):
        nearest_index = find_nearest_interval_index(i, arr)
        temp_sol = s[nearest_index] + get_score_of_interval(arr[i], score_dic)
        if temp_sol > s[i - 1]:
            s[i] = temp_sol
            trace[i] = list(trace[nearest_index])
            trace[i].append(i)
        else:
            trace[i] = list(trace[i - 1])
            s[i] = s[i - 1]  # find the interval maximum index j such that arr[j].end < start
    result = []
    for key in trace[arr_len - 1]:
        result.append(arr[key])
    return result


def process_text(text, comp_rex, out_rex):
    rep_dic = {}
    text_lower = text.lower()
    for i in range(len(comp_rex)):
        regex_comp = comp_rex[i]
        output = out_rex[i]
        for match in regex_comp.finditer(text_lower):
            start = match.start()
            end = match.end() - 1
            grp_dic = match.groupdict()
            if len(grp_dic) > 0:
                keys = grp_dic.keys()
                grp_key = keys[0]
                start = match.start(grp_key)
                end = match.end(grp_key) - 1
                rep_dic[(start, end)] = output
            else:
                rep_dic[(start, end)] = output
    inters = rep_dic.keys()
    f_inters = get_longest_non_overlaping_intervals(inters)
    new_rep_dic = {}
    for inter in f_inters:
        new_rep_dic[inter] = rep_dic[inter]
        start, end = inter
        old = text[start: end + 1]
    f_text = replace_str_with_dic(text, new_rep_dic)
    return f_text


def replace_text(input_s):
    return process_text(input_s, dictionary_db.REPLY_REGEXS, dictionary_db.REPLY_OUT)
