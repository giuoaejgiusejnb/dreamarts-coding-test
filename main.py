import sys
from dataclasses import dataclass


@dataclass
class Railway:
    """ " 路線を表すクラス"""

    id: int  # つながっている駅のID
    distance: float


@dataclass
class Station:
    """駅を表すクラス"""

    id: int
    Railways: list[Railway]

    def add_Railway(self, Railway: Railway) -> None:
        """駅に路線を追加する"""
        self.Railways.append(Railway)


class RailwayNetwork:
    def __init__(self, stations: list[Station]) -> None:
        self.stations = stations

    def find_longest_path(self) -> list[Station]:
        """最長経路を見つけるメソッド"""
        return self._reconstruct_path()

    def _compute_bit_dp(self):
        """ビットDPを用いて最長経路を計算するメソッド"""
        pass

    def _reconstruct_path(self) -> list[Station]:
        """最長経路を復元するメソッド"""
        return []


if __name__ == "__main__":
    # 標準入力から駅と路線の情報を読み込む
    station_map = {}  # 駅IDをキー、Stationオブジェクトを値とする辞書
    for line in sys.stdin:
        parts = [
            item.strip() for item in line.split(",")
        ]  # カンマで分割して前後の空白を削除
        uid = int(parts[0])
        vid = int(parts[1])
        distance = float(parts[2])

        # 駅がまだ辞書に存在しない場合は新しいStationオブジェクトを作成して追加
        if uid not in station_map:
            station_map[uid] = Station(id=uid, Railways=[])
        if vid not in station_map:
            station_map[vid] = Station(id=vid, Railways=[])

        # 路線を作成して両方の駅に追加
        station_map[uid].add_Railway(Railway(id=vid, distance=distance))
        station_map[vid].add_Railway(Railway(id=uid, distance=distance))

    # 最長経路を指定の形で出力
    railway_network = RailwayNetwork(stations=list(station_map.values()))
    for station in railway_network.find_longest_path():
        print(station.id)
