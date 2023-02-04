import os
from lxml import etree
import get_address as GA
import get_nearest_station as GNS

def add_info_gml(gml, file_name):
  # ファイル名と拡張子を分離
  file, ext = os.path.splitext(file_name)

  # XML ファイルから ElementTree オブジェクトを生成
  parser = etree.XMLParser(remove_blank_text=True)
  tree = etree.parse(gml, parser)

  # # 名前空間を取得
  # namespaces = {node[0]: node[1] for _, node in etree.iterparse(gml, events=['start-ns'])}
  # # 名前空間を設定
  # for key, value in namespaces.items():
  #   etree.register_namespace(key, value)

  # 先頭要素を表す Element オブジェクトを取得
  root = tree.getroot()
  #　処理対象のオブジェクト総数
  all_object_count = len(root.findall('{http://www.opengis.net/citygml/2.0}cityObjectMember'))
  #　処理済みのオブジェクト数
  processed_object_count = 0

  for building in root.findall('{http://www.opengis.net/citygml/2.0}cityObjectMember'):
    for gml_posList in building[0].findall('{http://www.opengis.net/citygml/building/2.0}lod0RoofEdge')[0][0][0][0][0][0]:
      posList = gml_posList.text.split()
      # 経度
      lon = posList[1]
      # 緯度
      lat = posList[0]

      '''建物の所在を取得して追記'''
      address_element = etree.SubElement(building[0], 'address')
      address = GA.rev_geo(lat, lon)
      address_element.text = address

      '''建物の郵便番号を取得して追記'''
      zipcode_element = etree.SubElement(building[0], 'zipcode')
      zipcode_element.text = GA.get_zipcode(address)

      '''最寄り駅の情報を取得して追記'''
      #最寄駅情報を取得
      nearest_station_json = GNS.nearest_station(lon, lat)
      #最寄り駅の子要素を作成
      nearest_station_element = etree.SubElement(building[0], 'nearestStation')

      #路線名
      nearest_station_line = etree.SubElement(nearest_station_element, 'line')
      #路線名を追加
      nearest_station_line.text = nearest_station_json['line']

      #駅名
      nearest_station_name = etree.SubElement(nearest_station_element, 'name')
      #駅名を追加
      nearest_station_name.text = nearest_station_json['name']

      #駅までの距離
      nearest_station_distance = etree.SubElement(nearest_station_element, 'distance')
      #距離(m)を追加
      nearest_station_distance.text = nearest_station_json['distance']


      '''周辺施設情報を取得して追記'''
      #周辺施設の情報を取得
      nearby_facilities_json = GA.nearby_place(lat, lon)
      #周辺施設エレメント（子）
      nearby_facilities_element = etree.SubElement(building[0], 'nearbyFacilities')
      #コンビニエレメント　（孫）
      facilities_category_element = etree.SubElement(nearby_facilities_element, 'convenienceStore')
      for nearby_facilities_object in nearby_facilities_json:
        
        #周辺施設エレメント(孫)
        facilities_element = etree.SubElement(facilities_category_element, 'facilities')

        #施設名エレメント(ひ孫)
        nearby_facilities_name = etree.SubElement(facilities_element, 'name')
        #施設名を追加
        nearby_facilities_name.text = nearby_facilities_object['name']

        #座標エレメント(ひ孫)
        nearby_facilities_location = etree.SubElement(facilities_element, 'location')
        #座標を追加
        location = str(nearby_facilities_object['geometry']['location']['lat']) + ' '  + str(nearby_facilities_object['geometry']['location']['lng'])
        nearby_facilities_location.text = location

        #近くの建物エレメント(ひ孫)
        nearby_facilities_location = etree.SubElement(facilities_element, 'vicinity')
        #近くの建物を追加
        nearby_facilities_location.text = nearby_facilities_object['vicinity']

    # 処理済みオブジェクト数を加算
    processed_object_count += 1
    # 処理状況をprint
    print('{}/{}'.format(processed_object_count, all_object_count))
  
  # ファイル名に追加した情報名を追記
  file = file + '_all'
  out_file_name = file + ext

  # gmlの情報を更新
  tree = etree.ElementTree(root)

  '''書き出し'''
  tree.write(out_file_name, encoding="UTF-8", xml_declaration=True, pretty_print=True)
  return out_file_name

def main():
  add_info_gml('53392546_bldg_6697_2_op.gml')

if __name__ == '__main__':
  main()