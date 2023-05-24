const patientId = sessionStorage.getItem("userId");
const doctorId = sessionStorage.getItem("doctorId")
const accessToken = sessionStorage.getItem("token")

async function makeAppointment() {
    const description = document.getElementById("description").value;
    const appointmentDate = document.getElementById("appointmentDate").value;
    const appointmentTime = document.getElementById("appointmentTime").value;
    const url = `http://0.0.0.0:8001/patient/${patientId}/make_appointment`;
    let body = JSON.stringify({
            patient_id: patientId,
            doctor_id: doctorId,
            description: description,
            appointment_datetime: appointmentDate + "T" + appointmentTime + ":00"
        })

    // Make the first POST request
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + accessToken
        },
        body: body
    })
        .then(async response => {
            if (response.status !== 200) {
                throw new Error('Произошла ошибка. Попробуйте перезагрузить страницу.');
            }
            return await response.json()
        })
        .then(async response => {
            window.location.replace("http://0.0.0.0:3001/appointments");
        })
        .catch(error => {
            alert(error.message)
        });
}