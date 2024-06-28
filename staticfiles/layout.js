const themeToggleBtn = document.getElementById("themeToggleBtn");
const html = document.querySelector('html');

function toggleTheme() {
    console.log(html.classList.contains('dark'));
    if(html.classList.contains('dark')){
        html.classList.remove('dark')
        themeToggleBtn.innerText = "Dark Mode";
    }else {
        html.classList.add('dark')
        themeToggleBtn.innerText = "Light Mode";
    }
}