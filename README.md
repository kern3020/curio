## Getting started (dev)

This is a Django app. To get started

check out code 

      git clone https://github.com/kern3020/curio.git

Before starting 

       $ python manage.py migrate
       Operations to perform:
        Apply all migrations: admin, auth, contenttypes, sessions
       Running migrations:
        Applying contenttypes.0001_initial... OK
        Applying auth.0001_initial... OK
        Applying admin.0001_initial... OK
        Applying sessions.0001_initial... OK

To fire up the development server
  
        $ ./manage.py runserver 
