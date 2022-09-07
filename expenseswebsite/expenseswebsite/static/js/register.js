const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector('#emailField');
const emailFeedBackArea = document.querySelector('.email_FeedBack');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const emailSuccessOutput = document.querySelector('.emailSuccessOutput');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const passwordField =  document.querySelector('#passwordField');

const handleToggleInput=(e)=>{

    if(showPasswordToggle.textContent === 'SHOW'){

        showPasswordToggle.textContent = 'HIDE';

        passwordField.setAttribute("type","text");

    }else{
        showPasswordToggle.textContent = 'SHOW';
        passwordField.setAttribute("type","password")
    }

}

showPasswordToggle.addEventListener("click",handleToggleInput)



emailField.addEventListener("keyup",(e)=>{

    const emailValue = e.target.value;
    emailSuccessOutput.style.display='block';
    emailSuccessOutput.textContent=`Cheking ${emailValue}!`;


    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display="none";

    if(emailValue.length>0){


        fetch("/authentication/validate-email",{
            body:JSON.stringify({email: emailValue}),
            method:"POST",

         }).then(res=>res.json())
         .then((data) =>{
            console.log("data",data);
            emailSuccessOutput.style.display='none';
            if (data.email_error) {
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display="block";
                emailFeedBackArea.innerHTML=`<p>${data.email_error}</p>`
            }
         });

    }


})



usernameField.addEventListener("keyup",(e)=>{

    const usernameValue = e.target.value;
    usernameSuccessOutput.style.display='block';
    usernameSuccessOutput.textContent=`Cheking ${usernameValue}!`

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display="none";

    if(usernameValue.length>0){
        fetch("/authentication/validate-username",{
            body:JSON.stringify({username: usernameValue}),
            method:"POST",

         }).then(res=>res.json())
         .then((data) =>{
            console.log("data",data);
            usernameSuccessOutput.style.display='none';
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display="block";
                feedBackArea.innerHTML=`<p>${data.username_error}</p>`
            }
         });

    }

    

    
})