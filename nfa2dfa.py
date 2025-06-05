import nfa


def nfa2dfa(fnfa):
    # Pregătim și validăm NFA-ul
    nfa_data = nfa.prep_nfa(fnfa)
    if nfa_data is None or not nfa.check_nfa(nfa_data):
        print("Error: Invalid NFA data.")
        return None

    print(
        f"Original NFA: States={nfa_data['states']}, Initial={nfa_data['init_state']}, Final={nfa_data['fin_states']}")

    # Eliminăm epsilon din simboluri pentru DFA
    dfa_symbols = [s for s in nfa_data["symbols"] if s not in ["e", "ε", "Îµ", "epsilon"]]

    # Calculăm epsilon closure pentru starea inițială
    start_closure = sorted(list(nfa.epsilon_closure(nfa_data, [nfa_data["init_state"]])))

    # Componentele DFA-ului
    dfa_states = []
    dfa_transitions = []
    dfa_fin_states = []
    dfa_init_state = None
    state_map = {}
    state_counter = 0

    # Inițializăm states2process
    states2process = [start_closure]
    processed = []

    # Procesăm fiecare stare DFA
    while states2process:
        curr_nfa_states = states2process.pop(0)

        if curr_nfa_states in processed:
            continue
        processed.append(curr_nfa_states)

        # Găsim sau creăm numele stării DFA
        curr_dfa_state = None
        for dfa_state, nfa_state_set in state_map.items():
            if nfa_state_set == curr_nfa_states:
                curr_dfa_state = dfa_state
                break

        if curr_dfa_state is None:
            curr_dfa_state = f"q{state_counter}"
            state_map[curr_dfa_state] = curr_nfa_states
            dfa_states.append(curr_dfa_state)
            state_counter += 1

            # Setăm starea inițială DFA
            if curr_nfa_states == start_closure:
                dfa_init_state = curr_dfa_state

            # Verificăm dacă e stare finală
            if any(state in nfa_data["fin_states"] for state in curr_nfa_states):
                dfa_fin_states.append(curr_dfa_state)

        # Calculăm tranzițiile pentru fiecare simbol
        for symbol in dfa_symbols:
            next_nfa_states = []

            # Găsim toate stările NFA accesibile cu acest simbol
            for nfa_state in curr_nfa_states:
                next_nfa_states.extend(nfa.next_states(nfa_data, [nfa_state], symbol))

            # Eliminăm duplicatele
            next_nfa_states = list(set(next_nfa_states))

            if next_nfa_states:
                # Calculăm epsilon closure
                next_closure = sorted(list(nfa.epsilon_closure(nfa_data, next_nfa_states)))

                # Verificăm dacă această combinație există deja
                existing_dfa_state = None
                for dfa_state, nfa_state_set in state_map.items():
                    if nfa_state_set == next_closure:
                        existing_dfa_state = dfa_state
                        break

                if existing_dfa_state:
                    target_state = existing_dfa_state
                else:
                    # Creăm stare nouă DFA
                    target_state = f"q{state_counter}"
                    state_map[target_state] = next_closure
                    dfa_states.append(target_state)
                    states2process.append(next_closure)
                    state_counter += 1

                    # Verificăm dacă e stare finală
                    if any(state in nfa_data["fin_states"] for state in next_closure):
                        dfa_fin_states.append(target_state)

                # Adăugăm tranziția
                dfa_transitions.append((curr_dfa_state, symbol, target_state))


    # Returnăm DFA-ul
    return {
        'symbols': dfa_symbols,
        'states': dfa_states,
        'transitions': dfa_transitions,
        'init_state': dfa_init_state,
        'fin_states': dfa_fin_states,
        'state_map': state_map
    }


def save_dfa(dfa, filename):
    with open(filename, 'w' ) as f:
        f.write("[States]\n")
        for state in dfa["states"]:
            if state == dfa["init_state"]:
                f.write(f"{state}-initial\n")
            elif state in dfa["fin_states"]:
                f.write(f"{state}-accept\n")
            else:
                f.write(f"{state}\n")
        f.write("DONE\n\n")

        f.write("[Symbols]\n")
        f.write(", ".join(dfa["symbols"]) + "\n")
        f.write("DONE\n\n")

        f.write("[Transitions]\n")
        for trans in dfa["transitions"]:
            f.write(f"{trans[0]} + {trans[1]} > {trans[2]}\n")
        f.write("DONE\n")

save_dfa(nfa2dfa("nfa.abc"), "n2d.t1")