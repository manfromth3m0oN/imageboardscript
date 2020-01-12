# Another chan script

## Aims

* Rewrite my previous imageboard scripts using a faster NoSQL database (MongoDB)
* Add features that werent present in my previous scripts e.g:
	* Jump to reply
	* User created boards
	* User CSS
	* Actually decent formatting

## Methods

There are a couple things that need to be defined first off:

* The post schema
* General logic structure
* Server filesystem structure

### Post Schema

To form a fully functional post 6 amount of things need to be included:

* post ID
* post body
* image/media
* board
* thread ID (basically the ID of the post which started the thread(will be labled as `replyingto` or similar))
* Name (if desired)

This will take a dictionary form while in python. Looking something like this

```python
post = {'id':654321, 'body':'this is a sample post', 'image':'456745.png', 'board': 'g', 'replyingto':'765432', 'name':'anon'}
```

### Logic

This project will be writen in flask as its fast and efficient. 
There will be an index page at `/`.

Each board will have a one to three letter identifier which will correspond to an actual title e.g:
```python
boards = {'g':'technology', 'b':'random', 'gif':'gif', 'hr':'high res'}
```
As each board page is accessed all of the threads will be gathered.
Threads are started with posts which have an empty `replyingto` field.
Along with the thread starting posts, aprox 3 more posts will be grabbed to be displayed under the thread. 

Threads will be ordered by number of replies by default. This will be changeable (I think)
On viewing a thread All posts within that board with a certain `replyingto` will be gathered and displayed

### Filesystem
