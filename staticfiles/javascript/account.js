document.addEventListener('DOMContentLoaded',()=>{
    const changemail = document.getElementById('changemail')
    const changephoneno = document.getElementById('changephoneno')
    const changepassword = document.getElementById('changepassword')

    changemail.addEventListener('click',()=>{
        window.location = "/teachers/change-email/"
    })
    changephoneno.addEventListener('click',()=>{
        window.location = "/teachers/change-number/"
    })
    changepassword.addEventListener('click',()=>{
        window.location = "/teachers/change-password/"
    })


    const btn = document.getElementById('changephoneno');
    const form = document.getElementById('phoneForm');
    const cancel = document.getElementById('cancelPhone');

    btn.addEventListener('click', () => {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    });

    cancel.addEventListener('click', () => {
        form.style.display = 'none';
    });


    const input = document.querySelector('input[name="newnumber"]');

    input.addEventListener('input', () => {
        let val = input.value.replace(/\D/g, '');

        if (val.startsWith('254')) val = '0' + val.slice(3);

        if (val.length > 4 && val.length <= 7)
            val = val.slice(0,4) + ' ' + val.slice(4);
        else if (val.length > 7)
            val = val.slice(0,4) + ' ' + val.slice(4,7) + ' ' + val.slice(7,10);

        input.value = val;
    });
})