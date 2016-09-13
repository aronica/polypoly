ps -ef | grep 'node app.js' | grep -v grep | awk '{print $2}' | while read pid
    do
        echo 'pid is '$pid
        kill -9 $pid
    done
echo 'node server stopped.'
