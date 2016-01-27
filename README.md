# Berichtenbox Forwarder

This little python script forwards all messages left in the message box of mijn.overheid.nl. The goverment decided it would be wise not to send any content... It takes a lot of manual labour to fetch the content of the message. This is why I wrote this script. You can run it from the commandline (or as a cronjob) with the following command and credentials from DigiD:

>	python berichtenbox.py --username="username" --password="password"

If you decide to put it in a cronjob, I've also added the functionality to cache which messages are already forwarded. This is done with the `shelf` module.

## Requirements

The only requirement this little script needs is Mechanize. Which you can easily install with: `pip install mechanize`.

## License

MIT