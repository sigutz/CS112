import prep


def prep_band(fband):
    band = []
    for line in fband:
        for c in line.strip().split():
            band.append(c)
    return band


def prep_states(fstate):
    states = []
    init_state = None
    fin_states = []
    for state in fstate:
        state = state.strip()
        if '-' in state:
            st, tip = state.split('-', maxsplit=1)
            states.append(st.strip())
            if tip == 'initial':
                if init_state is None:
                    init_state = st.strip()
                else:
                    print(f"Error: Multiple initial states found: {init_state} and {st}.")
                    return None, None, None
            elif tip == 'accept':
                fin_states.append(st.strip())
        else:
            states.append(state)
    return states, init_state, fin_states


def prep_symbols(fsymbols):
    symbols = []
    for line in fsymbols:
        for symbol in line.strip().split(','):
            symbol = symbol.strip()
            if symbol and symbol not in symbols:
                symbols.append(symbol)
    return symbols if symbols else None


def prep_transitions(ftransitions):
    transitions = []
    for transition in ftransitions:
        try:
            inp, rez = transition.split('>')
            in_state, symbol = inp.split('&')
            parts = rez.split(',')
            if len(parts) != 3:
                print(f"Error: Transition must have format: state & symbol > next_state, write, direction")
                return None
            next_state, write_symbol, turn = parts
            transitions.append((
                in_state.strip(),
                symbol.strip(),
                next_state.strip(),
                write_symbol.strip(),
                turn.strip()
            ))
        except ValueError:
            print(f"Error: Invalid transition format: {transition}")
            return None
    return transitions


def prep_turing(fturing):
    files = prep.prep_file(fturing)
    if not files:
        print("Error: No data found in the file.")
        return None
    turing = {}
    for cap in files.keys():
        if cap.upper() == "SYMBOLS":
            turing["symbols"] = prep_symbols(files[cap])
            if turing["symbols"] is None:
                return None
        elif cap.upper() == "STATES":
            result = prep_states(files[cap])
            if result[0] is None:
                return None
            turing["states"], turing["init_state"], turing["fin_states"] = result
        elif cap.upper() == "TRANSITIONS":
            turing["transitions"] = prep_transitions(files[cap])
            if turing["transitions"] is None:
                return None
        elif cap.upper() == "BAND":
            turing["band"] = prep_band(files[cap])
            if not turing["band"]:
                print("Error: Band cannot be empty.")
                return None
    return turing


def find_transition(turing, current_state, symbol):
    for transition in turing["transitions"]:
        if transition[0] == current_state and transition[1] == symbol:
            return transition
    return None


def run_tm(ftm):
    turing = prep_turing(ftm)
    if not turing:
        return None, None

    current_state = turing["init_state"]
    current_band = turing["band"].copy()
    pos = 0
    steps = 0
    max_steps = 1000

    print(f"Initial state: {current_state}")
    print(f"Initial band: {current_band}")
    print(f"Accept states: {turing['fin_states']}")

    while current_state not in turing["fin_states"] and steps < max_steps:

        symbol = current_band[pos]
        transition = find_transition(turing, current_state, symbol)

        if transition is None:
            print(f"No transition found for state '{current_state}' and symbol '{symbol}'")
            print("REJECTED")
            return current_band, current_state

        _, _, next_state, write_symbol, turn = transition

        current_band[pos] = write_symbol

        current_state = next_state

        if turn == 'R':
            pos += 1
        elif turn == 'L':
            pos -= 1
        elif turn == 'S':
            pass
        else:
            print(f"Error: Invalid turn direction '{turn}'.")
            return None, None

        steps += 1
        print(f"Step {steps}: State={current_state}, Pos={pos}, Band={''.join(current_band)}")

    if current_state in turing["fin_states"]:
        print("ACCEPTED")
    else:
        print(f"TIMEOUT after {steps} steps")

    return current_band, current_state
