cd /home/imconfusednow/repo/django_site
git pull
chmod 744 -R /home/imconfusednow/repo
chmown 744 -R /home/imconfusednow/repo
cp -R /home/imconfusednow/repo/django_site /home/imconfusednow/cv_project
manage collectstatic --noinput --clear
server_pid=`ps aux | grep coup_server.py | grep -v grep | awk '{print $2}'`
kill ${server_pid}
nohup python3 /home/imconfusednow/cv_project/coup/coup_server.py&