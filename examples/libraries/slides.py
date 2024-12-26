"""Slides"""

# Set from CLI
signature = None
available = None

cons = []


def nda_is_signed():
    return signature == 'jason'


def slides_are_available():
    return available


def check_contents_wrt_nda():
    x = "ok"
    cons.append(x)
    return x


def check_grammar_typos():
    x = "loos good!"
    cons.append(x)
    return x


def all_conditions_are_met():
    return all(cons)
