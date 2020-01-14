function openPage(url, elmnt, color, flag) {
    // Hide all elements with class="tabcontent" by default */
    var i, tabcontent, tablinks;
    //tabcontent = document.getElementsByClassName("tabcontent");
    //for (i = 0; i < tabcontent.length; i++) {
    // tabcontent[i].style.display = "none";
    //}

    // Remove the background color of all tablinks/buttons
    tablinks = document.getElementsByClassName("tabmain");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].style.backgroundColor = "";
    }

    //// Show the specific tab content
    //document.getElementById(cityName).style.display = "block";

    // Add the specific color to the button used to open the tab content
    window.location.href = url
    if (flag === 0) {
        elmnt.style.backgroundColor = color;
        //Redirecting the page
    }
    if (flag === 1) {
        document.getElementById(elmnt).style.backgroundColor = color;
        //Redirecting the page
    }
}

function displayDiv(divID) {
    var req_div = document.getElementById(divID)
    if req_div.style.display === block{
        req_div.style.display === hidden;
    }
    if req_div.style.display === hidden{
        req_div.style.display === block;
    }
}


// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

var TxtType = function(el, toRotate, period) {
 this.toRotate = toRotate;
 this.el = el;
 this.loopNum = 0;
 this.period = parseInt(period, 10) || 2000;
 this.txt = "";
 this.tick();
 this.isDeleting = false;
};

TxtType.prototype.tick = function() {
 var i = this.loopNum % this.toRotate.length;
 var fullTxt = this.toRotate[i];

 if (this.isDeleting) {
  this.txt = fullTxt.substring(0, this.txt.length - 1);
 } else {
  this.txt = fullTxt.substring(0, this.txt.length + 1);
 }

 this.el.innerHTML = '<span class="wrap">' + this.txt + "</span>";

 var that = this;
 var delta = 200 - Math.random() * 100;

 if (this.isDeleting) {
  delta /= 2;
 }

 if (!this.isDeleting && this.txt === fullTxt) {
  delta = this.period;
  this.isDeleting = true;
 } else if (this.isDeleting && this.txt === "") {
  this.isDeleting = false;
  this.loopNum++;
  delta = 500;
 }

 setTimeout(function() {
  that.tick();
 }, delta);
};

window.onload = function() {
 var elements = document.getElementsByClassName("typewrite");
 for (var i = 0; i < elements.length; i++) {
  var toRotate = elements[i].getAttribute("data-type");
  var period = elements[i].getAttribute("data-period");
  if (toRotate) {
   new TxtType(elements[i], JSON.parse(toRotate), period);
  }
 }
 // INJECT CSS
 var css = document.createElement("style");
 css.type = "text/css";
 css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #fff}";
 document.body.appendChild(css);
};

$("body").append(
 '<div style="" id="loadingDiv"><div class="loader">Loading...</div></div>'
);
$(window).on("load", function() {
 setTimeout(removeLoader, 2000); //wait for page load PLUS two seconds.
});
function removeLoader() {
 $("#loadingDiv").fadeOut(500, function() {
  // fadeOut complete. Remove the loading div
  $("#loadingDiv").remove(); //makes page more lightweight
 });
}