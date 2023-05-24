const accessToken = sessionStorage.getItem("token")
const userId = sessionStorage.getItem("userId");

if (isDoctor === "false") document.getElementById("userType").innerHTML = 'Врач';
else document.getElementById("userType").innerHTML = 'Пациент';

let userType;
if (isDoctor === "false") userType = 'patient';
else userType = 'doctor';

const fetchOptions = {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer ' + accessToken
  }
};

fetch(`http://0.0.0.0:8001/${userType}/${userId}/appointments`, fetchOptions)
  .then(response => response.json())
  .then(data => {
    console.log(data)
    for (let i = 0; i < data.length; i++) {
      let item = data[i]
      addRow(item);
    }
  })
  .catch(error => {
    // Handle the error
    console.error(error);
    responseElement.innerText = "Произошла ошибка при загрузке страницы. Попробуйте позднее";
  });

async function doctorAppointmentAction(doctor_id, appointment_id, approve) {
  const url = `http://0.0.0.0:8001/doctor/${doctor_id}/approve_appointment/${appointment_id}`;

  // Make the first POST request
  await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + accessToken
    },
    body: JSON.stringify({
      description: '',
      doctor_approved: approve
    })
  })
    .then(async response => {
      if (response.status !== 200) {
        throw new Error('Произошла ошибка. Попробуйте перезагрузить страницу.');
      }
      return await response.json()
    })
    .catch(error => {
      alert(error.message)
    });
}

async function appoveAppoinment(doctor_id, appointment_id) {
  await doctorAppointmentAction(doctor_id, appointment_id, true)
  alert("Вы одобрили приём!")
  window.location.reload();
}

function disappoveAppoinment(doctor_id, appointment_id) {
  doctorAppointmentAction(doctor_id, appointment_id, false)
  alert("Вы отказали в приёме!")
  window.location.reload();
}

function addRow(item) {
  var table = document.getElementById("table");
  var row = table.insertRow();
  console.log(item)

  var cell = row.insertCell();
  if (isDoctor === "false") cell.innerHTML = `<a href="` + "#" + ` " class="font-weight-bold blue-text">` + item.doctor_name + `</a>`;
  else cell.innerHTML = `<a href="` + "#" + ` " class="font-weight-bold blue-text">` + item.patient_name + `</a>`;
  cell = row.insertCell();
  cell.innerHTML = `<p class="font-weight-bold"> ` + item.description + `</p >`;
  cell = row.insertCell();
  cell.innerHTML = `<p class="font-weight-bold"> ` + item.appointment_datetime + `</p >`;
  cell = row.insertCell();
  if (item.doctor_approved === false) cell.innerHTML = `<p class="font-weight-bold"> Отказано </p>`;
  else if (item.doctor_approved === true) cell.innerHTML = `<p class="font-weight-bold"> Подтверждено </p>`;
  else if (isDoctor === "false") cell.innerHTML = `<p class="font-weight-bold"> Не подтверждено </p>`;
  else cell.innerHTML = `<div class="d-grid gap-2 col-4 mx-auto" >
    <input class="btn btn-outline-dark btn-rounded" type="submit" value="Подтвердить"
    onclick="appoveAppoinment(`+ item.doctor_id + `, ` + item.id + `); return false;" />
  </div>
  <div class="d-grid gap-2 col-4 mx-auto" >
    <input class="btn btn-outline-dark btn-rounded" type="submit" value="Отказать"
      onclick="disappoveAppoinment(`+ item.doctor_id + `, ` + item.id + `); return false;" />
  </div >`;
  cell = row.insertCell();
  cell.innerHTML = `
<a href="">
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" 
class="bi bi-arrow-right-square" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm4.5 5.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H4.5z"/>
</svg>
</a>
<p></p>
<a href="">
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
      class="bi bi-pencil-square" viewBox="0 0 16 16">
      <path
          d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
      <path fill-rule="evenodd"
          d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z" />
  </svg>
</a>`;
}