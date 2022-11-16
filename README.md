# job-app-quiz

This program was created to solve a puzzle hidden in the HTML of a trading firm's website. This program solved it, and the secret message was an email address to which I could send a message to contact a recruiter for that company.

# Notes

The site *REDACTED*.com/quiz has a list of numbers.

Hidden in the HTML is a Javascript function to encode a string
into a list of numbers using 3 offsets

These numbers presumably contain a message with instructions to send a CV
These instructions are presumably in English, using latin letters

This code will retrieve the HTML, parse it, use a partly-brute force and partly-intelligent algorithm to determine the likely encoding seeds, and reverse the encoding
