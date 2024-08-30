
let filters = [] 

var dict_filters = []

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll("#form-grid").forEach(grid => {
        grid.querySelectorAll("p").forEach(filter_name => {
            dict_filters.push({
                key: filter_name.innerHTML,
                value: "hi"
            })
        })
    })
})



function update_cards_or() {
    document.querySelectorAll(".form-check").forEach(form => {
        let checkbox = form.querySelector("input")
        checkbox.addEventListener('click', () => {
            if (checkbox.checked) {
                filters.push(checkbox.id)
            } else {
                filters.splice(filters.indexOf(checkbox.id), 1)
            }

            if (filters.length == 0) {
                document.querySelectorAll("#card-col").forEach(col => {
                    col.style.display = "block"
                })
            } else {
                document.querySelectorAll("#card-col").forEach(col => {
                    col.style.display = "none"
                })

                document.querySelectorAll("#card-col").forEach(col => {
                    col.querySelectorAll("#card-body").forEach(body => {
                        body.querySelectorAll("#filter").forEach(card_text => {
                            filters.forEach(filter => {
                                if(filter == card_text.innerHTML || card_text.innerHTML.includes(filter)) {
                                    col.style.display = "block";
                                }
                            })
                        })
                    })
                })
            }
        })
    })



    // function update_cards_and () {

    //     document.querySelectorAll("#filter-form").forEach(form => {
    //         let checkbox = form.querySelector("input")
    //         checkbox.addEventListener('click', () => {
    //             if (checkbox.checked) {
    //                 filters.push(checkbox.id)
    //             } else {
    //                 filters.splice(filters.indexOf(checkbox.id), 1)
    //             }
    
    //             if (filters.length == 0) {
    //                 document.querySelectorAll("#card-col").forEach(col => {
    //                     col.style.display = "block"
    //                 })
    //             } else {
    //                 document.querySelectorAll("#card-col").forEach(col => { 
    //                     col.style.display = "none";
    //                 })
                    
    //                 document.querySelectorAll("#card-body").forEach(card_body => {
    //                     card_body.querySelectorAll("#filter").forEach(card_text => {
    //                         filters.every(filter => {
    //                             if(filter == card_text.innerHTML) {
    //                                 console.log("running")
    //                                 card_body.parentNode.parentNode.style.display = "block";
    //                             } else {
    //                                 card_body.parentNode.parentNode.style.display = "none";
    //                             }
    //                             return filter == card_text.innerHTML
    //                         })
    //                     })
    //                 })
    //             }
    //         })
    //     })
    // }

}