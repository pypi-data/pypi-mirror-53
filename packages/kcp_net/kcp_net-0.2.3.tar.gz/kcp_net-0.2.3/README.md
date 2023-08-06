# kcp_net


底层是基于gevent的驱动的，并且经过实测，gevent下确实会有内存泄露。

而后来kcp_net的核心代码经过改造后加入xmaple_cluster，由于是使用twisted驱动，不再有内存泄露的问题。
