/*

	Rikaichan
	Copyright (C) 2005-2015 Jonathan Zarate
	http://www.polarcloud.com/

	---

	Originally based on RikaiXUL 0.4 by Todd Rudick
	http://www.rikai.com/
	http://rikaixul.mozdev.org/

	---

	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 2 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

	---

	Please do not change or remove any of the copyrights or links to web pages
	when modifying any of the files.

*/

/*
  Rikaisama
  Author:  Christopher Brochtrup
  Contact: cb4960@gmail.com
  Website: http://rikaisama.sourceforge.net/
*/

var rcxMain = {
	altView: 0,
	enabled: 0,
	sticky: false,
	id: '{697F6AFE-5321-4DE1-BFE6-4471C3721BD4}',
	version: null,
  lastTdata: null,              // TData used for Sanseido mode and EPWING mode popup
  sanseidoMode: false,          // Are we in Sanseido mode?
  sanseidoReq: false,           // XML HTTP Request object for sanseido mode
  sanseidoFallbackState: 0,     // 0 = Lookup with kanji form, 1 = Lookup with kana form
  superSticky: false,           // Are we in Super Sticky mode?
  superStickyOkayToShow: false, // Okay to show the popup in Super Sticky mode?
  superStickyOkayToHide: false, // Okay to hide the popup in Super Sticky mode?
  epwingMode: false,            // Are we in EPWING mode?
  epwingActive: false,          // Is the EPWING lookup in progress?
  epwingTotalHits: 0,           // The total number of EPWING hits for the current word
  epwingCurHit: 0,              // The current EPWING hit number (for showing hits one at a time)
  epwingPrevHit: 0,             // The previous EPWING hit number
  epwingCurDic: "",             // The EPWING dictionary to use (path)
  prevEpwingSearchTerm: "",     // The previous search term used with EPWING mode
  epwingFallbackCount: 0,       // How many times have we attempted to fallback to another EPWING dictionary?
  epwingStartDic: "",           // The dictionary used for the original EPWING lookup (before any fallbacks)
  epwingDicList: [],            // The list of EPWING dictionaries
  epwingDicTitleList: [],       // The list of EPWING dictionary titles
  saveKana: false,              // When saving a word, make the $d token equal to the $r token
  autoPlayAudioTimer: null,     // Timer used for automatically playing audio when a word is hilited
  epwingTimer: null,            // Timer used to lookup word in EPWING dictionary after word is hilited for a certain amount of time.
  noAudioFileHash: "",          // The hash of the no no_audio.mp3
  noAudioDic: null,             // Associative array containing words that have no audio clip. Key = "Reading - Expression.mp3", Value = true.
  knownWordsDic: null,          // Associative array containing the user's known words
  todoWordsDic: null,           // Associative array containing the user's to-do words
  prevKnownWordsFilePath: "",   // Previous path of the known words file. Used to determine in the use changed the path in the options.
  prevTodoWordsFilePath: "",    // Previous path of the to-do words file. Used to determine in the use changed the path in the options.
  epwingSearchTerm: "",         // Text to lookup in EPWING dictionary
  epwingSearchingNextLongest: false, // true = Searching for the next longest word in the gloss if the longest was not found.
                                     //        For example, Kojien6 doesn't have 自由研究 (which is in EDICT) but it does have 自由,
                                     //        so 自由 is used for the next longest search
  epwingResultList: [],         // List of results from the previous EPWING search
  freqDB: null,                 // Frequency database connection
  pitchDB: null,                // Pitch accent database connection


	global: function() {
		return null;
		/*
		return Components.classes["@mozilla.org/appshell/appShellService;1"]
			.getService(Components.interfaces.nsIAppShellService)
			.hiddenDOMWindow;
			*/
	},

	tbObs: {
		observe: function(subject, topic, data) {
			if (topic == 'mail:composeOnSend') {
				var e = document.getElementById('rikaichan-css');
				if (e) e.parentNode.removeChild(e);
				e = document.getElementById('rikaichan-window');
				if (e) e.parentNode.removeChild(e);
			}
		},
		register: function() {
		
		},
		unregister: function() {
			
		}
	},

	rcxObs: {
		observe: function(subject, topic, data) {
			if (topic == 'rikaichan') {
				if (data == 'getdic') {
					rcxMain.showDownloadPage();
					return;
				}

				if (data == 'dready') {
					if (rcxMain.tabSelectPending) {
						rcxMain.tabSelectPending = false;
						rcxMain.onTabSelect();
					}
					return;
				}

				// enmode: 0=tab, 1=browser, 2=all, 3=always
				/*
				if ((rcxConfig.enmode >= 2) && ((data == 'enable') || (data == 'disable'))) {
					if (rcxMain.enabled != (data == 'enable')) {
						if (rcxMain.enabled) rcxMain.disable(gBrowser.mCurrentBrowser, 0);
							else rcxMain.enabled = 1;
						rcxMain.onTabSelect();
					}
				}
				*/
			}
		},
		register: function() {
/*			
			Components.classes["@mozilla.org/observer-service;1"]
				.getService(Components.interfaces.nsIObserverService)
				.addObserver(rcxMain.rcxObs, 'rikaichan', false);
				*/
		},
		unregister: function() {
			/*		
			Components.classes['@mozilla.org/observer-service;1']
				.getService(Components.interfaces.nsIObserverService)
				.removeObserver(rcxMain.rcxObs, 'rikaichan');
				*/
		},
		notifyState: function(state) {
			/*
			Components.classes['@mozilla.org/observer-service;1']
				.getService(Components.interfaces.nsIObserverService)
				.notifyObservers(null, 'rikaichan', state);
				*/
		}
	},

	tbObs: {
		observe: function(subject, topic, data) {
			if (topic == 'mail:composeOnSend') {
				var e = document.getElementById('rikaichan-css');
				if (e) e.parentNode.removeChild(e);
				e = document.getElementById('rikaichan-window');
				if (e) e.parentNode.removeChild(e);
			}
		},
		register: function() {
			Components.classes['@mozilla.org/observer-service;1']
				.getService(Components.interfaces.nsIObserverService)
				.addObserver(rcxMain.tbObs, 'mail:composeOnSend', false);
		},
		unregister: function() {
			Components.classes['@mozilla.org/observer-service;1']
				.getService(Components.interfaces.nsIObserverService)
				.removeObserver(rcxMain.tbObs, 'mail:composeOnSend');
		}
	},

	tbTabMonitor: {
		monitorName: 'rikaichan',
		onTabSwitched: function(aTab, aOldTab) { rcxMain.onTabSelect() },
		onTabTitleChanged: function(aTab) { },
		onTabOpened: function(aTab, aIsFirstTab, aWasCurrentTab) { },
		onTabClosing: function(aTab) { },
		onTabPersist: function(aTab) { },
		onTabRestored: function(aTab, aState, aIsFirstTab) { }
	},

	init: function() {
		window.addEventListener('load', function() { rcxMain._init() }, false);
	},

	_init: function() {
		window.addEventListener('unload', function() { rcxMain.onUnload() }, false);

   // getBrowser: function() { return document; }, // new
    if (true) {
			let docID = document.documentElement.id;
			this.isTB = false;

			let mks = document.getElementById('mainKeyset') || document.getElementById('navKeys');
			if (mks) {
				let prefs = new rcxPrefs();
				['toggle', 'lbar'].forEach(function(name) {
					let s = prefs.getString(name + '.key');
					if ((s.length) && (s != '(disabled)')) {
						let key = document.createElementNS('http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul', 'key');
						key.setAttribute('id', 'rikaichan-key-' + name);
						if (s.length > 1) key.setAttribute('keycode', 'VK_' + s.replace(' ', '_').toUpperCase());	// "Page Up" -> "VK_PAGE_UP"
							else key.setAttribute('key', s);
						key.setAttribute('modifiers', prefs.getString(name + '.mod'));
						key.setAttribute('command', 'rikaichan-' + name + '-cmd');
						mks.appendChild(key);
					}
				});
			}
		}

		this.rcxObs.register();

		rcxConfig.load();
		rcxConfig.observer.start();

			this.getBrowser = function() { return document; }

		//	gBrowser.mTabContainer.addEventListener('select', this.onTabSelect, false);
		
			// enmode: 0=tab, 1=browser, 2=all, 3=always
		rcxConfig.enmode = 3;
		if (rcxConfig.enmode >= 2) {
				if ((rcxConfig.enmode == 3) || (this.global().rikaichanActive)) {
					this.enabled = 1;
					this.onTabSelect();
				}
			}

			// add icon to the toolbar
			try {
				let prefs = new rcxPrefs();
				if (prefs.getBool('firsticon')) {
					prefs.setBool('firsticon', false);

					// ref: https://developer.mozilla.org/En/Code_snippets:Toolbar#Adding_button_by_default
					let nb = document.getElementById('nav-bar');
					nb.insertItem('rikaichan-toggle-button');
					nb.setAttribute('currentset', nb.currentSet);
					document.persist(nb.id, 'currentset');
				}
			}
			catch (ex) { }

		this.checkVersion();

    // Enable Sanseido Mode at startup based on user preference
    if (rcxConfig.startsanseido)
    {
			rcxMain.sanseidoMode = true;
		}

    // Enable EPWING Mode at startup based on user preference
    if (rcxConfig.startepwing)
    {
			rcxMain.epwingMode = true;
		}

    // Enable Sticky Mode at startup based on user preference
    if (rcxConfig.startsticky)
    {
			rcxMain.sticky = true;
		}

    // Enable Super Sticky Mode at startup based on user preference
    if (rcxConfig.startsupersticky)
    {
			rcxMain.superSticky = true;
		}

    // Enable Lookup Bar at startup based on user preference
    if (rcxConfig.startlookupbar)
    {
			rcxMain.lbToggle();
		}

    // If the no audio dictionary has not yet been initialized
    if(!rcxMain.noAudioDic)
    {
      // Get the path of the no audio list file


      rcxMain.noAudioDic = {};
      rcxMain.readWordList('', rcxMain.noAudioDic, 1);
    }
	console.log('_init done');
	},


  // Read list of words in column wordColumn from file wordListFilePath into the outputDic associative array.
  // The key of outputDic will be the word, and the value will always be true.
  readWordList: function(wordListFilePath, outputDic, wordColumn)
  {
    // Check if the user entered a known words file
    outputDic[''] = true;

  }, /* readWordList */


  // Add entry to rcxMain.noAudioDic and append it to no_audio_list.txt
  addNoAudioListEntry: function(entry)
  {
    // If entry is already added, exit
    if(rcxMain.noAudioDic[entry])
    {
      return;
    }

    // Add the entry to rcxMain.noAudioDic
    rcxMain.noAudioDic[entry] = true;

 

  }, /* addNoAudioListEntry */


	onUnload: function() {
		this.rcxObs.unregister();
		rcxConfig.observer.stop();

		//	gBrowser.mTabContainer.removeEventListener('select', this.onTabSelect, false);

	},

	initDictionary: function() {
		if (rcxData.missing) {
			if (confirm('No dictionary file was found. Show the download page?')) {
				this.showDownloadPage();
			}
			return false;
		}
		try {
			rcxData.init();
		}
		catch (ex) {
			alert('Error: ' + ex);
			return false;
		}
		return true;
	},

	showDownloadPage: function() {
		const url = 'http://www.polarcloud.com/getrcx/?version=' + (this.version || '');
		try {

			//	gBrowser.selectedTab = gBrowser.addTab(url);
		}
		catch (ex) {
			alert('There was an error opening ' + url);
		}
	},

	checkVersion: function() {

	},

	onTabSelect: function() {
		// see rcxData.loadConfig
		if ((rcxData.dicPath) && (!rcxData.dicPath.ready)) {
			rcxMain.tabSelectPending = true;
		}
		else {
			rcxMain._onTabSelect();
		}
	},

	_onTabSelect: function() {
		var bro = this.getBrowser();

		if ((rcxConfig.enmode > 0) && (this.enabled == 1) && (bro.rikaichan == null)) {
			this.enable(bro, 0);
		}

		var en = (bro.rikaichan != null);

		var b = document.getElementById('rikaichan-toggle-cmd');
		if (b) {
			// FF 14/15/+? weirdness:
			//	attr false:   toolbar icon remains sunk (bad) / context/tools menu is unchecked (ok)
			//	attr removed: toolbar icon is normal (ok) / context/tools menu remains checked (bad)

			b.setAttribute('checked', en);

			if (!en) {
				b = document.getElementById('rikaichan-toggle-button');
				if (b) b.removeAttribute('checked');
				b = document.getElementById('rikaichan-toggle-button-gs');
				if (b) b.removeAttribute('checked');
			}
		}

		b = document.getElementById('rikaichan-status');
		if (b) b.setAttribute('rcx_enabled', en);
	},

	showPopup: function(text, elem, pos, lbPop)
  {
	  //console.log(text, elem, pos, lbPop);
    try
    {
      // outer-most document
      var content = window;
      var topdoc = document;

      var x = 0, y = 0;
      if (pos) {
        x = pos.clientX;
        y = pos.clientY;
      }

      this.lbPop = lbPop;

      var popup = topdoc.getElementById('rikaichan-window');
      if (!popup) {
        var css = topdoc.createElementNS('http://www.w3.org/1999/xhtml', 'link');
        css.setAttribute('rel', 'stylesheet');
        css.setAttribute('type', 'text/css');
        css.setAttribute('href', rcxConfig.css);
        css.setAttribute('id', 'rikaichan-css');

        head = topdoc.getElementsByTagName('head')[0];

        if(head)
        {
          head.appendChild(css);
        }
        else
        {
          console.error("showPopup(): Unable to append css to head!");
          return;
        }

        popup = topdoc.createElementNS('http://www.w3.org/1999/xhtml', 'div');
        popup.setAttribute('id', 'rikaichan-window');
        topdoc.documentElement.appendChild(popup);

        // if this is not set then Cyrillic text is displayed with Japanese
        // font, if the web page uses a Japanese code page as opposed to Unicode.
        // This makes it unreadable.
        popup.setAttribute('lang', 'en');

        popup.addEventListener('dblclick',
          function (ev) {
            rcxMain.hidePopup();
            ev.stopPropagation();
          }, true);

        if (rcxConfig.resizedoc) {
          if ((topdoc.body.clientHeight < 1024) && (topdoc.body.style.minHeight == '')) {
            topdoc.body.style.minHeight = '1024px';
            topdoc.body.style.overflow = 'auto';
          }
        }
      }

      popup.style.maxWidth = (lbPop ? '' : '600px');

      popup.style.opacity = rcxConfig.opacity / 100;

      if(rcxConfig.roundedcorners)
      {
        popup.style.borderRadius = '5px';
      }
      else
      {
        popup.style.borderRadius = '0px';
      }

      if (topdoc.contentType == 'text/plain') {
        var df = document.createDocumentFragment();
        var sp = document.createElementNS('http://www.w3.org/1999/xhtml', 'span');
        df.appendChild(sp);
        sp.innerHTML = text;
        while (popup.firstChild) {
          popup.removeChild(popup.firstChild);
        }
        popup.appendChild(df);
      }
      else {
        popup.innerHTML = text;
      }

      if (elem && (typeof elem !== 'undefined')
         && elem.parentNode && (typeof elem.parentNode !== 'undefined')) {
        popup.style.top = '-1000px';
        popup.style.left = '0px';
        popup.style.display = '';

        var width = popup.offsetWidth;
        var height = popup.offsetHeight;

        // guess! (??? still need this?)
        if (width <= 0) width = 200;
        if (height <= 0) {
          height = 0;
          var j = 0;
          while ((j = text.indexOf('<br', j)) != -1) {
            j += 5;
            height += 22;
          }
          height += 25;
        }

        if (this.altView == 1) {
          // upper-left
          x = 0;
          y = 0;
        }
        else if (this.altView == 2) {
          // lower-right
          x = (content.innerWidth - (width + 20));
          y = (content.innerHeight - (height + 20));
        }
        else {

          // when zoomed, convert to zoomed document pixel position
          // - not in TB compose and ...?
          try {
            var cb = this.getBrowser();
            var z = cb.fullZoom || 1;
            if (z != 1) {
              x = Math.round(x / z);
              y = Math.round(y / z);
            }
          }
          catch (ex) {
             console.log('ex: ' + ex)
          }

          if (false && elem instanceof Components.interfaces.nsIDOMHTMLOptionElement) {
            // these things are always on z-top, so go sideways
            x -= pos.pageX;
            y -= pos.pageY;
            var p = elem;
            while (p) {
              x += p.offsetLeft;
              y += p.offsetTop;
              p = p.offsetParent;
            }

            // right side of box
            var w = elem.parentNode.offsetWidth + 5;
            x += w;

            if ((x + width) > content.innerWidth) {
              // too much to the right, go left
              x -= (w + width + 5);
              if (x < 0) x = 0;
            }

            if ((y + height) > content.innerHeight) {
              y = content.innerHeight - height - 5;
              if (y < 0) y = 0;
            }
          }
          else {
            // go left if necessary
            if ((x + width) > (content.innerWidth - 20)) {
              x = (content.innerWidth - width) - 20;
              if (x < 0) x = 0;
            }

            // below the mouse
            var v = 25;

            // under the popup title
            if ((elem.title) && (elem.title != '')) v += 20;

            // go up if necessary
            if ((y + v + height) > content.innerHeight) {
              var t = y - height - 30;
              if (t >= 0) y = t;
            }
            else y += v;
          }
        }
      }
      else
      {
        console.error("showPopup(): elem or parentNode is not defined!");
      }

      popup.style.left = (x + content.scrollX) + 'px';
      popup.style.top = (y + content.scrollY) + 'px';
      popup.style.display = '';
	 // console.log('top ' + popup.style.top + ' ' + content.scrollY);
    }
    catch(ex)
    {
      console.error("showPopup() Exception: " + ex);
    }
	//console.log('showPopup end');
	},

	hidePopup: function()
  {
    // Reset the EPWING hit number and hit totals
    this.epwingTotalHits = 0;
    this.epwingCurHit = 0;
    this.epwingPrevHit = 0;

    // Don't hide popup in superSticky unless given permission to
    if(!this.superSticky || this.superStickyOkayToHide)
    {
      this.superStickyOkayToHide = false;

		  var doc = document;
		  var popup = doc.getElementById('rikaichan-window');

      if (popup)
      {
        popup.style.display = 'none';
        popup.innerHTML = '';

        // Stop the current auto play timer
        if(rcxConfig.autoplayaudio)
        {
          if(this.autoPlayAudioTimer)
          {
            clearTimeout(this.autoPlayAudioTimer);
            this.autoPlayAudioTimer = null;
          }
        }

        // Stop the EPWING timer
        if(this.epwingTimer)
        {
          clearTimeout(this.epwingTimer);
          this.epwingTimer = null;
        }
      }

      this.lbPop = 0;
      this.title = null;
    }
	},

	isVisible: function() {
		var doc = document;
		var popup = doc.getElementById('rikaichan-window');
		return (popup) && (popup.style.display != 'none');
	},

	clearHi: function() {
		var tdata = this.getBrowser().rikaichan;
		if ((!tdata) || (!tdata.prevSelView)) return;
		if (tdata.prevSelView.closed) {
			tdata.prevSelView = null;
			return;
		}

		var sel = tdata.prevSelView.getSelection();
		if ((sel.isCollapsed) || (tdata.selText == sel.toString())) {
			sel.removeAllRanges();
		}
		tdata.prevSelView = null;
		tdata.kanjiChar = null;
		tdata.selText = null;
	},

	//

	lastFound: null,

	savePrep: function(clip, saveFormat) {
		var me, mk;
		var text;
		var i;
		var f;
		var e;
		var s;
		var w;

		f = this.lastFound;
		s = this.sentence;
		sWBlank = this.sentenceWBlank;
		w = this.word;

		if ((!f) || (f.length == 0)) return null;

		if (clip) {
			me = rcxConfig.smaxce;
			mk = rcxConfig.smaxck;
		}
		else {
			me = rcxConfig.smaxfe;
			mk = rcxConfig.smaxfk;
		}

		if (!f.fromLB) mk = 1;

		e = f[0];
		text = rcxData.makeText(e, w, s, sWBlank, rcxMain.saveKana, saveFormat);

    // Result the save kana ($d=$r) flag
    rcxMain.saveKana = false;

		if (rcxConfig.snlf == 1) text = text.replace(/\n/g, '\r\n');
			else if (rcxConfig.snlf == 2) text = text.replace(/\n/g, '\r');

		var sep = rcxConfig.ssep;
		switch (sep) {
		case 'Tab':
			sep = '\t';
			break;
		case 'Comma':
			sep = ',';
			break;
		case 'Space':
			sep = ' ';
			break;
		}
		if (sep != '\t') return text.replace(/\t/g, sep);

		return text;
	},

	copyToClip: function() {
		console.error('copyToClip not impelemented');
		return;
		var text;

		if ((text = this.savePrep(1, rcxConfig.saveformat)) != null) {
			Components.classes['@mozilla.org/widget/clipboardhelper;1']
				.getService(Components.interfaces.nsIClipboardHelper)
				.copyString(text);
			this.showPopup('Copied to clipboard.');
		} else {
			this.showPopup('Please select something to copy in Preferences.');
			return;
		}
	},


  /* Get the CSS style to use when drawing the provided frequency */
  getFreqStyle: function(inFreqNum)
  {
    freqNum = inFreqNum.replace(/_r/g, "");

    var freqStyle = 'w-freq-rare';

    if (freqNum <= 5000)
    {
      freqStyle = "w-freq-very-common";
    }
    else if (freqNum <= 10000)
    {
      freqStyle = "w-freq-common";
    }
    else if (freqNum <= 20000)
    {
      freqStyle = "w-freq-uncommon";
    }

    return freqStyle;

  }, /* getFreqStyle */


  /* Get the frequency for the given expression/reading. If the frequency is based on the
     reading then "_r" is appended to the frequency string that is returned.

     useHilitedWord - Set to true to allow the hilited word to be considered when
                      determining frequency.

     Note: frequency information comes from analysis of 5000+ novels (via
           Japanese Text Analysis Tool). */
  getFreq: function(inExpression, inReading, useHilitedWord)
  {
    var expression = inExpression;
    var reading = inReading;
    var hilitedWord = this.word; // Hilited word without de-inflection

    var freqNum = "";
    var freqStr = "";
    var freqBasedOnReading = false;

    try
    {
      var readingFreqNum = this.lookupFreqInDb(reading);
      var readingSameAsExpression = (expression == reading);
      var expressionFreqNum = readingFreqNum;

      // Don't waste time looking up the expression freq if expression is same as the reading
      if(!readingSameAsExpression)
      {
        expressionFreqNum = this.lookupFreqInDb(expression);
      }

      // If frequency was found for either frequency or reading
      if((expressionFreqNum.length > 0) || (readingFreqNum.length > 0))
      {
        // If the hilited word does not contain kanji, and the reading is unique,
        // use the reading frequency
        if(useHilitedWord
            && !readingSameAsExpression
            && !this.containsKanji(hilitedWord)
            && (readingFreqNum.length > 0)
            && (rcxData.getReadingCount(reading) == 1))
        {
          freqNum = readingFreqNum;
          freqBasedOnReading = true;
        }

        // If expression and reading are the same, use the reading frequency
        if((freqNum.length == 0)
            && readingSameAsExpression
            && (readingFreqNum.length > 0))
        {
          freqNum = readingFreqNum;
        }

        // If the expression is in the freq db, use the expression frequency
        if((freqNum.length == 0) && (expressionFreqNum.length > 0))
        {
          freqNum = expressionFreqNum;
        }

        // If the reading is in the freq db, use the the reading frequency
        if((freqNum.length == 0) && (readingFreqNum.length > 0))
        {
          freqNum = readingFreqNum;
          freqBasedOnReading = true;
        }
      }

      freqStr = freqNum;

      // Indicate that frequency was based on the reading
      if(freqBasedOnReading)
      {
        freqStr += "_r";
      }
    }
    catch(ex)
    {
      console.error("getFreq() Exception: " + ex);
      freqStr = "";
    }

    return freqStr;

  }, /* getFreq */


  /* Lookup the provided word in the frequency database. */
  lookupFreqInDb: function(word)
  {
	  console.error('lookupFreqInDb not implemented' );
	  return 0;
    var freq = "";

    try
    {
      // If we have not yet made a connection to the database
      if(this.freqDB == null)
      {
        // Get the path of the frequency database
        var freqDbPath = Components.classes["@mozilla.org/file/directory_service;1"]
        .getService(Components.interfaces.nsIProperties)
        .get("ProfD", Components.interfaces.nsILocalFile);
        freqDbPath.append("extensions");
        freqDbPath.append(rcxMain.id); // GUID of extension
        freqDbPath.append("freq");
        freqDbPath.append("freq.sqlite");

        // Is the frequency database could not be found, return
        if(!freqDbPath.exists())
        {
          return "";
        }

        // Get file pointer to the frequency sqlite database
        var freqDbFile = Components.classes['@mozilla.org/file/local;1']
         .createInstance(Components.interfaces.nsILocalFile);
        freqDbFile.initWithPath(freqDbPath.path);

        // Open the frequency database
        this.freqDB = Components.classes['@mozilla.org/storage/service;1']
         .getService(Components.interfaces.mozIStorageService)
         .openDatabase(freqDbFile);
      }

      // Reference: https://developer.mozilla.org/en-US/docs/Storage
      var stFreq = this.freqDB.createStatement(
        "SELECT freq FROM Dict WHERE expression='" + word + "'");

      try
      {
        var freqFound = stFreq.executeStep();

        if(freqFound)
        {
          freq = stFreq.row.freq;
        }
      }
      finally
      {
        stFreq.reset();
      }
    }
    catch(ex)
    {
      console.error("lookupFreqInDb() Exception: " + ex);
      freq = "";
    }

    return freq;

  }, /* lookupFreqInDb */



  /* Get the pitch accent of the last hilited word if present. If inExpression is not provided,
     will get the pitch accent for the hilited word's expression and reading */
  getPitchAccent: function(inExpression, inReading)
  {
	  console.error('getPitchAccent not implemented' );
	  return "";
    try
    {
      // If we have not yet made a connection to the database
      if(this.pitchDB == null)
      {
        // Get the path of the pitch accent database
        var pitchDbPath = Components.classes["@mozilla.org/file/directory_service;1"]
        .getService(Components.interfaces.nsIProperties)
        .get("ProfD", Components.interfaces.nsILocalFile);
        pitchDbPath.append("extensions");
        pitchDbPath.append(rcxMain.id); // GUID of extension
        pitchDbPath.append("pitch");
        pitchDbPath.append("pitch_accents.sqlite");

        // Is the pitch accent database could not be found, return
        if(!pitchDbPath.exists())
        {
          return "";
        }

        // Get file pointer to the pitch accent sqlite database
        var pitchDbFile = Components.classes['@mozilla.org/file/local;1']
         .createInstance(Components.interfaces.nsILocalFile);
        pitchDbFile.initWithPath(pitchDbPath.path);

        // Open the pitch accent database
        this.pitchDB = Components.classes['@mozilla.org/storage/service;1']
         .getService(Components.interfaces.mozIStorageService)
         .openDatabase(pitchDbFile);
      }

      // If the caller provided an expression/reading, use them, otherwise use the
      // expression/reading of the hilited word
      if(inExpression)
      {
        var expression = inExpression;
        var reading = inReading;
      }
      else
      {
        var hilitedEntry = this.lastFound;

        if ((!hilitedEntry) || (hilitedEntry.length == 0)
          || !hilitedEntry[0] || !hilitedEntry[0].data[0])
        {
          return "";
        }

        var entryData = hilitedEntry[0].data[0][0].match(/^(.+?)\s+(?:\[(.*?)\])?\s*\/(.+)\//);

        //   entryData[0] = kanji/kana + kana + definition
        //   entryData[1] = kanji (or kana if no kanji)
        //   entryData[2] = kana (null if no kanji)
        //   entryData[3] = definition

        var expression = entryData[1];
        var reading = entryData[2];
      }

      // Form the SQL used to query the pitch accent
      if(!reading)
      {
        // Reference: https://developer.mozilla.org/en-US/docs/Storage
        var stPitch = this.pitchDB.createStatement("SELECT pitch FROM Dict WHERE expression='"
          + expression + "'");
      }
      else
      {
        var stPitch = this.pitchDB.createStatement("SELECT pitch FROM Dict WHERE expression='"
          + expression + "' AND reading='" + reading + "'");
      }

      var pitch = "";

      try
      {
        stPitch.executeStep();

        // Get the result of the query
        pitch = stPitch.row.pitch;
      }
      finally
      {
        stPitch.reset();
      }

      // If user wants to hide the part-of-speech unless , or | is present
      if(rcxConfig.hidepitchaccentpos)
      {
        if((pitch.indexOf(",") == -1) && (pitch.indexOf("|") == -1))
        {
          pitch = pitch.replace(/\(.*?\)/g, "")
        }
      }

      return pitch;
    }
    catch(ex)
    {
      return "";
    }

    return "";

  }, /* getPitchAccent */


  /*
   Returns:
     "*"    - If expression of last hilighted word is in the user's known words list.
     "*t"   - If expression of last hilighted word is in the user's to-do words list.
     "*_r"  - If reading of last hilighted word is in the user's known words list.
     "*t_r" - If reading of last hilighted word is in the user's to-do words list.
     ""     - If neither expression nor reading of last hilighted word was found.
   */
  getKnownWordIndicatorText: function()
  {
    var outText = "";
    var expression = "";
    var reading = "";

    // Get the last highlighted word
    if(this.lastFound[0].data)
    {
      // Extract needed data from the hilited entry
      //   entryData[0] = kanji/kana + kana + definition
      //   entryData[1] = kanji (or kana if no kanji)
      //   entryData[2] = kana (null if no kanji)
      //   entryData[3] = definition

      var entryData = this.lastFound[0].data[0][0].match(/^(.+?)\s+(?:\[(.*?)\])?\s*\/(.+)\//);
	  //console.log('entryData ' + entryData);
      expression = entryData[1];

      if(entryData[2])
      {
        reading = entryData[2];
      }
    }
    else
    {
      return "";
    }

    // Reload the known words associative array if needed
    if(!this.knownWordsDic || (this.prevKnownWordsFilePath != rcxConfig.vocabknownwordslistfile))
    {
      rcxMain.knownWordsDic = {};
      rcxMain.readWordList(rcxConfig.vocabknownwordslistfile, rcxMain.knownWordsDic, rcxConfig.vocabknownwordslistcolumn);
      this.prevKnownWordsFilePath = rcxConfig.vocabknownwordslistfile;
    }

    // Reload the to-do words associative array if needed
    if(!this.todoWordsDic || (this.prevTodoWordsFilePath != rcxConfig.vocabtodowordslistfile))
    {
      rcxMain.todoWordsDic = {};
      rcxMain.readWordList(rcxConfig.vocabtodowordslistfile, rcxMain.todoWordsDic, rcxConfig.vocabtodowordslistcolumn);
      this.prevTodoWordsFilePath = rcxConfig.vocabtodowordslistfile;
    }

    //
    // First try the expression
    //

    if(this.knownWordsDic[expression])
    {
      outText = "* ";
    }
    else if(this.todoWordsDic[expression])
    {
      outText = "*t ";
    }

    //
    // If expression not found in either the known words or to-do lists, try the reading
    //

    if(outText.length == 0)
    {
      if(this.knownWordsDic[reading])
      {
        outText = "*_r ";
      }
      else if(this.todoWordsDic[reading])
      {
        outText = "*t_r ";
      }
    }

    return outText;

  }, /* getKnownWordIndicatorText */


  // Send the highlighted word to Anki's Real-Time Import plugin
  sendToAnki: function()
  {
	  	  console.error('sentToAnki not implemented' );
	  return;
	  
    // Create message header
    var header = 'add\t1' // command and version

    // Get Anki field names to use
    var fieldNames = rcxMain.trim(rcxConfig.rtifieldnamestext);
    fieldNames = fieldNames.replace(/ /g, '\t')

    if (fieldNames.length == 0)
    {
      this.showPopup('Please enter Anki field names in Preferences.');
      return;
    }

    // Get tags
    var tags = rcxMain.trim(rcxConfig.atags);

    // Get the field contents
    if (rcxConfig.rti_save_format.length == 0)
    {
      this.showPopup('Please create a save format in Preferences (Anki tab).');
      return;
    }

    // Save the audio clip if the audio directory was specified by the user
    if (rcxConfig.rtisaveaudio && (rcxConfig.audiodir.length != 0))
    {
      this.playJDicAudio(true);
    }

    var fieldContents = this.savePrep(0, rcxConfig.rti_save_format);

    if(fieldContents == null)
    {
      return;
    }

    var port = rcxConfig.rtiudpport;

    if(port == null)
    {
      return;
    }

    // Create the text that will be saved to the file
    fileText = header + '\n' + fieldNames + '\n' + tags + '\n' + fieldContents;

    // Create the file that Real-Time Import will read
    var tempRtiFile = Components.classes["@mozilla.org/file/directory_service;1"]
      .getService(Components.interfaces.nsIProperties)
      .get("TmpD", Components.interfaces.nsIFile);
    tempRtiFile.append("~rikai_anki_rti.txt");

    // Open a safe file output stream for writing
    var ostream = FileUtils.openSafeFileOutputStream(tempRtiFile)

    // Convert the filename unicode string to an input stream
    var converter = Components.classes["@mozilla.org/intl/scriptableunicodeconverter"].
    createInstance(Components.interfaces.nsIScriptableUnicodeConverter);
    converter.charset = "UTF-8";
    var istream = converter.convertToInputStream(fileText);

    // Asynchronously Write the file text to the file
    NetUtil.asyncCopy(istream, ostream,
      // This function will be called when the write to file is complete
      function(status)
      {
        if (!Components.isSuccessCode(status))
        {
          // Error writing file
          rcxMain.showPopup('Error writing temp Real-Time Import file.');
          return;
        }
        else
        {
          // Send the UDP message to Anki's Real-Time Import containing location of information to add
          // Use Firefox's own barely-publicized UDP service
          let udpSocket = Cc["@mozilla.org/network/udp-socket;1"].createInstance(Ci.nsIUDPSocket);
          udpSocket.init(0, true, null);
          let utf8encoder = new TextEncoder('utf-8');
          let msg = utf8encoder.encode(tempRtiFile.path);
          udpSocket.send('127.0.0.1', port, msg, msg.length);
        }
      });

  }, /* sendToAnki */


  // Populate the EPWING dictionary list with the user-entered EPWING dictionaries
  populateEpwingDics: function()
  {
    var dicFound = false;

    // Reset the dictionary list
    this.epwingDicList = [];
    this.epwingDicTitleList = [];


    //
    // Add each dictionary to the list
    //

    let epwingPaths = rcxConfig.epwingdiclist.split('|');

    for (let i = 0; i < epwingPaths.length; ++i)
    {
      if(epwingPaths[i].length > 0)
      {
        let pathFields = epwingPaths[i].split('?'); // The paths are stored in "path?title" format

        if(pathFields && (pathFields[0].length > 0) && (pathFields[1].length > 0))
        {
          this.epwingDicList.push(pathFields[0]);
          this.epwingDicTitleList.push(pathFields[1]);
        }
      }
		}


    // Does the current dictionary exist in the new list?
    for(i = 0; i < this.epwingDicList.length; i++)
    {
      if(this.epwingDicList[i] == this.epwingCurDic)
      {
        dicFound = true;
        break;
      }
    }

    // If the current dictionary does not exist in the new list, use the first dictionary
    if(!dicFound)
    {
       if(this.epwingDicList.length > 0)
       {
         this.epwingCurDic = this.epwingDicList[0];
       }
       else
       {
         this.epwingCurDic = "";
       }
    }

  }, /* populateEpwingDics */


  // Get the index of the current dictionary (epwingCurDic) within the EPWING dictionary list (epwingDicList)
  getEpwingDicIndex: function()
  {
    var pos = 0;

    this.populateEpwingDics();

    for(i = 0; i < this.epwingDicList.length; i++)
    {
      if(this.epwingDicList[i] == this.epwingCurDic)
      {
        pos = i;
        break;
      }
    }

    return pos;

  }, /* getEpwingDicIndex */


  // Get the title of the current dictionary
  getCurEpwingDicTitle: function()
  {
    var dicIdx = rcxMain.getEpwingDicIndex();

    return rcxMain.epwingDicTitleList[dicIdx];
  },


  // Get the short form of the title for the current dictionary
  getCurEpwingDicShortTitle: function()
  {
    var title = rcxMain.getCurEpwingDicTitle();
    var shortTitle = "???";

    if(title == "研究社　新和英大辞典　第５版") // Kenkyusha 5th J-E. Contains example sentences.
    {
      shortTitle = "研究社五";
    }
    else if(title == "研究社　新英和・和英中辞典")  // Kenkyusha Shin Eiwa-Waei Chujiten J-E. Contains example sentences.
    {
      shortTitle = "中辞典";
    }
    else if(title == "大辞林 第2版") // Dajirin 2nd Edition. J-J. Japanese-only examples.
    {
      shortTitle = "大辞林二";
    }
    else if(title == "三省堂　スーパー大辞林") // Sanseido Super Daijirin
    {
      shortTitle = "大辞林二";
    }
    else if(title == "大辞泉") //  Daijisen. J-J. Japanese-only examples.
    {
      shortTitle = "大辞泉";
    }
    else if(title == "広辞苑第六版") // Kojien 6th Edition. J-J. Japanese-only examples.
    {
      shortTitle = "広辞苑六";
    }
    else if(title == "明鏡国語辞典") // Meikyo Kokugo Dictionary. J-J. Japanese-only examples.
    {
      shortTitle = "明鏡";
    }
    else if(title == "新明解国語辞典　第五版") // Shinmeikai Kokugojiten 5th Edition. J-J.
    {
      shortTitle = "新明解五";
    }
    else if(title == "ジーニアス英和〈第３版〉・和英〈第２版〉辞典") // Genius EJ 3rd J-E 2nd. Contains example sentences.
    {
      shortTitle = "ジー三・二";
    }
    else if(title == "ジーニアス英和・和英辞典") //  Genius EJ-JE. Contains example sentences.
    {
      shortTitle = "ジー英和・和英";
    }
    else if(title == "研究社　新編英和活用大辞典") //  Kenkyusha New Edition E-J.
    {
      shortTitle = "研究社・新編英和";
    }
    else if(title == "例文") // Tanaka Corpus example sentences
    {
      shortTitle = "例文";
    }
    else if(title == "ＮＨＫ　日本語発音アクセント辞典") // NHK Pitch Accent Dictionary
    {
      shortTitle = "NHK発音";
    }
    else
    {
      var shortNameLen = 6;

      if(title.length < shortNameLen)
      {
        shortNameLen = title.length;
      }

      shortTitle = rcxMain.trim(title.substring(0, shortNameLen));
    }

    return shortTitle;
  },


  // Sets the current EPWING dictionary (epwingCurDic) to the next available EPWING dictionary
  nextEpwingDic: function()
  {
    var dicPos = 0;

    // Populate epwingDicList
    this.populateEpwingDics();

    if(this.epwingDicList.length > 0)
    {
      // Find the position of the current dictionary
      for(i = 0; i < this.epwingDicList.length; i++)
      {
        if(this.epwingDicList[i] == this.epwingCurDic)
        {
          dicPos = i;
          break;
        }
      }

      // Increment to the next dictionary
      dicPos++;

      // Wrap?
      if(dicPos >= this.epwingDicList.length)
      {
        dicPos = 0;
      }

      // Set the current dictionary
      this.epwingCurDic = this.epwingDicList[dicPos];
    }

  }, /* nextEpwingDic */


  // Sets the current EPWING dictionary (epwingCurDic) to the previous available EPWING dictionary
  prevEpwingDic: function()
  {
    var dicPos = 0;

    // Populate epwingDicList
    this.populateEpwingDics();

    if(this.epwingDicList.length > 0)
    {
      // Find the position of the current dictionary
      for(i = 0; i < this.epwingDicList.length; i++)
      {
        if(this.epwingDicList[i] == this.epwingCurDic)
        {
          dicPos = i;
          break;
        }
      }

      // Decrement to the next dictionary
      dicPos--;

      // Wrap?
      if(dicPos < 0)
      {
        dicPos = this.epwingDicList.length - 1;
      }

      // Set the current dictionary
      this.epwingCurDic = this.epwingDicList[dicPos];
    }

  }, /* prevEpwingDic */


  // If in Super Sticky mode, allow the popup to show just once
  allowOneTimeSuperSticky: function()
  {
    if(this.superSticky)
    {
      this.superStickyOkayToShow = true;
    }

  }, /* allowOneTimeSuperSticky */


  // Toggle Super Sticky mode
  toggleSuperStickyMode: function()
  {
    this.superSticky = !this.superSticky;

    if(this.superSticky)
    {
      this.status('Super Sticky Mode: ON');
    }
    else
    {
      this.status('Super Sticky Mode: OFF');
    }

  }, /* toggleSuperStickyMode */


  // Toggle EPWING mode
  toggleEpwingMode: function()
  {
    this.epwingMode = !this.epwingMode;

    if(this.epwingMode)
    {
      this.status('EPWING Mode: ON');

      if(this.sanseidoMode)
      {
        this.sanseidoMode = false;
      }
    }
    else
    {
      this.status('EPWING Mode: OFF');
    }

  }, /* toggleEpwingMode */


  // Toggle Sanseido mode
  toggleSanseidoMode: function()
  {
    this.sanseidoMode = !this.sanseidoMode;

    if(this.sanseidoMode)
    {
      this.status('Sanseido Mode: ON');

      if(this.epwingMode)
      {
        this.epwingMode = false;
      }
    }
    else
    {
      this.status('Sanseido Mode: OFF');
    }

  }, /* toggleSanseidoMode */


  // Parse definition from Sanseido page and display it in a popup
  parseAndDisplaySanseido: function(entryPageText)
  {
    // Create DOM tree from entry page text
    var domPars = rcxMain.htmlParser(entryPageText);

    // Get list of div elements
    var divList = domPars.getElementsByTagName("div");

    // Will be set if the entry page actually contains a definition
    var entryFound = false;

    // Find the div that contains the definition
    for(divIdx = 0; divIdx < divList.length; divIdx++)
    {
      // Did we reach the div the contains the definition?
      if(divList[divIdx].className == "NetDicBody")
      {
        entryFound = true;

        // rcxDebug.echo("Raw definition: " + divList[divIdx].innerHTML);

        // Will contain the final parsed definition text
        var defText = "";

        // A list of all child nodes in the div
        var childList = divList[divIdx].childNodes;

        // Set when we need to end the parse
        var defFinished = false;

        // Extract the definition from the div's child nodes
        for(nodeIdx = 0; nodeIdx < childList.length && !defFinished; nodeIdx++)
        {
          // Is this a b element?
          if(childList[nodeIdx].nodeName == "b")
          {
            // How many child nodes does this b element have?
            if(childList[nodeIdx].childNodes.length == 1)
            {
              // Check for definition number: ［１］, ［２］, ... and add to def
              var defNum = childList[nodeIdx].childNodes[0].nodeValue.match(/［([１２３４５６７８９０]+)］/);

              if (defNum)
              {
                defText += "<br />" + RegExp.$1;
              }
              else
              {
                // Check for sub-definition number: （１）, （２）, ... and add to def
                var subDefNum = childList[nodeIdx].childNodes[0].nodeValue.match(/（([１２３４５６７８９０]+)）/);

                if (subDefNum)
                {
                  // Convert sub def number to circled number
                  defText += this.convertIntegerToCircledNumStr(this.convertJapNumToInteger(RegExp.$1));
                }
              }
            }
            else // This b element has more than one child node
            {
              // Check the b children for any spans. A span marks the start
              // of non-definition portion, so end the parse.
              for(bIdx = 0; bIdx < childList[nodeIdx].childNodes.length; bIdx++)
              {
                if(childList[nodeIdx].childNodes[bIdx].nodeName == "span")
                {
                  defFinished = true;
                }
              }
            }
          }

          // Have we finished parsing the text?
          if(defFinished)
          {
            break;
          }

          // If the current element is text, add it to the definition
          if((childList[nodeIdx].nodeName == "#text")
            && (rcxMain.trim(childList[nodeIdx].nodeValue) != ""))
          {
            defText += childList[nodeIdx].nodeValue;
          }
        }

        // If the definition is blank (search ばかり for example), fallback
        if(defText.length == 0)
        {
          // Set to a state that will ensure fallback to default JMDICT popup
          this.sanseidoFallbackState = 1;
          entryFound = false;
          break;
        }

        var jdicCode = "";

        // Get the part-of-speech and other JDIC codes
        rcxMain.lastFound[0].data[0][0].match(/\/(\(.+?\) ).+\//);

        if(RegExp.$1)
        {
          jdicCode = RegExp.$1;
        }

        // Replace the definition with the one we parsed from sanseido
        rcxMain.lastFound[0].data[0][0] = rcxMain.lastFound[0].data[0][0]
          .replace(/\/.+\//g, "/" + jdicCode + defText + "/");

        // Remove all words except for the one we just looked up
        rcxMain.lastFound[0].data = [rcxMain.lastFound[0].data[0]];

        // Prevent the "..." from being displayed at the end of the popup text
        rcxMain.lastFound[0].more = false;

        // Show the definition
        rcxMain.showPopup(rcxMain.getKnownWordIndicatorText() + rcxData.makeHtml(rcxMain.lastFound[0]),
          rcxMain.lastTdata.get().prevTarget, rcxMain.lastTdata.get().pos);

        // Entry found, stop looking
        break;
      }
    }

    // If the entry was not on sanseido, either try to lookup the kana form of the word
    // or display default JMDICT popup
    if(!entryFound)
    {
      this.sanseidoFallbackState++;

      if(this.sanseidoFallbackState < 2)
      {
        // Set a timer to lookup again using the kana form of the word instead
        window.setTimeout
        (
          function()
          {
            rcxMain.lookupSanseido();
          }, 10
        );
      }
      else
      {
        // Fallback to the default non-sanseido dictionary that comes with rikaichan (JMDICT)
        rcxMain.showPopup(rcxData.makeHtml(rcxMain.lastFound[0]), rcxMain.lastTdata.get().prevTarget, rcxMain.lastTdata.get().pos);
      }
    }
  }, /* parseAndDisplaySanseido */


  // Extract the first search term from the hilited word.
  // Returns search term string or null on error.
  // forceGetReading - true = force this routine to return the reading of the word
  extractSearchTerm: function(forceGetReading)
  {
    // Get the currently hilited entry
    var hilitedEntry = this.lastFound;

    if ((!hilitedEntry) || (hilitedEntry.length == 0))
    {
      return null;
    }

    var searchTerm = "";

    // Get the search term to use
    if(hilitedEntry[0] && hilitedEntry[0].kanji && hilitedEntry[0].onkun)
    {
      // A single kanji was selected

      searchTerm = hilitedEntry[0].kanji;
    }
    else if(hilitedEntry[0] && hilitedEntry[0].data[0])
    {
      // An entire word was selected

      var entryData = hilitedEntry[0].data[0][0].match(/^(.+?)\s+(?:\[(.*?)\])?\s*\/(.+)\//);

      // Example of what data[0][0] looks like (linebreak added by me):
      //   乃 [の] /(prt,uk) indicates possessive/verb and adjective nominalizer (nominaliser)/substituting
      //   for "ga" in subordinate phrases/indicates a confident conclusion/emotional emphasis (sentence end) (fem)/(P)/
      //
      // Extract needed data from the hilited entry
      //   entryData[0] = kanji/kana + kana + definition
      //   entryData[1] = kanji (or kana if no kanji)
      //   entryData[2] = kana (null if no kanji)
      //   entryData[3] = definition

      if(forceGetReading)
      {
        if(entryData[2])
        {
          searchTerm = entryData[2];
        }
        else
        {
          searchTerm = entryData[1];
        }
      }
      else
      {
        // If the highlighted word is kana, don't use the kanji.
        // Example1: if の is highlighted, use の rather than the kanji equivalent (乃)
        // Example2: if された is highlighted, use される rather then 為れる
        if(entryData[2] && !this.containsKanji(this.word))
        {
          searchTerm = entryData[2];
        }
        else
        {
          searchTerm = entryData[1];
        }
      }
    }
    else
    {
      return null;
    }

    return searchTerm;

  }, /* extractSearchTerm */


  // Perform cleanup and reset variables after performing an EPWING search
  cleanupLookupEpwing: function()
  {
    // Allow EPWING popups to occur again
    this.epwingActive = false;

    this.epwingFallbackCount = 0;

    // Reset to pre-fallback dictionary
    this.epwingCurDic = this.epwingStartDic;

    this.epwingSearchingNextLongest = false;

  }, /* cleanupLookupEpwing */


  // Lookup hilited word in EPWING dictionary
  lookupEpwing: function()
  {
	  	  console.error('lookupEpwing not implemented' );
	  return "";
	  
    // Is a word currently being looked up with EPWING?
    if(this.epwingActive)
    {
      return;
    }

    // Populate the EPWING dictionary list
    rcxMain.populateEpwingDics();

    // Save the current dictionary so that we can restore it if we have to fallback to another EPWING dictionary
    if(this.epwingFallbackCount == 0)
    {
      this.epwingStartDic = this.epwingCurDic;
    }

    // Did the user enter an EPWING path in the EPWING tab?
    try
    {
      var epwingDir = Components.classes["@mozilla.org/file/local;1"]
        .createInstance(Components.interfaces.nsILocalFile);
      epwingDir.initWithPath(this.epwingCurDic);

      if(!epwingDir.exists())
      {
        throw "Error";
      }
    }
    catch(ex)
    {
      if(this.epwingCurDic.length > 0)
      {
        rcxMain.showPopup('Invalid EPWING dictionary: ' + this.epwingCurDic);
      }
      else
      {
        rcxMain.showPopup('Please add an EPWING dictionary in the EPWING tab of the options dialog.');
      }

      return;
    }

    // Prevent other EPWING lookups until this one is finished
    this.epwingActive = true;

    // If searching for the next longest word in the gloss. For example, Kojien6 doesn't
    // have 自由研究 (which is in EDICT) but it does have 自由, so 自由 is used for the next longest search.
    if(rcxConfig.epwingsearchnextlongest && rcxMain.epwingSearchingNextLongest)
    {
      var hilitedEntry = this.lastFound;

      if(hilitedEntry && (hilitedEntry.length > 0) && hilitedEntry[0] && hilitedEntry[0].data && hilitedEntry[0].data[1])
      {
        var entryData = hilitedEntry[0].data[1][0].match(/^(.+?)\s+(?:\[(.*?)\])?\s*\/(.+)\//);

        if(entryData && entryData[1] && (entryData[1].length > 0))
        {
          this.epwingSearchTerm = entryData[1];
        }
      }
    }
    else // Normal search for the first word in the EDICT gloss
    {
      // Get the first search term from the hilited word.
      this.epwingSearchTerm = this.extractSearchTerm(false);

      if(!this.epwingSearchTerm)
      {
        rcxMain.cleanupLookupEpwing();
        return;
      }
    }

    // Reset the EPWING hit number and hit totals if a new word is being searched for
    if(this.epwingSearchTerm != this.prevEpwingSearchTerm)
    {
      this.epwingTotalHits = 0;
      this.epwingCurHit = 0;
      this.epwingPrevHit = 0;
      this.prevEpwingSearchTerm = this.epwingSearchTerm;
    }
    else
    {
      if(!rcxConfig.epwingshowallentries && (this.epwingCurHit != this.epwingPrevHit))
      {
        // If just viewing the next/prev entry, no need to re-lookup
        rcxMain.showEpwingPopup();
        return;
      }
    }

    // Form the list of words to lookup
    var wordList = [];
    wordList.push(this.epwingSearchTerm);

    // Perform lookup. When lookup is complete, the results will be passed to lookupEpwingPart2().
    rcxEpwing.lookupWords(rcxMain.epwingCurDic, wordList, rcxMain.lookupEpwingPart2);

  }, /* lookupEpwing */


  // Callback that will be called when the rcxEpwing.lookupWords() function in lookupEpwing() is
  // complete. It saves the EPWING results to rcxMain.epwingResultList. If no results are found,
  // it will fallback. If results are found, it will show a popup containing the results.
  lookupEpwingPart2: function(resultList)
  {
    rcxMain.epwingResultList = resultList;

    // If no result where found in current EPWING dictionary, fallback
    if(resultList.length === 0)
    {
      // If the user want to search for the next longest word and we haven't performed one yet
      if(rcxConfig.epwingsearchnextlongest && !rcxMain.epwingSearchingNextLongest)
      {
        rcxMain.epwingSearchingNextLongest = true;

        window.setTimeout
        (
          function()
          {
            rcxMain.epwingActive = false;
            rcxMain.lookupEpwing();
          }, 10
        );

        return;
      }
      else // Next longest search also failed
      {
        rcxMain.epwingSearchingNextLongest = false;
      }

      // How should we fallback?
      if(rcxConfig.epwingfallback == "none")
      {
        // Don't fallback
        rcxMain.showPopup("Entry not found.");
        rcxMain.cleanupLookupEpwing();
      }
      else if(rcxConfig.epwingfallback == "jmdict")
      {
        // Fallback to the default non-EPWING dictionary that comes with rikaichan (JMDICT)

        rcxMain.cleanupLookupEpwing();
        rcxMain.showPopup(rcxMain.getKnownWordIndicatorText() + rcxData.makeHtml(rcxMain.lastFound[0]),
          rcxMain.lastTdata.get().prevTarget, rcxMain.lastTdata.get().pos);
      }
      else
      {
        // Fallback to the next available EPWING dictionary. If there aren't any, fallback to JMDICT.

        // Are we out of EPWING dictionaries to fallback to?
        if(rcxMain.epwingFallbackCount > rcxMain.epwingDicList.length)
        {
          // If so, fallback to JMDICT
          rcxMain.cleanupLookupEpwing();
          rcxMain.showPopup(rcxMain.getKnownWordIndicatorText() + rcxData.makeHtml(rcxMain.lastFound[0]),
            rcxMain.lastTdata.get().prevTarget, rcxMain.lastTdata.get().pos);
          return;
        }

        // Set a timer to call this function again with the next available dictionary
        window.setTimeout
        (
          function()
          {
            rcxMain.epwingActive = false;
            rcxMain.epwingFallbackCount++;
            rcxMain.nextEpwingDic();
            rcxMain.lookupEpwing();
          }, 10
        );
      }

      return;
    }

    rcxMain.showEpwingPopup();

  }, /* lookupEpwingPart2 */


  // Display the EPWING results in rcxMain.epwingResultList.
  showEpwingPopup: function()
  {
    var epwingText = rcxMain.epwingResultList[0];

    //
    // Extract each entry
    //

    // Replace carriage returns + linefeeds with linefeeds
    epwingText = epwingText.replace(/\r\n/g, '\n');

    var entryFields = epwingText.split(/{ENTRY: \d+}\n/);
    var entryList = [];

    for (let i = 0; i < entryFields.length; ++i)
    {
      var curEntry = entryFields[i];

      if(curEntry.length > 0)
      {
        var isDuplicate = false;

        for(let j = 0; j < entryList.length; ++j)
        {
          if(curEntry == entryList[j])
          {
            isDuplicate = true;
            break;
          }
        }

        if(!isDuplicate)
        {
          entryList.push(entryFields[i]);
        }

        // If user wants to limit number of entries, check to see if we have enough
        if(rcxConfig.epwingshowallentries && (entryList.length >= rcxConfig.epwingmaxentries))
        {
          break;
        }
      }
    }

    // Store the total number of entries
    rcxMain.epwingTotalHits = entryList.length;

    var jmdictGloss = "";

    // Save the JMDICT gloss so that we can append it later
    if(rcxConfig.epwingappendjmdict)
    {
      jmdictGloss = rcxData.makeHtml(rcxMain.lastFound[0]);
    }

    //
    // Format the entry/entries
    //

    // The EPWING lookup text that will be used for the $n (translation) save token.
    var epwingDefText = "";

    // If user wants to display all entries from the same dictionary
    if(rcxConfig.epwingshowallentries)
    {
      epwingText = "";

      for (let i = 0; i < entryList.length; ++i)
      {
        epwingDefText += entryList[i];

        var showHeader = (i == 0);
        epwingText += rcxMain.epwingFormatEntry(entryList[i], showHeader, false);

        // Add entry separator
        if(i != entryList.length - 1)
        {
          epwingText += "<hr />";
          epwingDefText += "<br />";
        }
      }
    }
    else // Display one entry at a time
    {
      epwingDefText = entryList[rcxMain.epwingCurHit];
      epwingText = rcxMain.epwingFormatEntry(entryList[rcxMain.epwingCurHit], true, true);
    }

    // If we were searching the next longest word, perform a new EDICT search so that the
    // expression and reading save tokens will be correct
    if(rcxConfig.epwingsearchnextlongest && rcxMain.epwingSearchingNextLongest)
    {
      var e = rcxData.wordSearch(rcxMain.epwingSearchTerm);
		  this.lastFound = [e];
    }

    // Place the EPWING lookup text into rcxMain.lastFound so that the save and
    // real-time import features work correctly.
    try
    {
      if(rcxConfig.epwingstripnewlines)
      {
        epwingDefText = epwingDefText.replace(/\n/g, " ");
      }
      else
      {
        epwingDefText = epwingDefText.replace(/\n/g, "<br />");
      }

      // Strip initial whitespace/line break
      epwingDefText = epwingDefText.replace(/^( |<br \/>)/, "");

      rcxMain.lastFound[0].data[0][0] = rcxMain.lastFound[0].data[0][0]
        .replace(/\/.+\//g, "/" + epwingDefText + "/");

      // Remove all words except for the one we just looked up
      rcxMain.lastFound[0].data = [rcxMain.lastFound[0].data[0]];
    }
    catch(ex)
    {
      // Probably here because a single kanji was selected that isn't also a regular word.
    }

    // If the user wants to append the JMDICT gloss, do it
    if(rcxConfig.epwingappendjmdict)
    {
      epwingText += "<hr /><span class='epwing-dic-name'>EDICT</span>" + jmdictGloss;
    }

    // Show the EPWING text
    rcxMain.showPopup(epwingText, rcxMain.lastTdata.get().prevTarget, rcxMain.lastTdata.get().pos);

    rcxMain.cleanupLookupEpwing();
	},


  // Format a single EPWING entry for display in the popup.
  epwingFormatEntry: function(entryText, showHeader, showEntryNumber)
  {
    // Trim whitespace
    epwingText = rcxMain.trimEnd(entryText);

    // Remove text that matches the user's regex
    if(rcxConfig.epwingremoveregex != '')
    {
      // Get the regex
      var userRegex = new RegExp(rcxConfig.epwingremoveregex, "g");

      // Use the regex
      var afterRegexEpwingText = epwingText.replace(userRegex, "");

      //
      // Only apply the regex if it doesn't remove all of the text
      //

      var isBlank = afterRegexEpwingText.match(/^\s*$/);

      if(!isBlank)
      {
        epwingText = afterRegexEpwingText;
      }
    }

    // Expression parsed from entry if rcxConfig.epwingaddcolorandpitch is enabled
    var parsedExpression = "";
    var parsedReading = "";

    //
    // Parse entry and add color and pitch to the header line.
    // Only certain dictionaries are supported.
    //

    var dicTitle = rcxMain.getCurEpwingDicTitle();

    if(rcxConfig.epwingaddcolorandpitch
      &&  (rcxConfig.epwingforceparse
           || ((dicTitle == "研究社　新和英大辞典　第５版")
           ||  (dicTitle == "明鏡国語辞典")
           ||  (dicTitle == "大辞泉")
           ||  (dicTitle == "広辞苑第六版")
           ||  (dicTitle == "大辞林 第2版")
           ||  (dicTitle == "三省堂　スーパー大辞林")
           ||  (dicTitle == "新明解国語辞典　第五版"))))
    {
      var newLineIdx = epwingText.indexOf("\n", 1); // Start at 1 because 0 is a \n

      if(newLineIdx != -1)
      {
        // Extract the header line
        var headerLine = epwingText.substr(0, newLineIdx);
        headerLine = rcxMain.trim(headerLine)

        // Remove "ﾛｰﾏ" and onwards for Ken5
        if(dicTitle == "研究社　新和英大辞典　第５版")
        {
          headerLine = headerLine.replace(/ﾛｰﾏ.*/, '');
        }

        // Get the reading. Example the "じんかん" from "じんかん<sup>１</sup>【人間】 "
        headerLine.match(/^(.*?)[<【〘\[]/);
        var reading = RegExp.$1;

        // If no reading found it is because the header line did not contain a <, 【, etc.
        if(!reading)
        {
          reading = rcxMain.trim(headerLine);
        }

        // Get the expression. The "人間" from "じんかん<sup>１</sup>【人間】 "
        headerLine.match(/【(.*?)】/);
        var expression = RegExp.$1;

        // Some dics like Meikyo contain alternate brackets for the expression
        if(!expression)
        {
          headerLine.match(/〘(.*?)〙 /);
          expression = RegExp.$1;
        }

        // Determine the expression and reading to use to get pitch
        if(!expression)
        {
          var pitchExpression = reading;
          var pitchReading = null;
        }
        else
        {
          var pitchExpression = expression;
          var pitchReading = reading;

          if((dicTitle == "三省堂　スーパー大辞林") || (dicTitle == "大辞林 第2版"))
          {
           // If the pitch reading contains a space, remove it and everything after it
            if(pitchReading.indexOf(" ") != -1)
            {
              pitchReading = pitchReading.replace(/^(.*?) .*$/, '$1');
            }
          }

          pitchReading = pitchReading.replace(/[\-‐・ ]/g, '');
        }

        parsedReading = pitchReading;

        // If the pitch expression contains a "・", remove it and everything after
        if(pitchExpression.indexOf("・") != -1)
        {
          pitchExpression = pitchExpression.replace(/^(.*?)・.*$/, '$1');
        }

        // Remove characters found in some non-Ken5 dics
        pitchExpression = pitchExpression.replace(/[\-‐・▽▼△×《》○ ]/g, '');
        pitchExpression = pitchExpression.replace(/<.*?>/g, '');
        pitchExpression = pitchExpression.replace(/\(.*?\)/g, '');
        pitchExpression = pitchExpression.replace(/\（.*?\）/g, '');

        parsedExpression = pitchExpression;

        // Get the pitch accent
        var pitch = "";

        if(rcxConfig.showpitchaccent)
        {
          pitch = rcxMain.getPitchAccent(pitchExpression, pitchReading);
        }

        // Apply color and pitch
        if(headerLine[0] != '①') // This can happen in some non-Ken5 dictionaries
        {
          var newHeaderLine = "";

          if(expression)
          {
            newHeaderLine = "<span class='w-kanji'>" + expression + "</span>"
              + "<span class='w-kana'>" + reading + "</span> "
              + "<span class='w-conj'>" + pitch + "</span>";
          }
          else
          {
            newHeaderLine = "<span class='w-kana'>" + reading + "</span> "
             + "<span class='w-conj'>" + pitch + "</span>";
          }

          // Add in the new header line
          if(rcxConfig.epwingstripnewlines)
          {
            epwingText = newHeaderLine + "<br />" + epwingText.substr(newLineIdx);
          }
          else
          {
            epwingText = newHeaderLine + epwingText.substr(newLineIdx);
          }
        }
      }

    } // End add EPWING color and pitch

    // Show the header text? (known word indicator, entry number, frequency, dictionary number)
    if(showHeader)
    {
      //
      // Get the frequency
      //
      var freqStr = "";

      if(rcxConfig.showfreq)
      {
        // Used the parsed expression if found
        if(parsedExpression != "")
        {
          var freq = rcxMain.getFreq(parsedExpression, parsedReading, true);
        }
        else // Otherwise use the search term used for finding the EPWING entries
        {
          var freq = rcxMain.getFreq(rcxMain.epwingSearchTerm, 'DUMMY', false);
        }

        if(freq && (freq.length > 0))
        {
          var freqClass = rcxMain.getFreqStyle(freq);
          freqStr = ' <span class="' + freqClass + '">' + freq + '</span>';
        }
      }

      var entryNumber = "";

      // Format the (num_entries / total_entries) text?
      if(showEntryNumber)
      {
        entryNumber = "(" + (rcxMain.epwingCurHit + 1) + "/" + rcxMain.epwingTotalHits + ") ";
      }

      // Get the known/to-do list indicator
      knownWordIndicator =  rcxMain.getKnownWordIndicatorText();

      // Add a linefeed at the beginning of epwingText if one does not already exist
      if(epwingText[0] != "\n")
      {
        epwingText = "<br />" + epwingText;
      }

      // Format the conjugation
      var conjugation = "";

      if (rcxConfig.epwingshowconjugation && rcxMain.lastFound[0].data && rcxMain.lastFound[0].data[0][1])
      {
        conjugation = '<span class="w-conj">(' + rcxMain.lastFound[0].data[0][1] + ')</span>';
      }

      // Format the index and title of the current dictionary
      var whichDic = "";

      if(rcxConfig.epwingshowdicnum)
      {
        var dicPos = rcxMain.getEpwingDicIndex() + 1;
        var title = "";

        // If
        if(rcxConfig.epwingshowtitle)
        {
          if(rcxConfig.epwingshowshorttitle)
          {
            title = "　" + rcxMain.getCurEpwingDicShortTitle() + " - ";
          }
          else // Show long title
          {
            title = "　" + rcxMain.getCurEpwingDicTitle() + " - ";
          }
        }

        whichDic = '<span class="epwing-dic-name">' + title + dicPos + '</span>';
      }

      epwingText = knownWordIndicator + entryNumber + conjugation + freqStr + whichDic + epwingText;
    }

    var showDots = false;

    // Limit text to the user-specified number of lines (not
    // including lines generated from word wrap).
    // If 500 (max), don't even check.
    if(rcxConfig.epwingmaxlines != 500)
    {
      var maxLines = rcxConfig.epwingmaxlines;

      // Compensate for the header line
      if(showHeader)
      {
        maxLines++;
      }

      var epwingNumChars = epwingText.length;
      var newLines = 0;

      for(var i = 0; i < epwingNumChars; i++)
      {
        if(epwingText[i] == '\n')
        {
          newLines++;

          if(newLines >= maxLines)
          {
            epwingText = epwingText.substring(0, i);
            showDots = true;
            break;
          }
        }
      }
    }

    // Strip linefeeds or replace with "<br />"?
    if(rcxConfig.epwingstripnewlines)
    {
      epwingText = epwingText.replace(/\n/g, " ");
    }
    else
    {
      epwingText = epwingText.replace(/\n/g, "<br />");
    }

    // Show trailing dots if not all of the entry's lines could be displayed
    if(showDots)
    {
      epwingText += "<br />...";
    }

    return epwingText;

  }, /* epwingFormatEntry */


  // Fetch entry page from sanseido, parse out definition and display
	lookupSanseido: function()
  {
    // Determine if we should use the kanji form or kana form when looking up the word
    if(this.sanseidoFallbackState == 0)
    {
      // Get this kanji form if it exists
      var searchTerm = this.extractSearchTerm(false);
    }
    else if(this.sanseidoFallbackState == 1)
    {
      // Get the reading
      var searchTerm = this.extractSearchTerm(true);
    }

    if(!searchTerm)
    {
      return;
    }

    // If the kanji form was requested but it returned the kana form anyway, then update the state
    if((this.sanseidoFallbackState == 0) && !this.containsKanji(searchTerm))
    {
      this.sanseidoFallbackState = 1;
    }

    // Show the loading message to the screen while we fetch the entry page
    rcxMain.showPopup("Loading...", this.lastTdata.get().prevTarget, this.lastTdata.get().pos);

    //
    // Get entry page asynchronously
    //

    rcxMain.sanseidoReq = new XMLHttpRequest();
    rcxMain.sanseidoReq.open('GET', 'http://www.sanseido.net/User/Dic/Index.aspx?TWords='
      + searchTerm + '&st=0&DailyJJ=checkbox', true);

    // This routine is called periodically with status updates as the entry page is being fetched
    rcxMain.sanseidoReq.onreadystatechange = function (aEvt)
    {
      if(rcxMain.sanseidoReq.readyState == 4)
      {
        if(rcxMain.sanseidoReq.status == 200)
        {
          // Parse definition from page and display it
          rcxMain.parseAndDisplaySanseido(rcxMain.sanseidoReq.responseText);
        }
        else
        {
          // rcxDebug.echo("Error fetching sanseido entry!");
        }
      }
    };

    // Fetch the entry page
    rcxMain.sanseidoReq.send(null);

  }, /* lookupSanseido */


  // Convert an integer to a circled number string:
  // 1 --> ①, 2 --> ②.
  // Range: [0, 50].
  // If out of range, will return num surrounded by parens:
  // 51 --> (51)
  convertIntegerToCircledNumStr: function(num)
  {
    var circledNumStr = "(" + num + ")";

    if (num == 0)
    {
      circledNumStr = "⓪";
    }
    else if ((num >= 1) && (num <= 20))
    {
      circledNumStr = String.fromCharCode(("①".charCodeAt(0) - 1) + num);
    }
    else if ((num >= 21) && (num <= 35))
    {
      circledNumStr = String.fromCharCode(("㉑".charCodeAt(0) - 1) + num);
    }
    else if ((num >= 36) && (num <= 50))
    {
      circledNumStr = String.fromCharCode(("㊱".charCodeAt(0) - 1) + num);
    }

    return circledNumStr;

  }, /* convertIntegerToCircledNumStr */


  // Converts a Japanese number to an integer.
  // ５ --> 5, １２ --> 12, etc.
  convertJapNumToInteger: function(japNum)
  {
    var numStr = "";

    for (i = 0; i < japNum.length; i++)
    {
      c = japNum[i];

      if ((c >= "０") && (c <= "９"))
      {
        convertedNum = (c.charCodeAt(0) - "０".charCodeAt(0));
        numStr += convertedNum;
      }
    }

    return Number(numStr);

  }, /* convertJapNumToInteger */


  // Does the provided text contain a kanji?
  containsKanji: function(text)
  {
    for (i = 0; i < text.length; i++)
    {
      c = text[i];

      if((c >= '\u4E00') && (c <= '\u9FBF'))
      {
        return true;
      }
    }

    return false;
  },


  // Trim whitespace from the beginning and end of text
  trim: function(text)
  {
    return text.replace(/^\s\s*/, "").replace(/\s\s*$/, "");

  }, /* trim */


  // Trim whitespace from the end of text
  trimEnd: function(text)
  {
    return text.replace(/\s\s*$/, "");

  }, /* trimEnd */


  // Sanitize and create DOM tree from HTML input text
  htmlParser: function(aHTMLString)
  {
	  	  	  console.error('htmlParser not implemented' );
	  return 0;
	  
    var html = document.implementation.createDocument("http://www.w3.org/1999/xhtml", "html", null),
      body = document.createElementNS("http://www.w3.org/1999/xhtml", "body");
    html.documentElement.appendChild(body);

    body.appendChild(Components.classes["@mozilla.org/feed-unescapehtml;1"]
      .getService(Components.interfaces.nsIScriptableUnescapeHTML)
      .parseFragment(aHTMLString, false, null, body));

    return body;
  }, /* htmlParser */


  // Get the size of a file in bytes.
  getFileSize: function(path)
  {
	  	  console.error('getFileSize not implemented' );
	  return 0;
	  
    var file =
        Components.classes["@mozilla.org/file/local;1"].
        createInstance(Components.interfaces.nsILocalFile);
    file.initWithPath(path);
    return file.fileSize;

  }, /* getFileSize */


  // Return the two-digit hexadecimal code for a byte.
  toHexString: function(charCode)
  {
    return ("0" + charCode.toString(16)).slice(-2);

  }, /* toHexString */


  // Return the MD5 hash of the provided file as a string.
  // https://developer.mozilla.org/en-US/docs/XPCOM_Interface_Reference/nsICryptoHash
  // filePath - (string) The path of the file to hash.
  getFileHash: function(filePath)
  {
    var file = new FileUtils.File(filePath);

    var istream = Components.classes["@mozilla.org/network/file-input-stream;1"]
      .createInstance(Components.interfaces.nsIFileInputStream);

    // Open for reading
    istream.init(file, 0x01, 0444, 0);

    var ch = Components.classes["@mozilla.org/security/hash;1"]
      .createInstance(Components.interfaces.nsICryptoHash);

    // We want to use the MD5 algorithm
    ch.init(ch.MD5);

    // This tells updateFromStream to read the entire file
    const PR_UINT32_MAX = 0xffffffff;
    ch.updateFromStream(istream, PR_UINT32_MAX);

    istream.close();

    // Pass false here to get binary data back
    var hash = ch.finish(false);

    // Convert the binary hash data to a hex string
    var s = '';
	var arr = [];
	for (var i=0; i < hash.length; ++i) {
		hash.append(rcxMain.toHexString(hash.charCodeAt(i)));
	}
	s = arr.join("");
    return s;

  }, /* getFileHash */


  // Download the JDIC audio and then play it.
  // httpLoc - (string) The URL of the MP3 to download.
  // saveFilename - (string) Name of save file (without path).
  // saveAudioClipToDisk - (bool) True = Save the audio clip to the audio directory.
  downloadAndPlayAudio: function(httpLoc, saveFilename, saveAudioClipToDisk)
  {
	  console.warn('downloadAndPlayAudio not implemented');
	  return;
    if(!httpLoc || (httpLoc.length == 0)
      || !saveFilename || (saveFilename.length == 0))
    {
      return;
    }

    try
    {
      // The shorter 'no audio' mp3 file
      var noAudioPath = OS.Path.join(
        OS.Constants.Path.profileDir, "extensions", rcxMain.id, "audio", "no_audio.mp3");

      var savedAudioPath = null;

      // If the user entered a directory in which to store the audio files
      if(rcxConfig.audiodir && (rcxConfig.audiodir.length > 0))
      {
        // Create the file object for the file to save to the audio directory
        savedAudioPath = OS.Path.join(rcxConfig.audiodir, saveFilename);
      }

      // If saveFilename is in the 'no audio' dictionary
      if(rcxMain.noAudioDic[saveFilename])
      {
        // If user wants to hear the 'no audio' clip, play it
        if(rcxConfig.enablenoaudioclip)
        {
          rcxMain.playAudioFile(noAudioPath);
        }

        // Exit - There is nothing to save
        return;
      }

      // Does the file already exist in the audio dir? If so, play it and don't download.
      if(savedAudioPath)
      {
        // Create a file object for the saved file (for checking existence)
        var savedAudioFile = new FileUtils.File(savedAudioPath);

        // If the destination already exists, play it and skip the download
        if(savedAudioFile.exists())
        {
          // If the 'no audio' clip has not been hashed yet, hash it
          if(this.noAudioFileHash == "")
          {
            this.noAudioFileHash = rcxMain.getFileHash(noAudioPath);
          }

          // If user doesn't want to hear the 'no audio' clip.
          if(!rcxConfig.enablenoaudioclip)
          {
            // Hash the audio file and compare it against the hash of the 'no audio' clip
            // Note: As of v19.2, Rikaisama no longer saves the 'no audio' clips to the audio folder
            //       for caching purposes. This code is left here in case the user still has these
            //       clips in the audio folder from a previous version.
            var hash = rcxMain.getFileHash(savedAudioPath);

            if(hash == this.noAudioFileHash)
            {
              return;
            }
          }

          rcxMain.playAudioFile(savedAudioPath);
          return;
        }
      }

      var downloadedAudioPath = OS.Path.join(OS.Constants.Path.tmpDir, "~rikai_audio.mp3");
      var audioFileToPlay = null;

      Task.spawn(function ()
      {/*
        try
        {
          // Download the audio file and save to a temporary location
          yield Downloads.fetch(httpLoc, downloadedAudioPath);

          var fileSize = rcxMain.getFileSize(downloadedAudioPath);

          // Did we just download the 'no audio' clip? If so, play a shorter 'no audio' clip instead
          if(fileSize > 52000)
          {
            rcxMain.addNoAudioListEntry(saveFilename);

            // If the user wants to hear the 'no audio' clip
            if(rcxConfig.enablenoaudioclip)
            {
              audioFileToPlay = noAudioPath;
            }
          }
          else // Not the 'no audio' clip
          {
            audioFileToPlay = downloadedAudioPath;

            // Save audio file to user-provided directory
            if(saveAudioClipToDisk && savedAudioPath)
            {
              OS.File.copy(downloadedAudioPath, savedAudioPath);
            }
          }

          if(audioFileToPlay)
          {
            rcxMain.playAudioFile(audioFileToPlay);
          }
        }
        catch(ex)
        {
          console.error("[1] downloadAndPlayAudio() Error: " + ex);
        }*/
      }).then(null, console.error);
    }
    catch(ex)
    {
      console.error("[2] downloadAndPlayAudio() Error: " + ex);
    }
  }, /* downloadAndPlayAudio() */


  // Play the provided audio file.
  // audioFilePath - (string) The path of the audio file to play.
  playAudioFile: function(audioFilePath)
  {
	  console.error('playAudioFile not implemented' );
	  return 0;
	  
    var audioFile = new FileUtils.File(audioFilePath);

    // Get the URL of the file
    var ioService = Components.classes["@mozilla.org/network/io-service;1"]
                      .getService(Components.interfaces.nsIIOService);
    var fileURL = ioService.newFileURI(audioFile).spec;

    var audioCtx = new AudioContext();
    var source = audioCtx.createBufferSource();
    var request = new XMLHttpRequest();

    // Open the file and store into an ArrayBuffer
    request.open('GET', fileURL, true);
    request.responseType = 'arraybuffer';
    request.onload = function()
    {
      var audioData = request.response;

      audioCtx.decodeAudioData(audioData, function(buffer)
      {
          // Set the volume to a [0.0, 1.0] range
          var gainNode = audioCtx.createGain();
          gainNode.gain.value = rcxConfig.volume / 100.0;

          source.buffer = buffer;
          source.connect(gainNode);
          gainNode.connect(audioCtx.destination);

          // Play
          source.start();
      }, function(e){"Error with decoding audio data" + e.err});
    }

    request.send();

  }, /* playAudioFile */


  // Play the JDIC audio for the hilited word.
  // saveAudio - (boolean) Save the audio in the user specified audio folder
	playJDicAudio: function(saveAudio)
	{
    // Get the currently hilited entry
    var hilitedEntry = this.lastFound;

    if ((!hilitedEntry) || (hilitedEntry.length == 0))
    {
      return 0;
    }

    var kanjiText;
    var kanaText;

    // Is a single kanji selected?
    if(hilitedEntry[0] && hilitedEntry[0].kanji && hilitedEntry[0].onkun)
    {
      //rcxDebug.echo("hilitedEntry[0].kanji = \"" + hilitedEntry[0].kanji + "\"");
      //rcxDebug.echo("hilitedEntry[0].onkun = \"" + hilitedEntry[0].onkun + "\"");

      hilitedEntry[0].onkun.match(/^([^\u3001]*)/);

      kanjiText = hilitedEntry[0].kanji;
      kanaText = RegExp.$1;

      if(!kanjiText || !kanaText)
      {
        return 0;
      }

      // For kanji readings, JDIC uses hiragana instead of katakana
      kanaText = rcxData.convertKatakanaToHiragana(kanaText);

      if(!kanaText)
      {
        return 0;
      }
    }
    // Is an entire word selected?
    else if(hilitedEntry[0] && hilitedEntry[0].data[0])
    {
      // Extract needed data from the hilited entry
      //   entryData[0] = kanji/kana + kana + definition
      //   entryData[1] = kanji (or kana if no kanji)
      //   entryData[2] = kana (null if no kanji)
      //   entryData[3] = definition
      var entryData =
        hilitedEntry[0].data[0][0].match(/^(.+?)\s+(?:\[(.*?)\])?\s*\/(.+)\//);

      if (!entryData)
      {
        return 0;
      }

      // Get just the kanji and kana
      kanjiText = entryData[1];
      kanaText = entryData[2];

      if(!kanjiText)
      {
        return 0;
      }

      if(!kanaText)
      {
        kanaText = kanjiText;
      }
    }
    else
    {
      return 0;
    }

    //rcxDebug.echo("Kana =\"" + kanaText + "\"  Kanji = \"" + kanjiText + "\"");

    // Form the URL
    var jdicAudioUrlText =
      "http://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kana="
      + kanaText + "&kanji=" + kanjiText;

    //rcxDebug.echo(jdicAudioUrlText);

    // Encode link to ASCII character set
    //encodedJdicAudioUrlText = encodeURI(jdicAudioUrlText);

    var saveFile = kanaText + ' - ' + kanjiText + '.mp3';

    var saveAudioClipToDisk = (saveAudio || rcxConfig.saveaudioonplay);

    this.downloadAndPlayAudio(jdicAudioUrlText, saveFile, saveAudioClipToDisk);

	}, /* playJDicAudio */


	saveToFile: function() {
		var text;
		var i;
		var lf, fos, os;

		try
    {
			if (rcxConfig.sfile.length == 0)
      {
				this.showPopup('Please set the filename in Preferences.');
				return;
			}

			if (rcxConfig.saveformat.length == 0)
      {
				this.showPopup('Please create a save format in Preferences.');
				return;
			}

			if ((text = this.savePrep(0, rcxConfig.saveformat)) == null)
      {
        return;
      }

      // Save the audio clip if the audio directory was specified by the user
      if (rcxConfig.audiodir.length != 0)
      {
        this.playJDicAudio(true);
      }

			lf = Components.classes['@mozilla.org/file/local;1']
					.createInstance(Components.interfaces.nsILocalFile);

			lf.initWithPath(rcxConfig.sfile);
			let exists = lf.exists();

			fos = Components.classes['@mozilla.org/network/file-output-stream;1']
				.createInstance(Components.interfaces.nsIFileOutputStream);
			fos.init(lf, 0x02 | 0x08 | 0x10, -1, 0);	//writing only, create file if none exists, pointer set to end of file for writing

			if ((!exists) && (rcxConfig.ubom) && (rcxConfig.sfcs == 'utf-8')) {
				let bom = '\xEF\xBB\xBF';
				fos.write(bom, bom.length);
			}

			// note: nsIConverterOutputStream always adds BOM for UTF-16

			os = Components.classes['@mozilla.org/intl/converter-output-stream;1']
					.createInstance(Components.interfaces.nsIConverterOutputStream);
			os.init(fos, rcxConfig.sfcs, 0, 0x3F);	// unknown -> '?'
			os.writeString(text);
			os.close();

			fos.close();

			this.showPopup('Saved.');
		}
		catch (ex) {
			this.showPopup('Error while saving: ' + ex);
		}
	},

	configPage: function()
  {
		window.openDialog('//anjsub.com/mary/src/6ka/options.xul', '', 'chrome,centerscreen,resizable');
	},


	keysDown: [],

	onKeyDown: function(ev) { rcxMain._onKeyDown(ev) },
	_onKeyDown: function(ev) {
		//	this.status('keyCode=' + ev.keyCode + ' charCode=' + ev.charCode + ' detail=' + ev.detail);

		if ((ev.altKey) || (ev.metaKey) || (ev.ctrlKey)) return;
		if ((ev.shiftKey) && (ev.keyCode != 16)) return;
		if (this.keysDown[ev.keyCode]) return;
		if (!this.isVisible()) return;
		if ((rcxConfig.nopopkeys) && (ev.keyCode != 16)) return;

		var i;

		switch (ev.keyCode)
    {
		case 13:	// ENTER - Switch dictionary
			this.clearHi();
			// continues...
		case 16:	// SHIFT - Switch dictionary
      this.allowOneTimeSuperSticky();

			let tdata = ev.currentTarget.rikaichan;
			if (tdata) {
				rcxData.selectNext();	// @@@ hmm
				if (tdata.titleShown) this.showTitle(tdata);
					else this.show(tdata);
			}
			break;

		case 27:	// ESC - Remove popup

      // If in Super Sticky mode, allow the popup to hide
      if(this.superSticky)
      {
        this.superStickyOkayToHide = true;
      }

			this.hidePopup();
			this.clearHi();
			break;

		case parseInt(rcxConfig.kbalternateview): // a - Alternate popup location
      this.allowOneTimeSuperSticky();

			this.altView = (this.altView + 1) % 3;
			if (this.altView) this.status('Alternate View #' + this.altView);
				else this.status('Normal View');
			this.show(ev.currentTarget.rikaichan);
			break;

		case parseInt(rcxConfig.kbcopytoclipboard):	// c - Copy to clipboard
			this.copyToClip();
			break;

		case parseInt(rcxConfig.kbhideshowdefinitions):	// d - Hide/show definitions
      this.allowOneTimeSuperSticky();

			rcxConfig.hidedef = !rcxConfig.hidedef;
			this.status((rcxConfig.hidedef ? 'Hide' : 'Show') + ' definition');
			if (rcxConfig.hidedef) this.showPopup('Hiding definitions. Press "D" to show again.');
				else this.show(ev.currentTarget.rikaichan);
			break;

		case parseInt(rcxConfig.kbjdicaudio):	// f - JDIC Audio
			this.playJDicAudio(false);
			break;

		case parseInt(rcxConfig.kbsavetofile):	// s - Save to file
      rcxMain.saveKana = false;
			this.saveToFile();
			break;

		case parseInt(rcxConfig.kbsavetofilekana):	// x - Save to file (kana version $d=$r)
      rcxMain.saveKana = true;
			this.saveToFile();
			break;

		case parseInt(rcxConfig.kbpreviouscharacter):	// b - Previous character
      this.allowOneTimeSuperSticky();
			var ofs = ev.currentTarget.rikaichan.uofs;
			for (i = 50; i > 0; --i) {
				ev.currentTarget.rikaichan.uofs = --ofs;
				rcxData.select(0);
				if (this.show(ev.currentTarget.rikaichan) >= 0) {
					if (ofs >= ev.currentTarget.rikaichan.uofs) break;	// ! change later
				}
			}
			break;

		case parseInt(rcxConfig.kbnextcharacter):	// m - Next character
      this.allowOneTimeSuperSticky();
			ev.currentTarget.rikaichan.uofsNext = 1;

		case parseInt(rcxConfig.kbnextword):	// n - Next word
      this.allowOneTimeSuperSticky();

			for (i = 50; i > 0; --i) {
				ev.currentTarget.rikaichan.uofs += ev.currentTarget.rikaichan.uofsNext;
				rcxData.select(0);
				if (this.show(ev.currentTarget.rikaichan) >= 0) break;
			}
			break;

		case parseInt(rcxConfig.kbstickypopup):	// k - Sticky popup behavior
			this.sticky = !this.sticky;
			this.status(this.sticky ? 'Sticky Popup' : 'Normal Popup');
			break;

    case parseInt(rcxConfig.kbsanseidomode): // o - Sanseido mode
      this.allowOneTimeSuperSticky();
      this.toggleSanseidoMode();
      this.show(ev.currentTarget.rikaichan);
      break;

    case parseInt(rcxConfig.kbepwingmode): // p - EPWING mode
      this.allowOneTimeSuperSticky();
      this.toggleEpwingMode();
      this.show(ev.currentTarget.rikaichan);
      break;

    case parseInt(rcxConfig.kbrealtimeimport): // r - Anki Real-Time Import
      rcxMain.saveKana = false;
      this.sendToAnki();
      break;

    case parseInt(rcxConfig.kbrealtimeimportkana): // t - Anki Real-Time Import (kana version $d=$r)
      rcxMain.saveKana = true;
      this.sendToAnki();
      break;

    case parseInt(rcxConfig.kbsuperstickymode): // u - Super Sticky mode
      this.toggleSuperStickyMode();
      break;

		case parseInt(rcxConfig.kbmovepopupdown):	// y - Move popup location down
      this.allowOneTimeSuperSticky();

			this.altView = 0;
			ev.currentTarget.rikaichan.popY += 20;
			this.show(ev.currentTarget.rikaichan);
			break;

    case parseInt(rcxConfig.kbeditnotes): // j - Edit notes
      var notes = prompt("Enter text to use with the Notes save token:", rcxConfig.savenotes);

      // If OK was pressed, save the notes
      if(notes)
      {
        let prefs = new rcxPrefs();
        prefs.setString('savenotes', notes);
      }
      break;

		case parseInt(rcxConfig.kbepwingnextdic):	// + - Goto next dictionary
      var origDic = this.epwingCurDic;

      this.nextEpwingDic();

      if(origDic != this.epwingCurDic)
      {
        this.allowOneTimeSuperSticky();

        // Reset the EPWING hit number and hit totals
        this.epwingTotalHits = 0;
        this.epwingCurHit = 0;
        this.epwingPrevHit = 0;

        this.show(ev.currentTarget.rikaichan);
      }
			break;

		case parseInt(rcxConfig.kbepwingprevdic):	// - - Goto previous dictionary
      var origDic = this.epwingCurDic;

      this.prevEpwingDic();

      if(origDic != this.epwingCurDic)
      {
        this.allowOneTimeSuperSticky();

       // Reset the EPWING hit number and hit totals
        this.epwingTotalHits = 0;
        this.epwingCurHit = 0;
        this.epwingPrevHit = 0;

        this.show(ev.currentTarget.rikaichan);
      }
			break;

    case parseInt(rcxConfig.kbepwingpreventry): // [ - Move to previous hit (EPWING mode)
      if(this.epwingTotalHits > 0)
      {
        this.allowOneTimeSuperSticky();

        this.epwingPrevHit =  this.epwingCurHit;

        this.epwingCurHit--;

        if(this.epwingCurHit < 0)
        {
          this.epwingCurHit = this.epwingTotalHits - 1;
        }

        this.show(ev.currentTarget.rikaichan);
      }
      break;

    case parseInt(rcxConfig.kbepwingnextentry): // ] - Move to next hit (EPWING mode)

      if(this.epwingTotalHits > 0)
      {
        this.allowOneTimeSuperSticky();

        this.epwingPrevHit = this.epwingCurHit;
        this.epwingCurHit = (this.epwingCurHit + 1) % this.epwingTotalHits;
        this.show(ev.currentTarget.rikaichan);
      }
      break;

		default:
			if ((ev.keyCode >= 49) && (ev.keyCode <= 57)) // 1-9 - Switch dictionary
      {
        this.allowOneTimeSuperSticky();

				rcxData.select(ev.keyCode - 49);
				this.show(ev.currentTarget.rikaichan);
			}
			return;
		}

		this.keysDown[ev.keyCode] = 1;

		// don't eat shift if in this mode
		if (!rcxConfig.nopopkeys) {
			ev.stopPropagation();
			ev.preventDefault();
		}
	},


	onKeyUp: function(ev) {
		if (rcxMain.keysDown[ev.keyCode]) rcxMain.keysDown[ev.keyCode] = 0;
	},


	onMouseUp: function(ev)
  {
    // Did a Ctrl-right click just occur in Super Sticky mode?
    if(ev.ctrlKey && (ev.button == 2) && rcxMain.superSticky)
    {
      // Set a timer to remove the right-click context menu by creating a key press event
      // that simulates an ESC press. It won't work if we send the ESC press right away,
      // we have to wait a little while, hence the timer.
        window.setTimeout
        (
          function()
          {
            var evnt = document.createEvent("KeyboardEvent");
            evnt.initKeyEvent("keypress", true, true, window, false, false, false, false, 27, 0);
            ev.target.dispatchEvent(evnt);
          }, 15);
    }
  },


	onMouseDown: function(ev)
  {
    // Did a Ctrl-click or Alt-click just occur in Super Sticky mode?
    if(rcxMain.superSticky && (ev.ctrlKey || ev.altKey))
    {
      // Prevent the surrounding table element from hiliting when the user
      // performs a ctrl-left click
      if(ev.button == 0)
      {
        ev.preventDefault();
      }

      let tdata = ev.currentTarget.rikaichan;

      rcxMain.superStickyOkayToShow = true;

      if(tdata)
      {
        if (tdata.titleShown)
        {
          rcxMain.showTitle(tdata);
        }
        else
        {
          rcxMain.show(tdata);
        }
      }
    }
    else if(!rcxMain.cursorInPopup(ev))
    {
      rcxMain.superStickyOkayToHide = true;
      rcxMain.hidePopup();
    }
	},

	unicodeInfo: function(c) {
		const hex = '0123456789ABCDEF';
		const u = c.charCodeAt(0);
		return c + ' U' + hex[(u >>> 12) & 15] + hex[(u >>> 8) & 15] + hex[(u >>> 4) & 15] + hex[u & 15];
	},

	inlineNames: {
		// text node
		'#text': true,

		// font style
		'FONT': true,
		'TT': true,
		'I' : true,
		'B' : true,
		'BIG' : true,
		'SMALL' : true,
		//deprecated
		'STRIKE': true,
		'S': true,
		'U': true,

		// phrase
		'EM': true,
		'STRONG': true,
		'DFN': true,
		'CODE': true,
		'SAMP': true,
		'KBD': true,
		'VAR': true,
		'CITE': true,
		'ABBR': true,
		'ACRONYM': true,

		// special, not included IMG, OBJECT, BR, SCRIPT, MAP, BDO
		'A': true,
		'Q': true,
		'SUB': true,
		'SUP': true,
		'SPAN': true,
		'WBR': true,

		// ruby
		'RUBY': true,
		'RBC': true,
		'RTC': true,
		'RB': true,
		'RT': true,
		'RP': true,

    // User configurable elements
    'DIV': false,
	},


  // Configure this.inlineNames based on user settings.
  configureInlineNames: function()
  {
    this.inlineNames["DIV"] = rcxConfig.mergedivs;

  }, /* configureInlineNames */


	// Gets text from a node and returns it
	// node: a node
	// selEnd: the selection end object will be changed as a side effect
	// maxLength: the maximum length of returned string
	getInlineText: function (node, selEndList, maxLength) {
		if ((node.nodeType == Node.TEXT_NODE) && (node.data.length == 0)) return ''

		let text = '';
		let result = node.ownerDocument.evaluate('descendant-or-self::text()[not(parent::rp) and not(ancestor::rt)]',
						node, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
		while ((maxLength > 0) && (node = result.iterateNext())) {
			text += node.data.substr(0, maxLength);
			maxLength -= node.data.length;
			selEndList.push(node);
		}
		return text;
	},

	// Given a node which must not be null, returns either the next sibling or
	// the next sibling of the father or the next sibling of the fathers father
	// and so on or null
	getNext: function(node) {
		do {
			if (node.nextSibling) return node.nextSibling;
			node = node.parentNode;
		} while ((node) && (this.inlineNames[node.nodeName]));
		return null;
	},

	getTextFromRange: function(rangeParent, offset, selEndList, maxLength) {
		if (rangeParent.ownerDocument.evaluate('boolean(parent::rp or ancestor::rt)',
			rangeParent, null, XPathResult.BOOLEAN_TYPE, null).booleanValue)
			return '';

		if (rangeParent.nodeType != Node.TEXT_NODE)
			return '';

		let text = rangeParent.data.substr(offset, maxLength);
		selEndList.push(rangeParent);

		var nextNode = rangeParent;
		while ((text.length < maxLength) &&
			((nextNode = this.getNext(nextNode)) != null) &&
			(this.inlineNames[nextNode.nodeName])) {
			text += this.getInlineText(nextNode, selEndList, maxLength - text.length);
		}

		return text;
	},


	getInlineTextPrev: function (node, selEndList, maxLength)
  {
		if((node.nodeType == Node.TEXT_NODE) && (node.data.length == 0))
    {
      return ''
    }

		let text = '';

		let result = node.ownerDocument.evaluate('descendant-or-self::text()[not(parent::rp) and not(ancestor::rt)]',
						     node, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);

		while((text.length < maxLength) && (node = result.iterateNext()))
    {
      if(text.length + node.data.length >= maxLength)
      {
        text += node.data.substr(node.data.length - (maxLength - text.length), maxLength - text.length);
      }
      else
      {
			  text += node.data;
      }

			selEndList.push(node);
		}

		return text;
	},


	getPrev: function(node)
  {
		do
    {
			if (node.previousSibling)
      {
        return node.previousSibling;
      }

			node = node.parentNode;
		}
    while ((node) && (this.inlineNames[node.nodeName]));

		return null;
	},


	getTextFromRangePrev: function(rangeParent, offset, selEndList, maxLength)
  {
		if (rangeParent.ownerDocument.evaluate('boolean(parent::rp or ancestor::rt)',
			rangeParent, null, XPathResult.BOOLEAN_TYPE, null).booleanValue)
    {
			return '';
    }

		let text = '';
		var prevNode = rangeParent;

		while ((text.length < maxLength) &&
			((prevNode = this.getPrev(prevNode)) != null) &&
			(this.inlineNames[prevNode.nodeName]))
    {
      textTemp = text;
      text = this.getInlineTextPrev(prevNode, selEndList, maxLength - text.length) + textTemp;
		}

		return text;
	},


	highlightMatch: function(doc, rp, ro, matchLen, selEndList, tdata) {
		if (selEndList.length === 0) return;

		var selEnd;
		var offset = matchLen + ro;
		// before the loop
		// |----!------------------------!!-------|
		// |(------)(---)(------)(---)(----------)|
		// offset: '!!' lies in the fifth node
		// rangeOffset: '!' lies in the first node
		// both are relative to the first node
		// after the loop
		// |---!!-------|
		// |(----------)|
		// we have found the node in which the offset lies and the offset
		// is now relative to this node
		for (var i = 0; i < selEndList.length; ++i) {
			selEnd = selEndList[i]
			if (offset <= selEnd.data.length) break;
			offset -= selEnd.data.length;
		}

		var range = doc.createRange();
		range.setStart(rp, ro);
		range.setEnd(selEnd, offset);

		var sel = doc.defaultView.getSelection();
		if ((!sel.isCollapsed) && (tdata.selText != sel.toString()))
			return;
		sel.removeAllRanges();
		sel.addRange(range);
		tdata.selText = sel.toString();
	},

	show: function(tdata) {
		//console.log('show');
		var rp = tdata.prevRangeNode; // The currently selected node
		var ro = tdata.prevRangeOfs + tdata.uofs; // The position of the hilited text in the currently selected node
		var i;
		var j;

		tdata.uofsNext = 1;

		if (!rp) {
			this.clearHi();
			this.hidePopup();
			return 0;
		}

		if ((ro < 0) || (ro >= rp.data.length)) {
			this.clearHi();
			this.hidePopup();
			return 0;
		}

		// @@@ check me
		let u = rp.data.charCodeAt(ro);
		if ((isNaN(u)) ||
			((u != 0x25CB) &&
			((u < 0x3001) || (u > 0x30FF)) &&
			((u < 0x3400) || (u > 0x9FFF)) &&
			((u < 0xF900) || (u > 0xFAFF)) &&
			((u < 0xFF10) || (u > 0xFF9D)))) {
			this.clearHi();
			this.hidePopup();
			return -2;
		}

    // Configure this.inlineNames based on user settings
    this.configureInlineNames();

		//selection end data
		var selEndList = [];

    // The text here will be used to lookup the word
		var text = this.getTextFromRange(rp, ro, selEndList, 20);
	//	console.log(text);

    // The text from the currently selection node + 50 more characters from the next nodes
		var sentence = this.getTextFromRange(rp, 0, selEndList, rp.data.length + 50);

    // 50 characters from the previous nodes.
    // The above sentence var will stop at first ruby tag encountered to the
    // left because it has a different node type. prevSentence will start where
    // the above sentence left off moving to the left and will capture the ruby tags.
    var prevSentence = this.getTextFromRangePrev(rp, 0, selEndList, 50);

    // Combine the full sentence text, including stuff that will be chopped off later.
    sentence = prevSentence + sentence;

		//this.word = text;

    //
		// Find the sentence in the node
    //

    // Get the position of the first selected character in the sentence variable
		i = ro + prevSentence.length;

		var sentenceStartPos;
		var sentenceEndPos;

    // Find the last character of the sentence
		while (i < sentence.length)
    {
			if (sentence[i] == "。" || sentence[i] == "\n" || sentence[i] == "？" ||　sentence[i] == "！")
      {
				sentenceEndPos = i;
				break;
			}
      else if (i == (sentence.length - 1))
      {
				sentenceEndPos = i;
			}

			i++;
		}

		i = ro + prevSentence.length;


    // Find the first character of the sentence
		while (i >= 0)
    {
			if (sentence[i] == "。" || sentence[i] == "\n" || sentence[i] == "？" ||　sentence[i] == "！")
      {
				sentenceStartPos = i + 1;
				break;
			}
      else if (i == 0)
      {
				sentenceStartPos = i;
			}

			i--;
		}

    // Extract the sentence
		sentence = sentence.substring(sentenceStartPos, sentenceEndPos + 1);

    var startingWhitespaceMatch = sentence.match(/^\s+/);

    // Strip out control characters
		sentence = sentence.replace(/[\n\r\t]/g, '');

    var startOffset = 0;

   // Adjust offset of selected word according to the number of
   // whitespace chars at the beginning of the sentence
   if(startingWhitespaceMatch)
   {
     startOffset -= startingWhitespaceMatch[0].length;
   }

    // Trim
    sentence = rcxMain.trim(sentence);

		this.sentence = sentence;

		if (text.length == 0) {
			this.clearHi();
			this.hidePopup();
			return 0;
		}

		var e = rcxData.wordSearch(text);
		if (e == null) {
			this.hidePopup();
			this.clearHi();
			//console.log('exit because wordSearch return null for text: ' + text);
			return 0;
		}
		this.lastFound = [e];

    // Find the highlighted word, rather than the JMDICT lookup
		this.word = text.substring(0, e.matchLen);

		var wordPosInSentence = ro + prevSentence.length - sentenceStartPos + startOffset;

    // Add blanks in place of the hilited word for use with the save feature
		sentenceWBlank = sentence.substring(0, wordPosInSentence) + "___"
					+ sentence.substring(wordPosInSentence + e.matchLen, sentence.length);

		this.sentenceWBlank = sentenceWBlank;

		if (!e.matchLen) e.matchLen = 1;
		tdata.uofsNext = e.matchLen;
		tdata.uofs = (ro - tdata.prevRangeOfs);

		// don't try to highlight form elements
		if ((rcxConfig.highlight) && (!('form' in tdata.prevTarget))) {
			var doc = tdata.prevRangeNode.ownerDocument;
			if (!doc) {
				this.clearHi();
				this.hidePopup();
				return 0;
			}
			this.highlightMatch(doc, tdata.prevRangeNode, ro, e.matchLen, selEndList, tdata);
			tdata.prevSelView = doc.defaultView;
		}

		tdata.titleShown = false;

    // Save the tdata so that the sanseido routines can use it
    this.lastTdata = tdata; //Components.utils.getWeakReference(tdata);

    // When auto play is enabled, the user must hilite a word for at least 500 ms before
    // the audio will be played.
    if(rcxConfig.autoplayaudio)
    {
      if(this.autoPlayAudioTimer)
      {
        clearTimeout(this.autoPlayAudioTimer);
        this.autoPlayAudioTimer = null;
      }

      this.autoPlayAudioTimer = setTimeout(function() { rcxMain.playJDicAudio(false) }, 500);
    }

    // If not in Super Sticky mode or the user manually requested a popup
    if(!this.superSticky || this.superStickyOkayToShow)
    {
		//console.log('ssshow')
      // Clear the one-time okay-to-show flag
      this.superStickyOkayToShow = false;

      // If we are in sanseido mode and the normal non-names, non-kanji dictionary is selected
      if(this.sanseidoMode
        && (rcxData.dicList[rcxData.selected].name.indexOf("Names") == -1)
        && (rcxData.dicList[rcxData.selected].name.indexOf("Kanji") == -1))
      {
        this.sanseidoFallbackState = 0; // 0 = Lookup with kanji form (if applicable)
        this.lookupSanseido();
      }
      // If we are in EPWING mode and the normal non-names, non-kanji dictionary is selected
      else if(this.epwingMode
        && (rcxData.dicList[rcxData.selected].name.indexOf("Names") == -1)
        && (rcxData.dicList[rcxData.selected].name.indexOf("Kanji") == -1))
      {
        if(this.epwingTimer)
        {
          clearTimeout(this.epwingTimer);
          this.epwingTimer = null;
        }

        // The user must hilite a word for at least 100 ms before the lookup will occur
        this.epwingTimer = setTimeout(function() { rcxMain.lookupEpwing() }, 0);
      }
      // Normal popup
      else
      {
		 // console.log(rcxData.makeHtml(e))
        this.showPopup(rcxMain.getKnownWordIndicatorText() + rcxData.makeHtml(e), tdata.prevTarget, tdata.pos);
      }
    }

		return 1;
	},


	showTitle: function(tdata) {
		var e = rcxData.translate(tdata.title);
		if (!e) {
			this.hidePopup();
			return;
		}

		e.title = tdata.title.substr(0, e.textLen).replace(/[\x00-\xff]/g, function (c) { return '&#' + c.charCodeAt(0) + ';' } );
		if (tdata.title.length > e.textLen) e.title += '...';

		this.lastFound = [e];
		tdata.titleShown = true;

    if(!this.superSticky || this.superStickyOkayToShow)
    {
      // Clear the one-time okay-to-show flag
      this.superStickyOkayToShow = false;

		  this.showPopup(rcxData.makeHtml(e), tdata.prevTarget, tdata.pos);
    }
	},

	onMouseMove: function(ev) { rcxMain._onMouseMove(ev); },
	_onMouseMove: function(ev) {
		var tdata = ev.currentTarget.rikaichan;	// per-tab data
		var rp = null;
		var ro = -1;
		if(document.caretRangeFromPoint) {  // Webkit
			const rrange = document.caretRangeFromPoint(ev.x, ev.y);
			if(rrange) {
				rp = rrange.startContainer;
				ro = rrange.startOffset;
			}
		} else {                           // Mozilla
			rp = ev.rangeParent;
			ro = ev.rangeOffset;
		}
/*
		var cb = this.getBrowser();
		var bbo = cb.boxObject;
		var z = cb.markupDocumentViewer ? cb.markupDocumentViewer.fullZoom : 1;
		var y = (ev.screenY - bbo.screenY);
		this.status('sy=' + ev.screenY + ' z=' + z +
			' bsy=' + bbo.screenY + ' y=' + y + ' y/z=' + Math.round(y / z));
*/
		
		if ((this.sticky) && (this.cursorInPopup(ev))) {
			clearTimeout(tdata.timer);
			tdata.timer = null;
			return;
		}

		if (ev.target == tdata.prevTarget) {
			if (tdata.title) return;
			if ((rp == tdata.prevRangeNode) && (ro == tdata.prevRangeOfs)) return;
		}

		if (tdata.timer) {
			clearTimeout(tdata.timer);
			tdata.timer = null;
		}

		//ev.explicitOriginalTarget = ev.explicitOriginalTarget || ev.target;
		if ((ev.explicitOriginalTarget != undefined && ev.explicitOriginalTarget.nodeType != Node.TEXT_NODE) && !('form' in ev.target)) {
			rp = null;
			ro = -1;
		}

		tdata.prevTarget = ev.target;
		tdata.prevRangeNode = rp;
		tdata.prevRangeOfs = ro;
		tdata.title = null;
		tdata.uofs = 0;
		this.uofsNext = 1;

		if (ev.button != 0) return;
		if (this.lbPop) return;

		if ((rp) && (rp.data) && (ro < rp.data.length)) {
			rcxData.select(ev.shiftKey ? rcxData.kanjiPos : 0);
			//	tdata.pos = ev;
			tdata.pos = { screenX: ev.screenX, screenY: ev.screenY, pageX: ev.pageX, pageY: ev.pageY,
						  clientX: ev.clientX, clientY: ev.clientY};
			tdata.timer = setTimeout(function() { rcxMain.show(tdata) }, rcxConfig.popdelay);
			return;
		}

		if ((!this.superSticky || this.superStickyOkayToShow) && rcxConfig.title) {
			if ((typeof(ev.target.title) == 'string') && (ev.target.title.length)) {
				tdata.title = ev.target.title;
			}
			else if ((typeof(ev.target.alt) == 'string') && (ev.target.alt.length)) {
				tdata.title = ev.target.alt;
			}
		}

		if (ev.target.nodeName == 'OPTION') {
			tdata.title = ev.target.text;
		}
		else if (ev.target.nodeName == 'SELECT') {
			tdata.title = ev.target.options[ev.target.selectedIndex].text;
		}

		if (tdata.title) {
			//	tdata.pos = ev;
			tdata.pos = { screenX: ev.screenX, screenY: ev.screenY, pageX: ev.pageX, pageY: ev.pageY };
			tdata.timer = setTimeout(function() { rcxMain.showTitle(tdata) }, rcxConfig.popdelay);
			return;
		}

		if ((tdata.pos) && (!this.sticky)) {
			// dont close just because we moved from a valid popup slightly over to a place with nothing
			var dx = tdata.pos.screenX - ev.screenX;
			var dy = tdata.pos.screenY - ev.screenY;
			var distance = Math.sqrt(dx * dx + dy * dy);
			if (distance > 4) {
				this.clearHi();
				this.hidePopup();
			}
		}
		//console.log('_onMouseMove');
	},

	cursorInPopup: function(pos) {
		var doc = document;
		var popup = doc.getElementById('rikaichan-window');
		return (popup && (popup.style.display !== 'none') &&
			(pos.pageX >= popup.offsetLeft) &&
			(pos.pageX <= popup.offsetLeft + popup.offsetWidth) &&
			(pos.pageY >= popup.offsetTop) &&
			(pos.pageY <= popup.offsetTop + popup.offsetHeight));
	},

	_enable: function(b) {
		if ((b != null) && (b.rikaichan == null)) {
			//	alert('enable ' + b.id);
			b.rikaichan = {};
			b.addEventListener('mousemove', this.onMouseMove, false);
			b.addEventListener('mousedown', this.onMouseDown, false);
      b.addEventListener('mouseup', this.onMouseUp, false);
			b.addEventListener('keydown', this.onKeyDown, true);
			b.addEventListener('keyup', this.onKeyUp, true);
			return true;
		}
		return false;
	},

	enable: function(b, mode) {
		//if (!this.initDictionary()) return;
		var ok = this._enable(b, mode);

		if (ok) {
			if (mode == 1) {
				if (rcxConfig.enmode > 0) {
					this.enabled = 1;
					if (rcxConfig.enmode == 2) {
						this.global().rikaichanActive = true;
						this.rcxObs.notifyState('enable');
					}
				}
         // Show the minihelp?
				if(rcxConfig.minihelp)
        {
          // https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode
          var keycode2Key =
          {
            "65"  : "A",        "66"  : "B",        "67"  : "C",         "68"  : "D",        "69"  : "E",         "70"  : "F",        "71"  : "G",         "72"  : "H",        "73"  : "I",   "74" : "J",
            "75"  : "K",        "76"  : "L",        "77"  : "M",         "78"  : "N",        "79"  : "O",         "80"  : "P",        "81"  : "Q",         "82"  : "R",        "83"  : "S",   "84" : "T",
            "85"  : "U",        "86"  : "V",        "87"  : "W",         "88"  : "X",        "89"  : "Y",         "90"  : "Z",        "192" : "` ~",       "48"  : "0",        "173" : "- _", "61" : "= +",
            "219" : "[ {",      "221" : "] }",      "220" : "\ |",       "59"  : ", :",      "222" : "' &quot;",  "188" : ", &lt;",   "190" : ". &gt;",    "191" : "/ ?",
            "112" : "F1",       "113" : "F2",       "114" : "F3",        "115" : "F4",       "116" : "F5",        "117" : "F6",       "118" : "F7",        "119" : "F8",       "120" : "F9",
            "121" : "F10",      "122" : "F11",      "123" : "F12",       "32"  : "SPACE",    "8"   : "BACKSPACE", "45"  : "INSERT",   "46"  : "DELETE",    "36"  : "HOME",
            "35"  : "END",      "33"  : "PAGE UP",  "34"  : "PAGE DOWN", "37"  : "LEFT",     "39"  : "RIGHT",     "38"  : "UP",       "40"  : "DOWN",      "96"  : "NUMPAD 0",
            "97"  : "NUMPAD 1", "98"  : "NUMPAD 2", "99"  : "NUMPAD 3",  "100" : "NUMPAD 4", "101" : "NUMPAD 5",  "102" : "NUMPAD 6", "103" : "NUMPAD 7",
            "104" : "NUMPAD 8", "105" : "NUMPAD 9", "107" : "NUMPAD +",  "109" : "NUMPAD -", "111" : "NUMPAD /",  "106" : "NUMPAD *", "110" : "NUMPAD ."
          };

          var minihelpText = rcxFile.read('chrome://rikaichan/locale/minihelp.htm');

          minihelpText = minihelpText.replace(/@AlternatePopupLocation/   , keycode2Key[rcxConfig.kbalternateview]);
          minihelpText = minihelpText.replace(/@StickyPopupBehavior/      , keycode2Key[rcxConfig.kbstickypopup]);
          minihelpText = minihelpText.replace(/@MovePopupLocationDown/    , keycode2Key[rcxConfig.kbmovepopupdown]);
          minihelpText = minihelpText.replace(/@CopyToClipboard/          , keycode2Key[rcxConfig.kbcopytoclipboard]);
          minihelpText = minihelpText.replace(/@SaveToFile/               , keycode2Key[rcxConfig.kbsavetofile]);
          minihelpText = minihelpText.replace(/@SaveToFileKana/           , keycode2Key[rcxConfig.kbsavetofilekana]);
          minihelpText = minihelpText.replace(/@HideShowDefinitions/      , keycode2Key[rcxConfig.kbhideshowdefinitions]);
          minihelpText = minihelpText.replace(/@PreviousCharacter/        , keycode2Key[rcxConfig.kbpreviouscharacter]);
          minihelpText = minihelpText.replace(/@NextCharacter/            , keycode2Key[rcxConfig.kbnextcharacter]);
          minihelpText = minihelpText.replace(/@NextWord/                 , keycode2Key[rcxConfig.kbnextword]);
          minihelpText = minihelpText.replace(/@JDICAudio/                , keycode2Key[rcxConfig.kbjdicaudio]);
          minihelpText = minihelpText.replace(/@SanseidoMode/             , keycode2Key[rcxConfig.kbsanseidomode]);
          minihelpText = minihelpText.replace(/@EPWINGMode/               , keycode2Key[rcxConfig.kbepwingmode]);
          minihelpText = minihelpText.replace(/@AnkiRealTimeImport/       , keycode2Key[rcxConfig.kbrealtimeimport]);
          minihelpText = minihelpText.replace(/@AnkiRealTimeImportKana/   , keycode2Key[rcxConfig.kbrealtimeimportkana]);
          minihelpText = minihelpText.replace(/@SuperStickyMode/          , keycode2Key[rcxConfig.kbsuperstickymode]);
          minihelpText = minihelpText.replace(/@EditNotes/                , keycode2Key[rcxConfig.kbeditnotes]);
          minihelpText = minihelpText.replace(/@NextEPWINGDictionary/     , keycode2Key[rcxConfig.kbepwingnextdic]);
          minihelpText = minihelpText.replace(/@PreviousEPWINGDictionary/ , keycode2Key[rcxConfig.kbepwingprevdic]);
          minihelpText = minihelpText.replace(/@NextEPWINGEntry/          , keycode2Key[rcxConfig.kbepwingnextentry]);
          minihelpText = minihelpText.replace(/@PreviousEPWINGEntry/      , keycode2Key[rcxConfig.kbepwingpreventry]);

          this.showPopup(minihelpText);
        }
        else
        {
					this.showPopup('Rikaichan Enabled');
        }
			}
		}
	},

  _disable: function(b) {
		if (b != null) {
			//	alert('disable ' + b.id);
			b.removeEventListener('mousemove', this.onMouseMove, false);
			b.removeEventListener('mousedown', this.onMouseDown, false);
      b.removeEventListener('mouseup', this.onMouseUp, false);
			b.removeEventListener('keydown', this.onKeyDown, true);
			b.removeEventListener('keyup', this.onKeyUp, true);

			var e = b.contentDocument.getElementById('rikaichan-css');
			if (e) e.parentNode.removeChild(e);

			e = b.contentDocument.getElementById('rikaichan-window');
			if (e) e.parentNode.removeChild(e);

			delete b.rikaichan;
			return true;
		}
		return false;
	},

	disable: function(b, mode) {
		this._disable(b);
		if (this.enabled) {
			this.enabled = 0;
/*
			for (var i = 0; i < gBrowser.browsers.length; ++i) {
				this._disable(gBrowser.browsers[i], 0);
			}
*/
			if ((rcxConfig.enmode == 2) && (mode == 1)) {
				this.global().rikaichanActive = false;
				this.rcxObs.notifyState('disable');
			}
		}

		rcxData.done();
	},

	toggle: function() {
		var b = this.getBrowser();
		if (b.rikaichan) this.disable(b, 1);
			else this.enable(b, 1);
		this.onTabSelect();
	},

	getSelected: function(win) {
		var text;
		var s = win.getSelection()
		if (s) {
			text = s.toString();
			if (text.search(/[^\s]/) != -1) return text;
		}
		for (var i = 0; i < win.frames.length; ++i) {
			text = this.getSelected(win.frames[i]);
			if (text.length > 0) return text;
		}
		return '';
	},

	clearSelected: function(win) {
		var s = win.getSelection();
		if (s) s.removeAllRanges();
		for (var i = 0; i < win.frames.length; ++i) {
			this.clearSelected(win.frames[i]);
		}
	},


	lbHide: function() {
		document.getElementById('rikaichan-lbar').hidden = true;
		this.hidePopup();
		rcxData.done();
		this.lbText.value = '';
	},

	lbToggle: function() {
		let text = rcxConfig.selinlb ? this.getSelected(window.content).substr(0, 30) : '';
		this.lbText = document.getElementById('rcx-lookupbar-text');

		let e = document.getElementById('rikaichan-lbar');
		if (e.hidden) {
			// FF only
			if ((rcxConfig._bottomlb == true) != rcxConfig.bottomlb) {
				rcxConfig._bottomlb = rcxConfig.bottomlb;

				if (rcxConfig.bottomlb) {
					let bottom = document.getElementById('browser-bottombox');
					if ((bottom) && (e.parentNode != bottom)) {
						e.parentNode.removeChild(e);
						e.setAttribute('ordinal', 0);
						bottom.insertBefore(e, bottom.firstChild);
					}
				}
				else {
					let top = document.getElementById('navigator-toolbox');
					if ((top) && (e.parentNode != top)) {
						e.parentNode.removeChild(e);
						e.setAttribute('ordinal', 1000);
						top.appendChild(e);
					}
				}
			}

			e.hidden = false;
			this.lbText.focus();
		}
		else if (!this.lbText.getAttribute("focused")) {
			this.lbText.focus();
		}
		else if ((text.length == 0) || (text == this.lbLast)) {
			this.lbHide();
			return;
		}

		this.lbSearchButton();
	},

	lbKeyPress: function(ev) {
		switch (ev.keyCode) {
		case 13:
			this.lookupSearch(this.lbText.value);
			ev.stopPropagation();
			break;
		case 27:
			if (this.isVisible()) this.hidePopup();
				else this.lbToggle();
			ev.stopPropagation();
			break;
		}
	},

	lbSearchButton: function() {
		if (rcxConfig.selinlb) {
			let text = this.getSelected(window.content).substr(0, 30);
			if (text.length) {
				this.lbText.value = text;
				this.clearSelected(window.content);
			}
		}

		this.lookupSearch(this.lbText.value);

		this.lbText.select();
		this.lbText.focus();
	},


  // Perform lookup bar search
	lookupSearch: function(text) {
		let s = text.replace(/^\s+|\s+$/g, '');
		if (!s.length) return;

		if ((this.lbLast == s) && (this.isVisible())) {
			rcxData.selectNext();
		}
		else {
			this.lbLast = s;
			rcxData.select(0);
		}

		if ((s.length == 0) || (!this.initDictionary())) {
			this.hidePopup();
		}
		else {
			let result;
			let html;
			if ((s.search(/^:/) != -1) || (s.search(/^([^\u3000-\uFFFF]+)$/) != -1)) {
				// ":word"  = force a text search of "word"
				result = rcxData.textSearch(s.replace(/^:/, ''));
			}
			else {
				result = rcxData.wordSearch(s, true);
			}
			if (result) {
				html = rcxData.makeHtml(result);
				this.lastFound = [result];
			}
			else {
				html = '\u300C ' + s + ' \u300D was not found.';
				this.lastFound = [];
			}
			this.lastFound.fromLB = 1;

			let kanji = '';
			let have = {};
			let t = s + html;
			for (let i = 0; i < t.length; ++i) {
				let c = t.charCodeAt(i);
				if ((c >= 0x3000) && (c <= 0xFFFF)) {
					c = t.charAt(i);
					if (!have[c]) {
						result = rcxData.kanjiSearch(c);
						if (result) {
							this.lastFound.push(result);
							have[c] = 1;
							kanji += '<td class="q-k">' + rcxData.makeHtml(result) + '</td>';
						}
					}
				}
			}

			this.showPopup('<table class="q-tb"><tr><td class="q-w">' + this.getKnownWordIndicatorText()
        + html + '</td>' + kanji + '</tr></table>', null, null, true);
		}
	},

	lookupBoxKey: function(ev) {
		switch (ev.keyCode) {
		case 13:
			this.lookupSearch(ev.target.value);
			ev.stopPropagation();
			break;
		case 27:
			if (this.isVisible()) this.hidePopup();
			ev.target.value = "";
			ev.stopPropagation();
			break;
		}
	},

	statusClick: function(ev) {
		if (ev.button != 2) rcxMain.toggle();
	},

	statusTimer: null,

	status: function(text) {
		if (this.statusTimer) {
			clearTimeout(this.statusTimer);
			this.statusTimer = null;
		}
		var e = document.getElementById('rikaichan-status-text');
		if (e) {
			e.setAttribute('label', text.substr(0, 80));
			e.setAttribute('hidden', 'false');
			this.statusTimer = setTimeout(function() { e.setAttribute('hidden', 'true') }, 3000);
		}
	}
};

/*
var rcxLookupBar = {
};
*/

var rcxConfig = {
	observer: {
		observe: function(subject, topic, data) {
			// console.log('rcxConfig.observer: topic=' + topic);
			rcxConfig.load();
		},
		start: function() {
		//	this.branch = Components.classes['@mozilla.org/preferences-service;1']
		//		.getService(Components.interfaces.nsIPrefService)
		//		.getBranch('extensions.rikaisama.');
		//	this.branch.addObserver('', this, false);
		},
		stop: function() {
		//	this.branch.removeObserver('', this);
		}
	},

	load: function() {
		let p = new rcxPrefs();

		// fix 1.xx -> 2.xx
		try {
			if (p.branch.getPrefType('wpos') != p.branch.PREF_BOOL) {
				p.branch.clearUserPref('wpos');
			}
		}
		catch (ex) {
		}

		for (let i = rcxConfigList.length - 1; i >= 0; --i) {
			let [type, name] = rcxConfigList[i];
			switch (type) {
			case 0:
				rcxConfig[name] = p.getInt(name, null);
				break;
			case 1:
				rcxConfig[name] = p.getString(name, '');
				break;
			case 2:
				rcxConfig[name] = p.getBool(name, null);
				break;
			}
		}

		['cm', 'tm'].forEach(function(name) {
			let a = !rcxConfig[name + 'toggle'];
			let e = document.getElementById('rikaichan-toggle-' + name);
			if (e) e.hidden = a;

			let b = !rcxConfig[name + 'lbar'];
			e = document.getElementById('rikaichan-lbar-' + name);
			if (e) e.hidden = b;

			e = document.getElementById('rikaichan-separator-' + name);
			if (e) e.hidden = a || b;
		}, this);

		rcxConfig.css = (rcxConfig.css.indexOf('/') == -1) ? ('popup-' + rcxConfig.css + '.css') : rcxConfig.css;
		//rcxConfig.css = '';
	/*	 {
			for (let i = gBrowser.browsers.length - 1; i >= 0; --i) {
				let e = gBrowser.browsers[i].contentDocument.getElementById('rikaichan-css');
				if (e) e.setAttribute('href', rcxConfig.css);
			}
		}*/

		let e = document.getElementById('rikaichan-status');
		if (e) e.hidden = (rcxConfig.sticon == 0);

		if ((rcxConfig._bottomlb == true) != rcxConfig.bottomlb) {
			// switch it later, not at every change/startup
			e = document.getElementById('rikaichan-lbar');
			if (e) e.hidden = true;
		}

		rcxData.loadConfig();

    rcxMain.populateEpwingDics();
	}
};

rcxMain.init();
