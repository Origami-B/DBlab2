from flask_sqlalchemy import SQLAlchemy
import pymysql.cursors

db = SQLAlchemy()

# Connect to the database
db2 = pymysql.connect(host='localhost',
                            user='root',
                            password='000000',
                            db='bank',
                            cursorclass=pymysql.cursors.DictCursor)

# try:
#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "drop table `users`;"
#         cursor.execute(sql)

#     with connection.cursor() as cursor:
#         # Create a new table
#         sql = """
#         CREATE TABLE `users` (
#             `id` int(11) NOT NULL AUTO_INCREMENT,
#             `email` varchar(255) COLLATE utf8_bin NOT NULL,
#             `password` varchar(255) COLLATE utf8_bin NOT NULL,
#             PRIMARY KEY (`id`)
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
#         AUTO_INCREMENT=1 ;
#         """
#         cursor.execute(sql)

#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()

#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#         cursor.execute(sql, ('webmaster@python.org',))
#         result = cursor.fetchone()
#         print(result)

#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "drop table `users`;"
#         cursor.execute(sql)

# finally:
#     connection.close()
