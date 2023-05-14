const patientId = sessionStorage.getItem("userId");
const doctorId = sessionStorage.getItem("doctorId")

async function makeAppointment() {
    const description = document.getElementById("description").value;
    const appointmentDate = document.getElementById("appointmentDate").value;
    const url =  `http://0.0.0.0:8001/patient/${patient_id}/make_appointment`;

    // Make the first POST request
    await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            patientId: patientId,
            doctorId: doctorId,
            description: description,
            appointmentDate: appointmentDate,
            doctor_approved: null
        })
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