function uploadFile() {
    const fileInput = document.getElementById('file_upload');
    const resultDiv = document.getElementById('submit');
console.log('file', fileInput.files[0])
// Check if a file is selected
if (fileInput.files.length == 0) {
    resultDiv.innerText = 'Please select a file.';
    return;
}

const formData = new FormData();
for (let i = 0; i<fileInput.files.length; i++){
    formData.append('file_upload[]', fileInput.files[i]);
}

fetch('/', {
    method:'POST',
    body: formData,
})
.then(Response => Response.json())
.then(data => {
    // Handle the response from API
    resultDiv.innerText ='Server response:'+ JSON.stringify(data);
})
.catch(error=> {
    // Handle Errors
    resultDiv.innerText='Error:' + error.message;
});

}