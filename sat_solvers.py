import random
import time
from typing import Optional

from sat_problem import CNF, Model
from search_algorithm import SATAlgorithm
from search_solution import SATSolution


def randomly_assign_model(model: Model) -> None:
    """
    Randomly assign each variable in model to either a 0 or 1 with uniform probability.
    """
    for variable in model.variables:
        value = random.randint(0, 1)
        model.assign(variable, bool(value))


class Random(SATAlgorithm):
    """
    Baseline SAT algorithm that performs a random walk: at each step it flips
    a variable chosen uniformly at random, with no heuristic guidance.

    This is provided for you as a point of comparison for GSAT and WalkSAT.
    """

    name = "Random"

    def satisfy(self, CNF_formula: CNF) -> SATSolution:
        """
        Run a random walk on the given CNF formula.

        Args:
            CNF_formula: The CNF formula to satisfy (e.g., the result of
                NQueens(...).compile() or Sudoku(...).compile())

        Returns:
            A SATSolution with the satisfying Model (or None, if no solution
            was found) and search statistics.
        """
        solution = SATSolution()
        start_time = time.time()

        if self.existing_model is None:
            model = Model(CNF_formula)
            randomly_assign_model(model)
        else:
            model = self.existing_model

        for _ in range(self.num_randomized_restarts):
            solution.stats.num_unsatisfied_clauses = []
            for _ in range(self.max_iterations):
                if model.is_satisfied():
                    break
                model.flip(random.choice(model.variables))
                solution.stats.num_unsatisfied_clauses.append(
                    len(model.unsatisfied_clauses))

            if model.is_satisfied():
                solution.model = model
                break
            randomly_assign_model(model)

        solution.stats.num_iterations = len(solution.stats.num_unsatisfied_clauses)
        solution.stats.runtime_seconds = time.time() - start_time
        return solution


class GSAT(SATAlgorithm):
    """
    Implements the GSAT (Greedy-SAT) algorithm for solving SAT problems.

    GSAT uses a greedy approach with random restarts to search for satisfying
    assignments. At each step, it either randomly flips a variable
    (exploration) or greedily flips the variable that maximizes satisfied
    clauses (exploitation).
    """

    name = "GSAT"

    def __init__(
        self,
        max_iterations: int = 10000,
        p: float = 0.5,
        num_randomized_restarts: int = 1,
        existing_model: Optional[Model] = None,
    ) -> None:
        """
        Args:
            max_iterations: Maximum number of variable flips to perform per restart
            p: Probability of choosing a random variable to flip (vs greedy choice)
            num_randomized_restarts: Number of random restarts to attempt
            existing_model: Optional starting model (used primarily for testing).
                If provided, search starts from this model instead of a random
                assignment.
        """
        super().__init__(max_iterations, num_randomized_restarts, existing_model)
        self.p = p

    def satisfy(self, CNF_formula: CNF) -> SATSolution:
        """
        Run GSAT on the given CNF formula.

        Args:
            CNF_formula: The CNF formula to satisfy (e.g., the result of
                NQueens(...).compile() or Sudoku(...).compile())

        Returns:
            A SATSolution with the satisfying Model (or None, if no solution
            was found) and search statistics.
        """
        #Number randomized restarts


        # TODO: TASK 1
        #
        # Implement GSAT. At each iteration, with probability self.p flip a
        # random variable (exploration); otherwise, flip whichever variable
        # increases the number of satisfied clauses the most (exploitation),
        # breaking ties uniformly at random.
        #
        # Record the number of unsatisfied clauses after each flip in
        # `solution.stats.num_unsatisfied_clauses`, and the number of flips in
        # `solution.stats.num_iterations`. As soon as model.is_satisfied() is
        # True, set `solution.model = model` and return `solution`.
        #
        # If max_iterations is exhausted without finding a solution, use
        # randomly_assign_model to restart and try again, up to
        # self.num_randomized_restarts times. If every restart is exhausted,
        # leave `solution.model` as None and return `solution`.
        #
        # See the Random class above for an example of the overall structure.

        solution = SATSolution() #Fields: model, stats
        start_time = time.time()

        if self.existing_model is None:
            model = Model(CNF_formula)
            randomly_assign_model(model)
        else:
            model = self.existing_model

        probability_of_exploration = self.p

        for _ in range(self.num_randomized_restarts):

            for _ in range(self.max_iterations):
                if model.is_satisfied(): #Already solved (ex, the starting/restarted model happens to satisfy CNF)
                    solution.model=model
                    solution.stats.runtime_seconds = time.time() - start_time
                    return solution

                random_decimal = random.random()
                if random_decimal <= probability_of_exploration: #AT THIS ITERATION: EXPLORE!
                    #Ex. if random_decimal = .20 and p = .50. 
                    #Exploring means choosing a variable at random and switching it. 
                    num_vars = len(model.variables)
                    random_index = random.randint(0, num_vars -1)

                    model.flip(model.variables[random_index])
                    solution.stats.num_iterations += 1 #TEST THIS
                    solution.stats.num_unsatisfied_clauses.append(len(model.unsatisfied_clauses)) #TEST THIS
                    if model.is_satisfied():
                        solution.model=model
                        solution.stats.runtime_seconds = time.time() - start_time
                        return solution

                else: #AT THIS ITERATION: EXPLOIT HIGH-POTENTIAL VARS!
                    best_case_satisfied_clause_increase = float("-inf")
                    best_vars = []

                    for var in model.variables:
                        will_make, will_break = model.get_make_and_break(var)
                        net_positive = will_make - will_break

                        if net_positive > best_case_satisfied_clause_increase: 
                            best_case_satisfied_clause_increase = net_positive
                            best_vars = [var] 

                        elif net_positive == best_case_satisfied_clause_increase:
            # tied with the best so far: add it to the list
                            best_vars.append(var)


                    #What flipping any var will not increase it? 

                    best_case_var_to_flip = random.choice(best_vars)
                    
                    model.flip(best_case_var_to_flip)
                    solution.stats.num_iterations += 1
                    solution.stats.num_unsatisfied_clauses.append(len(model.unsatisfied_clauses))

                    if model.is_satisfied():
                        solution.stats.runtime_seconds = time.time() - start_time
                        solution.model=model
                        return solution

            #RESTART: this attempt ran out of iterations, so start the next one from a new random assignment
            randomly_assign_model(model)

        #Every restart used up without finding a model -> solution.model stays None
        solution.stats.runtime_seconds = time.time() - start_time
        return solution

