
from collections import defaultdict


def detect_dead_heats(results):
    """
    同じ着順に複数の馬がいる場合、同着として検出する。
    results: [(着順, 馬番, 馬名), ...]
    """
    positions = defaultdict(list)

    for rank, horse_number, horse_name in results:
        if rank <= 3:
            positions[rank].append({
                "horse_number": horse_number,
                "horse_name": horse_name
            })

    return {
        rank: horses
        for rank, horses in positions.items()
        if len(horses) >= 2
    }


if __name__ == "__main__":
    print("JRA同着通知システム")
    print("同着判定プログラムを起動しました。")
