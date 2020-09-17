# has
h(esabi) alerting system
this project is based on the simple correlation engines and is consisted of 4 main components.
1) sources
    these are the sources in which we read data from. for example the indexes of metricbeat in elasticsearch, zabbix or prometheus , ....
2) filters
    these are the filters that apply on the sources and take actions if they meet the filters
3) pipe types
    these pipe types determine if an action should get triggered or not
4) actions
    some actions to do in case of matching filters. for now i will add
    - ansible ad_hoc commands
    - ansible playbooks
    - email
    - commands (linux system commands(e.g. sms panels))
