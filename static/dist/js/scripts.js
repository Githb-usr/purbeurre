/*!
* Start Bootstrap - Creative v7.0.2 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Activate SimpleLightbox plugin for portfolio items
    new SimpleLightbox({
        elements: '#portfolio a.portfolio-box'
    });

});

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

// AJAX for delete a user favourite
function deleteSubstitute(id) {
    const myHeaders = new Headers();
    myHeaders.append("X-CSRFToken", getCookie('csrftoken'));
    myHeaders.append("Content-Type", "application/json");
    const request = new Request('/user/delete_substitutes/', {
        method: 'POST',
        headers: myHeaders,
        body: {substituteId: id}
    }) 

    fetch('/user/delete_substitutes/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({substituteId: id})
    })
    .then((response) => {
        const statusCode = response.status;
        if (statusCode === 204) {
            console.log("Good")
            location.reload();
            
        } else if (statusCode === 301) {
            // Do nothing
            console.log("301")
        } else if (statusCode === 404) {
            console.log("404")
            alert("Le produit n'a pas pu être supprimé !")
        }
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

$(document).ready(function() { 
    $( ".btn-delete" ).click(function() {
        const substituteId = $(this).attr('id');
        deleteSubstitute(substituteId)
    });

    $(".delete-form").submit(function(e){
        e.preventDefault();
    });
});

// We prevent the forms from being resubmitted when the page is refresh
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}
