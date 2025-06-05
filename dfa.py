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
        if state.find('-')!=-1:
            st,tip=state.split('-', maxsplit=1)
            states.append(st)
            if tip == 'initial':
                if init_state==None:
                    init_state = st
                else:
                    print(f"Error: Multiple initial states found: {init_state} and {st}.")
                    return None
            elif tip == 'accept':
                fin_states.append(st)
        else:
            states.append(state.strip())

    if init_state==None or len(fin_states)==0:
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

def prep_dfa(fdfa):
    files=prep.prep_file(fdfa)
    if not files:
        print("Error: No data found in the file.")
        return None
    dfa={}
    for cap in files.keys():
        if cap.upper()=="SYMBOLS":
            dfa["symbols"] = prep_symbols(files[cap])
            if dfa["symbols"] is None:
                return None
        elif cap.upper()=="STATES":
            states, init_state, fin_states = prep_states(files[cap])
            if states is None:
                return None
            dfa["states"] = states
            dfa["init_state"] = init_state
            dfa["fin_states"] = fin_states
        elif cap.upper()=="TRANSITIONS":
            dfa["transitions"] = prep_transitions(files[cap])
            if dfa["transitions"] is None:
                return None
    return dfa

def check_dfa(dfa):
    for t in dfa["transitions"]:
        if t[0] not in dfa["states"]:
            print(f"Error: Transition from non-existing state {t[0]}.")
            return False
        if t[1] not in dfa["symbols"]:
            print(dfa["symbols"],t[1])
            print(f"Error: Transition with non-existing symbol {t[1]}.")
            return False
        if t[2] not in dfa["states"]:
            print(f"Error: Transition to non-existing state {t[2]}.")
            return False
    return True

def next_state(dfa, current_state, symbol):
    for t in dfa["transitions"]:
        if t[0] == current_state and t[1] == symbol:
            return t[2]
    return None

def run_dfa(fdfa):
    dfa= prep_dfa(fdfa)
    if check_dfa(dfa):
        print("Select the mod you want to use:")
        print("1. Check a string")
        print("2. Check character by character")
        mode = input("Enter 1 or 2: ")
        while mode not in ["1", "2"]:
            print("Invalid choice. Please enter 1 or 2.")
            mode = input("Enter 1 or 2: ")
        if mode == "1":
            string = input("Enter a string to check: ")
            current_state = dfa["init_state"]
            for symbol in string.split():
                if symbol not in dfa["symbols"]:
                    print(f"Error: Symbol '{symbol}' not recognized.")
                    return
                next_st = next_state(dfa, current_state, symbol)
                if next_st is None:
                    print(f"No transition from state '{current_state}' with symbol '{symbol}'.")
                    return
                print(f"Transitioning from state '{current_state}' to '{next_st}' with symbol '{symbol}'.")
                current_state = next_st
            if current_state in dfa["fin_states"]:
                print(f"The string '{string}' is accepted by the DFA.")
            else:
                print(f"The string '{string}' is not accepted by the DFA. Ended in state '{current_state}'.")
        elif mode == "2":
            current_state = dfa["init_state"]
            while True:
                print(f"Current state: {current_state}")
                print("Available transitions:")
                for t in dfa["transitions"]:
                    if t[0] == current_state:
                        print(f"  {t[0]} + {t[1]} > {t[2]}")
                symbol = input("Enter a symbol to proceed (or type 'exit' to quit): ")
                if symbol.lower() == "exit":
                    break
                if symbol not in dfa["symbols"]:
                    print(f"Error: Symbol '{symbol}' not recognized.")
                    continue
                next_st = next_state(dfa, current_state, symbol)
                if next_st is None:
                    print(f"No transition from state '{current_state}' with symbol '{symbol}'.")
                    continue
                print(f"Transitioning from state '{current_state}' to '{next_st}' with symbol '{symbol}'.")
                current_state = next_st
                if current_state in dfa["fin_states"]:
                    print(f"Current state '{current_state}' is an accepting state.")
                else:
                    print(f"Current state '{current_state}' is not an accepting state.")
            if current_state in dfa["fin_states"]:
                print(f"Ended in accepting state '{current_state}'.")
            else:
                print(f"Ended in non-accepting state '{current_state}'.")

