from __future__ import print_function
import re

a_of_x = []
b_of_x = []
irr_poly = []

def check_input(word_arr):
    for x in word_arr:
        if (not(re.match("[0-9]+", x))):
            return False
    return True

def check_coef(word_arr, gf):
    for x in word_arr:
        if (int(x) > gf):
            return False
    return True

def input_validation():
    while(True):
        #A(x)
        while(True):
            a_of_x = raw_input("Input A(x): ")
            a_of_x = re.split("[ ]",a_of_x)
            if (check_input(a_of_x) == False):
                print("** Wrong input. Please input A(x) again **\n")
            else:
                break
        #B(x)
        while(True):
            b_of_x = raw_input("Input B(x): ")
            b_of_x = re.split("[ ]",b_of_x)
            if (check_input(b_of_x) == False):
                print("** Wrong input. Please input B(x) again **\n")
            else:
                break

        #P(x)
        while(True):
            irr_poly = raw_input("Input P(x): ")
            irr_poly = re.split("[ ]",irr_poly)
            if (check_input(irr_poly) == False):
                print("** Wrong input. Please input P(x) again **\n")
            else:
                break

        m = len(irr_poly)-1
        gf = 2**m - 1
        if (check_coef(a_of_x, gf) == False):
            print("** Wrong input for A(x). Coefficients must be from 0 to", gf, ", defined by P(x). Try again.")
        elif (check_coef(b_of_x, gf) == False):
            print("** Wrong input for B(x). Coefficients must be from 0 to", gf, ", defined by P(x). Try again.")
        else:
            break

    return(a_of_x, b_of_x, irr_poly)

def outputform(poly, string):
    poly = popzero(poly)
    #print(poly)
    print(string, end='')
    degree = len(poly)-1
    for a in range(degree+1):
        term = int(poly[a])
        term = str(term)
        if (term != '0'): #dont print if zero
            if (a == 0): #if first term, no plus
                if (a == degree): #if last term constant only
                    print("%s" % term, end='')
                elif (a == degree-1):
                    if (term == '1'):
                        term = ''
                    print("%sx" % term, end='')
                else:
                    if (term == '1'):
                        term = ''
                    print("%sx^%d"% (term, degree-a), end='')
            else:
                if (a == degree):
                    print(" + %s" % term, end='')
                elif (a == degree-1):
                    if (term == '1'):
                        term = ''
                    print(" + %sx" % term, end='')
                else:
                    if (term == '1'):
                        term = ''
                    print(" + %sx^%d"% (term, degree-a), end='')
        elif (term == '0' and degree == 0 and a == degree):
            print("%s" % term, end='')
    print()

def output():
    global a_of_x, b_of_x, irr_poly
    print("\nInputs")
    outputform(a_of_x, "A(x): ")
    outputform(b_of_x, "B(x): ")
    outputform(irr_poly, "P(x): ")

def popzero(poly):
    if (len(poly) > 1):
        while (poly[0] == 0 or poly[0] == '0'):
            poly.pop(0)
            if (len(poly) == 1):
                return poly
    return poly

def popzero_rev(poly):
    poly_rev = poly[::-1]
    poly_rev = popzero(poly_rev)
    return poly_rev[::-1]

def modulo(poly):
    for i in range(len(poly)):
        poly[i] = poly[i] % 2
    return poly

def addition(aox, box):
    #aox > box
    if (len(aox) < len(box)):
        temp = aox[:]
        aox = box[:]
        box = temp[:]

    plus = []
    for i in range(len(aox)):
        if (i < len(box)):
            a = int(aox[i])
            b = int(box[i])
            plus.append(a+b)
        else:
            plus.append(int(aox[i]))
    return(plus)

def subtraction(aox, box):
    box_neg = box[:]
    for i in range(len(box)):
        box_neg[i] = int(box[i])* -1
    poly = addition(aox, box_neg)
    return poly

def abs_subtraction(aox, box):
    box_neg = box[:]
    for i in range(len(box)):
        box_neg[i] = int(box[i])* -1
    poly = addition(aox, box_neg)
    for j in range(len(poly)):
        poly[j] = abs(int(poly[j]))
    poly = popzero_rev(poly)
    return poly

def multiplication(aox, box):
    if (len(aox) < len(box)):
        temp = aox[:]
        aox = box[:]
        box = temp[:]
    mul_poly = [0]
    for i in range(len(box)):
        sca_mul = []
        f = int(box[i])
        #shift
        for s in range(i):
            sca_mul.append(0)
        for j in range(len(aox)):
            sca_mul.append(int(aox[j])*f)
        #print("SMult",sca_mul)
        mul_poly = addition(sca_mul, mul_poly)
        #print("AMult",mul_poly)
    #print("final", mul_poly)
    return mul_poly

