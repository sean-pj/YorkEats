
let dict_filters = {}

all_filters = []


document.addEventListener('DOMContentLoaded', () => {

    // Learned dispatchEvent from https://bito.ai/resources/javascript-trigger-change-event-javascript-explained/
    // Create event
    const changeEvent = new Event('change');

    //Updates which navbar link is highlighted
    if (view.innerHTML === "\"open\"") {
        document.querySelector("#open-nav").classList.add("active")
    } else if ((view.innerHTML === "\"all\"")) {
        document.querySelector("#all-nav").classList.add("active")
    } else if ((view.innerHTML === "\"later\"")) {
        document.querySelector("#later-nav").classList.add("active")
    }

    //Show/hide edit_btn
    document.querySelectorAll("#edit-btn").forEach(edit_btn => {
        edit_btn.addEventListener('click', () => {
            if (edit_btn.nextElementSibling.style.display == "none") {
                edit_btn.nextElementSibling.style.display = "inline";
            } else {
                edit_btn.nextElementSibling.style.display = "none";
            }
        })
    })

    //Edit form behavior
    //Saves uploaded image to place model
    //Code for image uploading is adapted from my CS50 Project 4 JS
    //Which was learned from https://www.youtube.com/watch?v=O5YkEFLXcRg
    document.querySelectorAll("#edit-form").forEach(form => {
            form.querySelector("#save-btn").addEventListener('click', () => {

            // Learned to upload image files through JS from both the following links
            //https://stackoverflow.com/questions/36067767/how-do-i-upload-a-file-with-the-js-fetch-api
            //https://stackoverflow.com/questions/69120374/how-can-i-upload-file-and-also-include-json-data-with-fetch-api

            var formData = new FormData();

            if (form.querySelector("#image").files[0] != null) {
                //Hide form
                form.querySelector("#save-btn").parentNode.style.display = "none";

                //Learned CSRF from https://docs.djangoproject.com/en/5.1/howto/csrf/
                //Generate CSRF token for POST request
                const csrftoken = Cookies.get('csrftoken');

                //Save image and place id to formdata
                formData.append('image', form.querySelector("#image").files[0])
                formData.append('id', form.querySelector("#place-id").innerHTML)

                //Send form data to Django view to update place model
                fetch('edit', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    }, 
                    body: formData
                })
                .then(response => response.json())
                .then(result => {
                    // Print result
                    console.log(result)
                });

                //Learned to update JS image from https://stackoverflow.com/questions/40809635/js-function-to-change-image-on-page-with-file-upload
                //Updates page with uploaded image
                var URL = window.URL
                var url = URL.createObjectURL(form.querySelector("#image").files[0])
                form.parentNode.parentNode.querySelector("img").src = url

            } else {
                alert("Please upload an image.")
            }
        })
    })

    //User rating input actions
    //Updates Rating models based on user's input
    document.querySelectorAll("#user-rating").forEach(form => {

        form.querySelectorAll("input").forEach(input => {
            input.addEventListener('click', () => {

                var formData = new FormData();

                //Learned CSRF from https://docs.djangoproject.com/en/5.1/howto/csrf/
                //CSRF token for POST
                const csrftoken = Cookies.get('csrftoken');

                //Save number of stars selected and ID of place
                formData.append('stars', input.value)
                formData.append('id', form.querySelector("#id").innerHTML)

                //Send form data to Django view to update place model
                fetch('rating', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    }, 
                    body: formData
                })
                .then(response => response.json())
                .then(result => {
                    // Print result
                    console.log(result)

                    //Updates average rating and input html
                    if (result["stars"] != null) {
                        form.parentNode.querySelector(`input[value=\"${Math.round(result["stars"])}\"]`).checked = true
                        form.parentNode.querySelector("#avg_rating").innerHTML = result["stars"]
                    } else {
                        input.checked = false;
                        alert(result["error"])
                    }
                });
                
            })
        })
    })

    //Assign each filter category an array in a dictionary
    document.querySelector("#form-grid").querySelectorAll("#filter-name").forEach(filter_name => {
        dict_filters[filter_name.innerHTML] = []
    })

    //Clear filter button
    document.querySelector("#clear-filters").addEventListener('click', () => {
        document.querySelectorAll(".form-check").forEach(form => {
            form.querySelector("input").checked = false;

            // Trigger checkbox change event
            form.querySelector("input").dispatchEvent(changeEvent)
        })
    })

    //Search bar
    document.querySelector("#search-bar").addEventListener('focusout', () => {
        //Check if search bar is empty
        if (document.querySelector("#search-bar").value == "") {
            //Remove posts that don't match the search
            document.querySelectorAll("#place-name").forEach(name => {
            if (name.innerHTML.includes(document.querySelector("#search-bar").value)) {
                name.parentNode.parentNode.parentNode.parentNode.style.display = 'block';
            } else {
                name.parentNode.parentNode.parentNode.parentNode.style.display = 'none';
            }
            })
        } else {
            //Unhide all places
            document.querySelectorAll("#place-name").forEach(name => {
                    name.parentNode.parentNode.parentNode.parentNode.style.display = 'none';
            })
        }

        //Hide cards based on checkbox filters
        //Removes the places that don't match any filter.
        update_cards_or()
        //Remove the places that don't match all the filters from each column.
        update_cards_and()
    })
    
    //Checkbox behavior
    document.querySelectorAll(".form-check").forEach(form => {
        let checkbox = form.querySelector("input")
        let filter_name = form.parentNode.querySelector("#filter-name")

        //Uncheck checkbox's on page load
        checkbox.checked = false;

        //Checkbox click behavior
        checkbox.addEventListener('change', () => {

            //Updates store filters
            if (checkbox.checked) {
                dict_filters[filter_name.innerHTML].push(checkbox.id)
                all_filters.push(checkbox.id)
            } else {
                dict_filters[filter_name.innerHTML].splice( dict_filters[filter_name.innerHTML].indexOf(checkbox.id), 1)
                all_filters.splice(all_filters.indexOf(checkbox), 1)
            }

            //If there are no filters display every place, otherwise hide them all and only show the places that match the filters.
            if (all_filters.length == 0) {
                document.querySelectorAll("#card-col").forEach(col => {
                    col.style.display = "block"
                })
            } else {
                document.querySelectorAll("#card-col").forEach(col => {
                    col.style.display = "none"
                })
                //Removes the places that don't match any filter.
                update_cards_or()
                //Remove the places that don't match all the filters from each column.
                update_cards_and()
            }

            //Animate each place
            let delay = 0;
            document.querySelectorAll("#card-col").forEach(card => {
                if (card.style.display == 'block') {
                    // https://stackoverflow.com/questions/6268508/restart-animation-in-css3-any-better-way-than-removing-the-element
                    //Remove animation
                    card.style.animation = "none";
                    //Force reflow
                    card.offsetHeight;
                    //Restores animation from CSS
                    card.style.animation = "";
                    //Replay animation
                    card.style.animationPlayState = 'running';
                    //delay is used so each subsequent place is slightly more delayed. This is so every place executes the animation one after other.
                    card.style.animationDelay = delay.toString().concat('s');
                    delay += 0.1;
                }
            })

        })
    })

    //Animate each place
    let delay = 0;
    document.querySelectorAll("#card-col").forEach(card => {
        //delay is used so each subsequent place is slightly more delayed. This is so every place executes the animation one after other.
        card.style.animationDelay = delay.toString().concat('s');
        delay += 0.1;
        card.style.animationPlayState = 'running';
    })
    
})

