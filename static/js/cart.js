var updateBtns = document.getElementsByClassName('update-cart')
    // var btn = document.getElementsByClassName('add-btn1')
console.log('add-btn1 clicked...')
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        var minorder = this.dataset.minorder

        console.log("product id", productId, " action", action, "minorder", minorder)
        console.log('User : ', user)
        if (user == 'AnonymousUser') {
            // updateUserOrder(productId, action)
            console.log("unathenticated user")
        } else {
            updateUserOrder(productId, action, minorder)
        }
    })
}


function updateUserOrder(productId, action, minorder) {
    console.log("THROUGH API")

    var url = '/update_item'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': "application/json; odata=verbose",
                // 'Accept': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action, 'minorder': minorder, })
        })
        .then((response) => {
            console.log('api')
            return response.json()
        })
        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}