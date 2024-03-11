import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        domains_copy = copy.deepcopy(self.domains)

        for var, words in domains_copy.items():
            for word in words:
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Overlap between x and y
        # overlap = {v for k, v in self.crossword.overlaps.items() if k == (x, y)}.pop()
        overlap = self.crossword.overlaps[(x, y)]
        if overlap == None:
            return False
        x_char, y_char = overlap

        x_domain_copy = copy.deepcopy(self.domains[x])

        
        revisions = 0

        for x_word in x_domain_copy:
            inconsistencies = 0
            for y_word in self.domains[y]:
                if x_word[x_char] != y_word[y_char]:
                    inconsistencies += 1
            
            if inconsistencies == len(self.domains[y]):
                self.domains[x].remove(x_word)
                revisions += 1

        return True if revisions > 0 else False


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arcs is not provided, initiate the queue with all the possible arcs in the problem
        if arcs == None:
            queue = []
            for v1 in self.crossword.variables:
                for v2 in self.crossword.variables:
                    if v1 == v2:
                        continue
                    queue.append((v1, v2))
        else:
            queue = arcs

        while queue: # While queue is not empty
            # Get first and remove it from queue
            (x, y) = queue.pop(0)

            if self.revise(x, y):
                if len(self.domains[x]) == 0: # If resulting domain is empty, there is no solution
                    return False 
                
                # Add to queue all neighbors of x, except for y
                neighbors_of_x = self.crossword.neighbors(x)
                neighbors_of_x.remove(y)

                for z in neighbors_of_x:
                    queue.append((z, x))
                
        return True
            
                    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        return len(assignment) == len(self.crossword.variables)


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check if all values are distinct 
        distinct_values = set(assignment.values())
        if len(distinct_values) != len(assignment.values()):
            return False

        for k, v in assignment.items():

            if k.length != len(v):
                return False
            
            neighbors = self.crossword.neighbors(k)

            for neighbor in neighbors:
                if neighbor not in assignment.keys():
                    continue

                k_char, neighbor_char = self.crossword.overlaps[(k, neighbor)]
                if v[k_char] != assignment[neighbor][neighbor_char]:
                    return False 
                
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        domain_values = self.domains[var]
        
        rule_out_counting = {k: 0 for k in domain_values}

        neighbors = self.crossword.neighbors(var)

        for word in domain_values:
            for neighbor in neighbors:
                x, y = self.crossword.overlaps[(var, neighbor)]
                for neighbor_word in self.domains[neighbor]:
                    if word[x] != neighbor_word[y]:
                        rule_out_counting[word] += 1

        return sorted(rule_out_counting.keys(), key=lambda n: rule_out_counting[n])


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Dictionary containing all unassigned variables in self.domains with the number of remaining values
        unassigned_variables = {k: len(v) for k, v in self.domains.items() if k not in assignment.keys()}

        # Choose the variables with the minimum number of remaining values in its domain
        min_remaining_values = min(unassigned_variables.values())
        unassigned_variables = {k: v for k, v in unassigned_variables.items() if v == min_remaining_values}

        if len(unassigned_variables) == 1:
            return next(iter(unassigned_variables))
        else:
             unassigned_variables = {k: len(self.crossword.neighbors(k)) for k in unassigned_variables.keys()}
             max_neighbors = max(unassigned_variables.values())
             unassigned_variables = {k: v for k, v in unassigned_variables.items() if v == max_neighbors}
             return next(iter(unassigned_variables))
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment 
        
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result != None:
                    return result 
                assignment.pop(var)

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
