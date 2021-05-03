# Vertigo Discord Bot
Vertigo is a discord bot I created with discord.py. It has a couple of features:

## Command Prefix
The command prefix is a period/dot. ( . )

## Note Taking
You can use it to take plain-text notes. Only you can see your notes. The following commands are available for note-taking:

"notes" - Shows a list of all your notes.

"note [title]" - Shows a particular note. Please enter the correct title.

"writenote [title] [content]" - Use this to create a new note. The title should be wrapped in "double quotes".

"removenote [title]" Use this to delete an existing note that belongs to you. Please enter the correct title.

## Wishlist
You can put items in your wishlist, along with a URL to that item. The following commands are available for wishlist:

"wishlist" - Shows your wishlist and all the items in it.

"add-to-wl [item_name] [item_url]" - Use this to add an item to your wishlist. The item_name should be wrapped in "double quotes". The item_url is optional. 

"remove-from-wl [item_name]" - Use this to remove an existing item from your wishlist. Please enter the correct name of the item.

## Reminders
You can also use this bot to add reminders so you never forget anything. The bot will ping you when the reminder is due. The following commands are available for reminders:

"reminders" - Shows a list of all your reminders, along with when they are due.

"reminder [time] [reminder]" - Use this to create a new reminder. [time] should be in the format of 1d23h59m, where the number before "d" is the number of days, and the number before "h" is the number of hours, and so on.

"rm-reminder [reminder]" - Use this to remove an existing reminder from your account. Please enter the correct [reminder] text. You can also use "reminders" to get a list of all your reminders, and copy paste the reminder text from there.

## Misc features
This bot can also do a couple other things:

"dl-attachments [channel]" - Downloads all attachments from a particular channel, puts them all in a .zip file, and uploads the .zip file to the channel so you can downlaod it. This was a feature requested by a friend and isn't really something you'd see in most bots.

"clear [amount]" - Clears the last 5 messages if [amount] is not specified. Otherwise, deletes the amount of messages the user wants.

"kick [user] [reason]" - Use this to kick a user from your server. The reason is an optional argument.

"8ball [question]" - Ask the Magic 8 Ball a question. In my experience, it has always been correct :).
