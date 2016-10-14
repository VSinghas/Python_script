from psycopg2 import connect

def create_table_convex_hull_polygon():
	con = None
	con = connect(user='poly', dbname='polygon', password='poly')
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS convex_polygons")
	cur.execute('''CREATE TABLE convex_polygons
       (locality_id         INT          NOT NULL,
        poly geometry(Geometry,4326) NOT NULL);
       ''')
	con.commit()
	con.close()

def create_table_locality_id_map():
	con = None
	con = connect(user='poly', dbname='polygon', password='poly')
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS locality_id_map")
	cur.execute('''CREATE TABLE locality_id_map
       (locality         TEXT          NOT NULL,
        id INT NOT NULL);
       ''')
	con.commit()
	con.close()

if __name__ == '__main__':
	create_table_convex_hull_polygon()
