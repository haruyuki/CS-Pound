"use strict";
function typeItOut () {
  if (i < txt.length) {
    document.getElementsByClassName("terminal")[0].innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeItOut, 50);
  }
}
if (document.getElementsByClassName("terminal").length > 0) {
  var i = 0;
  var txt = `cat changelog.txt --latest
v1.6.1: 22/03/18
- Removed commands in ,help that aren't implemented yet
- Added note about not being able to remove Remindme's in Remindme's help page
- Changed playing status to replace bot version to my Discord tag. You can still view the bot version in ,statistics`;
  setTimeout(typeItOut, 1800);
}
