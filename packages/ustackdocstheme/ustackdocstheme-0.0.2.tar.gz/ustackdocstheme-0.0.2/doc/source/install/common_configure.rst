2. Edit the ``/etc/ustackdocstheme/ustackdocstheme.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://ustackdocstheme:USTACKDOCSTHEME_DBPASS@controller/ustackdocstheme
