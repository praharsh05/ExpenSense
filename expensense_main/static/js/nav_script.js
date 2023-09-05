const body = document.querySelector("body"),
    sidebar = body.querySelector(".sidebar"),
    toggle = body.querySelector(".toggle");

    if (toggle != null){
        toggle.addEventListener("click",()=>{
            sidebar.classList.toggle("close");
        });
    }
    
