# %%

class PARENT_OPERATOR (Enum):
    RWS = 0
    SUS = 1
    TOURNAMENT_RANKING = 2


def parent_selection_function(parent_selection_input):
    if parent_selection_input == PARENT_OPERATOR.RWS.value:
        return rws
    elif parent_selection_input == PARENT_OPERATOR.SUS.value:
        return sus
    elif parent_selection_input == PARENT_OPERATOR.TOURNAMENT_RANKING.value:
        return tournament_ranking
    return 


def rws():
    return

def sus():
    return

def tournament_ranking():
    return






# %%