# c_manga_d

CMD manga download and reader using Mangadex API
But you can manage more thing such as read list, rating etc


Idea:
  - Download mangas and read them using few commands
The project is in early-dev phase

How it works currently(mangadex part):
  - create a .env file
  - paste your mangadex username,password,client and secret key as [UNAME,PASSWORD,CLIENT_KEY,SECRET_KEY]

Commands:
 - rm: Get a random manga name
 - r <name>: Read <name> manga
 - dw <name>: Download <name> manga
 - upd <name>: Download the last uploaded chapter for <name> manga
 - addtolist <name>: Add to reading list, completed etc <name> manga. After this command a menu appears and you can choose the list
 - addtocustom <name>: Add <name> manga to a custom list. After the command an input field will appear and you have to write the list name
 - rate <name>: Rate <name> manga. After the command you can input the rating into an input field. 

To-Do list:
 - read✔️
 - auth and login ✔️
 - update downloaded chapters ✔️
 - add manga rating ✔️
 - add manga to custom lists and libraries(readlist, completed etc)✔️
 - cannot read long chapters because the canvas cut them -> paging✔️
 - TTS(Text To Speech) feature into the reader
 - tests
 - setup and "tutorial"
