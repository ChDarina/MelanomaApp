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
      class="bi bi-grid" viewBox="0 0 16 16">
      <path
          d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zM2.5 2a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zM1 10.5A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3z" />
  </svg>
</a>
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