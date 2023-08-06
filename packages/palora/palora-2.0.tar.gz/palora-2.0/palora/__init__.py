import cx_Oracle

class db:
	def __init__(self, user, pw, tns):
		self.conn = cx_Oracle.connect(user, pw, tns)
		self.conn.autocommit = 1

	def read(self, command, flat=True):
		with self.conn.cursor() as cur:
			cur.execute(command)
			f = cur.fetchall()
			if not f or not flat:
				return f
			else:
				if len(f[0]) == 1:
					f = [i[0] for i in f]
					if len(f) == 1:
						f = f[0]
				return f

	def read1(self, command):
		with self.conn.cursor() as cur:				
			cur.execute(command)
			f = cur.fetchone()
			if len(f) == 1:
				f = f[0]
			return f

	def write(self, command):
		with self.conn.cursor() as cur:
			cur.execute(command)

	def __del__(self):
		self.conn.close()

