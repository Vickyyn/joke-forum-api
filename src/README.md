# Jokes Forum API

## 1. Identification of the problem you are trying to solve by building this particular app

Problem 1: There are so many jokes that it can be difficult to find and separate the good from the bad. 
Problem 2: It can also be difficult to find good jokes of a particular category.
Problem 3: It is hard to find a creative outlet to contribute jokes.
Problem 4: It can be hard to get feedback for jokes you have created. 
Problem 5: It can be difficult to find a community that likes jokes as much as you do. 

The app allows an easy location to find jokes, listing them by popularity via the upvote system. Tags are utilised to allow an easy way to find the most humerous jokes by category. Comments are also allowed on jokes to allow for user interactions, whether it be to express reactions or give feedback, to further explain the joke, or to even add follow-up jokes.

## 2. Why is it a problem that needs solving?

The problems listed in question 1 require solving for a few reasons. Firstly, everyone can do with more humour in their life. The ability to view jokes by popularity helps to save time in busy lives (instead of having to trawl through lists of unfunny jokes), hopefully adding a bit more joy to people's lives. Secondly, not everyone has the same sense of humour, and the ability to to find top humerous jokes by tags or categories help to overcome that. Thirdly, for those wishing to create jokes it can be difficult to gauge feedback as there may be a limited number of people available, or else the particular community (family or friendship group) may have a different sense of humour. By expanding the reach and audience of the creations, with the option for direct feedback via upvotes and comments, a creator can more efficiently craft their art. Finally, by providing access to a community of like-minded people, and encouraging creativity and interaction, it will help foster greater emotional and social wellbeing. 

## 3. Why have you chosen this database system. What are the drawbacks compared to others?
PostgreSQL is chosen as the database system. The benefits include my familiarity, it being free and open source, and it being a relational database. Utilising a relational database is applicable to this app due to the interconnecting and rigid structure of components involved. As users interact with jokes and there are many relations between the two with upvotes and comments, a relational database allows easy grouping of data into well defined categories (e.g. users, jokes, comments, upvotes) with well defined attributes (e.g. all users have a username and a password), and easy and efficient relationship mappings to tie everything together (e.g. how a comment will be linked to a user and a joke, and similarly with upvotes). 

Other benefits of PostgreSQL include its excellent data integrity, and ability for concurrency. Deletion, modification and insertion anomalies can be minimised by using entity/referential/domain constraints, for example if a particular joke was deleted then relationships can be set to also delete any corresponding comments and upvotes. Data accuracy can be preserved by ensuring primary keys are unique and ensuring no duplications. Furthermore, as the app grows, the ability for concurrency would ensure improved efficiency for all users that may be using the app at the same time. 

Drawbacks of using a relational database include that it is difficult to work with data that has varying structures. For example, if later on we wanted to change the comment schema to also include a title, then all the existing data would need to be changed, requiring the database to be offline temporarily. Similarly, if the app were to be expanded by allowing direct messaging functionality between users, the varying size and structure of the data that would need to be stored and accessed may make it difficult to implement within the constraint of a relational database. Also, relational databases may require queries to numerous tables to execute an answer, whereas non-relational databases can query the database directly with ease. As the datasets enlarge and complexity increases, relational databases can run into scalability and performance issues.


## 4. Identify and discuss the key functionalities and benefits of an ORM
Object Relational Mapping (ORM) serves as a _bridge_ between _objects_ in an application, and data tables stored in a _relational_ database.

Key functionalities of an ORM include (using Flask and PostgreSQL as an example):
- Connect web application frameworks (e.g. Flask) with the database (e.g. PostgreSQL). This allows direct data manipulation via using programming languages such as Python, Ruby and more. 
- Mapping models (or objects) in Flask to tables in the database. By creating a class object in Flask, this maps to a table in the database. Attributes within the object model become attributes in the database table, with appropriate constraints including primary keys, data types, and more.
- Assists with commands to create, drop, and seed tables from objects. This allows the initial set up of the database, for the objects to map to tables in the database, and to allow instances of objects to map to instances/data in the tables. 
- Directly maps creating, reading, updating, and deleting (CRUD) functionalities between Flask and the database. For example takes an input instance and then creates the instance in the database (e.g. SQLAlchemy via session.add(instance) and session.commit()). With the help of a deserialization library (Marshmallow), it also retrieves or reads instances from the database, which is then converted to a readable form by Marshmallow, and the objects outputted (e.g. select or query to select instances from the appropriate table, with option to use filter and order by to fine-tune selections). This can all be done using Python rather than SQL. Further examples include session.delete(instance), mapping updates to instances from Python form to the database, and more. 
- Essentially, ORM allows SQL queries and database interactions to be performed using object-oriented programming of a preferred programming language


