
let dict_filters = {}

all_filters = []


document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#form-grid").querySelectorAll("p").forEach(filter_name => {
        dict_filters[filter_name.innerHTML] = []
    })
    console.log(Object.keys(dict_filters).length)
    update_cards_or()
})



function update_cards_or() {
    document.querySelectorAll(".form-check").forEach(form => {
        let checkbox = form.querySelector("input")
        let filter_name = form.parentNode.querySelector("p")
        let filters = dict_filters[filter_name.innerHTML]

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