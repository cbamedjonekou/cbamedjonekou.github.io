function closeNav() {
  document.getElementById("whole-sidebar-nav").style.width = "0";
  document.getElementById("main-content").style.marginLeft= "0";
  document.getElementById("footer-content").style.marginLeft= "0";
  document.getElementById("header-dnstsu").style.marginLeft= "0";
  document.body.style.backgroundColor = "black";
}

function openNav() {
  document.getElementById("whole-sidebar-nav").style.width = "300px";
  document.getElementById("main-content").style.marginLeft = "300px";
  document.getElementById("footer-content").style.marginLeft = "300px";
  document.getElementById("header-dnstsu").style.marginLeft = "300px";
  document.body.style.backgroundColor = "rgba(0,0,0,0.9)";
}