class WalkSAT(SATAlgorithm):
    """
    Implements the WalkSAT algorithm for solving SAT problems.

    WalkSAT focuses on unsatisfied clauses by selecting a random unsatisfied clause.
    If flipping a variable within that clause would result in zero broken clauses everywhere,
    flips that variable.
    Otherwise, either randomly flips a variable (exploration)
    or greedily flips the variable that minimizes broken clauses (exploitation).
    """

    name = "WalkSAT"

    def __init__(
        self,
        max_iterations: int = 100000,
        p: float = 0.5,
        num_randomized_restarts: int = 1,
        existing_model: Optional[Model] = None,
    ) -> None:
        """
        Args:
            max_iterations: Maximum number of variable flips to perform per restart
            p: Probability of choosing a random variable to flip (vs greedy choice)
            num_randomized_restarts: Number of random restarts to attempt
            existing_model: Optional starting model (used primarily for testing).
                If provided, search starts from this model instead of a random
                assignment.
        """
        super().__init__(max_iterations, num_randomized_restarts, existing_model)
        self.p = p

    def satisfy(self, CNF_formula: CNF) -> SATSolution:
        """
        Run WalkSAT on the given CNF formula.

        Args:
            CNF_formula: The CNF formula to satisfy (e.g., the result of
                NQueens(...).compile() or Sudoku(...).compile())

        Returns:
            A SATSolution with the satisfying Model (or None, if no solution
            was found) and search statistics.
        """
        solution = SATSolution()
        start_time = time.time()

        if self.existing_model is None:
            model = Model(CNF_formula)
            randomly_assign_model(model)
        else:
            model = self.existing_model

        # TODO: TASK 1
        #
        # Implement WalkSAT. At each iteration, pick a random unsatisfied
        # clause; with probability self.p flip a random variable within that
        # clause (exploration), otherwise flip whichever variable in that
        # clause increases the number of satisfied clauses the most
        # (exploitation), breaking ties uniformly at random.
        #
        # Record the number of unsatisfied clauses after each flip in
        # `solution.stats.num_unsatisfied_clauses`, and the number of flips in
        # `solution.stats.num_iterations`. As soon as model.is_satisfied() is
        # True, set `solution.model = model` and return `solution`.
        #
        # If max_iterations is exhausted without finding a solution, use
        # randomly_assign_model to restart and try again, up to
        # self.num_randomized_restarts times. If every restart is exhausted,
        # leave `solution.model` as None and return `solution`.
        #
        # See the Random class above for an example of the overall structure.

        #IMPLEMENT HERE.

        #1. 
        for _ in range(self.num_randomized_restarts):
            for _ in range(self.max_iterations):
                if model.is_satisfied(): #Already solved -> no unsatisfied clause to pick, so just return it
                    solution.model=model
                    solution.stats.runtime_seconds = time.time() - start_time
                    return solution

                num_uns_clauses = len(model.get_unsatisfied_clauses())

                random_index = random.randint(0, num_uns_clauses -1)
                random_clause = model.get_unsatisfied_clauses()[random_index]
                vars_in_clause = random_clause.variables_set

                #Find the BREAK count of every var in the clause (how many satisfied clauses flipping it would break)
                #Keep track of the var(s) with the FEWEST breaks.
                best_vars = []
                lowest_break = float("inf")

                for var in vars_in_clause:
                    will_make, will_break = model.get_make_and_break(var)

                    if will_break < lowest_break:
                        lowest_break = will_break
                        best_vars = [var]

                    elif will_break == lowest_break:
                        # tied with the best so far: add it to the list
                        best_vars.append(var)

                if lowest_break == 0: #FREE FLIP: some var breaks nothing, so flip it (no coin flip needed!)
                    var_to_flip = random.choice(best_vars)

                elif random.random() <= self.p: #EXPLORE: flip random var within clause with prob p.
                    var_to_flip = random.choice(tuple(vars_in_clause))

                else: #EXPLOIT: flip var that MINIMIZES broken clauses (ties broken at random)
                    var_to_flip = random.choice(best_vars)

                model.flip(var_to_flip)
                solution.stats.num_unsatisfied_clauses.append(len(model.unsatisfied_clauses))
                solution.stats.num_iterations += 1

                if model.is_satisfied():
                        solution.model=model
                        solution.stats.runtime_seconds = time.time() - start_time
                        return solution

            #RESTART: this attempt ran out of iterations, so start the next one from a new random assignment
            randomly_assign_model(model)

        #Every restart used up without finding a model -> solution.model stays None
        solution.stats.runtime_seconds = time.time() - start_time
        return solution
