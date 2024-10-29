# IA3: Python Regex Engine
## Overview
In this assignment, we will construct a regex engine in Python. 

We will:
- Complete a parser to convert a string into a regex Abstract Syntax Tree (AST, a structured representation of the expressions and subexpressions that make up the regex pattern)
- Convert the AST into an NFA using the McNaughton-Yamada-Thompson algorithm
- Convert the NFA into a DFA using the subset construction algorithm.

By completing these steps, we can effectively interpret regex patterns. Matching a string to a regex pattern will become equivalent to checking if the DFA accepts the string. 
For ease, we include code to visualize the DFA you generate from regex strings.

## Required Setup
### Project, not Notebook
This assignment requires you to work with a python project and not a Jupyter Notebook.

### Python version
This assignment requires Python 3.10 or newer. Check which version you have installed as follows:

```shell
    python --version
```
### Testing your project code
After you finish each part, you can test them using the command below.
```shell
python main.py test <x>
```

`<x>` denotes the parts you want to run. Since tests are cumulative, running `python main.py test 2` will test parts 1 and 2 of your code. Make sure your code runs without error and passes all the tests for parts 1 to 3.
**Note**: The tests here are minimal, they provide support for you to work on your code. These do not guarantee your code is completely correct, they just make sure the code works for these cases. 

### Visualization
We provide code using [the automathon library](https://pypi.org/project/automathon/) to visualize finite automatons in this assignment. The command format is:
```bash
python main.py visual {nfa|dfa} <regex>
```

While not required, we highly recommend you use this library to help working with your code. To do so, you will need to go to the `automathon` project page and install the requirements listed on your machine. Note that `automathon` relies on [GraphViz](https://www.graphviz.org/download/), which require additional setup beyond installing the package. You may use package managers (like Homebrew or MacPorts on MacOS) if needed.

We have provided code in `visualize.py` to convert our `NFA` and `DFA` objects into `automathon` compatible objects. Running the command above will generate a `.png` file in the folder which is the corresponding NFA or DFA graph. We encourage you to utilize `visualize.py` to verify if your NFA implementation has correct transitions. Feel free to add more tests in `main.py` to check and visualize different scenarios, but do not remove existing tests.


## Part 1: Python Warmup: Regular Expression Parsing
In this part, you will complete a data structure `RegExpr` to represent a regex as well as a parser that converts a string into an `RegExpr` object. You will complete parts for the the following basic regex components.

- `RNoString`: A regex that never matches (like an empty set).
- `REmptyString`: A regex that matches only the empty string.
- `RSingle`: A regex that matches exactly one character.
- `RConcat`: Concatenation of two regexes.
- `RUnion`: Union (alternation) between two regexes. (`|`)
- `RStar`: Kleene star (matches zero or more repetitions). (`*`)
- `RAny`: A regex that matches any character. (`.`)
- `RPlus`: Matches one or more repetitions. (`+`)
- `ROption`: Matches zero or one character. (`?`)

The Python classes to represent the operations mentioned above are given to you in `regex.py`. We also give you a simple `parse_regx()` implementation, which parses the regex string, producing a `RegExpr` AST.

Tasks:
1. Implement the `__str__` method for each class to generate a string visualization of the AST. This will be helpful for debugging the later parts of the project.

   For example, `str(parse_regex("(a|b)*c"))` will be
   ```
   RConcat(RStar(RUnion(RSingle('a'),RSingle('b'))),RSingle('c'))
   ```

   Unfinished code is marked with `NotImplementedError("Require student implementation")` in this assignment.

2. Implement the `__match__args__` to enable pattern matching. 

## Part 2: NFA with McNaughton-Yamada-Thompson algorithm (Thompson's Construct)
In this part, you will convert the `RegExpr` from an AST into an NFA. By converting a regex into an NFA, the problem of checking whether a regex matches a string can be reduced to checking whether the NFA accepts that string. Read the Dragon Book section 3.7.4 on how to construct an NFA from a regex using Thompson's Construct.

We use the class `NFAState` to represent states and `NFA` to represent automata. The class definition of `NFAState` and `NFA` is given to you in `fa.py`. An `accepts()` method to check if an `NFA` accepts a string is also implemented.

Tasks:
1. Implement the `_make_transition_table()` method for the `NFA` class to return a Python dictionary that include all the transitions. The `self.transition_table` structure is:

   - key: state IDs (integers).
   - value: a `dict` where each key is a transition symbol and each value is a `set` of target state IDs the symbol leads the current state to. Your epsilon transitions will be represented with the value `""` (an empty string); for convenience we name it `EPSILON` (you should use this name).

   Regarding missing transitions:
   - Only non-null transitions should be listed (i.e., if a symbol has no corresponding transitions out of a state, leave that symbol out of the `dict`).
   - If a state has no outgoing transitions, there are two valid ways to represent this: by omitting it from the table, or by mapping it to an empty `dict`. (You can implement either one.)

   Once you have implemented `_make_transition_table()`, it will be possible for you to play with the visualization module. We highly recommend doing so to test and debug your code.

2. Implement the `from_regex()` class method which is the conversion function that translates our `RegExpr` in Part 1 into an `NFA`. The constructions of `REmptyString` and `RSingle` (the base cases) are given to you. You need to implement constructions for `RConcat`, `RUnion` and `RStar` (the inductive cases) that are described in the textbook. You do not need to implement `RAny`, `RPlus` and `ROption`. 


## Part 3: Converting NFA to DFA
In this part, you will convert the NFA into a DFA using the subset construction algorithm described in Dragon Book section 3.7.1. We have also provided additional resources on Canvas for a more detailed walkthrough. For simplicity, the set of possible input symbols will be all lowercase ASCII letters, which is defined in `SUPPORTED_SYMBOLS` in our code.

The class definition of `DFAState` and `DFA` is given to you in `fa.py`. You should use those to represent your DFAs.

Tasks:
1. Implement the `_make_transition_table()` method for the `DFA` class similar to your implementation for `NFA`. The only change here is that for `DFA`, your target state will a single state ID instead of a `set` since DFAs are deterministic.

2. Implement the `accepts()` method for the `DFA` class that takes in a string and check if the DFA accepts the string using `self.transition_table`. (It will be much simpler than the NFA `accepts()` method!)

3. Implement the class method `from_nfa()` to convert your NFA class into a DFA. To do so, you will need to first implement helper functions `epsilon_closure()` and `move()` as described in the textbook.


