function listProperties(obj) {
   var propList = "";
   for(var propName in obj) {
      if(typeof(obj[propName]) != "undefined") {
         propList += (propName + ", ");
      }
   }
   alert(propList);
}


chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    if (msg.text === 'msg_KMLGenerator') {
        try {
            var result = document.evaluate(msg.xpath, document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
            if (result.resultType == 5) {
                //alert('content.js: XPath evaluation: ' + res.resultType);
                res = '';
                node = result.iterateNext();
                while (node) {
                    //alert('content.js: node: ' + node.textContent);
                    res = res + ';\n ' + node.textContent;
                    node = result.iterateNext();
                }
                sendResponse(res);
            }
            else {
                alert('content.js: unexpected XPath result ' + result.resultType);
            }
        }
        catch (exc) {
            alert('content.js exception: ' + exc);
        }
    }
});


/*

//*[@id="river"]/article/pre/code/text()

*/
