# ReadME


#######################################################################
Tell us about your implementation!

###GSAT: 
-GSAT takes in a CNF formula (ex, [[AVB],[BVC], [C,D]]). Its goal is 
to find a MODEL of the CNF, that is, an assignment of variables that make every
clause true, in turn making the CNF itself true, or 'satisfied.'

-GSAT is a local search algorithm that begins by randomly assigning every var in CNF a value 
(the "random local solution.") GSAT then restarts up to self.num_randomized_restarts times; AT EACH RESTART,
it performs self.max_iterations iterations.

-Each iteration is a serch for neighboring solutions that satisfy CNF. A GSAT iteration does one of two
things: EXPLOIT or EXPLORE. EXPLORE is done with probability p; exploit 1-p. 
    -EXPLORE: Flip a var at random. After each flip it records the number of unsatisfied clauses, and it returns as soon as the formula is satisfied.
    -EXPLOIT: flip var with highest net change in satisfied clauses. 

-once a model is found, solution is returned. If no model found, empty solution returned.

###WALKSAT: 
-WALKSat takes in a CNF formula (ex, [[AVB],[BVC], [C,D]]). Its goal is 
to find a MODEL of the CNF, that is, an assignment of variables that make every
clause true, in turn making the CNF itself true, or 'satisfied.'

-WalkSAT is a local search algorithm that begins by randomly assigning every var in CNF a value
(the "random local solution.") WalkSAT then restarts up to self.num_randomized_restarts times; AT EACH RESTART,
it re-randomizes the assignment and performs up to self.max_iterations iterations.

-The key difference from GSAT: each WalkSAT iteration FIRST picks a random UNSATISFIED clause, and only
considers flipping the vars INSIDE that clause (instead of every var in the CNF). This guarantees every
flip fixes at least that one clause, and makes each iteration much cheaper.

-Each iteration then does one of two things: EXPLOIT or EXPLORE. EXPLORE is done with probability p; exploit 1-p.
    -EXPLORE: Flip a random var from the chosen clause.
    -EXPLOIT: Flip the var from the chosen clause with the highest net change in satisfied clauses
     (make - break), breaking ties uniformly at random.
    -After each flip (explore OR exploit), it records the number of unsatisfied clauses, and returns as soon as the formula is satisfied.

-Once a model is found, solution is returned. If no model is found after all restarts, an empty solution (model = None) is returned.

###SUDOKU:

-The Sudoku compiler takes in a starting grid (ex, a 4x4 or 9x9 list of lists, where 0 = empty cell)
and turns it into a CNF formula. Any MODEL of that CNF corresponds to a valid, completed Sudoku board,
so GSAT/WalkSAT can solve the puzzle by satisfying the CNF.

-Each var, named x_row_col_n, means "cell (row, col) holds number n." (ex, x_0_2_3 = "row 0, col 2 is a 3").

-NARROWING SOLUTIONS AS MUCH AS POSSIBLE: Before making any clauses, I figure out which numbers each
EMPTY cell could possibly hold using a double-for loop and the dictionaries row_vars, column_vars,
subspace_vars, and a hand-written subspace calculator function. 

    -PASS 1: Every row, col, and box (subgrid) starts with all numbers 1..N. For each GIVEN number,
     remove it from its row, col, and box sets.
    -PASS 2: For each empty cell, its possible numbers = (row set) ∩ (col set) ∩ (box set).
    -Numbers ruled out this way never get a var at all, which makes the CNF much smaller.
    -get_subspace maps (row, col) to its box using subgrid_size, so it works for any size (4x4, 9x9, ...).

