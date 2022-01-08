cd /home/imconfusednow/repo/django_site
git pull
cp -r /home/imconfusednow/repo/django_site/* /home/imconfusednow/cv_project
chmod -R 775 /home/imconfusednow/cv_project
chown -R www-data:imconfusednow /home/imconfusednow/cv_project
python3 /home/imconfusednow/cv_project/manage.py collectstatic --noinput --clear
server_pid=`ps aux | grep coup_server.py | grep -v grep | awk '{print $2}'`
kill ${server_pid}
nohup python3 /home/imconfusednow/cv_project/coup/coup_server.py&
cd .