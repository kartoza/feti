# coding=utf-8

# Needs GeoPy :: https://github.com/geopy/geopy

import json
import urllib.error
import urllib.error
import urllib.parse
import urllib.parse
import urllib.request
import urllib.request

import psycopg2

from geopy.geocoders import GoogleV3

USER = ''
PASSWORD = ''


class OneMap(object):
    SERVER = 'http://www.1map.co.za'
    PATH_LOGIN = '/api/auth/login'
    PATH_LOGOUT = '/api/auth/logout'
    PATH_ADDRESS = '/api/address/search'

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.token = None
        self.serial = None

        self.login()

    def _request(self, url):
        raw_json_content = urllib.request.urlopen(url, timeout=30).read()
        json_content = json.loads(raw_json_content)
        return json_content

    def _query_string(self, dic):
        string = ''
        for key in list(dic.keys()):
            string += '"' + key + '":"' + str(dic[key]) + '",'
        string = string[:-1]
        return '?json={' + urllib.parse.quote(string) + '}'

    def login(self):
        url = self.SERVER + self.PATH_LOGIN
        params = {"uname": self.name, "upass": self.password}
        full_url = url + self._query_string(params)
        json_content = self._request(full_url)
        self.token = json_content['token']
        self.serial = json_content['serial']
        return self.token, self.serial

    def logout(self):
        url = self.SERVER + self.PATH_LOGOUT
        params = {"serial": self.serial, "token": self.token}
        full_url = url + self._query_string(params)
        json_content = self._request(full_url)
        return json_content['result_message']

    def search(self, address):
        url = self.SERVER + self.PATH_ADDRESS
        params = {
            "serial": self.serial, "token": self.token, "address": address}
        full_url = url + self._query_string(params)
        json_content = self._request(full_url)
        return json_content['items']


def get_wkt(lon, lat):
    return 'POINT(%s %s)' % (lon, lat)


def get_address(row, retry=1):
    address = []
    if retry == 1:
        if row[1] and row[1] != 'Cnr':
            address.append(row[1].strip())
        if row[2]:
            address.append(row[2].strip())
        if row[3]:
            address.append(row[3].strip())
        if row[4]:
            address.append(row[4].strip())
        if row[5]:
            address.append(row[5].strip())
    if retry == 2:
        if row[1] and row[1] != 'Cnr':
            address.append(row[1].strip())
        if row[2]:
            address.append(row[2].strip())
        if row[3] and row[3] != row[2]:
            address.append(row[3].strip())
        if row[4] and row[4] != row[3]:
            address.append(row[4].strip())
        if row[5]:
            address.append(row[5].strip())
    # address.append('south africa')
    return address


def get_sql(wkt, pkey, source):
    return 'UPDATE feti SET geom=ST_GeomFromText(\'%s\', 4326), ' \
           'source=\'%s\' WHERE id = %s' % (wkt, source, pkey)


def process():
    # Geocoding
    geocode = OneMap(USER, PASSWORD)
    # print geocode.search('20, Bella Road, Bellville 7530')
    geolocator = GoogleV3(timeout=20)

    try:
        conn = psycopg2.connect(
            "dbname='demacia' user='etienne' host='localhost' password='azerty'")
        print("Connected to the database")
    except:
        print("I am unable to connect to the database")

    cur = conn.cursor()
    cur.execute(
        """SELECT id, no_street, street_name, suburb, city, postal_code FROM feti WHERE source IS NULL AND id IS NOT NULL;""")
    rows = cur.fetchall()

    for row in rows:

        address = get_address(row, 1)
        address_str = ','.join(address)
        if address_str:
            results = geocode.search(address_str)
            if len(results):
                wkt = get_wkt(results[0]['cent_long'], results[0]['cent_lat'])
                sql = get_sql(wkt, row[0], 'onemap')
                print('onemap', address_str)
                cur.execute(sql)
                conn.commit()
            else:
                location = geolocator.geocode(address_str, components={'country': 'south africa'},
                                              bounds=[-35.299, 17.314, -30.183, 24.851])
                if location:
                    sql = get_sql(location.wkt, row[0], 'google')
                    print('google', address_str)
                    cur.execute(sql)
                    conn.commit()
                else:
                    address = get_address(row, 2)
                    address_str = ','.join(address)
                    if address_str:
                        results = geocode.search(address_str)
                        if len(results):
                            wkt = get_wkt(results[0]['cent_long'], results[0]['cent_lat'])
                            sql = get_sql(wkt, row[0], 'onemap')
                            print('onemap', address_str)
                            cur.execute(sql)
                            conn.commit()
                        else:
                            location = geolocator.geocode(address_str, components={'country': 'south africa'},
                                                          bounds=[-35.299, 17.314, -30.183, 24.851])
                            if location:
                                sql = get_sql(location.wkt, row[0], 'google')
                                print('google', address_str)
                                cur.execute(sql)
                                conn.commit()
                            else:
                                not_found = True
                                address = get_address(row, 2)
                                print(address)
                                while not_found:
                                    if len(address) == 0:
                                        break

                                    address.pop(0)
                                    address_str = ','.join(address)
                                    results = geocode.search(address_str)
                                    if len(results):
                                        wkt = get_wkt(results[0]['cent_long'], results[0]['cent_lat'])
                                        sql = get_sql(wkt, row[0], 'onemap')
                                        print('onemap', address_str)
                                        cur.execute(sql)
                                        conn.commit()
                                        not_found = False
                                    else:
                                        location = geolocator.geocode(address_str,
                                                                      components={'country': 'south africa'},
                                                                      bounds=[-35.299, 17.314, -30.183, 24.851])
                                        if location:
                                            sql = get_sql(location.wkt, row[0], 'google')
                                            print('google', address_str)
                                            cur.execute(sql)
                                            conn.commit()
                                            not_found = False

                                if not not_found:
                                    sql = 'UPDATE test SET source=\'unkown\' WHERE id = %s' % (row[0])
                                    cur.execute(sql)
                                    conn.commit()


def test():
    geolocator = GoogleV3()
    result = geolocator.geocode("KALKFONTEIN, KALKFONTEIN, KUILSRIVIER")
    print(result.raw)


# test()
process()

# geocode.logout()
