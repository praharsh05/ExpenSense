// code taken from Fetch API docs(Mozilla)

// function to get the CSRF cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

let company_field = document.getElementById("id_company")
let team_field = document.getElementById("id_team_name")
if (company_field != null) {

    company_field.addEventListener("change", pickState)
    function pickState(e) {
        let company_id = e.target.value
        const data = { comp_id: company_id }
        console.log(e.target.value)
        let url = "teams/"

        //call fetch api to get the teams in the company selected
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data[0]['team_name']);

                team_field.innerHTML = `<option value= "" selected>Select Team</option>`
                for (let i = 0; i < data.length; i++) {
                    // console.log('team selected:', data[i]['team_name']);
                    team_field.innerHTML += `<option value="${data[i]['id']}">${data[i]['team_name']}</option>`
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
}