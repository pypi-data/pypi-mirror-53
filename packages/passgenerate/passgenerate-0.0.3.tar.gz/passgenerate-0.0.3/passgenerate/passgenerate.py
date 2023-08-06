import random


def generate(
    times=5,
    passlength=32,
    include=[],
    exclude=[],
    include_numbers=True,
    include_big_letters=True,
    include_little_letters=True,
    include_special_chars1=False,
    include_special_chars2=False,
    include_special_chars3=False,
    include_special_chars4=False,
):
    if times == 0:
        return []

    included_chars = []

    special_chars1 = range(32, 48)
    numbers = range(48, 58)
    special_chars2 = range(58, 65)
    big_letters = range(65, 91)
    special_chars3 = range(91, 97)
    little_letters = range(97, 123)
    special_chars4 = range(123, 127)

    if include_special_chars1:
        included_chars += [chr(i) for i in special_chars1]
    if include_numbers:
        included_chars += [chr(i) for i in numbers]
    if include_special_chars2:
        included_chars += [chr(i) for i in special_chars2]
    if include_big_letters:
        included_chars += [chr(i) for i in big_letters]
    if include_special_chars3:
        included_chars += [chr(i) for i in special_chars3]
    if include_little_letters:
        included_chars += [chr(i) for i in little_letters]
    if include_special_chars4:
        included_chars += [chr(i) for i in special_chars4]

    included_chars += [i for i in include]
    for i in exclude:
        if i in included_chars:
            included_chars.remove(i)

    ic_size = len(included_chars)
    password = ""
    for i in range(0, passlength):
        password += included_chars[
            random.randint(0, ic_size - 1)
        ]

    return [
        password,
        *generate(
            times - 1,
            passlength,
            include,
            exclude,
            include_numbers,
            include_big_letters,
            include_little_letters,
            include_special_chars1,
            include_special_chars2,
            include_special_chars3,
            include_special_chars4,
        ),
    ]
