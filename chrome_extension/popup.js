function listProperties(obj) {
   var propList = "";
   for(var propName in obj) {
      if(typeof(obj[propName]) != "undefined") {
         propList += (propName + ", ");
      }
   }
   alert(propList);
}

function processResponce(res) {
  try {
    alert( 'popup.js: XPath evaluation: ' + res);
    //listProperties(domContent);
    //alert('I received the following DOM content:\n' + domContent.constructor.name);
    //var paragraphCount = domContent.evaluate( 'count(//div)', domContent, null, XPathResult.ANY_TYPE, null );

    //alert( 'This document contains ' + paragraphCount.numberValue + ' paragraph elements' );
  }
  catch (exc) {
    alert('popup.js exception: ' + exc);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var checkPageButton = document.getElementById('btnExtractKml');
  checkPageButton.addEventListener('click', function() {
    //xpath = document.getElementById('textXPath');
    //alert('test2 '+xpath.value);

    chrome.tabs.getSelected(null, function(tab) {
    //chrome.tabs.query(null, function(tabs) {
      //xpath = document.getElementById('textXPath').value;
      //outFile = document.getElementById('inputOutFile').value;
      //alert('Saving from ' + tab.url + ' to ' + outFile + ' according to ' + xpath);
      chrome.tabs.sendMessage(tab.id, {text: 'msg_KMLGenerator', xpath: document.getElementById('textXPath').value}, processResponce);

    });
  }, false);
}, false);