Benefits of ORM are:
- Allows coding and manipulation of data in a familiar language (eg Python) rather than SQL. This can greatly boost productivity, and programmers are able to use the language they are most comfortable with
- Make code cleaner by utilising more efficient language/not having to use SQL
- Allows use of object oriented programming, and improved code due to use of a model control view structure, and as the models are stored in one place and not repeated, it is easy to update and maintain code
- It is possible to switch database systems (eg SQLite and MySQL) with minimal code modifications, in case the testing and deployment environments are different, as the database system is abstracted 
- Sanitises incoming data and protects against SQL injections, as only set data types are accepted and the database is not queried using SQL
- Bonus advanced features can come with the ORM, for example support for migrations, transactions, and more 
- easy to use and maintain, do not have to do own convertions from objects to tables and vice versa 


## 5. Document all endpoints for your API

### /
Methods: GET  
Argument: None  
Required data: N/A  
Expected response data: JSON, `{'message': 'Welcome to the jokes forum!'}`  
Authentication method: Nil  
Description: Welcome message, public

## Users Documentation 
### /users/
Methods: GET  
Argument: None  
Required data: N/A  
Expected response data: JSON array of users  
Authentication method: Nil  
Description: List of all users, public  

### /users/<string:username>/
Methods: GET  
Argument: username (string)  
Required data: N/A  
Expected response data: JSON, corresponding user  
```py
{
    "id": 1,
    "username": "admin",
    "jokes": [],
    "is_admin": true,
    "comments": [
        {
            "id": 1,
            "joke_id": 1,
            "user_id": 1,
            "date": "2022-11-09",
            "body": "What a great joke"
        }
    ]
} 
```
Authentication method: Nil  
Description: View a particular user, public  

### /users/<int:id>/
Methods: GET  
Argument: id (integer)  
Required data: N/A  
Expected response data: JSON, corresponding user (same as above)  
Authentication method: Nil  
Description: View a particular user, public  

### /users/<int:id>/
Methods: DELETE  
Argument: id (integer)  
Required data: N/A  
Expected response data: JSON, `{'message': f'User {id} has been deleted'}`   
Authentication method: Bearer token  
Authorisation: Joke owner or admin (via Bearer token)    
Description: Delete a joke  

### /users/<int:id>/
Methods: PUT, PATCH  
Argument: id (integer)  
Required data: JSON object including keys of old_password and new_password, `{'old_password': 'oldpassword', 'new_password': 'newpassword'}`  
Expected response data: JSON, `{'message': 'You have changed your password'}`  
Authentication method: Bearer token  
Authorisation: Corresponding user (via Bearer token)  
Description: Change password for user  

## Authentication documentation
### /auth/register
Methods: POST  
Argument: Nil  
Required data: JSON object including keys of username and password, `{'username': 'username', 'password': 'password'}`  
Expected response data: JSON user object `{"id": 9, "username": "username"}`  
Authentication method: Nil  
Description: Register a user, public  

### /auth/login
Methods: POST  
Argument: Nil  
Required data: JSON object including keys of username and password, `{'username': 'username', 'password': 'password'}`  
Expected response data: JSON object with keys of username and JWT token `{'username': 'username', 'token': 'JWTtokenhere'}`  
Authentication method: Nil  
Description: Login, public  

### /auth/admin
Methods: POST  
Argument: Nil  
Required data: JSON object including key of username `{'username': 'username'}`    
Expected response data: JSON object of user   
```py
{
    "id": 3,
    "username": "Alice",
    "is_admin": true,
    "comments": [
        {
            "id": 4,
            "joke_id": 4,
            "user_id": 3,
            "date": "2022-11-09",
            "body": " "
        }
    ]
}
```  
Authentication method: Bearer token  
Authorization: Admin (via bearer token)  
Description: Create admin   

## Joke documentation
### /jokes/
Methods: GET  
Argument: Nil  
Required data: N/A  
Expected response data: JSON array of jokes  
Authentication method: Nil  
Description: View all jokes, public  

### /jokes/
Methods: POST  
Argument: Nil  
Required data: JSON object with keys of title and body `{'title': 'titlehere', 'body': 'funnyjokehere'}`  
Expected response data: JSON joke object   
```py
{
    "id": 6,
    "title": "funnytitlehere",
    "body": "muchfunny",
    "joke_tags": [],
    "date": "2022-11-11",
    "owner": 3,
    "user": {
        "username": "Alice"
    },
    "upvotes": 0,
    "comments": []
}
```  
Authentication method: Bearer token  
Authorization: Users (via Bearer token)  
Description: Create a joke  

### /jokes/tags/
Methods: GET  
Argument: Nil  
Required data: N/A  
Expected response data: JSON array of tags  
Authentication method: Nil  
Description: View all tags, public  

### /jokes/tags/<string:name>/
Methods: GET  
Argument: Nil  
Required data: N/A  
Expected response data: JSON array of jokes  
Authentication method: Nil  
Description: View all jokes with a corresponding tag, public  

### /jokes/comments/
Methods: GET  
Argument: Nil  
Required data: N/A  
Expected response data: JSON array of comments  
Authentication method: Nil  
Description: View all comments, public  

