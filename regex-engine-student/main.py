#main.py
import sys
from regex import parse_regex 
from fa import NFA, DFA
try:
    from visualize import convert_to_visual_fa
    __has_visual_fa = True

except ImportError:
    print("We won't be able to visualize the NFA")
    __has_visual_fa = False

from test import test_regexpr_str, test_nfa, test_dfa

def print_usage_and_exit():
    print("""Usage:
              python3 main.py test <x>
                  Run tests up to part x:
                    1 - test_regexpr_str
                    2 - test_regexpr_str, test_nfa
                    3 - test_regexpr_str, test_nfa, test_dfa
                    Example: python3 main.py test 3

              python3 main.py visual {nfa|dfa} <regex>
                  Generate and visualize an NFA or DFA from the provided regex.
                  Example: python3 main.py visual nfa "a*ba"
            """)
    sys.exit(1)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print_usage_and_exit()

    if args[0] == "test":
        if "1" in args[1:]:
            test_regexpr_str()
        elif "2" in args[1:]:
            test_regexpr_str()
            test_nfa()
        elif "3" in args[1:]:
            test_regexpr_str()
            test_nfa()
            test_dfa()
        else:
            print_usage_and_exit()

    elif args[0] == "visual" and __has_visual_fa:
        try:
            if len(args) != 3:
                print_usage_and_exit()
                
            fa_type, regex_str = args[1], args[2]
            parsed_regex = parse_regex(regex_str)
            if fa_type == "nfa":
                nfa = NFA.from_regex(parsed_regex)
                visual_nfa = convert_to_visual_fa(nfa)
                visual_nfa.view("NFA_Visualization " + regex_str)

            elif fa_type == "dfa":
                nfa = NFA.from_regex(parsed_regex)
                dfa = DFA.from_nfa(nfa)
                visual_nfa = convert_to_visual_fa(nfa)
                visual_nfa.view("NFA_Visualization " + regex_str)
                visual_dfa = convert_to_visual_fa(dfa)
                visual_dfa.view("DFA_Visualization " + regex_str)
            else:
                print_usage_and_exit()

        except Exception as e:
            print("Problem with visualizing the automata, supressing stacktrace")
            print(e)

    else:
        print_usage_and_exit()

