import random
import string


def new_discount_code():
    with open("discounts/discountCodes.txt") as f:
        lines = f.read().splitlines()
    f.close()
    S = 5  # number of characters in the string.
    # call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
    lines.append(ran)
    rewrite_discount_codes(lines)
    return ran


def check_discount(code):
    with open("discounts/discountCodes.txt") as f:
        lines = f.read().splitlines()
    f.close()

    if code in lines:
        lines.remove(code)
        rewrite_discount_codes(lines)
        return True
    return False


def rewrite_discount_codes(codes):
    with open("discounts/discountCodes.txt", "w") as f:
        for line in codes:
            f.write("%s\n" % line)
    f.close()

