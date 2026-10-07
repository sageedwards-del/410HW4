import unittest
import random
from typing import Optional

from sat_solvers import GSAT, WalkSAT
from sat_problem import Clause, Literal, Variable, CNF, Model
from sudoku import Sudoku
import examples



class IOTest(unittest.TestCase):
    """
    Tests input/output for SAT solver implementations.

    Contains basic test cases to verify that GSAT
    correctly solves simple CNF formulas and makes optimal decisions.
    """

    def test_basic_cnf_gsat(self) -> None:
        """
        Test if GSAT can solve a basic CNF formula.

        Tests GSAT's ability to find a satisfying assignment for a simple
        CNF formula starting from a partially unsatisfying initial state.

        CNF = (A or B) and (~B or C) and (B or ~A) and (B or D)
        Example solution: A=True, B=True, C=True, D=True
        """
        cnf = CNF()
        cnf.add_clause(
            Clause([Literal(Variable("A"), True), Literal(Variable("B"), True)]))
        cnf.add_clause(
            Clause([Literal(Variable("B"), False), Literal(Variable("C"), True)]))
        cnf.add_clause(
            Clause([Literal(Variable("B"), True), Literal(Variable("A"), False)]))
        cnf.add_clause(
            Clause([Literal(Variable("B"), False), Literal(Variable("D"), True)]))
        cnf_model = Model(cnf)
        cnf_model.assign(Variable("A"), False)
        cnf_model.assign(Variable("B"), False)
        cnf_model.assign(Variable("C"), True)
        cnf_model.assign(Variable("D"), False)
        result = GSAT(max_iterations=500, p=0,
                      existing_model=cnf_model).satisfy(cnf)
        self.assertIsNotNone(result.model, "The solver should return a solution model")
        model = result.model
        assert(model)
        A = model.assignment[Variable("A")]
        B = model.assignment[Variable("B")]
        C = model.assignment[Variable("C")]
        D = model.assignment[Variable("D")]

        self.assertTrue((A or B) and (not B or C)
                        and (B or not A) and (B or D))
        print('GSAT solves a simple CNF!')

    def test_test(self) -> None:
        assert 1 + 1 == 2 
         #Makes sure my test file can run!

    #PASSES!
    def get_make_and_break_test(self) ->None:
            #Goal boolean formula in CNF form:
            # CNF1= [[AVB]&[CV~A]]
            # A = 0, B = 0, C = 0
            # Flipping A to 1 would MAKE clause 1 but BREAK clause 2

            A = Variable("A")
            B = Variable("B")
            C = Variable("C")

            #Literals make up the clauses.
            litA = Literal(A, True)
            litnotA = Literal(A, False)
            litB = Literal(B, True)
            litC = Literal(C, True)

            #Clauses make up the CNF. 
            #For a clause to be true at least one concrete variable and its T/F assignment must match a literal
            Clause1 = Clause([litA, litB])
            Clause2 = Clause([litC, litnotA])

            cnf_final_formula = CNF()
            cnf_final_formula.add_clause(Clause1)
            cnf_final_formula.add_clause(Clause2)

            #Okay we have the logical structure! Now time to assign vals and start building our model (to fulfill)
            #A model is an assignment of T/F to all vars within a CNF formula, such that every clause = True and thus the CNF formula is true!
            #Ex, above, the assignments A=0,B=1, and C=0 would make CNF1 true.

            var_assign_model = Model(cnf_final_formula)
            var_assign_model.assign(A, False)
            var_assign_model.assign(B, False)
            var_assign_model.assign(C, False)

             # Again: Flipping A to True would MAKE clause 1 but BREAK clause 2
            print(var_assign_model.get_make_and_break(A))
            assert var_assign_model.get_make_and_break(A) == (1,1)

            #Flipping B. Would make clause1 true. 
            assert var_assign_model.get_make_and_break(B) == (1,0)
            print(var_assign_model.get_make_and_break(B))

            #Flipping C. Won't change anything because Clause2 is already true. 
            print(var_assign_model.get_make_and_break(C))
            assert var_assign_model.get_make_and_break(C) == (0,0)

    #PASSES!
    def get_make_and_break_test2(self)-> None:
         #CNF Formula: What to fulfill (Made up of clauses, made up of literals(var, assign)
         #Model: Assigning vals to vars to see which literals are fulfilled, thus what clauses

         #Goal: CNF = [[AVB] [BVC] [CVD] [DVE]]

            A = Variable("A")
            B = Variable("B")
            C = Variable("C")
            D = Variable("D")
            E = Variable("E")

            #Literals make up the clauses.
            litA = Literal(A, True)
            litnotA = Literal(A, False)
            litB = Literal(B, True)
            litC = Literal(C, True)
            litD =  Literal(D, True)
            litE = Literal(E,True)

            #Clauses make up the CNF. 
            #For a clause to be true at least one concrete variable and its T/F assignment must match a literal
            Clause1 = Clause([litA, litB])
            Clause2 = Clause([litB, litC])
            Clause3 = Clause([litD, litE])

            cnf = CNF([Clause1, Clause2, Clause3]) #formula to appease (watch those lit assigns!)
            model = Model(cnf)

            model.assign(A, False)
            model.assign(B, False)
            model.assign(C, False)
            model.assign(D, False)
            model.assign(E, False)

            assert model.get_make_and_break(A) == (1,0)
            assert model.get_make_and_break(B) == (2,0) #Ensures no data actually changed
            assert model.get_make_and_break(C) == (1,0)
            assert model.get_make_and_break(D) == (1,0)

    def test_GSAT(self) ->None:
          first_GSAT = GSAT(50, 0.5, 1)

          A = Variable("A")
          B = Variable("B")
          C = Variable("C")
          D = Variable("D")
          E = Variable("E")

            #Literals make up the clauses.
          litA = Literal(Variable("A"), True)
          litnotA = Literal(Variable("A"), False)
          litB = Literal(Variable("B"), True)
          litC = Literal(Variable("C"), True)
          litD =  Literal(Variable("D"), True)
          litE = Literal(Variable("E"),True)

          #Goal: CNF = [[AVB] [BVC] [DVE] []]

            #Clauses make up the CNF. 
            #For a clause to be true at least one concrete variable and its T/F assignment must match a literal
          Clause1 = Clause([litA, litB])
          Clause2 = Clause([litB, litC])
          Clause3 = Clause([litD, litE])
          Clause4 = Clause([litnotA])

          cnf = CNF([Clause1, Clause2, Clause3]) #formula to appease (watch those lit assigns!)

          solution = first_GSAT.satisfy(cnf)
          print(solution)


    #----------------------------------------------------------------------------------------------
    #HELPER (not a test, since name doesn't start with "test"): checks a finished sudoku board
    #Every row, col, and box must contain exactly the numbers 1..N
    def is_valid_sudoku(self, board) -> bool:
        n = len(board)
        box = int(n ** 0.5)
        all_nums = set(range(1, n + 1))

        for row in board: #Rows
            if set(row) != all_nums:
                return False

        for col in range(n): #Cols
            if set(board[row][col] for row in range(n)) != all_nums:
                return False

        for box_row in range(0, n, box): #Boxes (ex, 2x2 boxes for a 4x4)
            for box_col in range(0, n, box):
                nums_in_box = set()
                for i in range(box):
                    for j in range(box):
                        nums_in_box.add(board[box_row + i][box_col + j])
                if nums_in_box != all_nums:
                    return False

        return True


    def test_basic_cnf_walksat(self) -> None:
        '''WalkSAT solves simple CNF'''
        #CNF = (A or B) and (~B or C) and (B or ~A) and (B or D)
        A = Variable("A")
        B = Variable("B")
        C = Variable("C")
        D = Variable("D")

        cnf = CNF()
        cnf.add_clause(Clause([Literal(A, True), Literal(B, True)]))
        cnf.add_clause(Clause([Literal(B, False), Literal(C, True)]))
        cnf.add_clause(Clause([Literal(B, True), Literal(A, False)]))
        cnf.add_clause(Clause([Literal(B, False), Literal(D, True)]))

        result = WalkSAT(max_iterations=500, p=0.5).satisfy(cnf)
        self.assertIsNotNone(result.model, "WalkSAT should find a solution")
        model = result.model
        assert(model)

        a = model.assignment[A]
        b = model.assignment[B]
        c = model.assignment[C]
        d = model.assignment[D]
        self.assertTrue((a or b) and (not b or c) and (b or not a) and (b or d))


    
    def test_unsat_cnf_returns_none(self) -> None:
        '''BASIC TEST 2: An unsatisfiable CNF should return NO model (and not crash/hang!)'''
        #CNF = (A) and (~A) -> impossible!
        A = Variable("A")
        cnf = CNF([Clause([Literal(A, True)]), Clause([Literal(A, False)])])

        gsat_result = GSAT(max_iterations=50, p=0.5).satisfy(cnf)
        walksat_result = WalkSAT(max_iterations=50, p=0.5).satisfy(cnf)

        self.assertIsNone(gsat_result.model)
        self.assertIsNone(walksat_result.model)


    
    def test_stats_match_flips(self) -> None:
        '''BASIC TEST 3: Stats line up -> one 'unsatisfied clauses' entry per flip, and last entry is 0 when solved'''
        #CNF = (A or B) and (B or C) and (C or D)
        A = Variable("A")
        B = Variable("B")
        C = Variable("C")
        D = Variable("D")
        cnf = CNF([Clause([Literal(A, True), Literal(B, True)]),
                   Clause([Literal(B, True), Literal(C, True)]),
                   Clause([Literal(C, True), Literal(D, True)])])

        for solver in [GSAT(max_iterations=500, p=0.5), WalkSAT(max_iterations=500, p=0.5)]:
            result = solver.satisfy(cnf)
            self.assertIsNotNone(result.model)
            self.assertEqual(len(result.stats.num_unsatisfied_clauses), result.stats.num_iterations)
            if result.stats.num_iterations > 0: #If any flips happened, the last one solved it
                self.assertEqual(result.stats.num_unsatisfied_clauses[-1], 0)


    def test_gsat_greedy_pick(self) -> None:
        ''' p = 0 (always exploit), GSAT picks the BEST var to flip'''
        #CNF = (A or B) and (B or C) and (B or D), everything starts False
        #Flipping B MAKES 3 clauses; flipping A, C, or D only makes 1.
        #So with only ONE flip allowed, GSAT solves it only if it picks B.
        A = Variable("A")
        B = Variable("B")
        C = Variable("C")
        D = Variable("D")
        cnf = CNF([Clause([Literal(A, True), Literal(B, True)]),
                   Clause([Literal(B, True), Literal(C, True)]),
                   Clause([Literal(B, True), Literal(D, True)])])

        model = Model(cnf)
        model.assign(A, False)
        model.assign(B, False)
        model.assign(C, False)
        model.assign(D, False)

        result = GSAT(max_iterations=1, p=0, existing_model=model).satisfy(cnf)
        self.assertIsNotNone(result.model, "GSAT should flip B and solve it in 1 flip")
        assert(result.model)
        self.assertEqual(result.model.assignment[B], 1)

    def test_walksat_already_solved(self) -> None:
        '''   
    #BASIC TEST 5: If the starting model ALREADY satisfies the CNF, WalkSAT should just return it
    #(There are no unsatisfied clauses to pick from, so this catches a randint(0, -1) crash!)
        '''
        #CNF = (A or B), starting with A = True
        A = Variable("A")
        B = Variable("B")
        cnf = CNF([Clause([Literal(A, True), Literal(B, True)])])

        model = Model(cnf)
        model.assign(A, True)
        model.assign(B, False)

        result = WalkSAT(max_iterations=10, p=0.5, existing_model=model).satisfy(cnf)
        self.assertIsNotNone(result.model)

    def test_sudoku_4x4_valid(self) -> None:
        '''Solved 4x4 obeys every row/col/box rule'''
        random.seed(0)
        grid = examples.get_sudoku_puzzles()["easy"][0]
        problem = Sudoku(grid)
        result = WalkSAT(max_iterations=10000, p=0.5).satisfy(problem.compile())

        self.assertIsNotNone(result.model)
        assert(result.model)
        board = problem.get_board(result.model)
        self.assertTrue(self.is_valid_sudoku(board))


    def test_sudoku_9x9_valid(self) -> None:
        '''Solved 9x9 obeys every row/col/box rule'''
        random.seed(0)
        grid = examples.get_sudoku_puzzles()["hard"][0]
        problem = Sudoku(grid)
        result = WalkSAT(max_iterations=100000, p=0.5).satisfy(problem.compile())

        self.assertIsNotNone(result.model)
        assert(result.model)
        board = problem.get_board(result.model)
        self.assertTrue(self.is_valid_sudoku(board))

    def test_sudoku_givens_kept(self) -> None:
        '''Given (starting) numbers are never changed in the solution'''
        random.seed(0)
        grid = examples.get_sudoku_puzzles()["easy"][1]
        problem = Sudoku(grid)
        result = WalkSAT(max_iterations=10000, p=0.5).satisfy(problem.compile())

        self.assertIsNotNone(result.model)
        assert(result.model)
        board = problem.get_board(result.model)
        for row in range(len(grid)):
            for col in range(len(grid)):
                if grid[row][col] != 0:
                    self.assertEqual(board[row][col], grid[row][col])


    def test_sudoku_one_blank(self) -> None:
        '''A board with only ONE blank has only one possible number for it'''
        #Solved 4x4, with the top-left cell (should be 1) blanked out
        grid = [[0, 2, 3, 4],
                [3, 4, 1, 2],
                [2, 1, 4, 3],
                [4, 3, 2, 1]]
        problem = Sudoku(grid)
        cnf = problem.compile()

        #15 given clauses + 1 'at least one' clause for the blank (it only has 1 option, so no 'at most one' pairs)
        self.assertEqual(len(cnf.clauses), 16)

        result = WalkSAT(max_iterations=100, p=0.5).satisfy(cnf)
        self.assertIsNotNone(result.model)
        assert(result.model)
        self.assertEqual(problem.get_board(result.model)[0][0], 1)


    def test_sudoku_empty_clause_count(self) -> None:
        '''A board with only ONE blank has only one possible number for it'''
        problem = Sudoku([[0, 0, 0, 0] for _ in range(4)])
        cnf = problem.compile()

        #AT LEAST ONE: 16 cells -> 16 clauses
        #AT MOST ONE: 16 cells * (4 choose 2 = 6 pairs of numbers) -> 96 clauses
        #NO REPEATS: pairs of cells sharing a unit = 24 (rows) + 24 (cols) + 8 (box diagonals) = 56,
        #            each pair gets 1 clause per number (4) -> 224 clauses
        self.assertEqual(len(cnf.clauses), 16 + 96 + 224)

    def test_compare_both_solve_easy(self) -> None:
        ''' GSAT and WalkSAT both solve every easy 4x4, and both give valid boards'''
        random.seed(0)
        for grid in examples.get_sudoku_puzzles()["easy"]:
            problem = Sudoku(grid)

            gsat_result = GSAT(max_iterations=10000, p=0.2).satisfy(problem.compile())
            walksat_result = WalkSAT(max_iterations=10000, p=0.5).satisfy(problem.compile())

            self.assertIsNotNone(gsat_result.model)
            self.assertIsNotNone(walksat_result.model)
            assert(gsat_result.model and walksat_result.model)
            self.assertTrue(self.is_valid_sudoku(problem.get_board(gsat_result.model)))
            self.assertTrue(self.is_valid_sudoku(problem.get_board(walksat_result.model)))


    def test_compare_time_per_flip(self) -> None:
        '''Each WalkSAT flip is much cheaper than each GSAT flip on a 9x9
    #(GSAT scores EVERY var each exploit step; WalkSAT only scores the vars in ONE clause)'''
        random.seed(0)
        grid = examples.get_sudoku_puzzles()["hard"][0]
        problem = Sudoku(grid)

        #p = 0 so every flip is an exploit (the expensive kind); 50 flips is enough to compare
        gsat_result = GSAT(max_iterations=50, p=0).satisfy(problem.compile())
        walksat_result = WalkSAT(max_iterations=50, p=0).satisfy(problem.compile())

        gsat_time_per_flip = gsat_result.stats.runtime_seconds / max(gsat_result.stats.num_iterations, 1)
        walksat_time_per_flip = walksat_result.stats.runtime_seconds / max(walksat_result.stats.num_iterations, 1)

        print(f"GSAT: {gsat_time_per_flip:.6f}s/flip, WalkSAT: {walksat_time_per_flip:.6f}s/flip")
        self.assertLess(walksat_time_per_flip, gsat_time_per_flip)




if __name__ == "__main__":
    unittest.main()
