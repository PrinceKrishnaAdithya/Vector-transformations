import numpy as np
import sympy as sp
import time
import itertools

variables = [chr(x) for x in range(97, 123)]

def printMapping(inp, mapping):
    print("f(v)->w")
    if len(inp) == len(mapping):
        for i in range(len(inp)):
            print(f"{variables[i]}    {mapping[i]}")
    elif len(inp) > len(mapping):
        for i in range(len(inp)):
            if i < len(mapping):
                print(f"{variables[i]}    {mapping[i]}")
            if i >= len(mapping):
                print(f"{variables[i]}")
    elif len(inp) < len(mapping):
        for i in range(len(mapping)):
            if i < len(inp):
                print(f"{variables[i]}    {mapping[i]}")
            if i >= len(inp):
                print(f"     {mapping[i]}")

def RealSetMapping(inp, V, W):
    try:
        mapping = []
        for i in range(W):
            mapping.append(input(f"Enter mapping rule for entry {i+1} of resulting vector:"))
        selected_variables = variables[:V]
        M_variables = sp.symbols(' '.join(selected_variables))
        if isinstance(M_variables, sp.Symbol):
            M_variables = (M_variables,)
        mapping = [sp.sympify(x) for x in mapping]
        printMapping(inp, mapping)
        M_values = {}
        for i in range(len(selected_variables)):
            M_values[str(M_variables[i])] = inp[i]
        resultVector = [expr.subs(M_values) for expr in mapping]
        return resultVector
    except Exception as e:
        print(f"Error in RealSetMapping: {e}")

def LinearMapping(inp, V, W):
    try:
        d_min = min(V)
        d_max = max(V)
        cd_min = min(W)
        cd_max = max(W)
        resultVector = []
        for i in inp:
            resultVector.append(round(cd_min + ((i - d_min) / (d_max - d_min)) * (cd_max - cd_min)))
        return resultVector
    except Exception as e:
        print(f"Error in LinearMapping: {e}")

def CustomSetMapping(inp, V, W):
    try:
        mapping = []
        for i in range(len(inp)):
            mapping.append(input(f"Enter mapping rule for entry {i+1} of resulting vector:"))
        selected_variables = variables[:len(inp)]
        M_variables = sp.symbols(' '.join(selected_variables))
        if isinstance(M_variables, sp.Symbol):
            M_variables = (M_variables,)
        mapping = [sp.sympify(x) for x in mapping]
        printMapping(inp, mapping)
        M_values = {}
        for i in range(len(selected_variables)):
            M_values[str(M_variables[i])] = inp[i]
        resultVector = [expr.subs(M_values) for expr in mapping]
        ValidMapping = True
        print(resultVector)
        for i in resultVector:
            if i not in W:
                print(f"{i} not in the co-domain set")
                print("The given mapping is not valid")
                ValidMapping = False
                break
        if ValidMapping == False:
            print("Generating a valid mapping", end='')
            for i in range(3):
                print('.', end='')
                time.sleep(3)
            print("\nMapping formula:")
            print("co-domain_Minimum + ((x- domain_minimum)/(domain_max - domain_min)) * (co-domain_max - co_domain_min)")
            resultVector = LinearMapping(inp, V, W)
            return resultVector
        return resultVector
    except Exception as e:
        print(f"Error in CustomSetMapping: {e}")

def get_vector():
    while True:
        try:
            vector = input("Enter vector elements separated by spaces: ")
            vector = np.array([float(x) for x in vector.split()])
            return vector
        except ValueError:
            print("Invalid input. Please enter numeric values.")

def get_matrix(vector_length):
    while True:
        try:
            rows = int(input(f"Enter the number of rows for the matrix: "))
            cols = vector_length
            
            if rows != cols:
                print(f"The matrix must have {vector_length} columns to multiply with the vector of size {vector_length}.")
                continue

            matrix = []
            for i in range(rows):
                row = input(f"Enter row {i+1} elements separated by spaces: ")
                matrix.append([float(x) for x in row.split()])

            matrix = np.array(matrix)
            if matrix.shape[1] != vector_length:
                print(f"Each row must have {vector_length} elements. Please try again.")
            else:
                return matrix
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        except Exception as e:
            print(f"An error occurred: {e}")

def matrix_transform(vector, matrix):
    try:
        result = np.dot(matrix, vector)
        print("Result of matrix transformation:")
        print(result)
    except ValueError as ve:
        print(f"Error in matrix multiplication: {ve}")

while True:
    try:
        Mchoice = int(input("Menu:\n1. R set mapping\n2. Custom set mapping\n3. Matrix transformation\n4. Exit\nChoose an option: "))
        
        if Mchoice == 1:
            try:
                V = int(input("Enter the domain of the transformation (Real numbers 1, 2, 3, 4...): "))
                W = int(input("Enter the co-domain of the transformation: "))
                print(f"f(R^{V})->R^{W}")
                print("Give the input vector (element by element):")
                inputVector = [int(input()) for i in range(V)]
                print(f"f({inputVector}) = {RealSetMapping(inputVector, V, W)}")
            except ValueError:
                print("Invalid input. Please enter integers for V and W.")
        
        elif Mchoice == 2:
            try:
                v = int(input("Enter the size of domain set: "))
                w = int(input("Enter the size of co-domain set: "))
                V = set()
                W = set()

                tempv = int(input("For domain set:\n1. Sequence of numbers\n2. Custom input\n"))
                if tempv == 1:
                    start = int(input("Enter starting number of sequence: "))
                    end = int(input("Enter ending number of sequence: "))
                    tempv1 = input("Do you want an increment value in the sequence (y/n): ")
                    step = 1 if tempv1 == 'n' else int(input("Enter increment value: "))
                    if abs(((end - start) // step)) > v:
                        print("The given input exceeds the size of domain set")
                        continue
                    for i in range(start, end + 1, step):
                        V.add(i)
                elif tempv == 2:
                    print("Enter each element of the set:")
                    for i in range(v):
                        V.add(int(input()))

                tempw = int(input("For co-domain set:\n1. Sequence of numbers\n2. Custom input\n"))
                if tempw == 1:
                    start = int(input("Enter starting number of sequence: "))
                    end = int(input("Enter ending number of sequence: "))
                    tempw1 = input("Do you want an increment value in the sequence (y/n): ")
                    step = 1 if tempw1 == 'n' else int(input("Enter increment value: "))
                    if abs(((end - start) // step)) > w:
                        print("The given input exceeds the size of co-domain set")
                        continue
                    for i in range(start, end + 1, step):
                        W.add(i)
                elif tempw == 2:
                    print("Enter each element of the set (duplicates will be discarded):")
                    for i in range(w):
                        W.add(int(input()))

                print("Given domain:", V, sep='\n')
                print("Given co-domain:", W, sep='\n')
                Vt = int(input("Enter size of input vector for transformation: "))
                print("Give the input vector:")
                inputVector = [int(input()) for i in range(Vt)]
                for i in inputVector:
                    if i not in V:
                        print(f"{i} is not in the domain")
                print(f"f({inputVector}) = {CustomSetMapping(inputVector, V, W)}")
            except ValueError:
                print("Invalid input. Please enter integers.")
                
        
        elif Mchoice == 3:
            vector = get_vector()
            matrix = get_matrix(len(vector))
            matrix_transform(vector, matrix)
        
        elif Mchoice == 4:
            print("Exiting",end='')
            for i in range(3):
                print('.', end='')
                time.sleep(3)
            break
        
        else:
            print("Enter a valid choice")
    
    except ValueError:
        print("Invalid input. Please enter an integer option.")