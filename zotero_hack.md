Update 2019
---------------------------
Start with alwaysMap and follow. You'll find lots of maps.

My work from 2018
----------------------------

The below hack no longer works because the code has changed a lot since then.

- Open `BibTeX.js` in the `zotero/translators` directory.
- Try searching for `alwaysMap` and commenting out the baddies.
- Search for `function escapeSpecialCharacters` 
  and remove the first args of the `replace` commands corresponding to the characters you don't want edited.
- Restart Zotero.

If you want to just stop all escape character editing, `return str`.

Here's my code from 2018


```
// See http://tex.stackexchange.com/questions/230750/open-brace-in-bibtex-fields/230754
var vphantomRe = /\\vphantom{\\}}((?:.(?!\\vphantom{\\}}))*)\\vphantom{\\{}/g;
function escapeSpecialCharacters(str) {
  //replace(/[\{\}]/g, function(c) { return alwaysMap[c] })
	var newStr = str.replace(/([\#\%\&])/g, "\\$1");
	
	// We escape each brace in the text by making sure that it has a counterpart,
	// but sometimes this is overkill if the brace already has a counterpart in
	// the text.
	if (newStr.indexOf('\\vphantom') != -1) {
		var m;
		while (m = vphantomRe.exec(newStr)) {
			// Can't use a simple replace, because we want to match up inner with inner
			// and outer with outer
			newStr = newStr.substr(0,m.index) + m[1] + newStr.substr(m.index + m[0].length);
			vphantomRe.lastIndex = 0; // Start over, because the previous replacement could have created a new pair
		}
	}
	
	return newStr;
}
```

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

