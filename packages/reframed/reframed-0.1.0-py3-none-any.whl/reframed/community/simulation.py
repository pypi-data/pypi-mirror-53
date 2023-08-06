from .solution import CommunitySolution
from ..core.elements import molecular_weight
from ..solvers.solution import Status
from ..core.model import ReactionType
from ..solvers import solver_instance
from warnings import warn
from math import inf


def build_problem(community, growth=1, w_e=0.001, w_r=0.5, spontaneous='spontaneous', min_uptake=False, bigM=1000):

    solver = solver_instance()
    model = community.merged_model

    # create biomass variables
    for org_id in community.organisms:
        solver.add_variable(f"x_{org_id}", 0, 1, update=False)
    # min biomass
    solver.add_variable("x_min", 0, 1, update=False)

    # create all community reactions
    for r_id, reaction in model.reactions.items():
        if reaction.reaction_type == ReactionType.EXCHANGE:
            solver.add_variable(r_id, reaction.lb, reaction.ub, update=False)
        else:
            lb = -inf if reaction.lb < 0 else 0
            ub = inf if reaction.ub > 0 else 0
            solver.add_variable(r_id, lb, ub, update=False)

    # temporary variables for unidirectional values of uptake fluxes
    if min_uptake:
        uptake_vars = []
        for r_id in model.get_exchange_reactions():
            ub = -model.reactions[r_id].lb
            if ub > 0:
                solver.add_variable('f_' + r_id, 0, ub, update=False)
                uptake_vars.append(r_id)

    # temporary variables for computing absolute values of enzymatic reactions
    new_vars = {}
    tmp = {}

    for org_id, organism in community.organisms.items():
        new_vars[org_id] = []
        tmp[org_id] = []

        for r_id, reaction in organism.reactions.items():
            if (org_id, r_id) not in community.reaction_map:
                continue

            new_id = community.reaction_map[(org_id, r_id)]

            # test if reaction is enzymatic
            if reaction.gpr is not None and spontaneous not in reaction.get_genes():
                if reaction.reversible:
                    pos, neg = new_id + '+', new_id + '-'
                    solver.add_variable(pos, 0, inf, update=False)
                    solver.add_variable(neg, 0, inf, update=False)
                    new_vars[org_id].append(pos)
                    new_vars[org_id].append(neg)
                    tmp[org_id].append(new_id)
                else:
                    new_vars[org_id].append(new_id)

    solver.update()

    # sum biomass = 1
    solver.add_constraint("abundance", {f"x_{org_id}": 1 for org_id in community.organisms},
                          rhs=1, update=False)

    # biomass > biomass_min
    for org_id in community.organisms:
        solver.add_constraint("min_biomass", {f"x_{org_id}": 1, "x_min": -1}, '>', 0, update=False)

    # S.v = 0
    table = model.metabolite_reaction_lookup()
    for m_id in model.metabolites:
        solver.add_constraint(m_id, table[m_id], update=False)

    # organism-specific constraints
    for org_id, organism in community.organisms.items():

        for r_id, reaction in organism.reactions.items():
            if (org_id, r_id) not in community.reaction_map:
                continue

            new_id = community.reaction_map[(org_id, r_id)]

            # growth = mu * X
            if r_id == organism.biomass_reaction:
                solver.add_constraint(f"g_{org_id}", {f"x_{org_id}": growth, new_id: -1}, update=False)
            # lb * X < R < ub * X
            else:
                lb = -bigM if reaction.lb is None else reaction.lb
                ub = bigM if reaction.ub is None else reaction.ub

                if lb != 0:
                    solver.add_constraint(f"lb_{new_id}", {f"x_{org_id}": lb, new_id: -1}, '<', 0, update=False)

                if ub != 0:
                    solver.add_constraint(f"ub_{new_id}", {f"x_{org_id}": ub, new_id: -1}, '>', 0, update=False)

        # constrain absolute values
        for r_id in tmp[org_id]:
            pos, neg = r_id + '+', r_id + '-'
            solver.add_constraint('c' + pos, {r_id: -1, pos: 1}, '>', 0, update=False)
            solver.add_constraint('c' + neg, {r_id: 1, neg: 1}, '>', 0, update=False)

        # protein allocation constraints
        alloc_constr = {r_id: w_e for r_id in new_vars[org_id]}
        org_growth = community.reaction_map[(org_id, organism.biomass_reaction)]
        alloc_constr[org_growth] = w_r
        alloc_constr[f"x_{org_id}"] = -1
        solver.add_constraint(f"prot_{org_id}", alloc_constr, '<', 0, update=True)

    # constrain uptake fluxes to negative part of exchange reactions
    if min_uptake:
        for r_id in uptake_vars:
            solver.add_constraint('c_' + r_id, {r_id: 1, 'f_' + r_id: 1}, '>', 0, update=False)

    solver.update()

    # closure for updating growth
    def update_growth(value):
        coefficients = [(f"g_{x}", f"x_{x}", value) for x in community.organisms]
        solver.update_coefficients(coefficients)
    solver.update_growth = update_growth

    if min_uptake:
        solver.uptake_vars = uptake_vars

    return solver


