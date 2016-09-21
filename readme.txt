程序跑在 tmux 下面

tmux ls 可以查看所有 sessions

14: 1 windows (created Tue Aug 30 14:00:24 2016) [238x60]      node server session
bin: 1 windows (created Thu Aug 11 16:35:26 2016) [272x79]     python server session
redis: 1 windows (created Thu Aug 11 15:41:27 2016) [272x76]   redis server session


一个页面请求的大致流程为：

web（static 目录）-> node server（node 目录）-> python server (backend 目录)

static 目录结构很清晰
node 目录说明在 node/readme.md 中描述很清晰
backend 目录 TODO
