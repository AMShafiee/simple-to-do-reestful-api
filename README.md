# simple-to-do-reestful-api
This is a simple fun test of restful API for to-do tasks in some projects with a team of some developers and some (project) managers. 
I put these roles in a table to be extendable, but for now, it is assumed that each user just can take one role (the relationship between 
The User and the Role table is "one to many" and not "many to many").

My favourite framework is Django, and I'm an expert in it. But this is my first practice to code with the Flask framework.

As this is just an exercise task, I just put some arbitrary attributes in the models. As an instance, the User table just has first_name
and last_name where there are a lot of other important attributes that are candidates to be added, such as data_created, contact_info, etc.
Also, I hate it when programmers do not take enough care to validate the input values, but unfortunately, I didn't have enough time 
to put complete validators for this small fun task.

This is not a huge project that I use a microservice architecture for it. So I didn't consider more than one place to keep the data. 
But I designed two separate packages for the APIs. One for the APIs related to the users and authentication in two modules.
Another package contains the implementation of the APIs related to the projects and tasks.

However, I usually prefer to get the ID of the objects that the API will process, but this small project doesn't have getter APIs 
that provide the consumer with a list of objects with their IDs. The exception is the APIs to get the task list. So the frontend 
can use the task IDs in other task-related APIs. For other tables (User and Project), I used another unique attribute of them 
(username and project_name) to overcome the lack of access to IDs from the front-end. 

All of the APIs can be called by the more secure POST method, and return a value under the "was_successful" key that shows 
whether they could successfully do their duties or not. Another key is "message" that contains a human-readable text 
to explain the result to the caller. The status is always 200 and I didn't use 401 or another error status. 

I dockerized the project and also put some unit tests in it. I was writing the unit test and then implementing the API 
(as it is in the TDD methodology). It was OK till the start of the second package. An error occurred that I 
couldn't continue using the automatic unittest. So I used postman to completely test the functionality of the APIs. 
I will commit and push the patch to fix the problem with the unit test ASAP (if my daily routine duties give me any chance).