//If the user scrolls beyond, instantly play the animation
window.onscroll = () => {
    if (window.scrollY > 4000) {
        document.querySelectorAll("#card-col").forEach(card => {
            //delay is used so each subsequent place is slightly more delayed. This is so every place executes the animation one after other.
            card.style.animationDelay = '0s'
            card.style.animationPlayState = 'running';
        })
    }
}

//Filter checkbox behavior. 
//This function gets the places that matches the filters, but only one filter needs to be match. 
//Meaning if one filter matched a place, but another selected filter didn't, the place would still be selected.
//This is specifically for filters in the same column/category. So that you can for example see north american or italian restaurants.
function update_cards_or() {
    //Removes the places that don't match any filter.
    for (const key in dict_filters) {
        dict_filters[key].forEach(filter =>{
            document.querySelectorAll("#card-body").forEach(body => {
                body.querySelectorAll("#filter").forEach(card_text => {
                    if(filter == card_text.innerHTML || card_text.innerHTML.includes(filter)) {
                        body.parentNode.parentNode.style.display = "block";
                    }
                })
            })
        })
     }
}

//Filter checkbox behavior. 
//This function gets the places that matches the filters, but all filters in different categories must match in order for the place be selected.
//This is specifically done for filters in different columns. So that you can for example look for italian restaurants in two separate locations.
function update_cards_and() {
    document.querySelectorAll("#card-col").forEach(col => {
        //Selects places that haven't already been removed
        if (col.style.display == "block") {
            correct_filters = 0
            col.querySelector(".card").querySelector("#card-body").querySelectorAll("#filter").forEach(attribute => {
                //For every category of a place, if that category matches a currently selected filter, then add one to correct filters.  
                if (dict_filters[attribute.getAttribute("alt")].length > 0) {
                    dict_filters[attribute.getAttribute("alt")].forEach(filter => {
                        if (filter == attribute.innerHTML || attribute.innerHTML.includes(filter)) {
                            correct_filters++;
                        }
                    })

                } else {
                    //This is for the case that that no filter is selected for a category, in which case it should be interpreted the same way as a filter matching.
                    correct_filters++;
                }
            })
            //If the number of correct filters is less than the amount of identifying categories, than the place is removed.
            //This means that if every category doesn't either match a selected filter or doesn't have a selected filter, then it should be removed.
            if (correct_filters < Object.keys(dict_filters).length) {
                col.style.display = "none";
            }
        }
    })
}