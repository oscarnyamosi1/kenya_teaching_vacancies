document.addEventListener('DOMContentLoaded',()=>{
    let navbuttons = document.querySelectorAll('.menu-item')

    let pageName = document.querySelector('.pagename').value.trim()

    navbuttons.forEach((navbutton)=>{
        if(navbutton.classList.contains(`${pageName}`)){
            navbutton.classList.toggle('active')
        }
    })

    // view job details

    let viewjobdetailsButtons = document.querySelectorAll('.viewjobdetails')
    function viewjobdetails(){
        console.log("viewjobdetails")
    }
    viewjobdetailsButtons.forEach((viewjobdetailsButton)=>{
        viewjobdetailsButton.addEventListener('click',()=>{
            viewjobdetails()
        })
    })

    // create glasssmmorphism effects

    // Glassy hover glow
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect()
        const x = e.clientX - rect.left
        const y = e.clientY - rect.top
        card.style.setProperty('--glow', `radial-gradient(circle at ${x}px ${y}px, rgba(255, 255, 255, 0.22), transparent 80%)`);
        })
        card.addEventListener('mouseleave', () => card.style.removeProperty('--glow'));
    });

})
