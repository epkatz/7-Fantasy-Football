CMD="Drop Database fantasy; create Database fantasy;"
mysql -u XXX -h localhost -pXXX -e "$CMD"
python manage.py syncdb <<-CONFIRM
	no
CONFIRM
python manage.py runserver
