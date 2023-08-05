.. _examples:

========
Examples
========

.. _CRUD:

CRUD
----

The following examples make use of a simple table

.. code:: sql

   CREATE TABLE `users` (
       `id` int(11) NOT NULL AUTO_INCREMENT,
       `email` varchar(255) COLLATE utf8_bin NOT NULL,
       `password` varchar(255) COLLATE utf8_bin NOT NULL,
       PRIMARY KEY (`id`)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
   AUTO_INCREMENT=1 ;


.. code:: python

    import trio_mysql.cursors

    # Connect to the database
    connection = trio_mysql.connect(host='localhost',
                                 user='user',
                                 password='passwd',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=trio_mysql.cursors.DictCursor)

    async with connection:
        async with connection.transaction():
            async with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                await cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        # Transactions are auto-committed if they're exited without
        # error.

        async with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            await cursor.execute(sql, ('webmaster@python.org',))
            result = await cursor.fetchone()
            print(result)

        # When reading, you should periodically commit (or roll back) so
        # that the database can release any read locks.
        await connection.commit()
        # In this case it's superfluous because we end the connection
        # anyway.


This example will print:

.. code:: python

    {'password': 'very-secret', 'id': 1}
