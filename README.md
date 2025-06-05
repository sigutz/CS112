# Automata Theory Implementation Project

This project implements various types of automata including DFA (Deterministic Finite Automaton), NFA (Non-deterministic Finite Automaton), PDA (Pushdown Automaton), and Turing Machine. The implementation emphasizes **clear variable naming** and **intuitive transition formats** that make the code easy to understand and maintain.

## Table of Contents
- [File Format](#file-format)
- [DFA Implementation](#dfa-implementation)
- [NFA Implementation](#nfa-implementation)
- [NFA to DFA Conversion](#nfa-to-dfa-conversion)
- [PDA Implementation](#pda-implementation)
- [Turing Machine Implementation](#turing-machine-implementation)
- [Helper Module](#helper-module)

## File Format

All automata use a consistent, human-readable file format with clear section markers:

```
[Section_Name]
content line 1
content line 2
...
DONE
```

### Key Features:
- **Clear Section Headers**: Enclosed in square brackets `[States]`, `[Symbols]`, etc.
- **Section Terminator**: Each section ends with `DONE`
- **Comments**: Lines starting with `#` are ignored
- **Flexible Parsing**: The `prep.py` module handles all file parsing uniformly

## DFA Implementation

### Input File Format (`dfa.abc`)
```
[States]
q0-initial      # Initial state marked with '-initial'
q1
q2
q3-accept       # Accept states marked with '-accept'
DONE

[Symbols]
0, 1            # Comma-separated input symbols
DONE

[Transitions]
q0 + 1 > q1     # Format: current_state + symbol > next_state
q0 + 0 > q2
q1 + 0 > q3
DONE
```

### Key Functions in `dfa.py`

#### `prep_dfa(fdfa)`
Prepares the DFA by parsing the input file and organizing data into a dictionary with clear keys:
- `states`: List of all states
- `init_state`: The initial state
- `fin_states`: List of accepting states
- `symbols`: Input alphabet
- `transitions`: List of transition tuples

#### `check_dfa(dfa)`
Validates the DFA by ensuring:
- All transition states exist in the state list
- All transition symbols exist in the alphabet
- The DFA structure is complete and valid

#### `run_dfa(fdfa)`
Offers two execution modes:
1. **String Mode**: Process an entire string at once
2. **Interactive Mode**: Process symbol by symbol with visual feedback

**Clear Variable Names**:
- `current_state`: Tracks the automaton's current position
- `next_st`: The state to transition to
- `fin_states`: Final/accepting states

## NFA Implementation

### Input File Format (`nfa.abc`)
```
[States]
q0-initial
q1
q2
q3-accept
DONE

[Symbols]
0, 1, epsilon    # Includes epsilon transitions
DONE

[Transitions]
q0 + 1 > q1      # Multiple transitions from same state allowed
q0 + 1 > q2      # Non-deterministic behavior
q0 + 0 > q2
q1 + epsilon > q2 # Epsilon transitions supported
DONE
```

### Key Functions in `nfa.py`

#### `epsilon_closure(nfa, states)`
Computes the epsilon closure of a set of states:
- Uses a stack-based approach for efficiency
- Returns all states reachable via epsilon transitions
- Essential for NFA simulation

#### `next_states(nfa, current_states, symbol)`
Handles non-determinism by:
- Processing multiple current states simultaneously
- Returning all possible next states for a given symbol
- Maintaining the set of active states

## NFA to DFA Conversion

### `nfa2dfa.py` - Subset Construction Algorithm

#### Process Overview:
1. **Initial State**: Epsilon closure of NFA's initial state
2. **State Generation**: Each DFA state represents a set of NFA states
3. **Transition Computation**: For each symbol, compute reachable states
4. **Accept States**: DFA state is accepting if it contains any NFA accept state

#### `nfa2dfa(fnfa)`
Key implementation details:
- `state_map`: Maps DFA state names to sets of NFA states
- `states2process`: Queue of unprocessed state combinations
- `processed`: Tracks already processed combinations
- Generates clean DFA state names (q0, q1, q2...)

## PDA Implementation

### Input File Format (`pda.abc`)
```
[States]
q0-initial
q1
q2
q3-accept
DONE

[Symbols]
0, 1, epsilon
DONE

[Stack]
$, A, B          # Stack alphabet
DONE

[Transitions]
# Format: current_state & stack_top + input > next_state, stack_push
q0 & epsilon + epsilon > q0, $     # Initialize stack with $
q0 & $ + 1 > q1, A $               # Read 1, push A
q0 & $ + 0 > q2, B $               # Read 0, push B
q1 & A + 0 > q3, epsilon           # Read 0, pop A
DONE
```

### Intuitive Transition Format
The PDA uses a **highly readable transition format** that clearly shows:
- **State & Stack Context**: `q0 & $` - "In state q0 with $ on stack top"
- **Input Symbol**: `+ 1` - "Reading symbol 1"
- **Result**: `> q1, A $` - "Go to state q1, push A then $"

This format is more intuitive than traditional notation because it:
- Separates concerns clearly (state, stack, input)
- Uses natural reading order (condition → action)
- Makes stack operations explicit

### Key Functions in `pda.py`

#### `prep_transitions(ftransitions)`
Parses the intuitive transition format into tuples:
```python
(in_state, stack_top, symbol, next_state, stack_push)
```

#### `epsilon_closure(pda, states_with_stacks)`
Extended epsilon closure that tracks both states and stack contents:
- Handles epsilon transitions that modify the stack
- Maintains (state, stack) configurations
- Critical for PDA simulation

## Turing Machine Implementation

### Input File Format (`tm1.abc`)
```
[Band]
1 1 1 1 1 + 1 1 1 1 $    # Initial tape content
DONE

[States]
q0-initial
q1
q2-accept
DONE

[Symbols]
1, +, s, $               # Tape alphabet
DONE

[Transitions]
# Format: state & symbol > next_state, write_symbol, direction
q0 & 1 > q0, 1, R       # Move right without changing
q0 & + > q0, 1, R       # Replace + with 1, move right
q0 & $ > q1, s, L       # Found end, write s, move left
q1 & 1 > q2, $, L       # Write $, move left, accept
DONE
```

### Key Functions in `turing.py`

#### `run_tm(ftm)`
Simulates the Turing machine with:
- **Clear State Tracking**: `current_state`, `current_band`, `pos`
- **Step-by-step Execution**: Shows each configuration
- **Termination Conditions**: Accept states or max steps
- **Visual Output**: Displays tape and head position at each step

## Helper Module

### `prep.py` - Universal File Parser

#### `prep_file(fname)`
A flexible parser that:
- Reads sections marked by `[Section_Name]`
- Ignores comments (lines starting with `#`)
- Collects content until `DONE` marker
- Returns a dictionary mapping section names to content

This unified approach ensures:
- Consistent file format across all automata types
- Easy extension for new automata types
- Clean separation of parsing logic

## Project Highlights

### 1. **Clear Variable Naming**
- `init_state` instead of `q0` or `start`
- `fin_states` instead of `F` or `final`
- `current_states` for tracking active states in NFA
- `stack_push` explicitly names the stack operation

### 2. **Intuitive Formats**
- DFA/NFA transitions: `state + symbol > next_state`
- PDA transitions: `state & stack + input > next_state, stack_ops`
- Turing transitions: `state & symbol > next_state, write, direction`

### 3. **Modular Design**
- Separate modules for each automaton type
- Shared parsing logic in `prep.py`
- Consistent function naming: `prep_X`, `check_X`, `run_X`

### 4. **User-Friendly Features**
- Interactive and batch processing modes
- Clear error messages with context
- Visual feedback during execution
- Step-by-step trace for debugging

## Usage Examples

### Running a DFA
```python
from dfa import run_dfa
run_dfa("dfa.abc")
```

### Converting NFA to DFA
```python
from nfa2dfa import nfa2dfa, save_dfa
dfa = nfa2dfa("nfa.abc")
save_dfa(dfa, "converted_dfa.abc")
```

### Simulating a PDA
```python
from pda import run_pda
run_pda("pda.abc")
```

### Running a Turing Machine
```python
from turing import run_tm
final_tape, final_state = run_tm("tm1.abc")
```

## Conclusion

This project demonstrates that automata theory implementations can be both theoretically correct and practically readable. The emphasis on clear naming conventions and intuitive formats makes the code accessible to students and researchers alike, while maintaining the mathematical rigor required for formal language processing.
