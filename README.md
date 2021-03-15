# DSA Skills

## Dependencies

#### Flask

- Small, lightweight application framework used to create and manage a server.

#### pandas

- Used for importing csv to sqlite database for easier management and maintainability.

#### SQLAlchemy

- ORM used to simplify process of mapping database responses to python objects.

#### Flask-SQLAlchemy

- Flask extension that simplifies usage of SQLAlchemy for applications running specifically on Flask.

#### flask-restplus

- Flask extension that helps structure code when specifying an API.

---

## Installation

Clone repository.

Run `pip install -r requirements.txt` inside project root folder.

Put membership csv in project root directory as file named the value of `MEMBER_FILE_NAME` in config.py (defaults to `members.csv`)
## Running

Run `python app.py` to start

## Usage

Visit `localhost:5000` to view all members.

Call `GET localhost/api/members` to get a list of all members. 

- Add query parameter `?chapter_filter={string}` to filter by chapter name.

- Add query parameters `?sort_by=True&order={first_name|last_name}` to sort by first or last name. Add parameter `&inverse=True` to sort descending.

- Returns a list of member json objects and http response status code.

Call `POST localhost/api/members` to create new member (attach data as json object)

- Returns member json object and http response status code.

Call `GET localhost:5000/api/member/{id}` to retrieve member with known id (replace {id}).

- Returns member json object and http response status code.

Call `PUT localhost:5000/api/member/{id}` to update member with known id (replace {id} and attach data as json object).

- Returns member json object and http response status code.

Call `DELETE localhost:5000/api/member/{id}` to delete member with known id (replace {id}).

- Returns message: Member Deleted successfully if successfully deleted and http response status code.

Enter chapter name in input box and submit in order to filter by chapter.

Click column headers to sort by header.

# Questions

If you had multiple days to work on this, what improvements would you make and why? 
- I would enhance the code in a couple ways. First, I would add an authentication system to ensure that only authenticated users are allowed to access the endpoints. Next, I would create tests around each endpoint to ensure that the api remains healthy. I would also build out an error handling / logging system to quickly identify where in the code bugs appear, instead of relying on http status codes to determine if the correct code path is being followed. Additionally, adding type hints helps readability and maintainability to a project, so I would type all appropriate variables and properties. Finally, I would document the endpoints more thoroughly, recording things like the shape of each return object and all possible status code responses.

What follow-up features would you add?
- This depends entirely on the requirements of the project. If the project only calls for the creation of a membership api to be consumed by all external programs, regardless of things like authentication, then this code is sufficient to meet those needs and more features would only add technical debt and code that needs to be maintained. If the project owners/managers decided that additional requirements like authentication, a way for a member to update only their information, or for chapters to be able to access only those members who belong to their chapter, then those would be features I would implement. Regardless of those requirement considerations, I would absolutely migrate to a more robust database, as maintaining data in a csv file (or a sqlite database, used in my implementation) is not the most practical and scalable solution.