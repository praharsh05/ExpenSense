
// functions to show and hide loader for when a file api is called
function showLoader(){
    const loader = document.querySelector('.loader-container');
    loader.style.display = 'flex';
}

function hideLoader() {
    const loader = document.querySelector('.loader-container');
    loader.style.display = 'none';
}

// function fileSelect(event){
const fileInput = document.getElementById('id_receipt');
if(fileInput != null){
    // add an event listener to the file field
    fileInput.addEventListener("change",() =>{
        const file = fileInput.files[0];
        // console.log('File to send ',file)
        const formData = new FormData();
        formData.append('file', file);
        // console.log('form Data', formData)
        let url = "ocr_api/";
        // Make AJAX request to the OcrViewApi
        showLoader();
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success: ',data);
            updateFormFields(data);
            hideLoader();
        })
        .catch(error => {
            // Handle API error here
            console.error('Error calling the API:', error.message);
            hideLoader();
        });

    });
}


function updateFormFields(data){
    // extract the data from the JSON
    // console.log('data received is:', data);
    const { amount, date: { day, month, year } } = JSON.parse(data);
    // console.log('Amount: ', amount);
    // console.log('date: ', day,month,year);

    const formattedDate = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    // update the value
    document.getElementById('id_amount').value = amount;
    document.getElementById('id_expense_date').value = formattedDate;
}