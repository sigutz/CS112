import prep


def prep_states(fstates):
    states = []
    init_state = None
    fin_states = []
    for state in fstates:
        if state.find('-') != -1:
            st, tip = state.split('-', maxsplit=1)
            states.append(st.strip())
            if tip == 'initial':
                if init_state is None:
                    init_state = st.strip()
                else:
                    print(f"Error: Multiple initial states found: {init_state} and {st}.")
                    return None
            elif tip == 'accept':
                fin_states.append(st.strip())
        else:
            states.append(state.strip())

    if init_state is None or len(fin_states) == 0:
        print("Error: Initial state or final states are not defined.")
        return None

    return states, init_state, fin_states


def prep_symbols(fsymbols):
    symbols = []
    for line in fsymbols:
        for symbol in line.split(', '):
            symbol = symbol.strip()
            if symbol and symbol not in symbols:
                symbols.append(symbol)
    return symbols if symbols else None


def prep_stack(fstack):
    stack = []
    for line in fstack:
        for item in line.split(', '):
            item = item.strip()
            if item and item not in stack:
                stack.append(item)
    return stack if stack else None


def prep_transitions(ftransitions):
    transitions = []
    for transition in ftransitions:
        try:
            inp, rez = transition.split('>')
            cond, symbol = inp.split('+')
            in_state, stack_top = cond.split('&')
            next_state, stack_push = rez.split(',', 1)
            stack_push = [s.strip() for s in stack_push.split()]
            transitions.append((in_state.strip(), stack_top.strip(), symbol.strip(), next_state.strip(), stack_push))
        except ValueError:
            print(f"Error: Transition {transition} is invalid.")
            return None
    return transitions


def prep_pda(fpda):
    files = prep.prep_file(fpda)
    if not files:
        print("Error: No data found in the file.")
        return None
    pda = {}
    for cap in files.keys():
        if cap.upper() == "SYMBOLS":
            pda["symbols"] = prep_symbols(files[cap])
            if pda["symbols"] is None:
                return None
        elif cap.upper() == "STATES":
            result = prep_states(files[cap])
            if result is None:
                return None
            pda["states"], pda["init_state"], pda["fin_states"] = result
        elif cap.upper() == "STACK":
            pda["stack"] = prep_stack(files[cap])
            if pda["stack"] is None:
                return None
        elif cap.upper() == "TRANSITIONS":
            pda["transitions"] = prep_transitions(files[cap])
            if pda["transitions"] is None:
                return None
        else:
            print(f"Warning: Unrecognized section '{cap}' in PDA file.")

    return pda


def check_pda(pda):
    for t in pda["transitions"]:
        if t[0] not in pda["states"]:
            print(f"Error: Transition from non-existing state {t[0]}.")
            return False
        if t[1] not in pda["stack"] and t[1] != "epsilon":
            print(pda["stack"], t[1])
            print(f"Error: Transition with non-existing stack top {t[1]}.")
            return False
        if t[2] not in pda["symbols"] and t[2] != "epsilon":
            print(f"Error: Transition with non-existing symbol {t[2]}.")
            return False
        if t[3] not in pda["states"]:
            print(f"Error: Transition to non-existing state {t[3]}.")
            return False
        for s in t[4]:
            print(t[4])
            if s not in pda["stack"] and s != "epsilon":
                print(f"Error: Transition with non-existing stack push {s}.")
                return False
    return True


def epsilon_closure(pda, states_with_stacks):
    closure = set()
    stack = list(states_with_stacks)

    while stack:
        current_state, current_stack = stack.pop()
        state_stack_key = (current_state, tuple(current_stack))

        if state_stack_key in closure:
            continue
        closure.add(state_stack_key)

        stack_top = current_stack[-1] if current_stack else "epsilon"

        for tr in pda["transitions"]:
            ti, expected_stack_top, sym, to, stack_push = tr
            if ti == current_state and sym == "epsilon" and expected_stack_top == stack_top:
                new_stack = current_stack.copy()

                if expected_stack_top != "epsilon" and new_stack:
                    new_stack.pop()

                if stack_push != ["epsilon"]:
                    for s in reversed(stack_push):
                        new_stack.append(s)

                new_state_stack = (to, tuple(new_stack))
                if new_state_stack not in closure:
                    stack.append((to, new_stack))

    return [(state, list(stack_tuple)) for state, stack_tuple in closure]


def next_states(pda, current_states_stacks, symbol):
    next_states = []

    for current_state, current_stack in current_states_stacks:
        stack_top = current_stack[-1] if current_stack else "epsilon"

        for tr in pda["transitions"]:
            ti, expected_stack_top, sym, to, stack_push = tr
            if ti == current_state and expected_stack_top == stack_top and sym == symbol:
                new_stack = current_stack.copy()

                if expected_stack_top != "epsilon" and new_stack:
                    new_stack.pop()

                if stack_push != ["epsilon"]:
                    for s in reversed(stack_push):
                        new_stack.append(s)

                next_states.append((to, new_stack))

    return next_states


def run_pda(fpda):
    pda = prep_pda(fpda)
    print(f"Stack alphabet: {pda['stack']}")
    if not pda or not check_pda(pda):
        return None

    print("PDA Transitions:")
    for t in pda["transitions"]:
        print(f"  {t[0]} & {t[1]} + {t[2]} > {t[3]}, {' '.join(t[4])}")

    string = input("Enter the string to process (space-separated symbols): ")
    symbols = string.split() if string.strip() else []

    for symbol in symbols:
        if symbol not in pda["symbols"]:
            print(f"Error: Symbol '{symbol}' not recognized.")
            return

    current_states_stacks = [(pda["init_state"], [])]
    current_states_stacks = epsilon_closure(pda, current_states_stacks)

    print(f"\nProcessing string: {symbols}")
    print(f"Initial configuration: {current_states_stacks}")

    for i, symbol in enumerate(symbols):
        if not current_states_stacks:
            print(f"No valid configurations after symbol '{symbol}'")
            break

        next_configs = next_states(pda, current_states_stacks, symbol)
        if next_configs:
            current_states_stacks = epsilon_closure(pda, next_configs)
            print(f"After '{symbol}': {current_states_stacks}")
        else:
            current_states_stacks = []
            print(f"No transitions possible with symbol '{symbol}'")
            break

    accepted = False
    if current_states_stacks:
        for state, stack in current_states_stacks:
            if state in pda["fin_states"]:
                accepted = True
                print(f"ACCEPTED: Final state {state} with stack {stack}")
                break

    if not accepted:
        print("REJECTED: No accepting configuration found")

    return accepted

