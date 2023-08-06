# Django Autocomplete

substring occurrence search module.

  
Allows the use of celery, if it is in the mood. The following settings are required in settings.py
 ```
 AUTOCOMPLETER = {
    'SERILEZER_CLASSES': 'your_module_name.autocompleter',
    'LIMIT': 5,
    'CELERY': True
    }
 ```
 
Where:
 1. **SERILEZER_CLASSES** - indicates django_autompleter where to look for serialization ticket offices. The serialization class inherits from the base class **SearcherSerializer**. In the example below, we indicate which fields from the **Publication** model we want to return when requested.
  ```

  from autocompleter import SearcherSerializer
  
  class PublicationsSerializer(SearcherSerializer):
        class Meta:
            model = Publication
            fields = (
                'id',
                'title',
                ) 
  ```
2. **LIMIT** - indicates the number of records received that must be returned.
3. **CELERY** - indicates the start of the autompleter as a celery task. It is important, in this case, your project must have celery.py settings.

example:
 ```
from autocompleter import Autocompleter

autocomplete_coonection =  Autocompleter()

result = autocomplete_coonection.get(
                model=Publication,# search data model
                column="title",#column of the model to search for
                value=value # value
            )
  ```