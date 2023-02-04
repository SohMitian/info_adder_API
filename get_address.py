import googlemaps
import pprint
googleapikey = ''
gmaps = googlemaps.Client(key=googleapikey)

# 座標（経緯度）から住所を取得する関数
def rev_geo(lat, lon):
  geocord = lat + ", " + lon
  results = gmaps.reverse_geocode((geocord), language='ja')
  add = [d.get('formatted_address') for d in results]
  list_add = add[1].split()
  return list_add[1]

# 近くの施設を取得する関数
def nearby_place(lat, lon):
  loc = {'lat': lat, 'lng': lon}
  place_results = gmaps.places_nearby(location=loc, radius=20, keyword='コンビニ',language='ja')
  return place_results['results']

# 郵便番号を取得する関数
def get_zipcode(address):
  place_results = gmaps.find_place(input=address, input_type='textquery', fields=['name'], language='ja')
  temp_list = place_results['candidates'][0]['name'].split()
  zipcode = temp_list[0].replace('〒', '')
  return(zipcode)

def main():
  place_results = nearby_place(35.67508051373962, 139.76040808393296)
  pprint.pprint(place_results[0])
  # for i in place_results:
  #   pprint.pprint(i['name'])
  # print(get_zipcode('東京都千代田区有楽町１丁目９−１'))

if __name__ == '__main__':
  main()