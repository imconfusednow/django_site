cd /home/imconfusednow/repo/django_site
git pull
cp -R /home/imconfusednow/repo/django_site /home/imconfusednow/cv_project
chmod 744 -R /home/imconfusednow/cv_project
chown www-data:imconfusednow -R /home/imconfusednow/cv_project
python3 /home/imconfusednow/cv_project/manage.py collectstatic --noinput --clear
server_pid=`ps aux | grep coup_server.py | grep -v grep | awk '{print $2}'`
kill ${server_pid}
nohup python3 /home/imconfusednow/cv_project/coup/coup_server.py&