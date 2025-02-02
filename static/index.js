document.addEventListener("DOMContentLoaded", function(event) {
    let btnSend = document.getElementById("sendTranlsation");
    let lang = document.getElementById("lang");
    let text = document.getElementById("text");
    let responseDiv = document.getElementById("responseDiv");
    btnSend.addEventListener('click', function (event){
        let payload = {data:[{"lang": lang.value, "text": text.value}]}
        fetch('/translate',
            {
                    method: "POST",
                    body:JSON.stringify(payload),
                     headers: {"Content-Type": "application/json"},
            }).then(response=>{
            if(response.status===200){response.json().then(result=>{
                    responseDiv.innerText = result;
                    })
            }else{
                alert(response.json())
            }
        })
    })

})