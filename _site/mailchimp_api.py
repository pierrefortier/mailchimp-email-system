# Python script for updating mailchimp templates
#
# External dependencies:
#   - mailchimp_marketing
#   - python-frontmatter
#
# Created by Pierre Fortier
# fortier.20@osu.edu
#

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import frontmatter
import os

# Setup for mailchimp API
client = MailchimpMarketing.Client()
client.set_config({
    "api_key": "c124b6b7fce63279db5483bf247f3e3a-us1",
    "server": "us1"
})

# Read template directory and template frontmatter info
templateDirectory = r'email-templates/'
for entry in os.scandir(templateDirectory):
    if (entry.path.endswith(".md")
        or entry.path.endswith(".markdown")) and entry.is_file():

        template = frontmatter.load(entry.path) #Loads template frontmatter into 'template' var

        #Open HTML template file
        with open('_site' + template['permalink'] + '.html', 'r') as file:
            html = file.read().replace('\n', '')
            print("→ Updating template " + template['title'])
        try:
          # This pushes the html to mailchimp
          response = client.templates.update_template(template['mailchimp_id'], {"name": template['title'], "html": html})
          print("✓ Done")
        except ApiClientError as error:
          print("Error: {}".format(error.text))
