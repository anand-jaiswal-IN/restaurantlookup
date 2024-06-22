const deleteBtn = document.getElementById("deleteBtn");
const deletePopupText = document.getElementById("deletePopupText");

let URLForDeletion = null;
let DataToBeSend = null;
let clickedBtn = null;

function deletePopupOpen(btn) {
  /* this - contains 
    data-deleteType = ("restaurant_image", "dish", "restaurant")
    data-deleteId = id or pk of deleting data
    data-popupText  = text on delete popup
    */
  // console.log(btn.getAttribute());

  clickedBtn = btn

  deletePopupText.innerHTML = btn.getAttribute("data-popupText");

  if (btn.getAttribute("data-deleteType") == "restaurant") {
    URLForDeletion = "/delete_restaurant/";
    DataToBeSend = {
      pk: btn.getAttribute("data-deleteId"),
    };
  } else if (btn.getAttribute("data-deleteType") == "dish") {
    URLForDeletion = "/delete_restaurant_dish/";
    DataToBeSend = {
      pk: btn.getAttribute("data-deleteId"),
      restaurantId: btn.getAttribute("data-restaurantId"),
    };
  } else if (btn.getAttribute("data-deleteType") == "restaurant_image") {
    URLForDeletion = "/delete_restaurant_image/";
    DataToBeSend = {
      pk: btn.getAttribute("data-deleteId"),
      restaurantId: btn.getAttribute("data-restaurantId"),
    };
  }
}

function deleteData(){
  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", URLForDeletion, true);
  xhttp.setRequestHeader("X-CSRFToken", deleteBtn.getAttribute("data-csrf"));

  xhttp.send(JSON.stringify(DataToBeSend));

  xhttp.onreadystatechange = function () {
    if (xhttp.readyState == XMLHttpRequest.DONE) {
      if (xhttp.status === 200) {
        console.log("Response Text", JSON.parse(xhttp.responseText));
        if (clickedBtn.getAttribute("data-deleteType") == "restaurant") window.location.href = "/accounts/profile";
        else window.location.reload();
      } else {
        console.error("Error:", xhttp.status, JSON.parse(xhttp.statusText));
      }
    }
  };
}
function removeDataCollected(){
  URLForDeletion = null;
  DataToBeSend = null;
  clickedBtn = null;
}