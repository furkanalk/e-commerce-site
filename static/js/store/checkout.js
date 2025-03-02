let input = document.querySelector(".input");
let input_two = document.querySelector(".input_two");
let input_three = document.querySelector(".input_three");
let input_four = document.querySelector(".input_four");
let input_five = document.querySelector(".input_five");
let button = document.querySelector(".button");

button.disabled = true;
button.style.background = '#fed7aa'

input.addEventListener("change", stateHandle);
input_two.addEventListener("change", stateHandle);
input_three.addEventListener("change", stateHandle);
input_four.addEventListener("change", stateHandle);
input_five.addEventListener("change", stateHandle);

function stateHandle() {
    if (document.querySelector(".input").value.length == 0) {
        button.disabled = true;
        button.style.background = '#fed7aa'
        return
    }
    if(document.querySelector(".input_two").value.length == 0){
        button.disabled = true;
        button.style.background = '#fed7aa'
        return
    }
    if(document.querySelector(".input_three").value.length == 0){
        button.disabled = true;
        button.style.background = '#fed7aa'
        return
    }
    if(document.querySelector(".input_four").value.length == 0){
        button.disabled = true;
        button.style.background = '#fed7aa'
        return
    }
    if(document.querySelector(".input_five").value.length == 0){
        button.disabled = true;
        button.style.background = '#fed7aa'
        return
    }
    button.disabled = false;
    button.style.background = '#fb923c'
}

// Stripe Payment
function buy(event){
    event.preventDefault();
    
    let data = {
        'first_name': document.getElementById('id_first_name').value,
        'last_name': document.getElementById('id_last_name').value,
        'address': document.getElementById('id_address').value,
        'zipcode': document.getElementById('id_zipcode').value,
        'city': document.getElementById('id_city').value,
    }

    let stripe = Stripe('{{ pub_key }}');

    fetch('/cart/checkout/',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        credentials: 'same-origin',
        body: JSON.stringify(data)
    })
    
    .then(function(response) {
        return response.json()
    })
    .then(function(session) {
        return stripe.redirectToCheckout({ sessionId: session.session.id })
    })
    .then(function(result) {
        if(result.error){
            alert(result.error.message)
        }
    })
    .catch(error => console.error(error));

    return false;
}