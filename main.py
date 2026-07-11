import sys
import time
from dataclasses import dataclass


@dataclass
class Railway:
    """路線を表すクラス"""

    id: int  # つながっている駅のID
    distance: float  # 路線の距離


@dataclass
class Station:
    """駅を表すクラス"""

    id: int  # 駅のID
    railways: list[Railway]  # つながっている路線のリスト

    def add_railway(self, railway: Railway) -> None:
        """駅に路線を追加する"""

        self.railways.append(railway)


class RailwayNetwork:
    """鉄道ネットワークを表すクラス"""

    def __init__(self, stations: list[Station]) -> None:
        self.stations = stations
        self.N = len(self.stations)  # 駅の数
        # 駅の「id」から、stationsリストの「インデックス」へのマッピング
        self.id_to_index: dict[int, int] = {
            station.id: i for i, station in enumerate(self.stations)
        }

    def find_longest_path(self) -> list[Station]:
        """最長経路を見つけるメソッド"""

        dp, prev_idxs = self._compute_bit_dp()
        return self._reconstruct_path(dp, prev_idxs)

    def _compute_bit_dp(self) -> tuple[list[list[float]], list[list[int]]]:
        """ビットDPを用いて最長経路を計算するメソッド"""

        NEG_INF = float("-inf")

        # dp[ビット集合][現在の末尾頂点] = そのビット集合の経路で，その末尾頂点の状態における最長経路の長さ
        dp = [[NEG_INF] * self.N for _ in range(1 << self.N)]
        # 経路復元用の配列
        # prev_idxs[ビット集合][現在の末尾頂点] = そのビット集合の経路で，その末尾頂点の状態における最長経路の一つ前の駅のインデックス
        prev_idxs = [[-1] * self.N for _ in range(1 << self.N)]

        # 初期状態: 任意の1駅から始めて，その駅のみで終わる場合の最長経路の長さは0
        for i in range(self.N):
            dp[1 << i][i] = 0.0

        for visited_set in range(1 << self.N):
            for current_idx in range(self.N):
                if dp[visited_set][current_idx] == NEG_INF:
                    continue  # この状態がまだ計算されていない＝この状態になることはないのでスキップ

                for railway in self.stations[current_idx].railways:
                    next_idx = self.id_to_index.get(railway.id)
                    if next_idx is None:
                        continue
                    if visited_set & (1 << next_idx):
                        continue  # next_idxが訪問済みの場合はスキップ

                    next_visited_set = visited_set | (1 << next_idx)
                    new_length = dp[visited_set][current_idx] + railway.distance
                    if dp[next_visited_set][next_idx] < new_length:
                        # dpを更新
                        dp[next_visited_set][next_idx] = new_length
                        # 経路復元用に前の駅のインデックスを記録
                        prev_idxs[next_visited_set][next_idx] = current_idx

        return (dp, prev_idxs)

    def _reconstruct_path(
        self, dp: list[list[float]], prev_idxs: list[list[int]]
    ) -> list[Station]:
        """最長経路を復元するメソッド"""

        # まず，dpの中で最長経路の長さを持つ状態を探す
        max_length = float("-inf")
        best_states = []  # 最長経路の長さを持つ状態のリスト [[ビット集合, 現在の末尾頂点] の形で格納]
        for visited_set in range(1 << self.N):
            for current_idx in range(self.N):
                if dp[visited_set][current_idx] > max_length:
                    max_length = dp[visited_set][current_idx]
                    best_states = [[visited_set, current_idx]]
                elif dp[visited_set][current_idx] == max_length:
                    best_states.append([visited_set, current_idx])

        # 最長経路を求める
        best_state = best_states[0]  # 今回は一つだけ出力
        current_visited_set = best_state[0]
        current_idx = best_state[1]
        best_paths = []  # 最長経路の末尾駅のIDを格納
        while current_visited_set:
            best_paths.append(current_idx)
            prev_idx = prev_idxs[current_visited_set][current_idx]
            current_visited_set ^= 1 << current_idx
            current_idx = prev_idx

        # 後ろから追加しているので逆順に
        return [self.stations[i] for i in reversed(best_paths)]


if __name__ == "__main__":
    # 標準入力から駅と路線の情報を読み込む
    s = time.time()
    station_map = {}  # 駅IDをキー、Stationオブジェクトを値とする辞書
    for line in sys.stdin:
        if not line.strip():
            continue  # 空行はスキップ

        parts = [
            item.strip() for item in line.split(",")
        ]  # カンマで分割して前後の空白を削除
        uid = int(parts[0])
        vid = int(parts[1])
        distance = float(parts[2])

        # 駅がまだ辞書に存在しない場合は新しいStationオブジェクトを作成して追加
        if uid not in station_map:
            station_map[uid] = Station(id=uid, railways=[])
        if vid not in station_map:
            station_map[vid] = Station(id=vid, railways=[])

        # 路線を作成して両方の駅に追加
        station_map[uid].add_railway(Railway(id=vid, distance=distance))
        station_map[vid].add_railway(Railway(id=uid, distance=distance))

    # 最長経路を指定の形で出力
    railway_network = RailwayNetwork(stations=list(station_map.values()))
    for station in railway_network.find_longest_path():
        print(station.id, end="\r\n")
    t = time.time() - s
    print(f"Execution time: {t:.6f} seconds", file=sys.stderr)
