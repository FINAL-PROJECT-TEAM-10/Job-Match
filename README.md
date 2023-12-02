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

### 📷 Diagram 📷
![Entity Relationship Diagram](./images/job_match_final.png)
### 📌 Legend 📌
- Table Connections: primary keys and related foreign keys are in the same color
  - admins: blue
  - job seekers: dark teal
  - companies: dark blue
  - job ads: light blue
  - mini cvs: teal
  - skills and requirements: green
  - locations: dark green
- Conditionals: columns that are used in some sort of conditional logic
  - status, blocked status, approval status*, sender, level, career type*, main cv
  remote status: magenta
  - date posted* and date matched*: dark yellow
  - min_ salary, max salary: dark red
- Long Blob data: columns that are used to store large files
  - picture, logo: dark orange
- String data: columns that contain string information necessary for application functionality
  - username, password, description, etc.: grey
- Unconnected data: primary keys that do not interact with other tables but are necessary for Skill-Sync
  - temporary tokens (id): purple

Note*: approval status, career type, date posted, and date matched logic has not been
implemented in the backend but remains for future work. See [future work](README.md#-future-work-).

### 📑 Explanation 📑
Our database supports functionality for three types of users: Admins, Job Seekers, and Companies.
Admins are slightly simpler than job seekers because they do not require the
full functionality of the user experience. They are taken out in a separate table from
other people (job seekers) because admin and job seeker functionality might diverge
even further from the current point of time and it is, thus, logical to separate them as early
as possible in database formation.

Both admins and seekers were deemed to require the same contact information, which would
allow other users (and in the case of admins: developers) to contact them. This is why
their contacts converge in the _employee_contacts_ table.

Similarly, to these users, companies also have contacts,
however one company is allowed more than one address. Currently, database entries only have one
address because some form of conditional logic must be added to choose which address should be
taken from the database. (see [future work](README.md#-future-work-)).

All contacts must have a broader location (city, country), which is validated in the
back-end before input. Location logic is also necessary for job ads and CVs as
they reveal where a company or job seeker (respectively) would like the job to be done.
_job_ads_has_locations_ and _mini_cv_has_locations_ are linking tables which are involved
in the logic if a job ad matches a CV.

The meat of our project is the matching functionality. This is achieved by having many
job ads belonging to one company and many CVs belonging to one job seeker. Then, depending
on whether a job ads requires certain professional skills (_job_ads_has_requirements_)
or a CV advertises that a job seeker already possesses these skills (_mini_cvs_has_skills_)
and what level are these at, an additional link is created to the junction table
_skills_or_requirements_.

There, all the requirements or skills that could be used by job ads or CVs reside.
Currently, the skill/requirement pool is controlled by admins who can add and delete skills
based on user feedback. The reason for this pool is so that when using our front-end,
businesses and seekers can simply cherrypick required skills,
while admins have moderation control over the database.

Skills versus requirements are used to evaluate matches in the backend
so that users receive quantified results in percentages in terms of how good a match was.
After matches pass the match request threshold (which can be set by the user, e.g. "Best",
"Good", etc.) they are recorded in _job_ads_has_mini_cvs_, which also records
who initiated the request (a company or a job seeker) and the match status (at first: "Pending").

The "Pending" match status allows for a user, for example, a company to post a match
request. If a professional then requests the same match, after the back-end retrieves
the "Pending" status, it will set the match as succesful, essentially completing
the essential functionality of the project.

Throughout the database there are numerous conditional columns such as match status and sender
(see [the diagram](README.md#-diagram-) above), who are similarly used or can be used
to expand selection criteria of different services.

Perhaps of greatest importance is that the search for matches can be adjusted by salary,
and users can be blocked.

The database also supports some form of user expression as users can write summaries/descriptions
and images (only 1 MB JPEGs are allowed) can be stored in the database as Large Blobs.
These images can be used as pictures for job seekers and admins and logos as companies,
although, admittedly, there is no logic to differentiate pictures from logos in the back-end.
The difference arises from the naming.

As a side note: job ads and CVs also have a remote status in _job_ads_has_locations_
and _mini_cv_has_locations_ which allows for extended matching. In other words,
an ad or a CV is not limited to its actual location if remote.


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

#### 📃 Job Ads Routers 📃

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

#### 🗝️ Authorization Services 🗝️
| Method                                                                  | Parameters                        | Purpose                                                                                                                          |
|-------------------------------------------------------------------------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| _verify_password_                                                       | text_password, hashed password    | verifies input password against hashed password in database                                                                      |
| _get_password_hash_                                                     | password                          | used in user account creation and when a randomly generate password is created after email activation-based password reset       |
| _get_password_hash_                                                     | password                          | used in user account creation and when a randomly generate password is created after email activation-based password reset       |
| _get_pass_by_username_admin_ OR _get...seeker_ OR _get...company_       | username                          | finds hashed password in the database based on user type                                                                         |
| _authenticate_admin_ OR _authenticate_seeker_ OR _authenticate_company_ | username, password                | returns user if user exists and if the input password matches the hashed password in the database                                |
| _create_access_token_                                                   | user_data, expiration_delta       | accepts user data such as id, email, etc. to encode a token and sets an expiration time difference for the validity of the token |
| _create_activation_token_                                               | activation_data, expiration_delta | generates a custom token similar to the access token, but only used for a specific purpose, such as password reset               |
| _is_authenticated_                                                      | token                             | decodes a token based on a secret key                                                                                            |
| _is_authenticated_custom_                                               | token                             | decodes a token based on a secret key                                                                                            |
| _password_changer_                                                      | payload, new_password             | uses the payload to find a user's type and updates the hashed password in the database                                           |
| _is_password_identical_by_type_                                         | payload, new_password             | uses the payload's user type and checks the appropriate table's hashed password to the input password                            |
| _generate_password_                                                     | None                              | generates a random password, used in password reset                                                                              |
| _activation_token_exists_                                               | activation_token                  | checks database for activation token, such as one generated during password reset                                                |
| _store_activation_token_                                                | activation_token                  | stores in database an activation token, such as one generated during password reset                                              |
| _delete_activation_token_                                               | activation_token                  | deletes in database an activation token, used to remove used tokens that are not for authentication                              |


#### 🏛️ Company Services 🏛️

#### 📃 Job Ads Services 📃

#### 👤Job Seeker Services 👤

#### 📤 Upload Services📤
A routerless service file has been created to harbour upload functionality.
At the current stage, the upload services handles only the upload of pictures/avatars.

| Method           | Parameters          | Purpose                                                                                                                                                    |
|------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| _upload_picture_ | payload, image_data | takes the payload to find the table and user in order to insert the image binary data into the database at the appropriate location                        |
| _get_picture_    | user_id, user_group | the method takes user_id and user_group directly and not through the payload because we have considered pictures on our platform to be publicly accessible |
| _is_file_jpeg_   | file                | checks if a file is a jpg/jpeg; uses PIL library, note: this method requires cursor reset (file.seek(0)) after its use                                     |

These services has been compartmentalized in a separate file
and the basic logic for file upload has been written out,
so that it could be used to extend upload features if needed. 

### 🔏 Private Details🔏
When installing Skill Sync, you must create a _private_details.py_ file that holds the
private information regarding the application. The file should be created in the same folder
as _main.py_. For security reasons, we have not uploaded the file but will guide you on what
the file should contain, so that the app can work.

Notably, the file contains the authorized in the SQL database and password,
as well as the Azure address to which the app should connect to access the database.

In addition, _private_details.py_ contains information about the
Mailjet public and secret api keys as well as the sender email that
Mailjet, an automated mailing solution, uses when sending emails through the app.

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


## 🔧 Functionality Checklist 🔧
Here we have listed the RESTful API requirements of the Job Match task and marked what we have completed.

### Important Note
For readability, we have changed the name of Company Ads to CVs/Mini-CVs because semantically
this reflects the purpose of the so-called "Company Ads" better.
A "Company Ad" can be misinterpreted as an ad for a company, when in fact it is
what job seekers (aka professionals) post to attract the attention of companies.
Thus, we chose to use CVs or Mini-CVs.

### ❗ MUST Requirements: ❗
#### 🧱 REST API 🧱
- [x] Provide a restful API that supports the functionality of the system

#### 🗺️ Database 🗺️
- [x] Relational database
- [x] Normalized
- [ ] Script for creating the database
- [ ] Script for populating the database

#### 🌐 Public Part 🌐
- [x] Login endpoints
- [x] Register endpoints

These endpoints are handled by three separate routers for the three separate types of users:
- Admins
- Job Seekers
- Companies

#### 🏛️ Companies 🏛️
- [x] View and edit company Info
- [ ] View a company's job ads
- [ ] View a company's archived (matched) job ads
- [ ] Job ads can be created
- [ ] Companies can search in CVs

All of the above is accessible only when the user has been authenticated.

#### 👤Job Seekers/Professionals 👤
- [x] Can edit their own info
- [x] Can view own CVs
- [x] Can create, view, edit a CV
- [ ] Have a list of matches

#### 🔎 Searching 🔎
- [ ] Companies can search for CVs
- [ ] Professionals can search for job ads
- [ ] Salary range can be used in searches
- [ ] Skills requirements can be used in searches
- [ ] Locations can be used in searches
- [ ] Supports match functionality, i.e. returns a result

#### 🤝 Matching 🤝
- [ ] Companies can match more than one CV
- [ ] Job seekers can match a job ad

### ❕SHOULD Requirements❕
#### 🏛️ Companies 🏛️
- [x] Basic info
- [x] Can upload pictures 

#### 👤Job Seekers/Professionals 👤
- [x] Basic info
- [x] Can upload pictures
- [x] Can set up a main ad
- [ ] List of matches can be public or hidden

#### 📃 Job Ads 📃
- [x] Basic Info

#### 🪪 CVs 🪪
- [x] Basic Info
- [ ] Private (can be found by id, but does not appear in search)

#### 🔎 Searching 🔎
- [ ] Companies can search for professionals
- [ ] Professionals can search for companies
- [ ] Search threshold: searching can accept inexact matches
- [ ] Salary range can be soft, i.e. range can be expanded with acceptable flexibility (input percent)
- [ ] Skills/Requirements can be soft, i.e. some may be missing from a match

#### 📫 Mailjet Integration 📫 
- [ ] Notification for a matching request

#### 🐤 Twitter Integration 🐤
- [ ] Sends tweets on ad creation through a business account

#### 🧪 Unit Testing 🧪
- [ ] Service layer must be unit tested

#### 🌿 Git Repository 🌿
- [x] Contributions from all team members
- [x] Complete application source code
- [ ] Scripts for database creation and data population

#### 📖 README File 📖
- [x] Project description
- [x] Link to Swagger documentation
- [ ] Link to hosted project
- [ ] Instructions on local installation
- [ ] Images of database relations

### ✅ COULD Requirements ✅
#### 📃 Job Ads 📃
- [x] Set of requirements

Requirements are controlled by admins: only admins can add/delete requirements.

Job Ads and CVs are required to use the preset requirements.
In a real-world setting, users (job_seekers and companies) would be able to request skills or requirements.

#### 🔎 Searching 🔎
- [ ] Companies can search for other companies
- [ ] Professionals can search for other professionals

#### 🎛️ Administration 🎛️
- [ ] Admins approve companies' and job seekers' registration
- [ ] Admins can block/unblock companies and professionals
- [ ] Admins can delete application data (profiles, ads, CVs, etc.)
- [x] Admins can add/delete or approve skills/requirements

#### 📫 Mailjet Integration 📫
- [ ] Notification for ads/CVs

####  🦺 Mock Third-Party Services🦺
- [ ] Mock info for skills/requirements
- [ ] Make range suggestions or update the skill pool with trending entries

#### 📎 Other Third-Party Services📎
- [x] Validate geographic locations


### 💫 Bonus Work 💫
[We can add here bonus things that are outside of the scope of the official requirements]
#### 🔐 Forgotten Password 🔐
- [x] Password can be reset through registered email 

#### 📫 Mailjet Integration 📫
- [x] Password Reset functionality through two e-mails

The first email contains an activation link that uses a custom token for the reset,
the second contains a randomly generated password.
#### 🌿 Git Repository 🌿
- [x] Use of branches

#### 🗺️ Online Database 🗺️
- [x] Database hosted on Azure
 


## 📫 Mailjet Setup Guide 📫
To use the automatic emailing functionality through endpoint access, you need to set up
a Mailjet account and include the credentials in a _private_details.py_.

The guide to setting up Mailjet is provided on their website. You need to follow
[the getting started guide](https://dev.mailjet.com/email/guides/getting-started/).
Within the guide, it is explained [how to create a Mailjet account](https://app.mailjet.com/signup),
then how to retrieve [both your API and Secret keys](https://app.mailjet.com/account/api_keys).

For the mailing functionality of Skill-Sync to function, you need to include four things in
_job-match-app/private_details.py_: the public API, the Secret key, and the sender's email
(the registration email). The fourth is the address of Skill-Sync.

```
mailjet_public_api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
mailjet_secret_api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
mailjet_sender_email = 'XXXXXXXXXXXXXXXXXXXX@XXXX.XXX'
```

You also need to define the address on which the Skill-Sync API is run.
```
skill_sync_address = 'XXXXXXXXXXXXXXXXX'
```
For the purposes of a locally run installation, you can substitute the address with localhost.
For example:
```
skill_sync_address = 'http://127.0.0.1:8000/'
```

Our API imports these variables to support mailing functionality, which can be found in
_job-match-app/common/mailing.py_.


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
