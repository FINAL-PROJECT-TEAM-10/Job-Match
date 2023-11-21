# [A51] Skill Sync [2023]
_Skill, Sync, Match!_


## 🧑‍💻 Contributors 🧑‍💻
Borislav Bonev, Ivaylo Petrov, Andrey Filipov

## 🗺️Overview 🗺️
[To be finalized]

## ⚒️ Functionality ⚒️
[To be finalized]

## 💿Installation 💿
[To be finalized]

## 🗺️ Database Overview 🗺️
[To be finalized]

### Things to Note
[To be finalized]

#### ➕ _Junction Tables_ ➕



## 🏭 API Structure ️🏭


### 🗿 Models 🗿
Models are found in _/data/models.py_

| Modeled | Number of Models | Types of Models | Purpose |
|---------|------------------|-----------------|---------|
|         |                  |                 |         |
|         |                  |                 |
|         |                  |                 |         |
|         |                  |                 |         |
|         |                  |                 |         |
|         |                  |                 |         |
|         |                  |                 |         |

### 🗃️ Common Files 🗃️

#### 🗝️ Authorization 🗝️

#### 🌍 Country Validators 🌍

#### ☑️ Job Seeker Status Check ☑️

#### ➗ Separators Validator ➗

### 🛤️ Routers 🛤️

#### 🎛️ Admin Routers 🎛️

#### 🏛️ Company Routers 🏛️

#### 📄 Job Ads Routers 📄

#### 👤 Job Seeker Routers 👤

#### 🪙 Token Router 🪙

#### 📄 Further Documentation 📄
Some of the routers accept dynamic variables in the body of requests in JSON format.
We are using FastAPI, a framework that generates parts of the endpoint documentation automatically.
To see what is expected in the body of a request, start the server and go to the server's ip /docs.

With the default setup of our API's server, this additional documentation can be found at
http://127.0.0.1:8000/docs. The automatic documentation supports authentication and authorization
functionality.

### ⚙️ Services ⚙️
[To be finalized]
#### 🎛️ Admin services  🎛️

#### 🗝️ Authorization Serivces 🗝️

#### 🏛️ Company Services 🏛️

#### 📄 Job Ads Services 📄

#### 👤Job Seeker Services 👤

### 🔏 Private Details🔏
When installing Skill Sync, you must create a _private_details.py_ file that holds the
private information regarding the application. The file should be created in the same folder
as _main.py_. For security reasons, we have not uploaded the file but will guide you on what
the file should contain, so that the app can work.

Notably, the file contains the authorized in the SQL database and password,
as well as the Azure address to which the app should connect to access the database.

In addition, _private_details.py_ contains information about the
mailjet public and secret api keys as well as the sender email that
mailjet, an automated mailing solution, uses when sending emails through the app.

[To be finalized: upload a censored image]

### 📅 Database Communication 📅
Connections to the active database are described in _job-match-app/data/database.py_

The internal method __get_connection()_ can be used to set how connections are made to the database.

There are four types of queries that are written out in _database.py_

| # | Method                                                                                    | Returns                 | Explanation                                                                                                                             |
|---|-------------------------------------------------------------------------------------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| 1 | _read_query<br/>(sql: str, sql_params=())_                                                | results                 | method which returns the results of a SELECT query                                                                                      |
| 2 | _insert_query<br/>(sql: str, sql_params=())_                                              | last row index          | method which returns the index at which data has been inserted through an INSERT query                                                  |
| 3 | _update_query<br/>(sql: str, sql_params=())_                                              | number of affected rows | method which allows for the modification through an UPDATE or DELETE query                                                              |
| 4 | _update_queries_transaction<br/>(sql_queries: tuple[str, ...], sql_params: tuple[tuple])_ | boolean                 | method which allows for multiple UPDATE and DELETE transactions and returns a boolean on whether the transaction was successful or not. |



## 🔬 Future Work 🔬
### 🔐 Password reset 🔐
A possible addition to the database is to track when a password is last modified and prompt the user to change
their password once a certain threshold has been passed.

Currently, the password reset only asks for the user email and reset the password, stores it in the database
and sends an e-mail to the corresponding e-mail with the new password. This is not ideal
because it is susceptible to trolling. If a user knows somebody's email they can reset the password
for them. While this is not a security breach, it can frustrate users. 

A better way of implementing password reset is to initially send an email link with an activation link,
which when followed leads to the actual password reset.


### 🪙 Token handling 🪙
Currently, the token is issued at login and carries an expiration time.
The token is generated after querying the database.

For example, old admins and malicious
attackers only have 20 minutes to carry out token-based requests with old or hijacked tokens,
while normal users can have sessions of 1440 minutes (24 hours) without being reprompted to log back in.
[NOTE: Change it to 20 min before going live]

However, it would be better to use shorter access tokens (that do not query every time the database)
) and use refresh tokens, while also whitelisting/blacklisting tokens so that tokens can be managed better.
Even if refresh tokens check against the database if a user exists,
proper implementation can reduce the amount of checks against the database.

If important user changes happen or if we believe the database has been compromised, we can change the JWT in
order to force users to login again and receive their new, updated.

### 💥 Cascade deletions 💥


# Appendix

## 💻 Front-End  💻
[To be updated]


## 🔧 Functionality in Detail 🔧
Here we have listed the RESTful API requirements of the Job Match task and marked what we have completed.

### ❗ MUST Requirements: ❗
- [ ] [Checklist to be uploaded]

### ❕SHOULD Requirements❕
- [ ] [Checklist to be uploaded]


### ✅ COULD Requirements ✅
- [x] [Checklist to be uploaded]

## 📫 MailJet Setup Guide 📫
[To be finalized]

To use the automatic emailing functionality through endpoint access, you need to setup
a mailjet account and include the credentials in a _private_details.py_. To do so... [to be continued]

## 📦 Library Versions 📦
Python version used for the project is 3.11.

The project has been tested and works on MariaDB 10.11 and MariaDB 11.1.

Library versions of the working project have been provided in the
_requirements.txt_ file. [Will be uploaded at December 7th, the latest]

### 💿 Library Installation Code 💿

```
pip install opencage
pip install python-jose[cryptography] 
pip install passlib
pip install python-multipart
pip install bcrypt
pip install mailjet_rest
```

# Thanks!
