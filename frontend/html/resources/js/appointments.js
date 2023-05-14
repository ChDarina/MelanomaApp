const accessToken = sessionStorage.getItem("token")
const isDoctor = sessionStorage.getItem("isDoctor");
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
  const description = document.getElementById("description").value;
  const appointmentDate = document.getElementById("appointmentDate").value;
  const url = `/doctor/${doctor_id}/approve_appointment/${appointment_id}/`;

  // Make the first POST request
  await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
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

function appoveAppoinment(doctor_id, appointment_id) {
  doctorAppointmentAction(doctor_id, appointment_id, true)
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

  var cell = row.insertCell();
  if (isDoctor === "false") cell.innerHTML = `<a href="` + "#" + ` " class="font-weight-bold blue-text">` + item.doctor_name + `</a>`;
  else cell.innerHTML = `<a href="` + "#" + ` " class="font-weight-bold blue-text">` + item.patient_name + `</a>`;
  cell = row.insertCell();
  cell.innerHTML = `<p class="font-weight-bold"> ` + item.description + `</p >`;
  cell = row.insertCell();
  cell.innerHTML = `<p class="font-weight-bold"> ` + item.appointment_datetime + `</p >`;
  cell = row.insertCell();
  if (approve == "false") cell.innerHTML = `<p class="font-weight-bold"> Отказано </p>`;
  else if (approve == "true") cell.innerHTML = `<p class="font-weight-bold"> Подтверждено </p>`;
  else if (isDoctor === "false") cell.innerHTML = `<p class="font-weight-bold"> Не подтверждено </p>`;
  else cell.innerHTML = `<div class="d-grid gap-2 col-4 mx-auto" >
    <input class="btn btn-outline-dark btn-rounded" type="submit" value="Подтвердить"
    onclick="appoveAppoinment(`+ item.doctor_id + `, ` + item.id + `); return false;" />
  </div>
  <div class="d-grid gap-2 col-4 mx-auto" >
    <input class="btn btn-outline-dark btn-rounded" type="submit" value="Подтвердить"
      onclick="disappoveAppoinment(`+ item.doctor_id + `, ` + item.id + `); return false;" />
  </div >`;
}