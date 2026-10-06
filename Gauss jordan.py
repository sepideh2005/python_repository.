#about program
#converts a matrix into row echelon from and calculates its value.
#the writer: Sepideh Norozifard
#student of computer_since in Azad uni of Qom


from fractions import Fraction

EPS = 1e-9    #tolerance used instead of exact comparison with zero

def to_number(text):
    """convert ext such as '2.5' or '1/3' to a float."""
    return float(Fraction(text))


def rref(A):
    """reduce matrix a (list if lists) to reduced row echelon from, in place."""
    global pivot
    rows = len(A)
    cols = len(A[0])
    r = 0  #row where the next pivot will be placed

    for c in range(cols):
        if r >= rows:
            break
            #find a row (from r downward) with a non-zero entry in column c

        pivot_row = -1
        for i in range(r, rows):
            if abs(A[i][c]) > 0.000000001:
                pivot_row = i
                break

        if pivot_row == -1:
            continue    #no pivot in this column


#move the pivot row up and scale it so the pivot becoms 1
        A[r], A[pivot_row] = A[pivot_row], A[r]
        p = A[r][c]
        A[r] = [x / p for x in A[r]]

#eliminate column c in every other row
        for i in range(rows):
            if i != r:
                f = A[i][c]
                A[i] = [A[i][j] - f * A[r][j] for j in range(cols)]
        r += 1
    return A


def fmt(x):
    """format a number for printing(4 decimals, no '-0', no trailing '.0')"""
    x = round(x, 4)
    if x == 0:
        x = 0.0
    return f"{x:g}"


def pivot_columns(result, n_vars):
    """returns (column, row) for every non-zero row's pivot"""
    pivots = []
    for row in result:
        for j in range(n_vars):
            if abs(row[j]) > EPS:
                pivots.append((j, row))
                break
    return pivots


def print_general_solution(result, n_vars):
    """print the general solution using parameters t1, t2, ... for free variables"""
    pivots = pivot_columns(result, n_vars)
    pivot_cols = [j for j, _ in pivots]
    free_cols = [j for j in range(n_vars) if j not in pivot_cols]

    #give each free variable a parametr name
    param = {col: f"t{k + 1}" for k, col in enumerate(free_cols)}

    print("free variables:", "، ".join(f"x{c + 1} = {param[c]}" for c in free_cols))
    print("general solution:")

    for j in range(n_vars):
        if j in free_cols:
            print(f"x{j + 1} = {param[j]}")
        else:
            row = next(r for col, r in pivots if col == j)
            text = fmt(row[-1])
            for fc in free_cols:
                coef = -row[fc]          # move to the other side of the equation
                if abs(coef) > EPS:
                    sign = "+" if coef > 0 else "-"
                    text += f" {sign} {fmt(abs(coef))}*{param[fc]}"
            print(f"x{j + 1} = {text}")
    print("(each parameter t can be any real number.)")

def main():
    while True:
        try:
            number_of_equations = int(input("enter the number of equations: "))
            number_of_variables = int(input("enter the number of variables:"))
        except ValueError:
            print("please enter whole numbers only.")
            continue
        if number_of_equations < 1 or number_of_variables < 1:
            print("both values must be at least 1.")
            continue

        number_per_row = number_of_variables + 1
        print(f"enter {number_per_row} numbers for each equation.")
        print(
              "1. the last number you enter represents the right-hand side of the equation \n"
              "2. leave a space between the numbers you enter")

        data = []
        for i in range(number_of_equations):
            while True:
                row = []
                try:
                    row = [
                        to_number(t)
                        for t in input(f"enter the coefficients and constant of equation {i + 1}: ").split()
                    ]
                except (ValueError, ZeroDivisionError):
                    print("only numbers (or fractions like 1/3) are accepted.")
                    continue

                if len(row) == number_per_row:
                    break

                print(f"wrong amount of numbers. please enter exactly {number_per_row} numbers.")

            data.append(row)

        print(" \naugmented matrix:")
        for row in data:
            print(row)

        homogeneous_matrix = all(abs(row[-1]) < EPS for row in data)
        print("the system is homogeneous." if homogeneous_matrix else "the system is not homogeneous.")

        result = rref(data)
        print("\nreduced row echelon form")
        for row in result:
            print([round(x, 4) for x in row])
        number_of_pivots = 0
        no_solution = False
        for row in result:
            all_zero = all(abs(row[j]) < EPS for j in range(number_of_variables))
            if all_zero:
                if abs(row[-1]) > EPS:
                    no_solution = True      #row of the form 0 = nonzero
            else:
                number_of_pivots += 1

        if no_solution:
            print("the system has no solution.")
        elif number_of_pivots == number_of_variables:
            print("the system has a unique solution.")
            for i in range(number_of_variables):
                print(f"x{i + 1} =", fmt(result[i][-1]))
        else:
            print("the system has infinitely many solutions.")
            print_general_solution(result, number_of_variables)


        answer = input("solve another system?(yes/no): ").strip().lower()
        if answer not in ["yes", "yeah", "y"]:
            print("goodbye:)")
            break
if __name__ == "__main__":
    main()