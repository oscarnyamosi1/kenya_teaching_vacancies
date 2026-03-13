let navbuttons = document.querySelectorAll('.menu-item')
const themer = document.querySelector('.themer')
const mobileThemer = document.querySelector('.mobilethemer')
const themerIcon = document.querySelector('.themericon')
const body = document.getElementById('body')
let pageName = document.querySelector('.pagename').value.trim()
let is_dark_mode = JSON.parse(localStorage.getItem("is_dark_mode")) || false




function handleThemes(){
    if (is_dark_mode == true){  
        body.classList.remove('lightmode')

        themerIcon.classList.add('fa-sun-o')
        themerIcon.classList.remove('fa-moon-o')
    } else {
        body.classList.add('lightmode')

        themerIcon.classList.add('fa-moon-o')
        themerIcon.classList.remove('fa-sun-o')
    }    
    themer.addEventListener('click',()=>{
        body.classList.toggle('lightmode')
        body.classList.contains('lightmode')?(localStorage.setItem('is_dark_mode',JSON.stringify(false))):(localStorage.setItem('is_dark_mode',JSON.stringify(true)))
    })    
    mobileThemer.addEventListener('click',()=>{
        body.classList.toggle('lightmode')
        body.classList.contains('lightmode')?(localStorage.setItem('is_dark_mode',JSON.stringify(false))):(localStorage.setItem('is_dark_mode',JSON.stringify(true)))
    }) 
}    

function highlightNav(){
    navbuttons.forEach((navbutton)=>{
        if(navbutton.classList.contains(`${pageName}`)){
            navbutton.classList.toggle('active')
        }
    })
}

document.addEventListener('DOMContentLoaded',()=>{
    highlightNav()
    handleThemes()
        
    // if(window.innerWidth > 767){
    //     alert('hiding')
    //     // mobileThemer.classList.add = 'hidden'
    //     mobileThemer.style.color = 'transparent'
    // }


  
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


    const viewtrending = document.getElementById('viewtrending')
    const trendingcard = document.getElementById('trendingcard')
    const closetrending = document.getElementById('closetrending')
    viewtrending.addEventListener('click',()=>{
        trendingcard.classList.toggle('trending-card')
        closetrending.style.display = 'inline-block'
        viewtrending.style.display = 'none'
    })

    closetrending.addEventListener('click',()=>{
        trendingcard.classList.toggle('trending-card')
        closetrending.style.display = 'none'
        viewtrending.style.display = 'inline-block'

    })
})


