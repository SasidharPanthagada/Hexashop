var updatebtns = document.getElementsByClassName('update-cart')

for(var i=0;i<updatebtns.length;i++){
    updatebtns[i].addEventListener('click',function(){
        var productid = this.dataset.product
        var action = this.dataset.action
        console.log('productid:',productid , 'action:',action)

        console.log('User:' , user)
        if(user === 'AnonymousUser'){
            console.log('Not logged in')
        }
        else {
            updateuserorder(productid,action)
        }
            
    })
}

function updateuserorder(productid,action){
    console.log('User is logged in , sending data ...')

    var url = '/update_item/'
    fetch(url,{
        method : 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productid': productid , 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        
        console.log('data:' , data)
        location.reload()
    })
}