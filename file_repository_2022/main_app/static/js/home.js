// HOME PAGE JS

var lstContainer = document.getElementById("myLIST");


var btnList = lstContainer.getElementsByClassName("li");


for (var i = 0; i < btnList.length; i++) {
  btnList[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}

function userClick(){
  document.getElementById('user-type').value = "User";
  console.log(document.getElementById('user-type').value);
}
function adminClick(){
  document.getElementById('user-type').value = "Admin";
  console.log(document.getElementById('user-type').value);
}