-CLAUSES: The program then adds four kinds of clauses.
    -GIVENS: A one-literal clause nammed [x_r_c_v] for each given number.
    -CELL ASSIGNMENTS: For each empty cell, one clause OR-ing all its possible numbers (cell must hold one of them).
    -CELLS CAN'T HAVE MULTIPLE ASSIGNMENTS: For each empty cell, a [¬a V ¬b] clause for every pair of its possible numbers (cell can't hold two).
    -NO TWO CELLS IN SAME ROW, COL, OR BOX ARE ASSIGNED THE SAME. For every pair of empty cells in the same row, col, or box, a [¬x_cell1_n V ¬x_cell2_n]
     clause for each number n both could hold (two cells in a unit can't share a number).

-Then, the finished CNF is returned!

#######################################################################
Tell us about your tests!
##TODO SAGE!!

MY TESTS:
Here is what I test for in each.

GSAT:
- test_basic_cnf_gsat (line 20): solves a simple 4-clause CNF
- test_GSAT (line 150): GSAT runs on a small 3-clause CNF 
- (NO MODEL) test_unsat_cnf_returns_none (line 248): On an impossible CNF, (A) and (~A), GSAT returns no model 
- (NUM ITS = NUM ENTRIES, LAST ENTRY UNSAT. CLAUSES = 0)test_stats_match_flips (line 261): num_iterations equals the number of entries in num_unsatisfied_clauses
- (GSAT FLIPS BEST VAR)test_gsat_greedy_pick (line 280): With p = 0 (always exploit), GSAT flips the BEST var: B

WALKSAT:
- (4 CLAUSE) test_basic_cnf_walksat (line 222): WalkSAT solves the same 4-clause CNF as the GSAT test, and every clause comes out true.
- (IMPOSSIBLE: NO MODEL) test_unsat_cnf_returns_none (line 248): On an impossible CNF, (A) and (~A), WalkSAT returns no model instead of crashing or hanging. (Also tests GSAT.)
-( NUM ITS = NUM ENTRIES)test_stats_match_flips (line 261): num_iterations equals the number of entries in num_unsatisfied_clauses, and the last entry is 0
- (STARTING MODEL SATS) test_walksat_already_solved (line 306): If the starting model already satisfies the CNF, WalkSAT returns it 

GSAT VS WALKSAT:
- (BOTH SOLVE) test_compare_both_solve_easy (line 394): GSAT and WalkSAT both solve every easy 4x4 sudoku, with valid boards.
- (GSAT FLIPS COST MOREtest_compare_time_per_flip (line 411): On a 9x9 sudoku, each GSAT flip costs more than each WalkSAT flip, because GSAT scores EVERY var while WalkSAT only scores the vars in one clause.
- (test_compare_both_solve_easy (line 394): GSAT and WalkSAT both solve every easy 4x4 sudoku, with valid boards.
- test_compare_time_per_flip (line 411): On a 9x9 sudoku, each WalkSAT flip costs less than each GSAT flip.

SUDOKU COMPILER:
- is_valid_sudoku (line 196): HELPER, not  test. Checks that every row, col, and box of a finished board contains exactly 1..N.
-(RULES OBEYED) test_sudoku_4x4_valid (line 321): CONSTRAINTS. The solved easy 4x4 obeys every row, col, and box rule.
- (RULES OBEYED) test_sudoku_9x9_valid (line 334): CONSTRAINTS. The solved hard 9x9 obeys every row, col, and box rule.
-test_sudoku_givens_kept (line 347): Every given (starting) number has the same value in the solution.
- test_sudoku_one_blank (line 363): A solved 4x4 with one blank compiles to exactly 16 clauses (15 givens + 1), and the solver fills the blank with the only possible number (1).

#######################################################################
Answer the conceptual questions!

#Here is output from running python compare_performance.py --puzzle queens -n 8 --num_p 11
### GSAT Results
| $p$ | Run Time (Average) | Run Time (Standard Dev.) | Iterations (Average) | Iterations (Standard Dev.)| Success Rate |
| --- | --- | --- | --- | --- | --- |
| 0.00 | 13.93 | 0.00 | 10000 | 0 | 0.00 |
| 0.10 | 1.57 | 0.00 | 1569 | 0 | 1.00 |
| 0.20 | 0.06 | 0.00 | 61 | 0 | 1.00 |
| 0.30 | 2.56 | 0.00 | 3054 | 0 | 1.00 |
| 0.40 | 0.75 | 0.00 | 1129 | 0 | 1.00 |
| 0.50 | 0.05 | 0.00 | 103 | 0 | 1.00 |
| 0.60 | 0.06 | 0.00 | 115 | 0 | 1.00 |
| 0.70 | 3.99 | 0.00 | 10000 | 0 | 0.00 |
| 0.80 | 2.73 | 0.00 | 10000 | 0 | 0.00 |
| 0.90 | 3.33 | 0.00 | 10000 | 0 | 0.00 |
| 1.00 | 1.46 | 0.00 | 10000 | 0 | 0.00 |

#IN GENERAL:
- As p (probab. of exploring randomly) increases, runtime AND SD decrease. 
- However, as p increases, iterations increases.
-  As p increases, success rate decreases.

#HOW THIS COMPARES TO 20 QUEENS:
- 8 queens has lower runtime
- 8 queens ha 
### WalkSAT Results
| $p$ | Run Time (Average) | Run Time (Standard Dev.) | Iterations (Average) | Iterations (Standard Dev.) | Success Rate |
| --- | --- | --- | --- | --- | --- |
| 0.00 | 1.55 | 0.00 | 10000 | 0 | 0.00 |
| 0.10 | 0.01 | 0.00 | 29 | 0 | 1.00 |
| 0.20 | 0.14 | 0.00 | 736 | 0 | 1.00 |
| 0.30 | 0.01 | 0.00 | 30 | 0 | 1.00 |
| 0.40 | 0.01 | 0.00 | 65 | 0 | 1.00 |
| 0.50 | 0.04 | 0.00 | 315 | 0 | 1.00 |
| 0.60 | 0.01 | 0.00 | 29 | 0 | 1.00 |
| 0.70 | 0.01 | 0.00 | 68 | 0 | 1.00 |
| 0.80 | 0.02 | 0.00 | 116 | 0 | 1.00 |
| 0.90 | 0.42 | 0.00 | 4801 | 0 | 1.00 |
| 1.00 | 0.17 | 0.00 | 1980 | 0 | 1.00 |


#HOW THIS COMPARES WITH WALKSAT 20 QUEENS:
- 

#HOW WALKSAT AND GSAT COMPARE:
- walksat has much lower runtime. 
- Walksat has much lower runtime sd and iterations. 
-however, walksat has higher sd of iterations, indicating a wider spread.
- walksat has a much higher success rate. 

##4.1 WalkSAT's neighborhood operation is faster to compute than GSAT's. Why?
C: WalkSAT restricts its neighborhood to variables in a randomly chosen unsatisfied clause; GSAT considers flipping any variable in the model.

##4.2 Which of the following best summarizes the results in the tables?
D) WalkSAT is more robust to the choice of p than GSAT.

##4. 3Why are the algorithms more successful at smaller values of p?
C) As p->0,  , WalkSAT behaves like a greedy algorithm, but flips a variable that makes the most previously unsatisfied clauses satisfied.

##4.4 Which problem characteristic is most likely to make a higher value of 
 beneficial for WalkSAT?

 A) The problem's search landscape has many local optima and plateaus that can easily trap the algorithm.

#######################################################################
Hours taken:
7

Collaborators:
None

Known Bugs:
None

#######################################################################

##EOF##