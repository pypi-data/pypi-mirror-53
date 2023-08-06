Crawling-GoCD is a library that works for crawling the goCD build histories of pipelines and calculate the metrics.

### Installation
```
$ pip3 install crawling-gocd
```

### Usage
1. Input configration in the file `inputs.yaml`
```
pipelines:
  - 
    name: account-management-normal-master
    calc_grouped_stages: 
      ci:
        - code-scan
        - test-integration
        - build
      qa:
        - flyway-qa
        - deploy-qa
    start_time: 2019-07-10 00:00:00
    end_time: 2019-08-12 23:59:59
  - 
    name: account-management-normal-release
    calc_grouped_stages: 
      uat:
        - flyway-uat
        - deploy-uat

global:
  start_time: 2019-07-01 00:00:00
  end_time: 2019-08-12 23:59:59
```
Keys in the config file:  
`pipeline name` is the string in the history API URL.  


`pipeline calc_grouped_stages` includes each phase needed to calculate metrics.  
Such as, if we want to calculate the deployment frequency for QA environment, and the QA deployment has two stages.  
If one of the two stages fails, determines QA deployment failed, so we configure the qa phase has `flyway-qa`、`deploy-qa`.


`global start_time` and `global end_time`, determines the time slot for crawling pipeline histories.  
Also, there are `pipeline start_time` and `pipeline end_time`, they have a high priority to `global start_time` and `global end_time`.  

2. Code invoking
  ```
    from crawling_gocd.portal import Portal
    
    Portal().serve()
  ```
3. Set environment variables   
  Need set the environment variables `GOCD_SITE`、`GOCD_USER`、`GOCD_PASSWORD` before running the application.


### Expansibility
So far the crawling URL is according to the goCD version 18.11.  

