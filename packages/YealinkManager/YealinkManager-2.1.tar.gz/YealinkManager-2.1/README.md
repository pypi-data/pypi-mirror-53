# YealinkManager

install using ``` pip install YealinkManager```
after doing this you got two new shell commands:
```YealinkManager``` and the short form ```ym```.
you shuld use it in this way: 
    
    ym path/to/list.csv

This module read the csv file, that must be composed in this way:
    
    ip, action, credential, row comment 
    
Exemplum gratie:
    
    192.168.9.101,HEADSET,admin:admin,Commento1

One at time the script will read the parameters, build the action Uri and call it.

In the list the character ```#``` at the beginning of line is a comment.

__Remember to enable remote control on your yealink phone and set the remote controller ip correctly!__