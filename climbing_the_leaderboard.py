from utilities import get_random_list
from utilities import timeit


@timeit
def solve_ranked_pythonic(ranked, player):
    player_rank = []
    unique_sorted_rank = list(set(ranked))
    unique_sorted_rank.sort()

    i = 0
    current_position = len(unique_sorted_rank) + 1
    for score in player:
        if current_position > 1:
            while i < len(unique_sorted_rank) and score >= unique_sorted_rank[i]:
                current_position -= 1
                i += 1

        player_rank.append(current_position)

    return player_rank


@timeit
def solve_ranked_efficient(ranking, player):
    player_rank = []
    player_index = len(player) - 1
    ranking_size = len(ranking)
    ranking_index = 0
    position = 1

    while ranking_index < ranking_size and player_index >= 0:
        current_player = player[player_index]
        ranking_points = ranking[ranking_index]
        if current_player >= ranking_points:
            player_rank.append(position)
            player_index -= 1
        else:
            ranking_index += 1
            if ranking_index < ranking_size and ranking[ranking_index] < ranking[ranking_index - 1]:
                position += 1
    position += 1
    while player_index >= 0:
        player_rank.append(position)
        player_index -= 1

    return player_rank[::-1]


def test_exec_time():
    ranked = get_random_list()
    player = get_random_list()
    solve_ranked_pythonic(ranked, player)
    solve_ranked_efficient(ranked, player)


def test_ranked_pythonic():
    ranked = [100, 90, 90, 80]
    player = [70, 80, 105]
    result = solve_ranked_pythonic(ranked, player)

    assert result == [4, 3, 1]


def test_ranked_efficient():
    ranked = [100, 90, 90, 80]
    player = [70, 80, 105]
    result = solve_ranked_efficient(ranked, player)

    assert result == [4, 3, 1]
