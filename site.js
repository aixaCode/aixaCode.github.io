
(function(){
  var root=document.documentElement;
  var saved=localStorage.getItem("theme");
  if(saved){root.setAttribute("data-theme",saved);}
  else if(window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches){root.setAttribute("data-theme","dark");}
  var theme=document.getElementById("theme");
  if(theme){theme.addEventListener("click",function(){
    var next=root.getAttribute("data-theme")==="dark"?"light":"dark";
    root.setAttribute("data-theme",next);
    localStorage.setItem("theme",next);
  });}
  var yr=document.getElementById("yr");
  if(yr){yr.textContent=new Date().getFullYear();}
})();
