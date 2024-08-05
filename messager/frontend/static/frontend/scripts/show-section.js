function removeShowClass() {
    let sections = document.querySelectorAll('section');
    sections.forEach(element => {
        element.classList.remove("section--show")
    });
}

let user_badge = document.querySelector("#user-badge");
let profile_section = document.querySelector("#profile-section");

user_badge.addEventListener("click", function() {
    removeShowClass()
    profile_section.classList.add("section--show")
})


let btn_profile_change = document.querySelector("#profile-change-btn");
let profile_section_change = document.querySelector("#profile-section-change");

btn_profile_change.addEventListener("click", function() {
    removeShowClass()
    profile_section_change.classList.add("section--show")
})


document.addEventListener("change-profile-ok", function() {
    removeShowClass()
    profile_section.classList.add("section--show")
})

let users_link = document.querySelector("#users-link");
let section_users = document.querySelector("#section-users");

users_link.addEventListener("click", function() {
    removeShowClass()
    section_users.classList.add("section--show")
})

