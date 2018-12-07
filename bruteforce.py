from fractions import Fraction

def brute_force(x, y):
    return brute_force_helper(Fraction(x, y), 1)

def brute_force_helper(num, term_count):
    if num.numerator == 1:
        return [num]
    else:
        expansion = mustapha(num, term_count)
        if expansion:
            return expansion
        else:
            brute_force_helper(num, term_count + 1)

def mustapha(num, term_count):
    if term_count == 4:
        exit()
    if num.numerator == 1:
        return [num]
    elif term_count == 1:
        return None

    denominator = 2
    while num - Fraction(1, denominator) < 0:
        denominator += 1
    min_denominator = denominator

    while num - (Fraction(1, denominator) * term_count) > 0:
        denominator += 1
    max_denominator = denominator

    print min_denominator, max_denominator

    for denominator in range(min_denominator, max_denominator):
        result = mustapha(num - Fraction(1, denominator), term_count - 1)
        if result:
            return [Fraction(1, denominator)].append(result)

    return None


print(brute_force(4, 17))
