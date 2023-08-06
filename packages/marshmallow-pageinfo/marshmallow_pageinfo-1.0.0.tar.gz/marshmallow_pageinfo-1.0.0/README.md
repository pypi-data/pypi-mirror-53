# marshmallow_pageinfo

Page info marshmallow schema for api


### Installation

`pip install -U marshmallow_pageinfo`


### Example


```python
from marshmallow_pageinfo import PAGE_INFO_SCHEMA


@controller.route('/', methods=['GET'])
def get_todo():
	page_info = PAGE_INFO_SCHEMA.load(request.args)
	pagination = todo_q.paginate(page_info['page'], page_info['per_page'])
	return {
		'todos': TODO_SCHEMA.dump(pagination.items),
		'pageInfo': PAGE_INFO_SCHEMA.dump(pagination),
	}
```