### /jokes/comments/
Methods: DELETE  
Argument: Nil  
Required data: JSON object with key of id `{'id': '2'}`  
Expected response data: JSON, `{'message': f"Comment {request.json['id']} deleted"}`  
Authentication method: Bearer token  
Authorization: User that created the comment, or admin (via Bearer token)  
Description: Delete a comment  

### /jokes/comments/
Methods: PUT, PATCH  
Argument: Nil  
Required data: JSON object with keys of id and body `{'id': '3', 'body': 'newcommenthere'}`  
Expected response data: JSON, 
```py
{
    "id": 3,
    "joke_id": 2,
    "user_id": 4,
    "date": "2022-11-09",
    "body": "newcommenthere",
    "user": {
        "username": "Rhys"
    }
}
```  
Authentication method: Bearer token  
Authorization: User that created the comment (via Bearer token)  
Description: Edit a comment  

## Specific jokes documentation
### /jokes/<int:id>/
Methods: GET  
Argument: id (integer)  
Required data: N/A  
Expected response data: JSON object of particular joke  
Authentication method: Nil  
Description: View a joke, public  

### /jokes/<int:id>/
Methods: DELETE  
Argument: id (integer)  
Required data: N/A  
Expected response data: JSON, `{'message': f'Joke {joke.id} has been deleted'} `
Authentication method: Bearer token
Authorization: Owner of joke, or admin (via bearer token)  
Description: Delete a joke  

### /jokes/<int:id>/
Methods: PUT, PATCH  
Argument: id (integer)  
Required data: JSON object with keys of title and body `{'title': 'newtitle', 'body': 'newbody'}`  
Expected response data: JSON object of joke  
Authentication method: Bearer token  
Authorization: Owner of joke (via bearer token)  
Description: Edit a joke  

### /jokes/<int:id>/upvote/
Methods: POST  
Argument: id (integer)  
Required data: Nil  
Expected response data: JSON object of upvote  `{"id": 6, "joke_id": 3, "user_id": 3}`
Authentication method: Bearer token  
Authorization: Users (via bearer token)  
Description: Upvote a joke  

### /jokes/<int:id>/upvote/
Methods: DELETE  
Argument: id (integer)  
Required data: Nil  
Expected response data: JSON, `{'message':f'You have removed your upvote for joke {id}'}`
Authentication method: Bearer token  
Authorization: User who have previously upvoted the joke (via bearer token)  
Description: Delete an upvote  

### /jokes/<int:id>/tags/
Methods: POST  
Argument: id (integer)  
Required data: JSON object with key of tag `{'tag': 'newtag'}`  
Expected response data: JSON of corresponding joke tag, 
```py
{
    "id": 5,
    "joke_id": 3,
    "tag_id": 4,
    "tag": {
        "name": "newtag"
    }
}
```
Authentication method: Bearer token  
Authorization: Owner of joke, or admin (via bearer token)  
Description: Add a tag to a joke (creates a new tag if it does not previously exist)  

### /jokes/<int:id>/tags/
Methods: DELETE  
Argument: id (integer)  
Required data: JSON object with key of tag `{'tag': 'oldtag'}`
Expected response data: JSON, `{"message": f"you have deleted the tag {request.json.get('tag')} from joke {id}"}`
Authentication method: Bearer token  
Authorization: Owner of joke, or admin (via bearer token)  
Description: Delete a tag  

### /jokes/<int:id>/comments/
Methods: GET  
Argument: id (integer)  
Required data: N/A  
Expected response data: JSON array of comments for particular joke  
Authentication method: Nil  
Description: View all comments for a joke, public  

### /jokes/<int:id>/comments/
Methods: POST  
Argument: id (integer)  
Required data: JSON object with key of body `{'body': 'new comment here'}`  
Expected response data: JSON of comment
 ```py
 {
    "id": 5,
    "joke_id": 3,
    "user_id": 3,
    "date": "2022-11-11",
    "body": "new comment here",
    "user": {
        "username": "Alice"
    }
}
``` 
Authentication method: Bearer token  
Authorization: Users (via bearer token)  
Description: Add a comment  

## 6. An ERD for your app


## 7. Detail any third party services that your app will use
- can check this

## 8. Describe your projects models in terms of the relationsips they have with each other
- closely mirror ERD. describe in terms of SQLAlchemy/ORM/describe hwo they work
- ? what reference is created b/w a Card and a User? vs what r/ship exists in the DB
- talk about same, but how a FK constraint would be represented in column of SQLAlchemy field
- can do SQL screenshot and explanation 
- e.g. backpopulating and foreign key method

## 9. Discuss the database relations to be implemented in your application
- discuss at DB level using DB terminology
- eg how FK would look like in DB on DB1v1
- can refer to ERD

## 10. Describe the way tasks are allocated and tracked in  your project 
- Trello/Kanban
- Agile short stories recommended 