def min_uptake_objective(model):

    objective = {}

    for r_id in model.get_exchange_reactions():

        compounds = model.reactions[r_id].get_substrates()
        metabolite = model.metabolites[compounds[0]]
        formulas = metabolite.metadata['FORMULA']
        weight = molecular_weight(formulas[0])

        if weight is not None:
            objective['f_' + r_id] = weight

    return objective


def binary_search(solver, objective, obj_frac=1, minimize=False, max_iters=100, abs_tol=1e-3):

    previous_value = 0
    value = 1
    fold = 2
    feasible = False
    last_feasible = 0

    for i in range(max_iters):
        diff = value - previous_value

        if diff < abs_tol:
            break

        if feasible:
            last_feasible = value
            previous_value = value
            value = fold*diff + value
        else:
            if i > 0:
                fold = 0.5
            value = fold*diff + previous_value

        solver.update_growth(value)
        sol = solver.solve(objective, get_values=False, minimize=minimize)

        feasible = sol.status == Status.OPTIMAL

    if feasible:
        solver.update_growth(obj_frac * value)
    else:
        solver.update_growth(obj_frac * last_feasible)

    sol = solver.solve(objective, minimize=minimize)

    if i == max_iters - 1:
        warn("Max iterations exceeded.")

    return sol


def SteadierCom(community, obj_frac=1, w_e=0.001, w_r=0.5, min_uptake=False, max_iters=100, spontaneous='spontaneous',
                solver=None):

    if solver is None:
        solver = build_problem(community, w_e=w_e, w_r=w_r, spontaneous=spontaneous, min_uptake=min_uptake)

    if min_uptake:
        objective = min_uptake_objective(community.merged_model)
        sol = binary_search(solver, objective, obj_frac=obj_frac, minimize=True, max_iters=max_iters)
    else:
        objective = "x_min"
        sol = binary_search(solver, objective, obj_frac=obj_frac, minimize=False, max_iters=max_iters)

    solution = CommunitySolution(community, sol)

    if min_uptake:
        solution.total_uptake = sum(-sol.values[r_id]*objective["f_" + r_id] for r_id in solver.uptake_vars)

    return solution


def SteadyCom(community, obj_frac=1, min_uptake=False, max_iters=100, spontaneous='spontaneous', solver=None):
    return SteadierCom(community, obj_frac=obj_frac, w_e=0, w_r=0, min_uptake=min_uptake, max_iters=max_iters,
                       spontaneous=spontaneous, solver=solver)


def SteadierComVA(community, obj_frac=1, w_e=0.001, w_r=0.5, max_iters=100, spontaneous='spontaneous', solver=None):

    if solver is None:
        solver = build_problem(community, w_e=w_e, w_r=w_r, spontaneous=spontaneous)

    objective = {community.merged_model.biomass_reaction: 1}

    sol = binary_search(solver, objective, max_iters=max_iters)

    growth = obj_frac * sol.values[community.merged_model.biomass_reaction]

    solver.update_growth(growth)

    variability = {org_id: [None, None] for org_id in community.organisms}

    for org_id in community.organisms:
        sol2 = solver.solve({f"x_{org_id}": 1}, minimize=True, get_values=False)
        variability[org_id][0] = sol2.fobj

    for org_id in community.organisms:
        sol2 = solver.solve({f"x_{org_id}": 1}, minimize=False, get_values=False)
        variability[org_id][1] = sol2.fobj

    return variability


def SteadyComVA(community, obj_frac=1, max_iters=100, spontaneous='spontaneous', solver=None):
    return SteadierComVA(community, obj_frac=obj_frac, w_e=0, w_r=0, max_iters=max_iters,
                         spontaneous=spontaneous, solver=solver)
