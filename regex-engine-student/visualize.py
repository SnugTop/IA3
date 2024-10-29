from fa import NFA, DFA, SUPPORTED_SYMBOLS
try:
    from automathon import NFA as VisualNFA
    __has_automathon = True
except ImportError:
    print("""The 'automathon' dependency is not installed.
        Please install it to use visualization
    """)
    has_automathon = False

def convert_transitions(fa):
    transitions = {}
    
    for state in fa.states:
        state_id = f"q{state.id}" 
        if state_id not in transitions:
            transitions[state_id] = {}

        for symbol, target_states in state.transitions.items():
            if symbol not in transitions[state_id]:
                transitions[state_id][symbol] = set()
            if isinstance(fa, NFA):
                transitions[state_id][symbol] = {f"q{target.id}" for target in target_states}
            elif isinstance(fa, DFA):
                transitions[state_id][symbol] = {f"q{target_states.id}"}
    
    return transitions


def convert_to_visual_fa(fa):    
    states = {f"q{state.id}" for state in fa.states}
    input_symbols = SUPPORTED_SYMBOLS
    transitions = convert_transitions(fa)
    initial_state = f"q{fa.start_state.id}"
    final_states = {f"q{state.id}" for state in fa.states if state.is_final}
    return VisualNFA(states, input_symbols, transitions, initial_state, final_states)