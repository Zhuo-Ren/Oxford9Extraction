function getElementByAttr(t,e,i){for(var n=document.getElementsByTagName(t),d=[],r=0;r<n.length;r++)n[r].getAttribute(e)==i&&d.push(n[r]);return d}function expand_big(t){var e=getElementByAttr("div","idd",t.getAttribute("idd"));e[0].setAttribute("style","display:none"),e[1].setAttribute("style","display:block")}function expand_thumb(t){var e=getElementByAttr("div","idd",t.getAttribute("idd"));e[1].setAttribute("style","display:none"),e[0].setAttribute("style","display:block")}