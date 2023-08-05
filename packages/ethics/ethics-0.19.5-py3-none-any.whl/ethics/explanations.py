from ethics.language import *
from ethics.solver import *


def find_all_models(formula):
    return list(map(set, smt_all_models(formula)))


def hitting_sets_gde(sets):
    sets = sorted(sets, key=len)
    hitting_sets = [set()]
    for current_set in sets:
        new_hitting_sets = list(hitting_sets)
        for hitting_set in hitting_sets:
            # Check if hitting_set hits current_set
            if hitting_set.intersection(current_set) == set():
                new_hitting_sets.remove(hitting_set)
                # no hit
                for element in current_set:
                    candidate = hitting_set.union({element})

                    is_valid = True
                    for hs in new_hitting_sets:
                        if hs.issubset(candidate):
                            is_valid = False
                            break
                    if is_valid:
                        new_hitting_sets.append(candidate)

        hitting_sets = list(new_hitting_sets)

    return hitting_sets

def remove_trivial_clauses(clauses):
    r = []
    for c in clauses:
        neg_c = {n.getNegation() for n in c}
        if len(c & neg_c) == 0:
            r.append(c)
    return r

def compute_primes(formula):
    models = find_all_models(formula)
    prime_implicates = remove_trivial_clauses(hitting_sets_gde(models))
    prime_implicants = remove_trivial_clauses(hitting_sets_gde(prime_implicates))
    return prime_implicants, prime_implicates


def generate_reasons(model, principle, *args):
    perm = principle.permissible()

    # Compute prime implicants and prime implicates
    if perm:
        cants, cates = compute_primes(principle.buildConjunction().nnf())
    else:
        cants, cates = compute_primes(Not(principle.buildConjunction()).nnf())

    # Sufficient reasons from prime implicants
    suff = [Formula.makeConjunction(c) for c in cants if model.models(Formula.makeConjunction(c))]

    # Necessary reasons from prime implicates
    necc = set()
    for cc in cates:
        necc_reason = []
        for c in cc:
            if model.models(c):
                necc_reason.append(c)
        if len(necc_reason) > 0:
            necc.add(Formula.makeDisjunction(necc_reason))
    necc = list(necc)

    # Preparing output
    result = []
    for c in suff:
        result.append({"model": model, "perm": perm, "reason": c, "type": "sufficient"})
    for c in necc:
        result.append({"model": model, "perm": perm, "reason": c, "type": "necessary"})

    return result


def generate_inus_reasons(reasons):
    suff = [r["reason"] for r in reasons if r["type"] == "sufficient"]
    nec = [r["reason"] for r in reasons if r["type"] == "necessary"]
    inus = []
    for rn in nec:
        rn_check = None
        rn_check = rn.getClause()
        for rs in suff:
            rs_check = None
            rs_check = rs.getConj()
            if set(rn_check) <= set(rs_check):
                inus.append(Formula.makeDisjunction(rn_check))
                break
    return inus


