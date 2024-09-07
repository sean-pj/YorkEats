
let dict_filters = {}

all_filters = []


document.addEventListener('DOMContentLoaded', () => {

    //Show hide edit_btn
    document.querySelectorAll("#edit-btn").forEach(edit_btn => {
        edit_btn.addEventListener('click', () => {
            if (edit_btn.nextElementSibling.style.display == "none") {
                edit_btn.nextElementSibling.style.display = "inline";
            } else {
                edit_btn.nextElementSibling.style.display = "none";
            }
        })
    })

    //Edit btn behavior
    document.querySelectorAll("#edit-form").forEach(form => {
            form.querySelector("#save-btn").addEventListener('click', () => {

            // Learned to upload image files through JS from both the following links
            //https://stackoverflow.com/questions/36067767/how-do-i-upload-a-file-with-the-js-fetch-api
            //https://stackoverflow.com/questions/69120374/how-can-i-upload-file-and-also-include-json-data-with-fetch-api

            var formData = new FormData();

            if (form.querySelector("#image").files[0] != null) {
                //hide form
                form.querySelector("#save-btn").parentNode.style.display = "none";

                //Learned CSRF from https://docs.djangoproject.com/en/5.1/howto/csrf/
                const csrftoken = Cookies.get('csrftoken');

                formData.append('image', form.querySelector("#image").files[0])
                formData.append('id', form.querySelector("#place-id").innerHTML)

                //Send form data to Django view to update post model
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
                var URL = window.URL
                var url = URL.createObjectURL(form.querySelector("#image").files[0])
                form.parentNode.parentNode.querySelector("img").src = url

            } else {
                alert("cannot edit place without image")
            }
        })
    })

    //Update public rating stars
    document.querySelectorAll("#public-rating").forEach(form => {

        fetch(`public_rating/${form.querySelector("#id").innerHTML}`)
        .then(response => response.json())
        .then(result => {
            // Print result
            // console.log(result["stars"])
            // console.log(`input[value=\"${result["stars"]}\"]`)
            if (result["stars"] != 0) {
                form.querySelector(`input[value=\"${Math.round(result["stars"])}\"]`).checked = true
            }
        });
    })

    //User rating input actions
    document.querySelectorAll("#user-rating").forEach(form => {

        fetch(`user_rating/${form.querySelector("#id").innerHTML}`)
        .then(response => response.json())
        .then(result => {
            // Print result
            // console.log(result["stars"])
            // console.log(`input[value=\"${result["stars"]}\"]`)
            if (result["stars"] != 0) {
                form.querySelector(`input[value=\"${Math.round(result["stars"])}\"]`).checked = true
            }
        });

        form.querySelectorAll("input").forEach(input => {
            input.addEventListener('click', () => {

                var formData = new FormData();

                //Learned CSRF from https://docs.djangoproject.com/en/5.1/howto/csrf/
                const csrftoken = Cookies.get('csrftoken');

                formData.append('stars', input.value)
                formData.append('id', form.querySelector("#id").innerHTML)

                //Send form data to Django view to update post model
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
    update_cards_or()

    //Animate each post
    let delay = 0;
    document.querySelectorAll("#card-col").forEach(card => {
        //delay is used so each subsequent post is slightly more delayed. This is so every post executes the animation one after other.
        card.style.animationDelay = delay.toString().concat('s');
        delay += 0.1;
        card.style.animationPlayState = 'running';
    })
    
})

//Filter checkbox behavior. 
//This function gets the places that matches the filters, but only one filter needs to be match. 
//Meaning if one filter matched a place, but another selected filter didn't, the place would still be selected.
//This is specifically for filters in the same column/category. So that you can for example see north american or italian restaurants.
function update_cards_or() {
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
                //Removes the places that don't match any filter
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
                //Remove the places that don't match all the filters from each column
                update_cards_and()
            }

            //Animate each post
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
                    //delay is used so each subsequent post is slightly more delayed. This is so every post executes the animation one after other.
                    card.style.animationDelay = delay.toString().concat('s');
                    delay += 0.1;
                }
            })

        })
    })
}

//Filter checkbox behavior. 
//This function gets the places that matches the filters, but all filters must match in order for the place be selected.
//This is specifically done for filters in different columns. So that you can for example look for italian restaurants in two separate locations.
function update_cards_and() {
    document.querySelectorAll("#card-col").forEach(col => {
        //Selects places that are haven't already been removed
        if (col.style.display == "block") {
            correct_filters = 0
            col.querySelector(".card").querySelector("#card-body").querySelectorAll("#filter").forEach(attribute => {
                //For every category of a place, if that category matches a currently selected filter, than add one to correct filters  
                if (dict_filters[attribute.getAttribute("alt")].length > 0) {
                    dict_filters[attribute.getAttribute("alt")].forEach(filter => {
                        if (filter == attribute.innerHTML || attribute.innerHTML.includes(filter)) {
                            correct_filters++;
                        }
                    })

                } else {
                    //This is for the case that that no filter is selected for a category, in which case it should be interpreted the same way as a filter matching
                    correct_filters++;
                }
            })
            //If the number of correct filters is less than the amount of identifying categories, than the place is removed
            //This means that if every category doesn't either match a selected filter or doesn't have a selected filter, than it should be removed.
            if (correct_filters < Object.keys(dict_filters).length) {
                col.style.display = "none";
            }
        }
    })
}