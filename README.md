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
