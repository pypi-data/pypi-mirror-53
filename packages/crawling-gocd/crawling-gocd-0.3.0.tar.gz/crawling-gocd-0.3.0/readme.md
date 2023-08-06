## Crawling-GoCD
This project works for crawling the build histories of pipelines and calculate the metrics.

### Installation
1. python 3
2. pipenv

### Development
1. Install the packages
  ```
  pipenv install
  ```
2. Run test
  ```
  pipenv run python -m unittest discover
  ```

### Run
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
  `pipeline name` is the string in the history API URL.  


  `pipeline calc_grouped_stages` includes each phase needed to calculate metrics.  
  Such as, if we want to calculate the deployment frequency for QA environment, and the QA deployment has two stages.  
  If one of the two stages fails, determines QA deployment failed, so we configure the qa phase has `flyway-qa`、`deploy-qa`.


  `global start_time` and `global end_time`, determines the time slot for crawling pipeline histories.  
  Also, there are `pipeline start_time` and `pipeline end_time`, they have a high priority to `global start_time` and `global end_time`.  

2. Run command
  ```
  pipenv run python -m crawling_gocd
  ``` 
  __Attention__: Need set the environment variables `GOCD_SITE`、`GOCD_USER`、`GOCD_PASSWORD` before running the command.
  Alternatively, use the following command:
  ```
  GOCD_SITE="<your_gocd_site>" GOCD_USER="<your_username>" GOCD_PASSWORD="<your_password>" pipenv run python -m crawling_gocd
  ```

### Expansibility
So far the crawling URL is according to the goCD version 18.11.  
If need use to incompatible goCD version, just replace the file `Crawler.py`.  
If need some new metrics handler, just write the implementation class under the superclass  `CalculateStrategyHandler`, and assemble into `Calculator` in the file `Portal`.
