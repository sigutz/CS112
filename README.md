# Automata Theory Implementation Project

CS112 Lab Project

This project implements various types of automata including DFA (Deterministic Finite Automaton), NFA (Non-deterministic Finite Automaton), PDA (Pushdown Automaton), and Turing Machine. The implementation features **intuitive transition formats** and **modular architecture** that make automata theory concepts accessible and easy to work with.

## Table of Contents
- [File Format](#file-format)
- [DFA Implementation](#dfa-implementation)
- [NFA Implementation](#nfa-implementation)
- [NFA to DFA Conversion](#nfa-to-dfa-conversion)
- [PDA Implementation](#pda-implementation)
- [Turing Machine Implementation](#turing-machine-implementation)
- [Helper Module](#helper-module)
- [Project Architecture](#project-architecture)

## File Format

All automata use a consistent, human-readable file format with structured sections:

```
[Section_Name]
content line 1
content line 2
...
DONE
```

### Key Features:
- **Structured Sections**: Each component is clearly separated (`[States]`, `[Symbols]`, etc.)
- **Explicit Terminators**: `DONE` marks the end of each section
- **Comment Support**: Lines starting with `#` are ignored for documentation
- **Unified Parsing**: The `prep.py` module handles all file types consistently

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
Prepares the DFA by parsing the input file and organizing the automaton components:
- Extracts states with their properties (initial/accept)
- Builds the input alphabet
- Parses transitions into a structured format
- Returns a complete DFA dictionary

#### `check_dfa(dfa)`
Validates the DFA structure by ensuring:
- All referenced states exist
- All symbols belong to the defined alphabet
- The automaton is properly formed

#### `run_dfa(fdfa)`
Offers two execution modes:
1. **String Mode**: Process an entire input string and show the path taken
2. **Interactive Mode**: Step through transitions manually for learning/debugging

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
Implements epsilon closure computation:
- Uses stack-based algorithm for efficiency
- Finds all states reachable through epsilon transitions
- Essential for proper NFA simulation

#### `next_states(nfa, current_states, symbol)`
Handles non-deterministic transitions:
- Processes multiple active states simultaneously
- Returns all possible successor states
- Maintains the complete state set during execution

## NFA to DFA Conversion

### `nfa2dfa.py` - Subset Construction Algorithm

#### Implementation Approach:
1. **Starting Point**: Begin with epsilon closure of NFA's initial state
2. **State Mapping**: Each DFA state represents a set of NFA states
3. **Systematic Construction**: Build transitions for all state combinations
4. **Acceptance Criteria**: Mark states containing NFA accept states

#### `nfa2dfa(fnfa)`
The conversion process:
- Creates a mapping between DFA states and NFA state sets
- Uses a queue to process new state combinations
- Generates minimal DFA with clean state naming (q0, q1, q2...)
- Preserves the language while eliminating non-determinism

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
The PDA uses a **highly readable transition format** that clearly expresses the automaton's behavior:

**Format**: `state & stack_top + input > next_state, stack_operations`

This design is more intuitive than traditional notation because:
- **Logical Grouping**: State and stack conditions are paired with `&`
- **Clear Input Marking**: The `+` symbol distinctly marks the input
- **Explicit Stack Operations**: Push/pop operations are clearly listed
- **Natural Flow**: Reads left-to-right like a rule: "IF in this state AND stack has this WHEN reading this THEN go here and do this"

Example breakdown:
- `q0 & $ + 1 > q1, A $` means:
  - IF in state q0 AND $ is on stack top
  - WHEN reading input 1
  - THEN transition to q1 and push A then $ onto stack

### Key Functions in `pda.py`

#### `prep_transitions(ftransitions)`
Parses the intuitive format into computational tuples:
- Extracts all components of each transition
- Handles epsilon transitions properly
- Converts stack operations into list format

#### `epsilon_closure(pda, states_with_stacks)`
Extended epsilon closure for PDAs:
- Tracks both state and stack contents
- Handles epsilon transitions that modify the stack
- Maintains complete configurations (state, stack) during closure

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
Simulates the Turing machine execution:
- Tracks tape content and head position
- Shows step-by-step execution trace
- Implements proper halting conditions
- Provides visual feedback of machine state

## Helper Module

### `prep.py` - Universal File Parser

#### `prep_file(fname)`
A flexible parsing system that:
- Recognizes section markers `[Section_Name]`
- Collects content until `DONE` markers
- Filters out comments for cleaner processing
- Returns organized data structure for each file type

This unified approach ensures:
- Consistent file handling across all automata
- Easy extension for new automata types
- Centralized parsing logic

## Project Architecture

### 1. **Modular Design**
- Each automaton type has its own module
- Shared utilities in `prep.py`
- Consistent function patterns across modules
- Easy to extend with new automaton types

### 2. **User-Friendly Formats**
The transition formats prioritize readability:
- DFA/NFA: `state + symbol > next_state`
- PDA: `state & stack + input > next_state, stack_ops`
- Turing: `state & symbol > next_state, write, direction`

### 3. **Educational Features**
- Interactive execution modes
- Step-by-step trace options
- Detailed error messages
- Visual representation of automaton behavior

### 4. **Robust Implementation**
- Input validation at multiple levels
- Proper handling of edge cases
- Efficient algorithms (e.g., epsilon closure)
- Complete automaton checking

## Usage Examples

### Running a DFA
```python
from dfa import run_dfa
run_dfa("dfa.abc")
# Choose mode 1 for string checking or mode 2 for interactive
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
# Enter space-separated input string
```

### Running a Turing Machine
```python
from turing import run_tm
final_tape, final_state = run_tm("tm1.abc")
# Watch the step-by-step execution
```

## Error Handling

The project includes comprehensive error checking:
- **File Format Errors**: Clear messages for malformed input files
- **Invalid Transitions**: Detection of references to non-existent states/symbols
- **Runtime Errors**: Graceful handling of invalid inputs during execution
- **Validation Functions**: Each automaton type has a `check_` function

## Educational Value

This implementation serves as an excellent learning tool:
1. **Visualization**: See how automata process input step-by-step
2. **Experimentation**: Easy to modify and test different automata
3. **Understanding**: Transition formats mirror theoretical notation
4. **Debugging**: Interactive modes help trace execution paths
