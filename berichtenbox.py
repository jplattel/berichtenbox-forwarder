import argparse
import mechanize
import logging
import shelve

# Argparse
parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='Digid Gebruikersnaam', required=True)
parser.add_argument('-p','--password', help='Digid Wachtwoord', required=True)
args = parser.parse_args()

# History, for caching which messages are forwarded
history = shelve.open('history')

# Configure logging
logging.basicConfig(format='%(asctime)s [%(levelname)s] : %(message)s', level=logging.INFO)

# Set up mechanize (ignore robots so it is possible to run this script)
br = mechanize.Browser(factory=mechanize.RobustFactory())
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Open the page for getting the auth token
logging.info('Getting authentication token')
br.open('https://mijn.overheid.nl/berichtenbox')
br.select_form(nr=0)
br.submit()

# Select login form and put in data, then submit
logging.info('Logging in to mijn.overheid.nl')
br.select_form(nr=0)
br.form['authentication[digid_username]'] = args.username
br.form['authentication[wachtwoord]'] = args.password
br.submit()

# Check if new providers have been added. Nobody cares, so just accept 'em
for form in br.forms():
    if 'class' in form.attrs and str(form.attrs["class"] == "newproviders"):
	
        logging.info('New providers found. Automatically accepting...')

        br.form = form
        br.find_control('acceptatie_afnemers[accept_afnemers]').items[0].selected = True
        br.submit()
        break
	
# Get to berichtenbox
logging.info('Navigating to Berichtenbox')

br.follow_link(list(br.links(text_regex='Berichtenbox'))[0])

# Parse links for each message
for l in br.links(url_regex='/berichtenbox/bericht/'):

	# If this message has not been forwarded yet:
	if not history.has_key(l.url):

		logging.info('Forwarding: ' + str(l.text))

		# Forward this messages
		br.follow_link(l)	
		br.select_form(nr=1)
		br.submit(name='send')

		# Add to history
		history[l.url] = l.text

	# If the message already has been forwarded, skip it.
	else:
		logging.info('Not forwarding, file already forwarded.')
		
logging.info('Done!')
history.close()

