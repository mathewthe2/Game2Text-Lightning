/*

	Rikaichan
	Copyright (C) 2005-2015 Jonathan Zarate
	http://www.polarcloud.com/

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

var rcxOptions = {
	togbar: ['toggle', 'lbar'],
	modifiers: ['accel', 'alt', 'shift'],
	keys: ['(disabled)',
		'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K',
		'L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Back','Escape','Page Up',
		'Page Down','End','Home','Left','Up','Right','Down','Insert','Delete','F1','F2','F3',
		'F4','F5','F6','F7','F8','F9','F10','F11','F12'],
	kindex: ['COMP', 'H','L','E','DK','N','V','Y','P','IN','I','U'],
	importsLoaded: false,
  curEpwingDicPath: "",

	checkRange: function(e, name, min, max) {
		e = document.getElementById(e);
		let v = e.value * 1;
		if ((isNaN(v)) || (v < min) || (v > max)) {
			e.focus();
			alert('Invalid ' + name + ' (' + v + '). Valid range: ' + min + '-' + max);
			return false;
		}
		e.value = parseInt(v);
		return true;
	},

	onLoad: function() {
		if (navigator.userAgent.search(/thunderbird|shredder/i) != -1) {
			document.getElementById('rcp-enmode-box').hidden = true;
		}
		else if (navigator.userAgent.search(/firefox/i) != -1) {
			document.getElementById('rcp-bottomlb').hidden = false;
		}

		let pb = new rcxPrefs();

		for (let i = 0; i < this.togbar.length; ++i) {
			let name = this.togbar[i];
			let s = pb.getString(name + '.mod');
			for (let j = 0; j < this.modifiers.length; ++j) {
				let mo = this.modifiers[j];
				document.getElementById('rcp-' + name + '-' + mo).checked = (s.indexOf(mo) != -1);
			}

			let list = document.getElementById('rcp-' + name + '-list');
			for (let j = 0; j < this.keys.length; ++j) {
				let m = document.createElementNS('http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul', 'menuitem');
				m.setAttribute('label', this.keys[j]);
				list.appendChild(m);
			}

			s = pb.getString(name + '.key');
			if (s == '') s = this.keys[0];
			let e = document.getElementById('rcp-' + name + '-key');
			e.value = s;
			this.keyChanged(e);
		}

		let k = pb.getString('kindex').split(',');
		for (let i = 0; i < k.length; ++i) {
			let e = document.getElementById('rcp-kindex-' + k[i]);
			if (e) e.checked = true;
		}

		for (let i = 0; i < rcxConfigList.length; ++i) {
			let cfg = rcxConfigList[i];
			let e = document.getElementById('rcp-' + cfg[1]);
			if (e) {
				switch (cfg[0]) {
				case 0:
					e.value = pb.getInt(cfg[1]);
					break;
				case 1:
					e.value = pb.getString(cfg[1]);
					break;
				case 2:
					e.checked = pb.getBool(cfg[1]);
					break;
				}
			}
		}
		
    //
    // Fill in the dictionary listbox in the Dictionaries tab
    //
		let e = document.getElementById('rcp-priority');
		let s = pb.getString('dpriority').split('|');
		for (let i = 0; i < s.length; ++i) {
			if (s[i].match(/(.+?)#(.+)/)) e.appendItem(RegExp.$2, RegExp.$1);
		}
		
		if ((window.arguments) && (window.arguments.length) && (window.arguments[0] == 'dic')) {
			document.getElementById('rcp-tabbox').selectedIndex = 3;
		}
    
    
    //
    // Fill in the EPWING dictionary listbox in the EPWING tab
    //
    
    let epwingDicListBox = document.getElementById('rcp-epwingpathlistbox');
    let epwingDics = pb.getString('epwingdiclist').split('|');

    for (let i = 0; i < epwingDics.length; ++i) 
    {
      if(epwingDics[i].length > 0)
      {
        if (epwingDics[i].match(/(.+?)\?(.+)/))
        { 
          epwingDicListBox.appendItem("『" + RegExp.$2 + "』 - " + RegExp.$1, 
            RegExp.$1 + "?" + RegExp.$2); // data?label
        }
      }
		}
	},

	onOK: function() {
		// type="number" min="3" max="100" <-- can use, but limited to FX3+, TB?, SM?
    if (!this.checkRange('rcp-opacity', 'Opacity', 60, 100)) return false;
    if (!this.checkRange('rcp-volume', 'Volume', 0, 100)) return false;
		if (!this.checkRange('rcp-wmax', 'Maximum Entries To Display', 3, 100)) return false;
		if (!this.checkRange('rcp-namax', 'Maximum Entries To Display', 3, 100)) return false;
    if (!this.checkRange('rcp-rtiudpport', 'UDP Port', 49152, 65535)) return false;

		let pb = new rcxPrefs();

		for (let i = 0; i < this.togbar.length; ++i) {
			let name = this.togbar[i];
			let m = [];
			for (let j = 0; j < this.modifiers.length; ++j) {
				let mo = this.modifiers[j];
				if (document.getElementById('rcp-' + name + '-' + mo).checked) m.push(mo);
			}
			pb.setString(name + '.mod', m.join(' '));

			let key = document.getElementById('rcp-' + name + '-key').value;
			pb.setString(name + '.key', (key == '(disabled)') ? '' : key);
		}


		let k = [];
		for (let i = 0; i < this.kindex.length; ++i) {
			let c = this.kindex[i];
			if (document.getElementById('rcp-kindex-' + c).checked) k.push(c);
		}
		pb.setString('kindex', k.join(','));

		for (let i = 0; i < rcxConfigList.length; ++i) {
			let cfg = rcxConfigList[i];
			let e = document.getElementById('rcp-' + cfg[1]);
			if (e) {
				switch (cfg[0]) {
				case 0:
					pb.setInt(cfg[1], e.value);
					break;
				case 1:
					pb.setString(cfg[1], e.value);
					break;
				case 2:
					pb.setBool(cfg[1], e.checked);
					break;
				}
			}
		}

    //
    // Save the dictionary priorities in the Dictionary tab to a variable
    //
    
		let buffer = [];
		let e = document.getElementById('rcp-priority');
		for (let i = 0; i < e.itemCount; ++i) {
			let item = e.getItemAtIndex(i);
			buffer.push(item.value + '#' + item.label);
		}
		pb.setString('dpriority', buffer.join('|'));
    
    
    //
    // Save the EPWING dictionaries in the EPWING tab to a variable
    //
    
    let epwingDicBuffer = [];
    let epwingDicListBox = document.getElementById('rcp-epwingpathlistbox');
    
    for (let i = 0; i < epwingDicListBox.itemCount; ++i) 
    {
			let item = epwingDicListBox.getItemAtIndex(i);
			epwingDicBuffer.push(item.value);
		}
    
    pb.setString('epwingdiclist', epwingDicBuffer.join('|'));

		return true;
	},

	keyChanged: function(e) {
		e.value = e.value.replace(/^\s+|\s+$/g, '').replace(/\s+/g, ' ');
		let disable = ((e.value == '') || (e.value == '(disabled)'));
		for (let i = this.modifiers.length - 1; i >= 0; --i) {
			document.getElementById(e.id.replace('key', this.modifiers[i])).disabled = disable;
		}
	},

	browseFile: function(id) {
		const nsIFilePicker = Components.interfaces.nsIFilePicker;
		let fp = Components.classes['@mozilla.org/filepicker;1'].createInstance(nsIFilePicker);

		fp.init(window, 'Browse', nsIFilePicker.modeSave);
		fp.appendFilters(nsIFilePicker.filterAll | nsIFilePicker.filterText);
		fp.defaultString = document.getElementById(id).value;

		let r = fp.show();
		if ((r == nsIFilePicker.returnOK) || (r == nsIFilePicker.returnReplace))
			document.getElementById(id).value = fp.file.path;
	},
  
  chooseFile: function(id) {
		const nsIFilePicker = Components.interfaces.nsIFilePicker;
		let fp = Components.classes['@mozilla.org/filepicker;1'].createInstance(nsIFilePicker);

		fp.init(window, 'Browse', nsIFilePicker.modeOpen);
		fp.appendFilters(nsIFilePicker.filterAll | nsIFilePicker.filterText);
		fp.defaultString = document.getElementById(id).value;

		let r = fp.show();
		if ((r == nsIFilePicker.returnOK) || (r == nsIFilePicker.returnReplace))
			document.getElementById(id).value = fp.file.path;
	},
  
  browseDir: function(id) 
  {
		const nsIFilePicker = Components.interfaces.nsIFilePicker;
		let fp = Components.classes['@mozilla.org/filepicker;1'].createInstance(nsIFilePicker);

		fp.init(window, 'Browse', nsIFilePicker.modeGetFolder);
		fp.appendFilters(nsIFilePicker.filterAll | nsIFilePicker.filterText);
		fp.defaultString = document.getElementById(id).value;

		let r = fp.show();
    
		if ((r == nsIFilePicker.returnOK) || (r == nsIFilePicker.returnReplace))
			document.getElementById(id).value = fp.file.path;
	},
	
  // Change built-in dictionary priority in Dictionary tab
	movePriority: function(dir) {
		let list = document.getElementById('rcp-priority');

		let i = list.selectedIndex;
		if (i == -1) return;

		let j = i + dir;
		if ((j < 0) || (j >= list.itemCount)) return;

		// these are lost from removed item
		let label = list.selectedItem.label;
		let value = list.selectedItem.value;

		list.removeItemAt(i);
		list.insertItemAt(j, label, value);
		list.selectedIndex = j;
	},
	
  // Download built-in dictionary in Dictionary tab
	Download: function() {
		Components.classes['@mozilla.org/observer-service;1']
			.getService(Components.interfaces.nsIObserverService)
			.notifyObservers(null, 'rikaichan', 'getdic');
	},
  
  
  // Change EPWING dictionary priority in EPWING tab.
  moveEpwingPriority: function(amount) 
  {
    let epwingDicListBox = document.getElementById('rcp-epwingpathlistbox');
    
    let selectedIndex = epwingDicListBox.selectedIndex;
    
    if (selectedIndex == -1)
    {
      return;
    }
    
    let newSelectedIndex = selectedIndex + amount;
    
    if ((newSelectedIndex < 0) || (newSelectedIndex >= epwingDicListBox.itemCount)) 
    {
      return;
    }
    
    let itemLabel = epwingDicListBox.selectedItem.label;
    let itemValue = epwingDicListBox.selectedItem.value;
    
    epwingDicListBox.removeItemAt(selectedIndex);
    epwingDicListBox.insertItemAt(newSelectedIndex, itemLabel, itemValue);
    epwingDicListBox.selectedIndex = newSelectedIndex;
  },
  
  
  // Add an EPWING dictionary to the list in the EPWING tab
  addEpwingDictionary: function() 
  {
    let epwingDicListBox = document.getElementById('rcp-epwingpathlistbox');
    
    let selectedIndex = epwingDicListBox.selectedIndex;
    let addIndex = selectedIndex;
    let itemValue = '';
    
    if (selectedIndex >= 0)
    {
      let item = epwingDicListBox.getItemAtIndex(selectedIndex);
	    itemValue = item.value;
    }
        
    const nsIFilePicker = Components.interfaces.nsIFilePicker;
    let fp = Components.classes['@mozilla.org/filepicker;1'].createInstance(nsIFilePicker);
    
    let osString = Components.classes["@mozilla.org/xre/app-info;1"]
          .getService(Components.interfaces.nsIXULRuntime).OS;
    fp.init(window, 'Browse', nsIFilePicker.modeOpen);
    if (osString != 'Darwin') {
      // Don't add filters on OS X - it fails on them.
      fp.appendFilter('EPWING Dictionaries', 'CATALOGS;CATALOG');
    }
    fp.defaultString = itemValue;
    
    let result = fp.show();
    
    if ((result == nsIFilePicker.returnOK) || (result == nsIFilePicker.returnReplace))
    {
      // Load imports needed for the title lookup
      if(!rcxOptions.importsLoaded)
      {
        Components.utils.import("resource://gre/modules/FileUtils.jsm");
        Components.utils.import("resource://gre/modules/NetUtil.jsm");
        
        rcxOptions.importsLoaded = true;
      }
    
      rcxOptions.curEpwingDicPath = fp.file.path;
    
      rcxEpwing.lookupTitle(fp.file.path, rcxOptions.addEpwingDictionaryPart2);
    }
  },
  
  
  addEpwingDictionaryPart2: function(title)
  {
    let epwingDicListBox = document.getElementById('rcp-epwingpathlistbox');
    
    let selectedIndex = epwingDicListBox.selectedIndex;
    let addIndex = selectedIndex;
    
    if(addIndex == -1)
    {
      epwingDicListBox.appendItem("『" + title + "』 - " + rcxOptions.curEpwingDicPath, 
        rcxOptions.curEpwingDicPath + "?" + title);
    }
    else
    {
      epwingDicListBox.insertItemAt(addIndex, "『" + title + "』 - " + rcxOptions.curEpwingDicPath, 
        rcxOptions.curEpwingDicPath + "?" + title);
    }
  },
  
  
  // Remove an EPWING dictionary from the list in the EPWING tab
  removeEpwingDictionary: function() 
  {
    let epwingDicListBox = document.getElementById('rcp-epwingpathlistbox');
    
    let selectedIndex = epwingDicListBox.selectedIndex;
    
    if (selectedIndex == -1)
    {
      return;
    }
    
    epwingDicListBox.removeItemAt(selectedIndex);
  }
  
};
