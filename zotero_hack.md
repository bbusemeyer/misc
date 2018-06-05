My work from 2018
----------------------------

The below hack no longer works because the code has changed a lot since then.

- Try searching for `alwaysMap` and commenting out the baddies.
- Search for `function escapeSpecialCharacters` 
  and remove the first args of the `replace` commands corresponding to the characters you don't want edited.
- Restart Zotero.

If you want to just stop all excape character editing, `return str`.

Advice from 2009
----------------

[source](https://forums.zotero.org/discussion/5324/bibtex-and-greek-characters/p1)

1) Find your profile. 
2) Go under the zotero\translators and edit the BibTeX.js file
3) Change line the "alwaysMap" array (line 1528) from the following:

var alwaysMap = {
"|":"{\\textbar}",
"<":"{\\textless}",
">":"{\\textgreater}",
"~":"{\\textasciitilde}",
"^":"{\\textasciicircum}",
"\\":"{\\textbackslash}"
};

to the following

var alwaysMap = {
"|":"{\\textbar}",
"<":"{\\textless}",
">":"{\\textgreater}" //,
//  "~":"{\\textasciitilde}",
//  "^":"{\\textasciicircum}" 
//  "\\":"{\\textbackslash}"
};

This will remove escaping ~, ^ and \.

Now change the following on line 1806:

value = value.replace(/[|\<\>\~\^\\]/g, mapEscape).replace(/([\#\$\%\&\_])/g, "\\$1");

to the following:

value = value.replace(/[|\<\>]/g, mapEscape).replace(/([\#\%\&])/g, "\\$1");

4) Save the file. You won't even need to restart Firefox!

Awesome. I'm a happy tomato. Sorry for the trouble and thanks again for the help!

