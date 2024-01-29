function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const resultDiv = document.getElementById(result);

// Check if a file is selected
if (fileInput.files.length == 0) {
    resultDiv.innerText = 'Please select a file.';
    return;
}

const file = fileInput.files[0];
const formData = new FormData();
formData.append('file', file);

fetch('', {
    method:'POST',
    body: formData,
})
.then(Response => Response.json())
.then(data => {
    // Handle the response from API
    resultDiv.innerText ='File uploaded successfully. Response: ${JSON.stringify(data)}';
})
.catch(error=> {
    // Handle Errors
    resultDiv.innerText='Error: ${error.message}';
});

}