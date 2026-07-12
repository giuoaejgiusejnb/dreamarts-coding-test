import sys
from collections import deque

# import time
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

    def find_longest_path(self) -> list[int]:
        """最長経路を見つけるメソッド"""

        max_length = float("-inf")
        best_path_ids: list[int] = []
        # 始点を固定して最長距離を求める
        # 始点と終点のみ一致していいという条件なので，始点を特別扱い
        for station in self.stations:
            start_id = station.id
            # dfsで最長経路を探索
            current_max_length, current_path_ids = self._dfs(start_id)
            # 現在の最長経路がこれまでの最長経路よりも長ければ更新
            if current_max_length > max_length:
                max_length = current_max_length
                best_path_ids = current_path_ids

        return best_path_ids

    def _dfs(self, start_id: int) -> tuple[float, list[int]]:
        """深さ優先探索で最長経路を見つけるメソッド"""

        # [現在の経路（駅IDのリスト）, 現在の距離]
        stack = deque([([start_id], 0.0)])
        # 現在の最長距離
        max_dist = float("-inf")
        # 現在の最長経路
        best_path_ids: list[int] = []

        while stack:
            path_ids, dist = stack.pop()
            # 現在の駅を取得
            curr_station = self.stations[self.id_to_index[path_ids[-1]]]
            # 現在の距離がこれまでの最長距離よりも長ければ更新
            if dist > max_dist:
                max_dist = dist
                best_path_ids = path_ids

            for r in curr_station.railways:
                # 始点に戻る場合の処理（サイクルを形成する場合）
                if r.id == start_id and len(path_ids) > 2:
                    total_dist = dist + r.distance
                    if total_dist > max_dist:
                        max_dist = total_dist
                        best_path_ids = path_ids + [start_id]
                        continue  # サイクルを形成する場合は、次のノードへ進む前にスキップ

                # 次のノードへ（訪問済み駅はスキップ）
                if r.id in path_ids:
                    continue
                stack.append((path_ids + [r.id], dist + r.distance))

        return max_dist, best_path_ids


if __name__ == "__main__":
    # 標準入力から駅と路線の情報を読み込む
    # s = time.time()
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
    for station_id in railway_network.find_longest_path():
        print(station_id, end="\r\n")
    # t = time.time() - s
    # print(f"Execution time: {t:.6f} seconds", file=sys.stderr)
