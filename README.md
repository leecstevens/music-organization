# music-organization

This was a project that was started as a "Screw You, Apple" project after calling their support and finding a "Scorched Earth" way of organizing all of my massive music collection WITHOUT having to manually choose file by file.

I was told in order to remove duplicates from my library I needed to "Command-Click" every file individually and then delete said entry from the library.

This was WAY too time consuming and I had over 25,000 entries to delete.  So, this project is 2 seperate processes, one to organize files, and another to organize metadata.

# Before you begin - IMPORTANT

## This is a powerful piece of code, and will screw you over if you let it and are not careful, keep reading below.  I know we all hate text walls, but it will be the difference in swearing by me rather than at me in the future.

This code was written for me, and as such I have no regard for you or your situation.  I was out to solve my own problem, as you are out to solve yours (or stalk my repository looking to steal code).

As a result, make sure you have multiple backups of your collection, as you are likely going to screw something up.  This is not a challenge or a call to be better, this is a simple warning not to be stupid.  I won't be liable for your stupidity, lack thereof, or any emotion besides gratitude you have for this free code I'm giving to the world of my own kindness.

# The problem statement

With the file system:

- Too many excess files - I had m4a and mp3 files duplicated in multiple places.
- I had files that were stacked from "auto-copies" such as: "My Song.mp3" and "My Song 1.mp3" and "My Song 2.mp3" and so on.
- Once going to a Mac, the .DS_Store file loves to find its way places.

With the Metadata:

- Too much going on in the Metadata to speak of.
- Too many "like" entries as artists, such as Artist 1 would be teamed with Artist 1/Artist 2 and so forth, so it led me to have multiple artists which were really the same artist.
- Too many "Unknown" or "Various" artists, so clean them up and change the metadata to add them to the MP3 metadata.  After all, who doesn't love organizing with every box marked "Miscellaneous"?  Yeah, didn't think so.
- Often, a "Various" or "Sountrack" had identification data from its composer.  Use that info to keep it from the "Various" bucket as much as possible.
- Almost ALL my files have a number (track) preceeding them.  This may be okay in the file system, but I use a streaming service where if I want to delete a file from the server, I need to know the preceeding track + file name to find it easily.  Screw that, just remove the leading numbers.  Not fool proof, but I am fine with a few song casualties out of tens of thousands.
- When there is no artist or album artist (contributor) available, keep it from going "Unknown" by using the parent folder name.  The name is organized as such:  Root / Artist / Album / Song
- Some artists have improper capitialization

I'm sure more will come up over time, but this is my first thoughts.

# The real problem statement

I am someone who badly neglected their digital music collection for over 20 years, so now enough is enough.

# Lastly...

Enjoy the code, but again, don't just run it.  If bad things happen to you, I will laugh at your complaints and cries.  If you were stupid enough not to play with safe data, there is really no hope for you or your music collection.  Did I drive that home enough?

It is my hope this code will be a benefit to you, and to those of you learning Python, something to learn from.
