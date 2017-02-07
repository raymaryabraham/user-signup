#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re

signup_form="""
<!DOCTYPE html>
<html>
  <head>
	<title>Unit 2 Signup</title>
	</head>
	<body>
		<h2>Signup</h2>
		<form method="post">
			<table>
			      <tr>
			         <td><label>Username </label></td>
					 <td><input type="text" name="username" value="%(username)s">
				     <span style="color: red">%(e_name)s</span></td>
				  </tr>
				  <tr>
				     <td><label>Password</label></td>
					 <td><input type="password" name="password">
				     <span style="color: red">%(e_pass)s</span></td>
				  </tr>
				  <tr>
				  	 <td><label>Verify Password </label></td>
					 <td><input type="password" name="verify">
				     <span style="color: red">%(e_verify)s</span></td>
				  </tr>
                  <tr>
				     <td><label>Email (optional)</label></td>
					 <td><input type="text" name="email" value="%(email)s">
				     <span style="color: red">%(e_email)s</span></td>
				  </tr>
			</table>
			<input type="submit">
		</form>
	</body>
</html>
"""

welcome_form="""
<!DOCTYPE html>
<html>
	<head>
		<title>Unit 2 Signup - Welcome</title>
	</head>
	<body>
		<h2>Welcome, %s!</h2>
	</body>
</html>
"""

def escape_html(s):
	return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_name(s):
	return USER_RE.match(s)

def valid_pass(s):
	return PASS_RE.match(s)

def valid_email(s):
	if s == "":
		return True
	else:
		return EMAIL_RE.match(s)

def match_pass(p1, p2):
	return p1 == p2

class Signup(webapp2.RequestHandler):
	def write_form(self, username="", email="",
		           e_name="", e_pass="", e_verify="", e_email=""):
		self.response.out.write(signup_form % {"username": escape_html(username),
			                             "email": escape_html(email),
			                             "e_name": e_name,
			                             "e_pass": e_pass,
			                             "e_verify": e_verify,
			                             "e_email": e_email})

	def get(self):
		self.write_form()

	def post(self):
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		user_verify = self.request.get('verify')
		user_email = self.request.get('email')


		password = valid_pass(user_pass)
		verify = valid_pass(user_verify)
		email = valid_email(user_email)

		e_name = ''
		e_pass = ''
		e_verify = ''
		e_email = ''

		if not user_name and valid_name(user_name):
			e_name = "That's not a valid Username"
		if not password:
			e_pass = "That's wasn't a valid Password"
		if not match_pass(user_pass, user_verify):
			e_verify = "Your passwords didn't match"
		if not email:
			e_email = "That's not a valid email"

		if password and (not e_verify) and name:
			self.redirect('/welcome?username=%s' % user_name)
		else:
			self.write_form(user_name, user_email, e_name, e_pass, e_verify, e_email)

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.out.write(welcome_form % username)

app = webapp2.WSGIApplication([
	('/', Signup),
	('/welcome', WelcomeHandler)
], debug=True)
