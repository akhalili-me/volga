// Grab elements
const selectElement = selector => {
    const element = document.querySelector(selector)
    if(element) return element;
    throw new Error(`something went wrong, make sure ${selector} exists.` )
}

//Nav styles on scroll
// TO DO: write it with toggle
const scrollHeader = () => {
    const headerElement = selectElement('#header')
    if (this.scrollY >= 15) {
        headerElement.classList.add('activated')
    }else{
        headerElement.classList.remove('activated')
    }
}
window.addEventListener('scroll',scrollHeader)

// Open menu & search pop-up
const menuToggleIcon = selectElement('#menu-toggle-icon')
const toggleMenu = () => {
    const mobileMenu = selectElement('#menu')
    mobileMenu.classList.toggle('activated')
    menuToggleIcon.classList.toggle('activated')
}
menuToggleIcon.addEventListener('click',toggleMenu)

// Open/Close search form popup
const openSearchForm = selectElement('#search-btn')
const closeSearchForm = selectElement('#form-close-btn')
const searchForm = selectElement('#search-form-container')
toggleSearchForm = () => {
    searchForm.classList.toggle('activated')
}
searchButtons = [openSearchForm,closeSearchForm]
searchButtons.forEach(element => {
    element.addEventListener('click',toggleSearchForm)
});

// -- Close the search form popup on ESC keypress
window.addEventListener('keyup',(element) => {
    if (element.key === 'Escape') {
        searchForm.classList.remove('activated')
    }
})
// Switch theme/add to local storage

// Swiper
const swiper = new Swiper('.swiper',{
    slidesPerView:1,
    spaceBetween: 20,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    loop: true,
    breakpoints:{
        700:{
            slidesPerView:2
        },
        1200:{
            slidesPerView:3
        }
    }
})

//Comments
$("#comment_form").submit(function(e){
    e.preventDefault();
    var serializedData = $(this).serialize();

    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            // 1. clear the form.
            $("#comment_form").trigger('reset');
            // display the newly friend to table.
            var instance = JSON.parse(response["instance"]);
            var fields = instance[0]["fields"];
            var user = JSON.parse(document.getElementById('user').textContent);
            $("#user_comments").prepend(
                `<div class="comment" >
                    <p>
                        <h3>${user}</h3>
                        ${fields["content"]}
                    </p>
                </div>`
            );
            $("#comment_text").hide();
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    })
})