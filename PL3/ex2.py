import sys

if len(sys.argv) != 2:
    sys.exit("usage: " + sys.argv[0] + " <string>")
    
str_to_test = sys.argv[1]

freq_analysis_dict = {}
for s in str_to_test:
    if s in freq_analysis_dict:
        freq_analysis_dict[s] += 1
    else:
        freq_analysis_dict[s] = 1

print(freq_analysis_dict)