from scipy.spatial import ConvexHull
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from table_creator import create_table_convex_hull_polygon, create_table_locality_id_map
from psycopg2 import connect
import cPickle as pickle

def locality_polygon():
    con = connect(user='poly', dbname='polygon', password='poly')
    cur = con.cursor()
    # psql_connection, psql_cursor = get_connection_and_cursor(
    #     psql_db, psql_user, psql_password)
    # query = '''
    #         SELECT
    #             node_id,latitude,longitude
    #         FROM
    #             locality_coordinates;
    #         '''
    # psql_cursor.execute(query)
    # rows = psql_cursor.fetchall()
    create_table_convex_hull_polygon()
    create_table_locality_id_map()
    # locality = {}
    # for row in rows:
    #     node_id = row[0]
    #     lat = row[1]
    #     lng = row[2]
    #     if node_id in locality:
    #         locality[node_id].append((lat, lng))
    #     else:
    #         locality[node_id] = [(lat, lng)]

    # locality_list = [{'node_id': node_id, 'LatLng': LatLng}
    #                  for node_id, LatLng in locality.items()]
    with open('/home/delhivery/Documents/vsingh/polygon/locality_list.pickle', 'rb') as f:
        locality_list = pickle.load(f)

    with open('/home/delhivery/Documents/vsingh/polygon/locality_id_map.pickle', 'rb') as f:
        locality_id_map = pickle.load(f)
    
    for locality, loc_id in locality_id_map.items():
        if str(locality) != 'nan':
            query = '''INSERT INTO
                        locality_id_map (locality, id)
                        VALUES ('{}', {})
                    '''.format(locality, loc_id)
            cur.execute(query)


    for rows in locality_list:
        print rows['locality_id']
        if str(rows['locality_id']) == 'nan':
            print rows['locality_id']
            continue
        if len(rows['LatLng']) < 3:
            continue  # convex hull need atleast 3 points for makinh a polygon
        cv = ConvexHull(rows['LatLng'])
        hull_points = cv.vertices
        poly = ""
        for num in hull_points:
            lat = rows['LatLng'][num][0]
            lon = rows['LatLng'][num][1]
            poly += str(lon) + " " + str(lat) + ", "
        # adding last point again to complete the polygon
        num1 = hull_points[0]
        lat1 = (rows['LatLng'][num1][0])
        lon1 = (rows['LatLng'][num1][1])
        poly += str(lon1) + " " + str(lat1) + ", "
        poly = poly.rstrip(", ")
        poly = "ST_GeomFromText('POLYGON ((" + poly + "))', 4326)"
        query = '''INSERT INTO
						convex_polygons (locality_id, poly)
		        	VALUES ({},{})
		        '''.format(rows['locality_id'], poly)
        cur.execute(query)
    con.commit()

if __name__ == '__main__':
    locality_polygon()


# from scipy.spatial import ConvexHull
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# from utilities.psql_utils import get_connection_and_cursor
# from config.config import psql_db, psql_user, psql_password

# import matplotlib.pyplot as plt


# # postgis 4326
# def polygon():
#     psql_connection, psql_cursor = get_connection_and_cursor(
#         psql_db, psql_user, psql_password)
#     query = '''
#             SELECT
#                 node_id,latitude,longitude
#             FROM
#                 locality_coordinates;
#             '''
#     psql_cursor.execute(query)
#     rows = psql_cursor.fetchall()

#     locality = {}
#     for row in rows:
#         node_id = row[0]
#         lat = row[1]
#         lng = row[2]
#         if node_id in locality:
#             locality[node_id].append((lat, lng))
#         else:
#             locality[node_id] = [(lat, lng)]

#     locality_list = [{'node_id': node_id, 'LatLng': LatLng}
#                      for node_id, LatLng in locality.items()]
#     i = 0
#     for rows in locality_list:
#         if i > 1:
#             break
#         i += 1
#         x = []
#         y = []
#         if len(rows['LatLng']) < 3:
#             continue

#         print len(rows['LatLng'])
#         row1 = rows['LatLng']
#         cv = ConvexHull(row1)
#         hull_points = cv.vertices

#         print hull_points, rows['node_id']
        # ax = plt.gca()
        # ax.get_xaxis().get_major_formatter().set_useOffset(False)
        # ax.get_xaxis().get_major_formatter().set_scientific(False)
        # ax.get_yaxis().get_major_formatter().set_useOffset(False)
        # ax.get_yaxis().get_major_formatter().set_scientific(False)
#         for num in hull_points:
#             x.append(rows['LatLng'][num][0])
#             y.append(rows['LatLng'][num][1])
#         num1 = hull_points[0]
#         x.append(rows['LatLng'][num1][0])
#         y.append(rows['LatLng'][num1][1])
#         plt.plot(x, y, 'r--', lw=2)
#         plt.plot(x[0], y[0], 'ro')
#         plt.show()
#         poly = ""
#         for num in hull_points:
#             lat = rows['LatLng'][num][0]
#             lon = rows['LatLng'][num][1]
#             poly += str(lon) + " " + str(lat) + ", "

#         num1 = hull_points[0]
#         lat1 = (rows['LatLng'][num1][0])
#         lon1 = (rows['LatLng'][num1][1])
#         poly += str(lon1) + " " + str(lat1) + ", "
#         poly = poly.rstrip(", ")
#         create_query = '''CREATE TABLE IF NOT EXISTS
#                             convex_hull_polygons (
#                                 node_id INT NOT NULL,
#                                 poly geometry(Geometry,4326) NOT NULL
#                             )'''
#         psql_cursor.execute(create_query)
#         poly = "ST_GeomFromText('POLYGON ((" + poly + "))', 4326)"
#         query =  '''INSERT INTO convex_hull_polygons (poly)
#                 VALUES ({})'''.format(
#             poly)
#         print(poly)
#         psql_cursor.execute(query)
#         psql_connection.commit()


# polygon()
