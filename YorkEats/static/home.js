
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

    document.querySelector("#form-grid").querySelectorAll("p").forEach(filter_name => {
        dict_filters[filter_name.innerHTML] = []
    })
    update_cards_or()
})



function update_cards_or() {
    document.querySelectorAll(".form-check").forEach(form => {
        let checkbox = form.querySelector("input")
        let filter_name = form.parentNode.querySelector("p")

        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                dict_filters[filter_name.innerHTML].push(checkbox.id)
                all_filters.push(checkbox.id)
            } else {
                dict_filters[filter_name.innerHTML].splice( dict_filters[filter_name.innerHTML].indexOf(checkbox.id), 1)
                all_filters.splice(all_filters.indexOf(checkbox), 1)
            }

            if (all_filters.length == 0) {
                document.querySelectorAll("#card-col").forEach(col => {
                    col.style.display = "block"
                })
            } else {
                document.querySelectorAll("#card-col").forEach(col => {
                    col.style.display = "none"
                })
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
                 update_cards_and()
            }

        })
    })

}
function update_cards_and() {
    document.querySelectorAll("#card-col").forEach(col => {
        if (col.style.display == "block") {
            correct_filters = 0
            col.querySelector(".card").querySelector("#card-body").querySelectorAll("#filter").forEach(attribute => {
                if (dict_filters[attribute.getAttribute("alt")].length > 0) {
                    dict_filters[attribute.getAttribute("alt")].forEach(filter => {
                        if (filter == attribute.innerHTML || attribute.innerHTML.includes(filter)) {
                            correct_filters++;
                        }
                    })

                } else {
                    correct_filters++;
                }
            })
            if (correct_filters < Object.keys(dict_filters).length) {
                col.style.display = "none";
            }
        }
    })
}