document.addEventListener("DOMContentLoaded",()=>{
    const profileContainer  = document.querySelector('.profile-container')


    // sort locations of documents with id's

    const teacherDocuments = JSON.parse(document.getElementById("teacherDocuments").textContent)
    

    // detect file type b4 use from the objects parsed
    function getFileType(fileUrl) {
        const extension = fileUrl.split('.').pop().toLowerCase();

        if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension)) {
            return 'image';
        } 
        else if (extension === 'pdf') {
            return 'pdf';
        } 
        else {
            return 'unknown';
        }
    }
    // create display cards with their contents
teacherDocuments.forEach(function(teacherDocument) {
    let filetype = getFileType(teacherDocument.file);

    // build full media URL
    let fileUrl = `/media/${teacherDocument.file}`;

    if (filetype === 'image') {
        profileContainer.innerHTML += `
            <div id="${teacherDocument.id}" class="card ${teacherDocument.document_type} documentdisplay">
                <button id="${teacherDocument.id}" class="btn btn-outline closebtn">Close</button>
                
                <div class="preview-box">
                    <img 
                        src="${fileUrl}" 
                        alt="Document Image"
                        class="preview-media">
                </div>
            </div>
        `;
    } 
    else if (filetype === 'pdf') {
        profileContainer.innerHTML += `
            <div id="${teacherDocument.id}" class="card ${teacherDocument.document_type} documentdisplay">
                <button id="${teacherDocument.id}" class="btn btn-outline closebtn">Close</button>
                
                <div class="preview-box">
                    <iframe 
                        src="${window.location.origin}${fileUrl}" 
                        class="preview-media"
                        frameborder="0">
                    </iframe>
                </div>
            </div>
        `;
    } 
    else {
        profileContainer.innerHTML += `
            <div id="${teacherDocument.id}" class="card ${teacherDocument.document_type} documentdisplay">
                <button id="${teacherDocument.id}" class="btn btn-outline closebtn">Close</button>
                
                <div class="preview-box unsupported-box">
                    <p>Unsupported file type</p>
                    <a href="${fileUrl}" target="_blank">Download File</a>
                </div>
            </div>
        `;
    }
});

    const documentDisplays  = document.querySelectorAll('.documentdisplay')
    const closeButtons = document.querySelectorAll('.closebtn')
    const docItems = document.querySelectorAll('.doc-item')

    // display selected document item (docitem) from the list of documents

    function displayDocument(doctype){
        if(doctype == 'cv'){
            // display cv
            documentDisplays.forEach((documentDisplay)=>{
                if(documentDisplay.classList.contains('Carriculum')){
                    documentDisplay.style.display = 'block'
                }
            })
        }else if(doctype == 'certificate'){
            // display tsc
            documentDisplays.forEach((documentDisplay)=>{
                if(documentDisplay.classList.contains('Degree')){
                    documentDisplay.style.display = 'block'
                }else if(documentDisplay.classList.contains('Diploma')){
                    documentDisplay.style.display = 'block'
                }else if(documentDisplay.classList.contains('Certificate') && documentDisplay.classList.contains('TSC') ){
                    documentDisplay.style.display = 'none'
                }else if(documentDisplay.classList.contains('Certificate')){
                    documentDisplay.style.display = 'block'
                }
            })
        }
        else if(doctype == 'tsc'){
            // display tsc
            documentDisplays.forEach((documentDisplay)=>{
                if(documentDisplay.classList.contains('TSC')){
                    documentDisplay.style.display = 'block'
                }
            })
        }
    }

    docItems.forEach(function(docItem){
        docItem.addEventListener('click',function(){
            // displayDocument(docItem.id)
            if(docItem.classList.contains('cvitem')){
                displayDocument('cv')
            }else if(docItem.classList.contains('certificateitem')){
                displayDocument('certificate')
            }else if(docItem.classList.contains('tscitem')){
                displayDocument('tsc')
            }else {
                alert('Content may not be available at the moment !')
            }
        })
    })

    // close diplayed documents in the view profile page
    closeButtons.forEach(function(closeButton){
            closeButton.addEventListener('click',function(){
                documentDisplays.forEach(function(documentDisplay){
                    if (documentDisplay.id == closeButton.id){
                        documentDisplay.style.display = 'none'
                    }
                })
            })
    })

})