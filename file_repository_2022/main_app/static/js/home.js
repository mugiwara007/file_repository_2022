// HOME PAGE JS

var lstContainer = document.getElementById("myLIST");


var btnList = lstContainer.getElementsByClassName("li");


for (var i = 0; i < btnList.length; i++) {
  btnList[i].addEventListener("click", function () {
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}
function sweetalert() {
  Swal.fire({
    title: 'Are you sure?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, Put this file in Archive'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire(
        'Archived',
        'Your file has been sent to Archive.',
        'success'
      )
    }
  })
}
function loginalert() {
  Swal.fire({
    icon: 'error',
    title: 'Oops...',
    text: 'Ivalid Username or password'
  })
}

function deleteaccountalert() {
  Swal.fire({
    title: 'Are you sure?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, Delete my Account'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire(
        'Deleted',
        'Your Account has been Deleted',
        'success'
      )
    }
  })
}
function deleteuser() {
  Swal.fire({
    title: 'Are you sure you want to remove this User?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Delete this User'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire(
        'Archived',
        'This user has been sent to Archive',
        'success'
      )
    }
  })
}
function deletefilepermanently() {
  Swal.fire({
    title: 'Do you want to Delete this file permenantly?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Delete File Permanently'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire(
        'Deleted',
        'This File has been Deleted Permanently',
        'success'
      )
    }
  })
}

function restorefile() {
  Swal.fire({
    title: 'Do you want to Restore this file?',
    showDenyButton: true,
    confirmButtonText: 'Restore',
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      Swal.fire('Restored!', '', 'success')
    } else if (result.isDenied) {
      Swal.fire('File not Restored', '', 'info')
    }
  })
}


function deleteuserpermanently() {
  Swal.fire({
    title: 'Do you want to Delete this User permanently?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Delete User Permanently'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire(
        'Deleted',
        'This User has been Deleted Permanently',
        'success'
      )
    }
  })
}

function userClick() {
  document.getElementById('user-type').value = "User";
  console.log(document.getElementById('user-type').value);
}
function adminClick() {
  document.getElementById('user-type').value = "Admin";
  console.log(document.getElementById('user-type').value);
}

$('#user_search_input').on('keyup', function (e) {
  e.preventDefault();

  $.ajax({
    type: 'get',
    url: "/User/",
    data: {
      search: $('#user_search_input').val()
    },
    success: function (data) {
      $('#table').html(data.rendered_table);
    },
    error: function (data) {
      alert('have an error');
    },
  });
});

$('#admin_search_input').on('keyup', function (e) {
  e.preventDefault();

  $.ajax({
    type: 'get',
    url: "/Admin/",
    data: {
      search: $('#admin_search_input').val()
    },
    success: function (data) {
      $('#table').html(data.rendered_table);
    },
    error: function (data) {
      alert('an error');
    },
  });
});

$('#admin_user_search').on('keyup', function (e) {
  e.preventDefault();

  $.ajax({
    type: 'get',
    url: "/AdminUserTab/",
    data: {
      search: $('#admin_user_search').val()
    },
    success: function (data) {
      $('#table').html(data.rendered_table);
    },
    error: function (data) {
      alert('an error');
    },
  });
});

