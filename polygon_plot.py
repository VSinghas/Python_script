from scipy.spatial import ConvexHull
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
import cPickle as pickle
import matplotlib.pyplot as plt


def locality_polygon():

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
    # create_table_convex_hull_polygon()
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

    for rows in locality_list:
        if len(rows['LatLng']) < 3:
            continue  # convex hull need atleast 3 points for makinh a polygon
        cv = ConvexHull(rows['LatLng'])
        hull_points = cv.vertices
        # poly = ""
        lats = []
        longs = []
        for num in hull_points:
            lats.append(rows['LatLng'][num][0])
            longs.append(rows['LatLng'][num][1])
            # lat = rows['LatLng'][num][0]
            # lon = rows['LatLng'][num][1]
            # poly += str(lon) + " " + str(lat) + ", "
        # adding last point again to complete the polygon
        num1 = hull_points[0]
        lats.append(rows['LatLng'][num1][0])
        longs.append(rows['LatLng'][num1][1])

        ax = plt.gca()
        ax.get_xaxis().get_major_formatter().set_useOffset(False)
        ax.get_xaxis().get_major_formatter().set_scientific(False)
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        ax.get_yaxis().get_major_formatter().set_scientific(False)

        plt.plot(lats, longs, 'r--', lw=2)
        plt.plot(lats[0], longs[0], 'ro')
        plt.show()
        # poly += str(lon1) + " " + str(lat1) + ", "
        # poly = poly.rstrip(", ")
        # poly = "ST_GeomFromText('POLYGON ((" + poly + "))', 4326)"
    #     -- query = '''INSERT INTO 
				# 		convex_hull_polygons (node_id,poly) 
		  #       	VALUES ({},{})
		  #       '''.format(rows['node_id'], poly)
    #     psql_cursor.execute(query)
    # psql_connection.commit()

if __name__ == '__main__':
    locality_polygon()
    
