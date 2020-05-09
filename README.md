### Django REST API Logger

> Mixin which logs all needed data from API

Just import `APILoggingMixin` and put it in first base class of your API and it'll do the rest

#### Requirements
- Django

#### Installation
The package is available on [PyPI](https://pypi.org/project/django-rest-api-logger/):

```pip install django-rest-api-logger```


### How to use
> IMPORTANT: Don't forget to put it in the first base class
```
class ProductListAPI(APILoggingMixin, OtherMixinsOrClass):
    ...
```


#### Modes
> Put these variables in your django settings file
- ##### Native Logger <br/>
    ```
    # file ------> Writes logs to file 
    # console ---> Prints logs in console
    DRF_LOGGER_HANDLER = ["file", "console"]
    
    # Log file directory
    # Make sure directory exists  
    DRF_LOGGER_FILE = "/tmp/custom_logger.log"
    ```
      
- ##### Mongo Log <br/>
    ```
    # Mongo Host
    DRF_LOGGER_MONGO_HOST = "mongodb://username:password@localhost:27017/"
       
    # Mongo Attempting Connection Timeout:
    DRF_LOGGER_MONGO_TIMEOUT_MS = 10
    
    # Log db
    DRF_LOGGER_MONGO_LOG_DB = "log"
    
    # Log collection
    DRF_LOGGER_MONGO_LOG_COLLECTION = "logs"
    ```
   
- ##### Custom
    ```
    # If DRF_LOGGER_CUSTOM_HANDLER is set to false then aboves modes won't work
    # You have to override `handle_log` function in order to implement your own handler
    DRF_LOGGER_CUSTOM_HANDLER = False
    ```
