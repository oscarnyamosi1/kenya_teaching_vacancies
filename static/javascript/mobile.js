document.addEventListener('DOMContentLoaded',()=>{
    const sidebarRight = document.querySelector('.sidebar-right')
    const sidebarLeft = document.querySelector('.sidebar-left')
    const appcontainer = document.querySelector('.app-container')
    const logoText = document.querySelector('.logo-text')
    const hambuger = document.querySelector('.menu-toggle ')
    const body = document.querySelector('body')
    const overlay = document.getElementById('overlay')


    if(window.innerWidth < 767){
        sidebarRight.classList.add = 'hidden'
        sidebarLeft.classList.add = 'hidden'
        logoText.classList.add = 'hidden'
        appcontainer.style.display = 'flex'
        hambuger.classList.remove = 'hidden'

        hambuger.addEventListener('click',()=>{
            overlay.classList.toggle('active')
               
              })
        overlay.addEventListener('click',()=>{
            overlay.classList.toggle('active')
        })

    }else{
        hambuger.style.display = 'none'
    }

    mobileThemer.addEventListener('click',()=>{
        alert('themed')
    })
})
