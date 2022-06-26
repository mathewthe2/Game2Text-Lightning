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

// 0 = integer, 1 = string, 2 = checkbox/boolean
var rcxConfigList = [
	// general
	[1, 'css'],
	[0, 'enmode'],
	[2, 'highlight'],
	[2, 'title'],
	[2, 'selinlb'],
	[2, 'bottomlb'],
	[2, 'resizedoc'],
	[2, 'sticon'],
	[2, 'minihelp'],
	[0, 'volume'],
	[2, 'autoplayaudio'],
	[2, 'enablenoaudioclip'],
	[0, 'opacity'],
	[2, 'roundedcorners'],
  [2, 'mergedivs'],
    
  // startup
	[2, 'startlookupbar'],
	[2, 'startepwing'],
	[2, 'startsanseido'],
	[2, 'startsticky'],
	[2, 'startsupersticky'],
  
	// menus
	[2, 'tmtoggle'],
	[2, 'tmlbar'],
	[2, 'cmtoggle'],
	[2, 'cmlbar'],

	// keyboard
	[2, 'nopopkeys'],
	[1, 'kbalternateview'],
	[1, 'kbstickypopup'],
	[1, 'kbmovepopupdown'],
	[1, 'kbcopytoclipboard'],
	[1, 'kbsavetofile'],
	[1, 'kbsavetofilekana'],
	[1, 'kbhideshowdefinitions'],
	[1, 'kbpreviouscharacter'],
	[1, 'kbnextcharacter'],
	[1, 'kbnextword'],
	[1, 'kbjdicaudio'],
	[1, 'kbsanseidomode'],
	[1, 'kbepwingmode'],
	[1, 'kbrealtimeimport'],
	[1, 'kbrealtimeimportkana'],
	[1, 'kbsuperstickymode'],
	[1, 'kbeditnotes'],
	[1, 'kbepwingnextdic'],
	[1, 'kbepwingprevdic'],
	[1, 'kbepwingnextentry'],
	[1, 'kbepwingpreventry'],

	// dictionary
	[2, 'wpos'],					// ! this was an integer in 1.xx: 0=hide, 1=show entry type
	[2, 'wpop'],
	[0, 'wmax'],
	[0, 'namax'],
	[2, 'hidex'],
	[2, 'showfreq'],
	[2, 'showpitchaccent'],
	[2, 'hidepitchaccentpos'],
	
	// kanji
	[1, 'kindex'],
  
	// EPWING
	[1, 'epwingdiclist'],           // Format: dic1?dic1_title|dic2?dic2_title|etc...
	[1, 'epwingfallback'],          // none, jmdict, or epwing
	[0, 'epwingmaxlines'],          // Max lines per entry
	[0, 'epwingmaxentries'],        // Max entries to show (when epwingshowallentries is set)
	[2, 'epwingshowconjugation'],   // Show conjugation rule
	[2, 'epwingshowdicnum'],        // Show dic num and title in popup
 	[2, 'epwingshowtitle'],         // Show title next to dic num in popup
	[2, 'epwingshowshorttitle'],    // Show short version of title in popup
	[2, 'epwingstripnewlines'],     // Remove \r and \n from entries
  [2, 'epwingshowallentries'],    // Append all entries from same dictionary into same popup
 	[2, 'epwingappendjmdict'],      // Append EDICT gloss to EPWING results
	[2, 'epwingaddcolorandpitch'],  // Parse entry
  [2, 'epwingforceparse'],        // Force entry to be parsed even if dic is not supported
	[2, 'epwingsearchnextlongest'], // Search for next longest word if longest word not found
 	[1, 'epwingremoveregex'],       // Remove text matching this regex
 	[2, 'epwing_apply_remove_regex_when_saving'], // True = Apply epwingremoveregex when saving EPWING text
 	[2, 'epwingusewine'],           // On Linux, use Wine with the Windows exe instead of using the native exe

	// clipboard / save file
	[1, 'sfile'],
	[1, 'audiodir'],
	[2, 'saveaudioonplay'],
	[1, 'sfcs'],
	[2, 'ubom'],
	[0, 'smaxfe'],
	[0, 'smaxfk'],
	[0, 'smaxce'],
	[0, 'smaxck'],
	[0, 'snlf'],
	[1, 'ssep'],
	[1, 'atags'],
	[1, 'savenotes'],
	[1, 'saveformat'],
  
  // Vocab
	[1, 'vocabknownwordslistfile'],
	[0, 'vocabknownwordslistcolumn'],
  [1, 'vocabtodowordslistfile'],
	[0, 'vocabtodowordslistcolumn'],

  // Anki
  [1, 'rti_save_format'],
	[1, 'rtifieldnamestext'],
	[2, 'rtisaveaudio'],
	[0, 'rtiudpport'],
  
	// not in GUI
	[0, 'popdelay'],
	[2, 'hidedef'],
//	[2, 'sticky']
];



function rcxPrefs() {
	this.branch = null;
}

rcxPrefs.prototype = {
	
	stringVal : {
		'css' : 'resources/rikaisama/popup-blue.css'
	},
	
	getString: function(key) {
		console.log('getString with ' + key);
		val = this.stringVal[key]
		return val == undefined ? '' : val;
	},

	setString: function(key, value) {

	},
	
	intVal : { 'wmax' : 3, 
	           'namax' : 3,
			   'popdelay' : 20,
			   'smaxck' : 10,
			   'smaxce' : 10,
			   'smaxfk' : 10,
			   'smaxfe' : 10,
			   'opacity' : 100,
			   
			 },

	getInt: function(key) {
		console.log('getInt with ' + key);
		return this.intVal[key] != undefined ? this.intVal[key] : 0;
	},

	setInt: function(key, value) {

	},

	boolVal : { 'selinlb' : true, 
	           'bottomlb' : true,
			   'highlight' : true,
			   'roundedcorners': true,
			 },

	getBool: function(key) {
		console.log('getBool with ' + key);
		val = this.boolVal[key]
		return val == undefined ? false : val;		
	},

	setBool: function(key, value) {
	
	}
};
