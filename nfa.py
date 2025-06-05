import prep
def prep_symbols(fsymbols):
    symbols = []
    for line in fsymbols:
        for symbol in line.split(', '):
            symbol = symbol.strip()
            if symbol and symbol not in symbols:
                symbols.append(symbol)
    return symbols
def prep_states(fstates):
    states = []
    init_state = None
    fin_states = []
    for state in fstates:
        if state.find('-') != -1:
            st, tip = state.split('-', maxsplit=1)
            states.append(st)
            if tip == 'initial':
                if init_state is None:
                    init_state = st
                else:
                    print(f"Error: Multiple initial states found: {init_state} and {st}.")
                    return None
            elif tip == 'accept':
                fin_states.append(st)
        else:
            states.append(state.strip())

    if init_state is None or len(fin_states) == 0:
        print("Error: Initial state or final states are not defined.")
        return None

    return states, init_state, fin_states

def prep_transitions(ftransitions):
    transitions = []
    for transition in ftransitions:
        try:
            inp, rez = transition.split('>')
            in_state, symbol = inp.split('+')
            transitions.append((in_state.strip(), symbol.strip(), rez.strip()))
        except ValueError:
            print(f"Error: Invalid transition format: {transition}")
            return None
    return transitions

def prep_nfa(fnfa):
    files = prep.prep_file(fnfa)
    if not files:
        print("Error: No data found in the file.")
        return None
    nfa = {}
    for cap in files.keys():
        if cap.upper() == "SYMBOLS":
            nfa["symbols"] = prep_symbols(files[cap])
            if nfa["symbols"] is None:
                return None
        elif cap.upper() == "STATES":
            nfa["states"], nfa["init_state"], nfa["fin_states"] = prep_states(files[cap])
            if nfa["states"] is None:
                return None
        elif cap.upper() == "TRANSITIONS":
            nfa["transitions"] = prep_transitions(files[cap])
            if nfa["transitions"] is None:
                return None
    return nfa
def check_nfa(nfa):
    for t in nfa["transitions"]:
        if t[0] not in nfa["states"]:
            print(f"Error: Transition from non-existing state {t[0]}.")
            return False
        if t[1] not in nfa["symbols"]:
            print(nfa["symbols"],t[1])
            print(f"Error: Transition with non-existing symbol {t[1]}.")
            return False
        if t[2] not in nfa["states"]:
            print(f"Error: Transition to non-existing state {t[2]}.")
            return False
    return True

def next_states(nfa, current_states, symbol):
    next_states = []
    for state in current_states:
        for transition in nfa["transitions"]:
            if transition[0] == state and transition[1] == symbol:
                next_states.append(transition[2])
    return next_states


def epsilon_closure(nfa, states):
    closure = set(states)
    stack = list(states)

    while stack:
        state = stack.pop()
        for transition in nfa["transitions"]:
            if transition[0] == state and transition[1] == 'epsilon':
                if transition[2] not in closure:
                    closure.add(transition[2])
                    stack.append(transition[2])

    return closure

def run_nfa(fnfa):
    nfa = prep_nfa(fnfa)
    if check_nfa(nfa):
        print("Select the mod you want to use:")
        print("1. Check a string")
        print("2. Check character by character")
        mode = input("Enter 1 or 2: ")
        while mode not in ["1", "2"]:
            print("Invalid choice. Please enter 1 or 2.")
            mode = input("Enter 1 or 2: ")

        current_states = list(epsilon_closure(nfa, [nfa["init_state"]]))

        if mode == "1":
            string = input("Enter a string: ")
            for symbol in string.split():
                if symbol not in nfa["symbols"]:
                    print(f"Error: Symbol '{symbol}' not recognized.")
                    return

            for symbol in string.split():
                next_st = next_states(nfa, current_states, symbol)
                if not next_st:
                    print(f"No transition from states {current_states} with symbol '{symbol}'.")
                    return
                print(f"Transitioning from states {current_states} to {next_st} with symbol '{symbol}'.")
                current_states = list(epsilon_closure(nfa, next_st))

            if any(state in nfa["fin_states"] for state in current_states):
                print(f"The string is accepted by the NFA, ending in states: {current_states}.")
            else:
                print(f"The string is not accepted by the NFA, ending in states: {current_states}.")
        else :
            while True:
                print(f"Current states: {current_states}")
                print("Available transitions:")
                for t in nfa["transitions"]:
                    if t[0] in current_states:
                        print(f"  {t[0]} + {t[1]} > {t[2]}")
                symbol = input("Enter a symbol to proceed (or type 'exit' to quit): ")
                if symbol.lower() == "exit":
                    break
                if symbol not in nfa["symbols"]:
                    print(f"Error: Symbol '{symbol}' not recognized.")
                    continue
                next_st = next_states(nfa, current_states, symbol)
                if not next_st:
                    print(f"No transition from states {current_states} with symbol '{symbol}'.")
                    continue
                print(f"Transitioning from states {current_states} to {next_st} with symbol '{symbol}'.")
                current_states = list(epsilon_closure(nfa, next_st))
                if any(state in nfa["fin_states"] for state in current_states):
                    print(f"Current states {current_states} include accepting states.")
                else:
                    print(f"Current states {current_states} do not include accepting states.")
            if any(state in nfa["fin_states"] for state in current_states):
                print(f"Ending in accepting states: {current_states}.")
            else:
                print(f"Ending in non-accepting states: {current_states}.")



