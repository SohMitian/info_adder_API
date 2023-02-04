import requests
import pprint

# 座標の最寄り駅を取得する関数 引数:lon=経度, lat=緯度 
def nearest_station(lon: float, lat: float) -> object:
  '''最寄り駅を取得

  指定した座標の最寄り駅情報を取得する関数

  Args:
    lon (float): 経度
    lat (float): 緯度
  
  Returns:
    JSON: 最寄り駅情報
  '''
  # HeartRails Express の最寄り駅API
  url = "http://express.heartrails.com/api/json?method=getStations"
  # 経緯度を入力 x=経度, y=緯度
  payload = {"x":lon, "y":lat}
  r_json = requests.get(url, params=payload).json()
  # 最寄り駅情報を返す
  return r_json['response']['station'][0]


# デバッグ用
def main():
  r_json = nearest_station(139.76040808393296, 35.67508051373962)
  pprint.pprint(r_json)

if __name__ == "__main__":
    main()