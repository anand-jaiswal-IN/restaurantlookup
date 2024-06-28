const sendOtpBtn = document.getElementById("sendOtpBtn");
const otpForm = document.getElementById("otpForm");

sendOtpBtn.addEventListener("click", function (e) {
  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/accounts/generate_email_otp/");
  xhttp.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
  xhttp.send();

  xhttp.onreadystatechange = function () {
    if (xhttp.readyState == XMLHttpRequest.DONE) {
      if (xhttp.status === 200) {
        console.log("Success:", xhttp.responseText);
      } else {
        console.error("Error:", xhttp.status, xhttp.statusText);
      }
    }
  };
  otpForm.classList.remove("hidden");
});
