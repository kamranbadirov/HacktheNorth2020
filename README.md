# Gregor - HackTheNorth2020

This is Gregor, built for Hack the North 2020++

![Gregor logo](https://github.com/kamrandb/HacktheNorth2020/blob/main/gregorlogowhite.png)

## Inspiration
When COVID hit, all events were moved online. Many have turned to announcing events on social media platforms, where information about the date, time, and location of the event are contained in visually appealing infographics. However, this isn't very user friendly - presenting the event as an image requires the user to manually enter the information in their calendar app. This creates a barrier of entry, since by the time the user has finished scrolling through social media and has time to upload an event in their calendar, they may have forgotten key elements, and don't want to go through the trouble of finding the post all over again. This decreases attendance of an event.

This increase in virtual meetings and events also corresponded with a globalization of participants - now that the principle avenue of meeting is virtual, collaborators don't have to be in the same room, or even in the same country! Yet, there still needs to be a way to include everyone, regardless of global position or time zone. To keep graphics visually appealing, usually only one time zone is included - for people living across the world, this can be a big nuisance!

So that events are more internationally accessible and have greater attendance, there is room in the market for a tool that can parse graphic images to create calendar invites, so events are easy to join and interpret for everyone.

## Introducing Gregor
The majority of the world uses the Gregorian calendar, introduced in the 1500s. This format is ubiquitous and understandable to everyone - the way we share events should be, too. Gregor is a tool that makes this possible, bringing the old technology of the calendar into the modern world.

Gregor requires input of an image (a poster or infographic) and timezone (of the user, and of the poster), so that the event is customized to you, helping you stay organized and in touch, wherever in the world you are. From this input, it automatically generates a calendar event that is added to your Google Calendar.

Gregor's backend comprises of two main parts: a machine learning algorithm that uses Microsoft's Azure API to recognize and interpret text corresponding to calendar events, and a integrated framework that uses the data found in the image to create a new event in your calendar using the Google Calendar API.

## Challenges we ran into
- We had difficulty figuring out how to have the user locally upload an image into Azure so that we could analyze it with our algorithm. This was solved by putting our heads together as a team, and asking for help - we spoke with multiple Microsoft representatives, who helped significantly to finding a suitable workaround.
- Integrating the Framer UI design with the front end proved to be more difficult than we anticipated. Although we originally planned on using React and importing Framer designs directly, we ended up using Framer only as a prototyping tool and as inspiration for the website. Final coding was done in HTML/CSS using graphic softwares to create artwork and tools from Bootstrap. The Flask framework in python was used to combine the front-end and back-end.

## What's next for Gregor
- Integrating with a browser extension so that Gregor can create calendar invites directly from your social media app.
- Determining time zone directly from the image and from the geographic location of the user, so no time zone input is required.
- The ability to parse more complex calendar images, such as those with multiple events on the same image, or with graphical time blocking.
- Directly changing the time text of an graphic to the user's timezone to generate a series of more usable graphics for different geographic locations.

## Tools we used
Backend:
- Microsoft Azure API
- Google Calendar API
- Python(Flask Framework)

Frontend:
- Framer UI design
- HTML/CSS
- Boostrap 
- Flask to tie together frontend and backend

## How to use
Step 1. Create a virtual environment and activate it.
Step 2. Run on terminal: pip install -r requirements.txt
Step 3. Run on terminal: python app.py
Step 4. visit localhost:/5000