def division(aox, box):
    high = aox[:]
    low = box[:]
    #diff =
    #print(high, low)
    h = len(high)-1
    delta = len(high) - len(low)
    quotient = [0]
    for s in range(delta): #shift
        quotient.append(0)
    #print(high, low, delta)
    while (delta >= 0):
        for s in range(delta): #shift
            low.insert(0,0)
        #print(high, low)

        multiplier = int(high[h]) // int(low[h])
        quotient[delta] = multiplier
        for i in range(len(low)): #multiply
            low[i] = int(low[i])*multiplier
        #print(multiplier, high, low)

        high = abs_subtraction(high, low)
        low = box[:]
        delta = len(high) - len(low)
        h = len(high)-1
        #print(high, low, delta)
    rem = high
    return quotient, rem


def simplify_irr(poly, pox_org):
    pox = pox_org[:]
    m = len(pox)-1
    pox.pop()
    n = len(poly)-1 #P(x) and poly discrepancy
    shift = n - m
    for s in range(shift):
        pox.insert(0, 0)
    #outputform(pox[::-1], "shifted pox ")
    #print()

    while(len(poly)-1 >= m):
        coef = poly.pop()
        if (coef != 0):
            #print("time to add ", coef, poly, pox)
            poly = addition(poly, pox)
            poly = modulo(poly)
            #print(poly)
        pox.pop(0)
    #print(poly)
    return poly

op = -1
while(True): #whole program
    a_of_x, b_of_x, irr_poly = input_validation()
    m = len(irr_poly)-1

    aox = a_of_x[::-1]
    box = b_of_x[::-1]
    pox = irr_poly[::-1]

    output()

    while(True): #operations
        print("\n[1] A(x) + B(x)   [2] A(x) - B(x)   [3] A(x) x B(x)   [4] A(x) / B(x)   [5] Change Inputs   [6] Quit\n")
        op = raw_input("Operation (refer above): ")
        op = int(op)
        print()
        if (op == 1):
            print("[1] ADDITION: A(x) + B(x)\n----------------------------------------------------\nSolutions:")
            sum_poly = addition(aox, box)
            outputform(sum_poly[::-1], "A(x) + B(x): \n                      ")
            sum_poly = modulo(sum_poly)
            outputform(sum_poly[::-1], "A(x) + B(x) mod 2: \n                      ")
            print("----------------------------------------------------")
            outputform(a_of_x, "A(x): ")
            outputform(b_of_x, "B(x): ")
            outputform(sum_poly[::-1], "Final Answer A(x) + B(x): ")

        elif (op == 2):
            print("[2] SUBTRACTION: A(x) - B(x)\n----------------------------------------------------\nSolutions:")
            diff_poly = subtraction(aox, box)
            outputform(diff_poly[::-1], "A(x) - B(x): \n                      ")
            diff_poly = modulo(diff_poly)
            outputform(diff_poly[::-1], "A(x) - B(x) mod 2: \n                      ")
            print("----------------------------------------------------")
            outputform(a_of_x, "A(x): ")
            outputform(b_of_x, "B(x): ")
            outputform(diff_poly[::-1], "Final Answer A(x) - B(x): ")

        elif (op == 3):
            print("[3] MULTIPLICATION: A(x) x B(x)\n----------------------------------------------------\nSolutions:")
            mul_poly = multiplication(aox, box)
            outputform(mul_poly[::-1], "A(x) x B(x): \n                      ")
            mul_poly = modulo(mul_poly)
            outputform(mul_poly[::-1], "A(x) x B(x) mod 2: \n                      ")
            mul_poly = simplify_irr(mul_poly, pox)
            outputform(mul_poly[::-1], "A(x) x B(x) mod P(x): \n                      ")
            print("----------------------------------------------------")
            outputform(a_of_x, "A(x): ")
            outputform(b_of_x, "B(x): ")
            outputform(mul_poly[::-1], "Final Answer A(x) x B(x): ")

        elif (op == 4):
            print("[4] DIVISION: A(x) / B(x)\n----------------------------------------------------\nSolutions:")
            div_poly, rem_poly = division(aox, box)
            outputform(div_poly[::-1], "A(x) / B(x): \n                      Quotient: ")
            outputform(rem_poly[::-1], "                      Remainder: ")
            div_poly = modulo(div_poly)
            rem_poly = modulo(rem_poly)
            outputform(div_poly[::-1], "A(x) / B(x) mod 2: \n                      Quotient: ")
            outputform(rem_poly[::-1], "                      Remainder: ")
            div_poly = simplify_irr(div_poly, pox)
            rem_poly = simplify_irr(rem_poly, pox)
            outputform(div_poly[::-1], "A(x) / B(x) mod P(x): \n                      Quotient: ")
            outputform(rem_poly[::-1], "                      Remainder: ")
            print("----------------------------------------------------")
            outputform(a_of_x, "A(x): ")
            outputform(b_of_x, "B(x): ")
            outputform(div_poly[::-1], "Final Answer A(x) / B(x) - Quotient: ")
            outputform(rem_poly[::-1], "A(x) / B(x) - Remainder: ")

        elif (op == 5):
            print("[5] CHANGE INPUTS\n")
            break

        elif (op == 6):
            print("[5] QUIT\n")
            break

        else:
            print("Invalid operation. Try again")

    if (op == 6):
        break
